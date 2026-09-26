"""
ValueAI — Phase 15 SageMaker Deployment

Deploys the configured JumpStart model to a SageMaker real-time endpoint.

IMPORTANT:
    This version uses SageMaker InstancePools for automatic capacity
    fallback.

    Instead of asking SageMaker for only one instance type:

        ml.g6e.xlarge

    the endpoint configuration contains an ordered list:

        Priority 1 -> ml.g6e.xlarge
        Priority 2 -> ml.g6e.2xlarge
        Priority 3 -> ml.g6e.4xlarge

    If SageMaker cannot obtain capacity for the higher-priority instance,
    SageMaker automatically attempts the next pool.

Model:
    huggingface-llm-qwen2-5-7b-instruct

Deployment flow:

    JumpStartConfig
        ↓
    ModelBuilder.from_jumpstart_config()
        ↓
    set_deployment_config()
        ↓
    build()
        ↓
    boto3.create_endpoint_config(InstancePools=...)
        ↓
    boto3.create_endpoint()
        ↓
    wait for endpoint

Prerequisites:
    - AWS credentials available through the normal AWS credential chain
    - An IAM execution role ARN usable by SageMaker
    - SageMaker Python SDK V3
    - boto3/botocore with InstancePools API support
    - An AWS region where the selected JumpStart model is available

Example PowerShell:

    python scripts/deploy_sagemaker.py `
      --role-arn "arn:aws:iam::932453198323:role/ValueAI-SageMaker-ExecutionRole" `
      --endpoint-name "valueai-qwen25-7b" `
      --instance-type "ml.g6e.xlarge" `
      --config-name "generate_lowest_cost" `
      --model-version "1.42.0"

IMPORTANT:
    In PowerShell, do NOT escape ':' characters in the ARN.

    Correct:
        arn:aws:iam::932453198323:role/ValueAI-SageMaker-ExecutionRole

    Incorrect:
        arn\\:aws\\:iam::932453198323\\:role/ValueAI-SageMaker-ExecutionRole
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# AWS IMPORTS
# ============================================================

import boto3

from botocore.exceptions import BotoCoreError, ClientError


# ============================================================
# VALUEAI CONFIGURATION
# ============================================================

from src.utils.config import (
    get_aws_region,
    get_sagemaker_endpoint_name,
    get_sagemaker_model_id,
)


# ============================================================
# DEFAULTS
# ============================================================

DEFAULT_INSTANCE_TYPE = "ml.g6e.xlarge"

DEFAULT_CONFIG_NAME = "generate_lowest_cost"

DEFAULT_MODEL_VERSION = "1.42.0"

# SageMaker InstancePools supports up to five pools.
#
# Priority 1 = preferred / lowest-cost choice.
# Priority 2 = first fallback.
# Priority 3 = second fallback.
#
# These are all instances reported by the JumpStart model metadata
# in the current ValueAI deployment.
DEFAULT_INSTANCE_POOLS = [
    "ml.g6e.xlarge",
    "ml.g6e.2xlarge",
    "ml.g6e.4xlarge",
]

# Capacity provisioning timeout.
#
# AWS allows 300-3600 seconds.
#
# This controls capacity provisioning across the pools. It does NOT
# include model download/container startup time.
DEFAULT_PROVISION_TIMEOUT_SECONDS = 900

DEFAULT_POLL_SECONDS = 10

DEFAULT_ENDPOINT_TIMEOUT_SECONDS = 3600


# ============================================================
# ARGUMENT PARSING
# ============================================================


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Deploy the ValueAI JumpStart model to SageMaker "
            "using InstancePools for automatic capacity fallback."
        )
    )

    parser.add_argument(
        "--role-arn",
        default=None,
        help=(
            "SageMaker execution role ARN. "
            "Example: "
            "arn:aws:iam::932453198323:role/"
            "ValueAI-SageMaker-ExecutionRole"
        ),
    )

    parser.add_argument(
        "--endpoint-name",
        default=None,
        help=(
            "SageMaker endpoint name. "
            "If omitted, VALUEAI_SAGEMAKER_ENDPOINT_NAME "
            "is used."
        ),
    )

    parser.add_argument(
        "--instance-type",
        default=DEFAULT_INSTANCE_TYPE,
        help=(
            "Primary SageMaker inference instance type. "
            f"Default: {DEFAULT_INSTANCE_TYPE}"
        ),
    )

    parser.add_argument(
        "--fallback-instance-types",
        default=None,
        help=(
            "Comma-separated fallback instance types. "
            "Example: ml.g6e.2xlarge,ml.g6e.4xlarge"
        ),
    )

    parser.add_argument(
        "--config-name",
        default=DEFAULT_CONFIG_NAME,
        help=(
            "Published JumpStart deployment configuration. "
            f"Default: {DEFAULT_CONFIG_NAME}"
        ),
    )

    parser.add_argument(
        "--model-version",
        default=DEFAULT_MODEL_VERSION,
        help=(
            "Pinned JumpStart model version. "
            f"Default: {DEFAULT_MODEL_VERSION}"
        ),
    )

    parser.add_argument(
        "--provision-timeout",
        type=int,
        default=DEFAULT_PROVISION_TIMEOUT_SECONDS,
        help=(
            "Maximum capacity-provisioning timeout across "
            "InstancePools. Valid range: 300-3600 seconds. "
            f"Default: {DEFAULT_PROVISION_TIMEOUT_SECONDS}"
        ),
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Validate configuration and AWS access without "
            "creating or changing SageMaker resources."
        ),
    )

    return parser.parse_args()


# ============================================================
# CONFIGURATION HELPERS
# ============================================================


def normalize_role_arn(
    role_arn: str | None,
) -> str | None:
    """
    Normalize an IAM role ARN.

    Handles accidentally escaped PowerShell ARNs:

        arn\\:aws\\:iam::123456789012\\:role/MyRole

    and converts them to:

        arn:aws:iam::123456789012:role/MyRole
    """

    if not role_arn:
        return None

    normalized = role_arn.strip()

    normalized = normalized.replace("\\:", ":")

    return normalized


def get_endpoint_name(
    cli_value: str | None,
) -> str:
    """Resolve the SageMaker endpoint name."""

    if cli_value:
        return cli_value.strip()

    return get_sagemaker_endpoint_name().strip()


def build_instance_pool_types(
    primary_instance_type: str,
    fallback_instance_types: str | None,
) -> list[str]:
    """
    Build the ordered InstancePools list.

    Priority order:

        1. primary instance
        2. first fallback
        3. second fallback
        ...

    Duplicate instance types are removed while preserving order.
    """

    values: list[str] = []

    primary = primary_instance_type.strip()

    if primary:
        values.append(primary)

    if fallback_instance_types:
        for value in fallback_instance_types.split(","):
            normalized = value.strip()

            if normalized:
                values.append(normalized)

    # Remove duplicates while preserving order.
    unique_values: list[str] = []

    for value in values:
        if value not in unique_values:
            unique_values.append(value)

    if not unique_values:
        raise ValueError(
            "At least one SageMaker instance type must be supplied."
        )

    if len(unique_values) > 5:
        raise ValueError(
            "SageMaker InstancePools supports a maximum of "
            "5 instance types."
        )

    return unique_values


# ============================================================
# AWS IDENTITY
# ============================================================


def check_aws_identity(
    region: str,
) -> dict[str, str]:
    """
    Confirm that AWS credentials are available and return
    the current caller identity.
    """

    sts = boto3.client(
        "sts",
        region_name=region,
    )

    response = sts.get_caller_identity()

    return {
        "Account": response["Account"],
        "Arn": response["Arn"],
        "UserId": response["UserId"],
    }


# ============================================================
# IAM ROLE VALIDATION
# ============================================================


def validate_role_arn(
    role_arn: str,
) -> dict[str, str]:
    """
    Validate that the supplied IAM role exists.

    This is read-only and does not modify IAM.
    """

    iam = boto3.client("iam")

    role_name = role_arn.rsplit("/", 1)[-1]

    response = iam.get_role(
        RoleName=role_name,
    )

    role = response["Role"]

    actual_arn = role["Arn"]

    if actual_arn != role_arn:
        raise ValueError(
            "The supplied SageMaker role ARN does not match "
            "the IAM role returned by AWS.\n"
            f"Supplied: {role_arn}\n"
            f"AWS:      {actual_arn}"
        )

    return {
        "RoleName": role["RoleName"],
        "Arn": role["Arn"],
        "Path": role["Path"],
    }


# ============================================================
# ENDPOINT CHECK
# ============================================================


def check_existing_endpoint(
    region: str,
    endpoint_name: str,
) -> str | None:
    """
    Return the current endpoint status.

    Returns:
        EndpointStatus if the endpoint exists.
        None if the endpoint does not exist.
    """

    client = boto3.client(
        "sagemaker",
        region_name=region,
    )

    try:
        response = client.describe_endpoint(
            EndpointName=endpoint_name,
        )

        return response["EndpointStatus"]

    except client.exceptions.ClientError as exc:
        error_code = (
            exc.response
            .get("Error", {})
            .get("Code")
        )

        if error_code == "ValidationException":
            return None

        raise


# ============================================================
# JUMPSTART MODEL METADATA
# ============================================================


def validate_model_metadata(
    region: str,
    model_id: str,
) -> dict:
    """
    Retrieve published JumpStart model metadata.

    This does not create SageMaker resources.
    """

    client = boto3.client(
        "sagemaker",
        region_name=region,
    )

    response = client.describe_hub_content(
        HubName="SageMakerPublicHub",
        HubContentType="Model",
        HubContentName=model_id,
    )

    return json.loads(
        response["HubContentDocument"]
    )


# ============================================================
# JUMPSTART DEPLOYMENT CONFIGURATION
# ============================================================


def validate_deployment_configuration(
    *,
    region: str,
    model_id: str,
    model_version: str,
    config_name: str,
    instance_type: str,
    role_arn: str,
) -> None:
    """
    Validate the requested JumpStart deployment configuration.

    The validation still uses ModelBuilder because we want the
    official JumpStart published configuration to build the model
    correctly.

    InstancePools themselves are created later with boto3 because
    the current ModelBuilder deploy() path does not expose the
    InstancePools production-variant configuration directly.
    """

    from sagemaker.core.jumpstart.configs import JumpStartConfig
    from sagemaker.serve import ModelBuilder

    print(
        "\nCreating temporary ModelBuilder for "
        "deployment-configuration validation..."
    )

    jumpstart_config = JumpStartConfig(
        model_id=model_id,
        model_version=model_version,
        inference_config_name=config_name,
    )

    model_builder = ModelBuilder.from_jumpstart_config(
        jumpstart_config=jumpstart_config,
        role_arn=role_arn,
    )

    if not hasattr(
        model_builder,
        "additional_model_data_sources",
    ):
        model_builder.additional_model_data_sources = None

    model_builder.set_deployment_config(
        config_name=config_name,
        instance_type=instance_type,
    )

    print(
        "Deployment configuration accepted by "
        "SageMaker ModelBuilder."
    )

    resolved_instance = getattr(
        model_builder,
        "instance_type",
        None,
    )

    if resolved_instance:
        print(
            f"Resolved instance type: {resolved_instance}"
        )

    resolved_config = getattr(
        model_builder,
        "deployment_config",
        None,
    )

    if resolved_config:
        print(
            f"Resolved deployment config: {resolved_config}"
        )


# ============================================================
# MODEL NAME EXTRACTION
# ============================================================


def get_model_name(model) -> str:
    """
    Extract the SageMaker model name from the SDK V3 Model
    resource returned by ModelBuilder.build().
    """

    # Most SDK V3 Model resources expose model_name.
    model_name = getattr(
        model,
        "model_name",
        None,
    )

    if model_name:
        return str(model_name)

    # Some resource representations may expose name.
    model_name = getattr(
        model,
        "name",
        None,
    )

    if model_name:
        return str(model_name)

    # Fall back to ARN extraction.
    arn = getattr(
        model,
        "arn",
        None,
    )

    if arn:
        arn = str(arn)

        return arn.rsplit("/", 1)[-1]

    raise RuntimeError(
        "SageMaker ModelBuilder created a model, but the "
        "model name could not be determined."
    )


# ============================================================
# INSTANCE POOL DISPLAY
# ============================================================


def print_instance_pools(
    instance_types: list[str],
) -> None:
    """Display the InstancePools priority order."""

    print("\n[INSTANCE POOLS]")

    print(
        "SageMaker will attempt instance types in this order:"
    )

    for priority, instance_type in enumerate(
        instance_types,
        start=1,
    ):
        if priority == 1:
            label = "PRIMARY"
        else:
            label = f"FALLBACK {priority - 1}"

        print(
            f"  Priority {priority}: "
            f"{instance_type:<18} [{label}]"
        )


# ============================================================
# CREATE INSTANCE-POOL ENDPOINT
# ============================================================


def deploy_with_instance_pools(
    *,
    region: str,
    model,
    endpoint_name: str,
    instance_types: list[str],
    provision_timeout_seconds: int,
):
    """
    Create the SageMaker endpoint using InstancePools.

    This intentionally bypasses ModelBuilder.deploy() after the
    model has been built.

    Why?

    ModelBuilder.build() is still responsible for creating the
    correct JumpStart model resource/container configuration.

    But boto3 CreateEndpointConfig gives us direct access to:

        InstancePools
        VariantInstanceProvisionTimeoutInSeconds

    which is exactly the AWS mechanism recommended for this
    insufficient-capacity situation.
    """

    if not (
        300
        <= provision_timeout_seconds
        <= 3600
    ):
        raise ValueError(
            "provision_timeout_seconds must be between "
            "300 and 3600 seconds."
        )

    client = boto3.client(
        "sagemaker",
        region_name=region,
    )

    model_name = get_model_name(model)

    # --------------------------------------------------------
    # Create a unique endpoint configuration name.
    #
    # EndpointConfig names cannot be reused once deleted.
    # --------------------------------------------------------

    timestamp = int(time.time())

    endpoint_config_name = (
        f"{endpoint_name}-pool-{timestamp}"
    )

    # --------------------------------------------------------
    # Build InstancePools.
    # --------------------------------------------------------

    instance_pools = []

    for priority, instance_type in enumerate(
        instance_types,
        start=1,
    ):
        instance_pools.append(
            {
                "InstanceType": instance_type,
                "Priority": priority,
            }
        )

    # --------------------------------------------------------
    # Create endpoint configuration.
    #
    # IMPORTANT:
    #
    # When InstancePools is supplied, we deliberately do NOT
    # supply the old single InstanceType field.
    # --------------------------------------------------------

    print("\n[ENDPOINT CONFIGURATION]")

    print(
        "Creating SageMaker EndpointConfig with "
        "InstancePools..."
    )

    print(
        f"EndpointConfig: {endpoint_config_name}"
    )

    print(
        f"Model:          {model_name}"
    )

    print(
        "Initial count:  1"
    )

    print(
        "Provision timeout: "
        f"{provision_timeout_seconds} seconds"
    )

    response = client.create_endpoint_config(
        EndpointConfigName=endpoint_config_name,
        ProductionVariants=[
            {
                "VariantName": "AllTraffic",
                "ModelName": model_name,
                "InitialInstanceCount": 1,
                "InstancePools": instance_pools,
                "VariantInstanceProvisionTimeoutInSeconds": (
                    provision_timeout_seconds
                ),
            }
        ],
    )

    print(
        "EndpointConfig created:"
    )

    print(
        response.get(
            "EndpointConfigArn",
            endpoint_config_name,
        )
    )

    # --------------------------------------------------------
    # Create endpoint.
    # --------------------------------------------------------

    print("\n[ENDPOINT]")

    print(
        f"Creating endpoint: {endpoint_name}"
    )

    client.create_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=endpoint_config_name,
    )

    print(
        "Endpoint creation requested."
    )

    # --------------------------------------------------------
    # Wait for endpoint.
    # --------------------------------------------------------

    print(
        "\n[WAIT]"
    )

    print(
        "SageMaker will now attempt the InstancePools "
        "in priority order."
    )

    print(
        "This may still take time for model download and "
        "container startup after capacity is found."
    )

    start_time = time.time()

    while True:
        response = client.describe_endpoint(
            EndpointName=endpoint_name,
        )

        status = response.get(
            "EndpointStatus",
            "Unknown",
        )

        elapsed = int(
            time.time() - start_time
        )

        print(
            f"[WAIT] Status: {status} "
            f"| elapsed: {elapsed}s"
        )

        if status == "InService":
            print(
                "\n[OK] SageMaker endpoint is InService."
            )

            return {
                "endpoint_name": endpoint_name,
                "endpoint_config_name": endpoint_config_name,
                "model_name": model_name,
                "status": status,
            }

        if status == "Failed":
            failure_reason = response.get(
                "FailureReason",
                "Unknown SageMaker failure.",
            )

            raise RuntimeError(
                "SageMaker endpoint creation failed.\n"
                f"FailureReason: {failure_reason}\n"
                f"EndpointConfig: {endpoint_config_name}\n"
                f"Model: {model_name}"
            )

        if (
            time.time() - start_time
            >= DEFAULT_ENDPOINT_TIMEOUT_SECONDS
        ):
            raise TimeoutError(
                f"Timed out waiting for endpoint "
                f"'{endpoint_name}' after "
                f"{DEFAULT_ENDPOINT_TIMEOUT_SECONDS} seconds.\n"
                f"EndpointConfig: "
                f"{endpoint_config_name}"
            )

        time.sleep(
            DEFAULT_POLL_SECONDS
        )


# ============================================================
# DEPLOY MODEL
# ============================================================


def deploy_model(
    *,
    region: str,
    model_id: str,
    model_version: str,
    endpoint_name: str,
    role_arn: str,
    instance_type: str,
    config_name: str,
    instance_types: list[str],
    provision_timeout_seconds: int,
):
    """
    Build the JumpStart model and deploy it through a custom
    InstancePools EndpointConfig.
    """

    from sagemaker.core.jumpstart.configs import JumpStartConfig
    from sagemaker.serve import ModelBuilder

    print("\n[JUMPSTART CONFIG]")

    print(
        f"Model ID:       {model_id}"
    )

    print(
        f"Model version:  {model_version}"
    )

    print(
        f"Config name:    {config_name}"
    )

    print(
        f"Primary type:   {instance_type}"
    )

    print(
        f"Execution role: {role_arn}"
    )

    print_instance_pools(
        instance_types
    )

    # --------------------------------------------------------
    # JumpStart configuration.
    # --------------------------------------------------------

    jumpstart_config = JumpStartConfig(
        model_id=model_id,
        model_version=model_version,
        inference_config_name=config_name,
    )

    # --------------------------------------------------------
    # Create ModelBuilder.
    # --------------------------------------------------------

    print(
        "\nCreating SageMaker ModelBuilder..."
    )

    model_builder = ModelBuilder.from_jumpstart_config(
        jumpstart_config=jumpstart_config,
        role_arn=role_arn,
    )

    if not hasattr(
        model_builder,
        "additional_model_data_sources",
    ):
        model_builder.additional_model_data_sources = None

    # --------------------------------------------------------
    # Select the published JumpStart configuration.
    #
    # The primary instance is used here because this is the
    # published configuration we are using to construct the
    # correct model/container.
    #
    # InstancePools are applied separately at endpoint-config
    # creation time.
    # --------------------------------------------------------

    print(
        "\n[DEPLOYMENT CONFIGURATION]"
    )

    print(
        "Selecting the requested published "
        "JumpStart deployment configuration..."
    )

    model_builder.set_deployment_config(
        config_name=config_name,
        instance_type=instance_type,
    )

    print(
        "Deployment configuration selected."
    )

    # --------------------------------------------------------
    # BUILD
    # --------------------------------------------------------

    print("\n[BUILD]")

    print(
        "Building SageMaker model resource..."
    )

    model = model_builder.build(
        region=region,
        role_arn=role_arn,
        reuse_resources=True,
    )

    print(
        "SageMaker model resource built successfully."
    )

    model_name = get_model_name(model)

    print(
        f"Model resource name: {model_name}"
    )

    # --------------------------------------------------------
    # INSTANCE-POOL DEPLOYMENT
    # --------------------------------------------------------

    print("\n[INSTANCE POOL DEPLOYMENT]")

    endpoint = deploy_with_instance_pools(
        region=region,
        model=model,
        endpoint_name=endpoint_name,
        instance_types=instance_types,
        provision_timeout_seconds=provision_timeout_seconds,
    )

    return endpoint


# ============================================================
# MAIN
# ============================================================


def main() -> int:
    """Main deployment workflow."""

    args = parse_args()

    print("=" * 72)

    print(
        "VALUEAI — PHASE 15 SAGEMAKER DEPLOYMENT"
    )

    print(
        "INSTANCE-POOL CAPACITY FALLBACK ENABLED"
    )

    print("=" * 72)

    try:
        # ----------------------------------------------------
        # Resolve configuration.
        # ----------------------------------------------------

        region = get_aws_region()

        model_id = get_sagemaker_model_id()

        endpoint_name = get_endpoint_name(
            args.endpoint_name
        )

        role_arn = normalize_role_arn(
            args.role_arn
        )

        instance_types = build_instance_pool_types(
            primary_instance_type=args.instance_type,
            fallback_instance_types=args.fallback_instance_types,
        )

        # ----------------------------------------------------
        # Configuration validation.
        # ----------------------------------------------------

        print("\n[CONFIG]")

        print(
            f"Region:              {region}"
        )

        print(
            f"Model ID:             {model_id}"
        )

        print(
            f"Model version:        {args.model_version}"
        )

        print(
            f"Endpoint:             {endpoint_name}"
        )

        print(
            f"Primary instance:     {args.instance_type}"
        )

        print(
            f"Config:               {args.config_name}"
        )

        print(
            "Provision timeout:    "
            f"{args.provision_timeout}s"
        )

        print(
            "Role ARN:             "
            + (
                role_arn
                if role_arn
                else "<not supplied>"
            )
        )

        if not endpoint_name:
            raise ValueError(
                "SageMaker endpoint name cannot be empty."
            )

        if not role_arn:
            raise ValueError(
                "An explicit --role-arn is required. "
                "The current AWS identity is an IAM user, "
                "so SageMaker SDK V3 cannot automatically "
                "resolve a serving execution role."
            )

        if not (
            300
            <= args.provision_timeout
            <= 3600
        ):
            raise ValueError(
                "--provision-timeout must be between "
                "300 and 3600 seconds."
            )

        # ----------------------------------------------------
        # Instance pools.
        # ----------------------------------------------------

        print_instance_pools(
            instance_types
        )

        # ----------------------------------------------------
        # AWS identity.
        # ----------------------------------------------------

        print("\n[AWS CREDENTIALS]")

        identity = check_aws_identity(
            region
        )

        print(
            f"Account:        {identity['Account']}"
        )

        print(
            f"Caller ARN:     {identity['Arn']}"
        )

        # ----------------------------------------------------
        # IAM execution role.
        # ----------------------------------------------------

        print("\n[IAM ROLE]")

        role = validate_role_arn(
            role_arn
        )

        print(
            f"Role name:      {role['RoleName']}"
        )

        print(
            f"Role ARN:       {role['Arn']}"
        )

        # ----------------------------------------------------
        # JumpStart model metadata.
        # ----------------------------------------------------

        print("\n[JUMPSTART MODEL]")

        metadata = validate_model_metadata(
            region=region,
            model_id=model_id,
        )

        supported_instances = metadata.get(
            "SupportedInferenceInstanceTypes",
            [],
        )

        default_instance = metadata.get(
            "DefaultInferenceInstanceType"
        )

        print(
            f"Default instance: {default_instance}"
        )

        print(
            "Supported default instances: "
            f"{', '.join(supported_instances)}"
        )

        # ----------------------------------------------------
        # Validate every InstancePool candidate.
        # ----------------------------------------------------

        invalid_pool_types = [
            instance_type
            for instance_type in instance_types
            if (
                supported_instances
                and instance_type not in supported_instances
            )
        ]

        if invalid_pool_types:
            raise ValueError(
                "The following InstancePool types are not "
                "listed in the JumpStart model metadata:\n"
                + "\n".join(
                    f"  - {value}"
                    for value in invalid_pool_types
                )
            )

        # ----------------------------------------------------
        # Existing endpoint.
        # ----------------------------------------------------

        current_status = check_existing_endpoint(
            region=region,
            endpoint_name=endpoint_name,
        )

        print("\n[ENDPOINT]")

        if current_status:
            print(
                f"Existing endpoint status: {current_status}"
            )
        else:
            print(
                "Endpoint does not currently exist."
            )

        # ----------------------------------------------------
        # Already running.
        # ----------------------------------------------------

        if current_status == "InService":
            print(
                "\nEndpoint is already InService."
            )

            print(
                "No deployment is necessary."
            )

            print("=" * 72)

            return 0

        # ----------------------------------------------------
        # Endpoint operation already in progress.
        # ----------------------------------------------------

        if current_status in {
            "Creating",
            "Updating",
            "SystemUpdating",
        }:
            raise RuntimeError(
                f"Endpoint '{endpoint_name}' is currently "
                f"{current_status}.\n"
                "Wait for the current SageMaker operation "
                "to finish or destroy the endpoint before "
                "starting another deployment."
            )

        # ----------------------------------------------------
        # Deployment configuration validation.
        # ----------------------------------------------------

        print("\n[VALIDATION]")

        print(
            "Validating the requested JumpStart "
            "deployment configuration..."
        )

        validate_deployment_configuration(
            region=region,
            model_id=model_id,
            model_version=args.model_version,
            config_name=args.config_name,
            instance_type=args.instance_type,
            role_arn=role_arn,
        )

        print(
            "\nDeployment configuration validation completed."
        )

        # ----------------------------------------------------
        # Dry run.
        # ----------------------------------------------------

        if args.dry_run:
            print("\n[DRY RUN]")

            print(
                "AWS credentials are valid."
            )

            print(
                "IAM execution role exists."
            )

            print(
                "JumpStart model metadata is available."
            )

            print(
                "JumpStart deployment configuration "
                "was accepted by ModelBuilder."
            )

            print(
                "InstancePool configuration:"
            )

            for priority, instance_type in enumerate(
                instance_types,
                start=1,
            ):
                print(
                    f"  Priority {priority}: "
                    f"{instance_type}"
                )

            print(
                "No SageMaker resources were created "
                "or modified."
            )

            print("=" * 72)

            return 0

        # ----------------------------------------------------
        # Deployment.
        # ----------------------------------------------------

        print("\n[DEPLOYMENT]")

        print(
            "Starting SageMaker deployment "
            "with automatic InstancePool fallback."
        )

        print(
            "SageMaker will try the instance types "
            "in priority order."
        )

        endpoint = deploy_model(
            region=region,
            model_id=model_id,
            model_version=args.model_version,
            endpoint_name=endpoint_name,
            role_arn=role_arn,
            instance_type=args.instance_type,
            config_name=args.config_name,
            instance_types=instance_types,
            provision_timeout_seconds=args.provision_timeout,
        )

        # ----------------------------------------------------
        # Complete.
        # ----------------------------------------------------

        print("\n[DEPLOYMENT COMPLETE]")

        print(
            f"Endpoint: "
            f"{endpoint['endpoint_name']}"
        )

        print(
            f"EndpointConfig: "
            f"{endpoint['endpoint_config_name']}"
        )

        print(
            f"Model: "
            f"{endpoint['model_name']}"
        )

        print(
            f"Status: "
            f"{endpoint['status']}"
        )

        print(
            "\nThe endpoint is now InService."
        )

        print("\n[NEXT]")

        print(
            "Run:"
        )

        print(
            "python scripts/test_sagemaker.py"
        )

        print(
            "Do not change VALUEAI_AI_PROVIDER to "
            "sagemaker until the endpoint smoke test passes."
        )

        print("=" * 72)

        return 0

    # --------------------------------------------------------
    # Expected AWS/configuration errors.
    # --------------------------------------------------------

    except (
        ValueError,
        BotoCoreError,
        ClientError,
    ) as exc:

        print("\n[FAIL]")

        print(
            str(exc)
        )

        print("=" * 72)

        return 1

    # --------------------------------------------------------
    # Unexpected errors.
    # --------------------------------------------------------

    except Exception as exc:

        print("\n[FAIL]")

        print(
            f"{type(exc).__name__}: {exc}"
        )

        print("=" * 72)

        return 1


# ============================================================
# ENTRY POINT
# ============================================================


if __name__ == "__main__":
    raise SystemExit(
        main()
    )