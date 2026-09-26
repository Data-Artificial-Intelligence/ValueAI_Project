"""
Destroy the ValueAI SageMaker deployment.

This script removes the SageMaker resources associated with
the ValueAI endpoint:

1. SageMaker endpoint
2. Endpoint configuration
3. SageMaker model

The IAM execution role is intentionally NOT deleted.

This script is designed to clean up both:

    - InService endpoints
    - Failed endpoints caused by insufficient capacity
    - Endpoints interrupted while Creating

Usage:

    python scripts/destroy_sagemaker.py

Optional:

    python scripts/destroy_sagemaker.py `
        --endpoint-name valueai-qwen25-7b

    python scripts/destroy_sagemaker.py `
        --dry-run
"""

from __future__ import annotations

import argparse
import sys
import time

import boto3

from botocore.exceptions import (
    BotoCoreError,
    ClientError,
)


# ============================================================
# DEFAULTS
# ============================================================

DEFAULT_REGION = "us-east-1"

DEFAULT_ENDPOINT_NAME = "valueai-qwen25-7b"

DEFAULT_POLL_SECONDS = 10

DEFAULT_TIMEOUT_SECONDS = 1800


# ============================================================
# CLIENT
# ============================================================


def build_client(region: str):
    """Create the SageMaker client."""

    return boto3.client(
        "sagemaker",
        region_name=region,
    )


# ============================================================
# ENDPOINT
# ============================================================


def endpoint_exists(
    client,
    endpoint_name: str,
) -> bool:
    """Return True if the endpoint exists."""

    try:

        client.describe_endpoint(
            EndpointName=endpoint_name
        )

        return True

    except client.exceptions.ClientError as exc:

        error_code = (
            exc.response
            .get("Error", {})
            .get("Code")
        )

        if error_code == "ValidationException":
            return False

        raise


def get_endpoint_resources(
    client,
    endpoint_name: str,
) -> tuple[str | None, str | None]:
    """
    Retrieve:

        endpoint configuration name
        model name

    from the endpoint.

    Returns:

        (endpoint_config_name, model_name)
    """

    endpoint = client.describe_endpoint(
        EndpointName=endpoint_name
    )

    endpoint_config_name = endpoint.get(
        "EndpointConfigName"
    )

    if not endpoint_config_name:
        return None, None

    endpoint_config = client.describe_endpoint_config(
        EndpointConfigName=endpoint_config_name
    )

    production_variants = endpoint_config.get(
        "ProductionVariants",
        [],
    )

    if not production_variants:
        return endpoint_config_name, None

    model_name = production_variants[0].get(
        "ModelName"
    )

    return endpoint_config_name, model_name


# ============================================================
# DELETE ENDPOINT
# ============================================================


def delete_endpoint(
    client,
    endpoint_name: str,
) -> None:
    """Delete the SageMaker real-time endpoint."""

    try:

        print()
        print(
            f"[DELETE] Endpoint: {endpoint_name}"
        )

        client.delete_endpoint(
            EndpointName=endpoint_name
        )

        print(
            "[OK] Endpoint deletion requested."
        )

    except client.exceptions.ClientError as exc:

        error_code = (
            exc.response
            .get("Error", {})
            .get("Code")
        )

        if error_code == "ValidationException":

            print(
                "[INFO] Endpoint does not exist."
            )

            return

        raise


# ============================================================
# WAIT FOR ENDPOINT
# ============================================================


def wait_for_endpoint_deleted(
    client,
    endpoint_name: str,
    poll_seconds: int = DEFAULT_POLL_SECONDS,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> None:
    """
    Wait until SageMaker confirms that the endpoint
    has been deleted.
    """

    print()
    print(
        "[WAIT] Waiting for endpoint deletion..."
    )

    start = time.time()

    while True:

        try:

            response = client.describe_endpoint(
                EndpointName=endpoint_name
            )

            status = response.get(
                "EndpointStatus",
                "UNKNOWN",
            )

            elapsed = int(
                time.time() - start
            )

            print(
                f"[WAIT] Endpoint status: {status} "
                f"| elapsed: {elapsed}s"
            )

            if (
                time.time() - start
                >= timeout_seconds
            ):

                raise TimeoutError(
                    f"Timed out waiting for endpoint "
                    f"'{endpoint_name}' to be deleted."
                )

            time.sleep(
                poll_seconds
            )

        except client.exceptions.ClientError as exc:

            error_code = (
                exc.response
                .get("Error", {})
                .get("Code")
            )

            if error_code == "ValidationException":

                print(
                    "[OK] Endpoint has been deleted."
                )

                return

            raise


# ============================================================
# DELETE ENDPOINT CONFIG
# ============================================================


def delete_endpoint_config(
    client,
    endpoint_config_name: str | None,
) -> None:
    """Delete the endpoint configuration."""

    if not endpoint_config_name:

        print(
            "[INFO] No endpoint configuration found."
        )

        return

    try:

        print()
        print(
            "[DELETE] Endpoint configuration: "
            f"{endpoint_config_name}"
        )

        client.delete_endpoint_config(
            EndpointConfigName=endpoint_config_name
        )

        print(
            "[OK] Endpoint configuration deleted."
        )

    except client.exceptions.ClientError as exc:

        error_code = (
            exc.response
            .get("Error", {})
            .get("Code")
        )

        if error_code == "ValidationException":

            print(
                "[INFO] Endpoint configuration "
                "does not exist."
            )

            return

        raise


# ============================================================
# DELETE MODEL
# ============================================================


def delete_model(
    client,
    model_name: str | None,
) -> None:
    """Delete the SageMaker model."""

    if not model_name:

        print(
            "[INFO] No SageMaker model found."
        )

        return

    try:

        print()
        print(
            f"[DELETE] Model: {model_name}"
        )

        client.delete_model(
            ModelName=model_name
        )

        print(
            "[OK] SageMaker model deleted."
        )

    except client.exceptions.ClientError as exc:

        error_code = (
            exc.response
            .get("Error", {})
            .get("Code")
        )

        if error_code == "ValidationException":

            print(
                "[INFO] SageMaker model "
                "does not exist."
            )

            return

        raise


# ============================================================
# PARSE ARGS
# ============================================================


def parse_args():

    parser = argparse.ArgumentParser(
        description=(
            "Destroy the ValueAI SageMaker deployment."
        )
    )

    parser.add_argument(
        "--endpoint-name",
        default=DEFAULT_ENDPOINT_NAME,
        help=(
            "SageMaker endpoint name. "
            f"Default: {DEFAULT_ENDPOINT_NAME}"
        ),
    )

    parser.add_argument(
        "--region",
        default=DEFAULT_REGION,
        help=(
            "AWS region. "
            f"Default: {DEFAULT_REGION}"
        ),
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Show what would be deleted without "
            "deleting resources."
        ),
    )

    return parser.parse_args()


# ============================================================
# MAIN
# ============================================================


def main() -> int:

    args = parse_args()

    print("=" * 72)

    print(
        "VALUEAI — SAGEMAKER RESOURCE DESTRUCTION"
    )

    print("=" * 72)

    print()

    print("[CONFIG]")

    print(
        f"Region:   {args.region}"
    )

    print(
        f"Endpoint: {args.endpoint_name}"
    )

    client = build_client(
        args.region
    )

    try:

        # ----------------------------------------------------
        # AWS identity
        # ----------------------------------------------------

        sts = boto3.client(
            "sts",
            region_name=args.region,
        )

        identity = sts.get_caller_identity()

        print()

        print("[AWS CREDENTIALS]")

        print(
            f"Account:     {identity['Account']}"
        )

        print(
            f"Caller ARN:  {identity['Arn']}"
        )

        # ----------------------------------------------------
        # Endpoint lookup
        # ----------------------------------------------------

        exists = endpoint_exists(
            client,
            args.endpoint_name,
        )

        if not exists:

            print()

            print("[INFO]")

            print(
                f"Endpoint '{args.endpoint_name}' "
                "does not exist."
            )

            print(
                "No endpoint resources can be discovered "
                "through the endpoint."
            )

            print(
                "If a previous deployment was interrupted "
                "before endpoint creation, inspect SageMaker "
                "Models and Endpoint configurations manually."
            )

            print("=" * 72)

            return 0

        # ----------------------------------------------------
        # Discover resources.
        # ----------------------------------------------------

        endpoint_config_name, model_name = (
            get_endpoint_resources(
                client,
                args.endpoint_name,
            )
        )

        print()

        print("[RESOURCES FOUND]")

        print(
            f"Endpoint:          "
            f"{args.endpoint_name}"
        )

        print(
            "Endpoint config:   "
            f"{endpoint_config_name or 'NOT FOUND'}"
        )

        print(
            f"Model:             "
            f"{model_name or 'NOT FOUND'}"
        )

        # ----------------------------------------------------
        # Dry run.
        # ----------------------------------------------------

        if args.dry_run:

            print()

            print("[DRY RUN]")

            print(
                "The following resources would be deleted:"
            )

            print(
                f"  Endpoint:        "
                f"{args.endpoint_name}"
            )

            print(
                f"  Endpoint config: "
                f"{endpoint_config_name or 'N/A'}"
            )

            print(
                f"  Model:           "
                f"{model_name or 'N/A'}"
            )

            print(
                "IAM execution role would be retained."
            )

            print("=" * 72)

            return 0

        # ----------------------------------------------------
        # Confirmation.
        # ----------------------------------------------------

        print()

        print("[WARNING]")

        print(
            "This will delete:"
        )

        print(
            f"  - Endpoint: "
            f"{args.endpoint_name}"
        )

        print(
            f"  - Endpoint configuration: "
            f"{endpoint_config_name or 'N/A'}"
        )

        print(
            f"  - SageMaker model: "
            f"{model_name or 'N/A'}"
        )

        print()

        print(
            "The IAM execution role will NOT be deleted."
        )

        confirmation = input(
            "\nType DELETE to continue: "
        ).strip()

        if confirmation != "DELETE":

            print()

            print("[CANCELLED]")

            print(
                "No resources were deleted."
            )

            print("=" * 72)

            return 0

        # ----------------------------------------------------
        # 1. Delete endpoint
        # ----------------------------------------------------

        delete_endpoint(
            client,
            args.endpoint_name,
        )

        # ----------------------------------------------------
        # 2. Wait
        # ----------------------------------------------------

        wait_for_endpoint_deleted(
            client,
            args.endpoint_name,
        )

        # ----------------------------------------------------
        # 3. Delete endpoint configuration
        # ----------------------------------------------------

        delete_endpoint_config(
            client,
            endpoint_config_name,
        )

        # ----------------------------------------------------
        # 4. Delete model
        # ----------------------------------------------------

        delete_model(
            client,
            model_name,
        )

        # ----------------------------------------------------
        # Complete.
        # ----------------------------------------------------

        print()

        print("=" * 72)

        print(
            "VALUEAI SAGEMAKER CLEANUP COMPLETE"
        )

        print("=" * 72)

        print()

        print("[DELETED]")

        print(
            f"Endpoint:        "
            f"{args.endpoint_name}"
        )

        print(
            f"Endpoint config: "
            f"{endpoint_config_name or 'N/A'}"
        )

        print(
            f"Model:           "
            f"{model_name or 'N/A'}"
        )

        print()

        print("[RETAINED]")

        print(
            "IAM execution role: "
            "ValueAI-SageMaker-ExecutionRole"
        )

        print()

        print(
            "The IAM role remains available for the "
            "next deployment."
        )

        return 0

    except KeyboardInterrupt:

        print()

        print(
            "[CANCELLED] Operation interrupted."
        )

        return 130

    except TimeoutError as exc:

        print()

        print(
            f"[ERROR] {exc}"
        )

        return 1

    except (
        BotoCoreError,
        ClientError,
    ) as exc:

        print()

        print("[AWS ERROR]")

        print(
            str(exc)
        )

        return 1

    except Exception as exc:

        print()

        print("[ERROR]")

        print(
            f"{type(exc).__name__}: {exc}"
        )

        return 1


# ============================================================
# ENTRY POINT
# ============================================================


if __name__ == "__main__":

    sys.exit(
        main()
    )