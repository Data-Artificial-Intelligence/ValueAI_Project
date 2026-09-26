"""
ValueAI SageMaker Integration Test
===================================

Phase 14 acceptance test for Phases 9-14.

Tests:

    1. AWS configuration
    2. AWS credential resolution
    3. AWS identity
    4. SageMaker endpoint existence
    5. SageMaker endpoint status
    6. Raw Qwen endpoint invocation
    7. ValueAI evidence-first SageMaker invocation

This script does NOT:

    - create AWS resources
    - deploy a SageMaker endpoint
    - modify AWS resources
    - modify .env
    - modify agent_graph.py
    - fall back to Ollama

A live endpoint is required for the final two tests.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )


# ============================================================
# THIRD-PARTY IMPORTS
# ============================================================

import boto3
from botocore.exceptions import BotoCoreError, ClientError


# ============================================================
# VALUEAI IMPORTS
# ============================================================

from src.ai_agent.sagemaker_agent import (
    build_sagemaker_payload,
    invoke_sagemaker_agent,
    invoke_sagemaker_endpoint,
)
from src.utils.config import (
    get_aws_region,
    get_sagemaker_endpoint_name,
    get_sagemaker_model_id,
    get_sagemaker_max_new_tokens,
    get_sagemaker_temperature,
    get_sagemaker_top_p,
)


# ============================================================
# TEST CONFIGURATION
# ============================================================

RAW_TEST_PROMPT = (
    "Respond with exactly one short sentence: "
    "What is the purpose of a healthcare data analytics platform?"
)

EVIDENCE_TEST_QUERY = (
    "Analyze the high-risk cluster and give 3 strategic recommendations."
)


# ============================================================
# OUTPUT HELPERS
# ============================================================


def success(message: str) -> None:
    print(f"[PASS] {message}")


def info(message: str) -> None:
    print(f"[INFO] {message}")


def failure(message: str) -> None:
    print(f"[FAIL] {message}")


# ============================================================
# PHASE 12 — CONFIGURATION TEST
# ============================================================


def test_configuration() -> tuple[str, str]:
    print()
    print("=" * 72)
    print("TEST 1 — SAGEMAKER CONFIGURATION")
    print("=" * 72)

    region = get_aws_region()
    endpoint_name = get_sagemaker_endpoint_name()
    model_id = get_sagemaker_model_id()
    max_new_tokens = get_sagemaker_max_new_tokens()
    temperature = get_sagemaker_temperature()
    top_p = get_sagemaker_top_p()

    info(f"AWS Region: {region}")
    info(f"Endpoint: {endpoint_name}")
    info(f"Expected Model ID: {model_id}")
    info(f"Max New Tokens: {max_new_tokens}")
    info(f"Temperature: {temperature}")
    info(f"Top P: {top_p}")

    if not endpoint_name.strip():
        raise RuntimeError(
            "VALUEAI_SAGEMAKER_ENDPOINT_NAME is empty. "
            "A live SageMaker endpoint must exist before the "
            "full Phase 14 test can run."
        )

    success("SageMaker configuration is present.")

    return region, endpoint_name


# ============================================================
# AWS CREDENTIAL TEST
# ============================================================


def test_aws_credentials(
    region: str,
) -> None:
    print()
    print("=" * 72)
    print("TEST 2 — AWS CREDENTIALS / IDENTITY")
    print("=" * 72)

    session = boto3.Session(
        region_name=region
    )

    credentials = session.get_credentials()

    if credentials is None:
        raise RuntimeError(
            "No AWS credentials were resolved by boto3."
        )

    success(
        "AWS credentials were resolved by the boto3 credential chain."
    )

    sts = session.client(
        "sts"
    )

    try:

        identity = sts.get_caller_identity()

    except (ClientError, BotoCoreError) as exc:

        raise RuntimeError(
            f"AWS identity check failed: {exc}"
        ) from exc

    success("AWS identity check succeeded.")

    account = identity.get(
        "Account",
        "<unknown>",
    )

    arn = identity.get(
        "Arn",
        "<unknown>",
    )

    info(f"AWS Account: {account}")
    info(f"AWS Identity: {arn}")


# ============================================================
# ENDPOINT TEST
# ============================================================


def test_endpoint_status(
    region: str,
    endpoint_name: str,
) -> dict:
    print()
    print("=" * 72)
    print("TEST 3 — SAGEMAKER ENDPOINT STATUS")
    print("=" * 72)

    client = boto3.client(
        "sagemaker",
        region_name=region,
    )

    try:

        response = client.describe_endpoint(
            EndpointName=endpoint_name
        )

    except ClientError as exc:

        error = exc.response.get(
            "Error",
            {},
        )

        raise RuntimeError(
            "Unable to describe SageMaker endpoint. "
            f"Code: {error.get('Code', 'Unknown')}. "
            f"Message: {error.get('Message', str(exc))}"
        ) from exc

    status = response.get(
        "EndpointStatus"
    )

    info(f"Endpoint: {endpoint_name}")
    info(f"Endpoint Status: {status}")

    if status != "InService":
        raise RuntimeError(
            f"SageMaker endpoint is not InService. "
            f"Current status: {status}"
        )

    success(
        "SageMaker endpoint exists and is InService."
    )

    return response


# ============================================================
# RAW PAYLOAD CONTRACT TEST
# ============================================================


def test_payload_contract() -> None:
    print()
    print("=" * 72)
    print("TEST 4 — SAGEMAKER PAYLOAD CONTRACT")
    print("=" * 72)

    payload = build_sagemaker_payload(
        RAW_TEST_PROMPT
    )

    info(
        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False,
        )
    )

    if payload.get("inputs") != RAW_TEST_PROMPT:
        raise RuntimeError(
            "Payload 'inputs' field is incorrect."
        )

    parameters = payload.get(
        "parameters"
    )

    if not isinstance(
        parameters,
        dict,
    ):
        raise RuntimeError(
            "Payload 'parameters' object is missing."
        )

    required_parameters = {
        "max_new_tokens",
        "temperature",
        "top_p",
        "return_full_text",
    }

    missing = (
        required_parameters
        - set(parameters.keys())
    )

    if missing:
        raise RuntimeError(
            "Payload is missing parameters: "
            + ", ".join(sorted(missing))
        )

    success(
        "SageMaker Qwen text-generation payload contract is valid."
    )


# ============================================================
# RAW ENDPOINT INVOCATION
# ============================================================


def test_raw_endpoint() -> str:
    print()
    print("=" * 72)
    print("TEST 5 — RAW SAGEMAKER QWEN INVOCATION")
    print("=" * 72)

    response = invoke_sagemaker_endpoint(
        RAW_TEST_PROMPT
    )

    if not response.strip():
        raise RuntimeError(
            "SageMaker returned an empty generated response."
        )

    success(
        "Raw SageMaker inference succeeded."
    )

    print()
    print("SageMaker Response:")
    print("-" * 72)
    print(response)
    print("-" * 72)

    return response


# ============================================================
# EVIDENCE-FIRST INTEGRATION TEST
# ============================================================


def test_evidence_first_agent() -> str:
    print()
    print("=" * 72)
    print("TEST 6 — VALUEAI EVIDENCE-FIRST SAGEMAKER AGENT")
    print("=" * 72)

    info(
        "Test query:"
    )

    print(
        EVIDENCE_TEST_QUERY
    )

    response = invoke_sagemaker_agent(
        EVIDENCE_TEST_QUERY
    )

    if not response.strip():
        raise RuntimeError(
            "Evidence-first SageMaker agent returned an empty response."
        )

    success(
        "ValueAI evidence-first SageMaker invocation succeeded."
    )

    print()
    print("ValueAI SageMaker Response:")
    print("-" * 72)
    print(response)
    print("-" * 72)

    return response


# ============================================================
# MAIN
# ============================================================


def main() -> int:

    print()
    print("=" * 72)
    print("VALUEAI — PHASE 9-14 SAGEMAKER ACCEPTANCE TEST")
    print("=" * 72)

    print()
    print(
        "This test validates the SageMaker provider without "
        "modifying the frozen local agent."
    )

    try:

        # ----------------------------------------------------
        # Phase 12
        # ----------------------------------------------------

        region, endpoint_name = test_configuration()

        # ----------------------------------------------------
        # AWS credential chain
        # ----------------------------------------------------

        test_aws_credentials(
            region
        )

        # ----------------------------------------------------
        # Endpoint status
        # ----------------------------------------------------

        test_endpoint_status(
            region,
            endpoint_name,
        )

        # ----------------------------------------------------
        # Phase 9 payload contract
        # ----------------------------------------------------

        test_payload_contract()

        # ----------------------------------------------------
        # Phase 14 raw endpoint
        # ----------------------------------------------------

        test_raw_endpoint()

        # ----------------------------------------------------
        # Phases 10 + 11 + 14
        # ----------------------------------------------------

        test_evidence_first_agent()

    except Exception as exc:

        failure(
            str(exc)
        )

        print()
        print("=" * 72)
        print("SAGEMAKER ACCEPTANCE TEST FAILED")
        print("=" * 72)

        return 1

    print()
    print("=" * 72)
    print("SAGEMAKER ACCEPTANCE TEST PASSED")
    print("=" * 72)

    print()
    print("Validated:")
    print("  ✓ Phase 9  — SageMaker inference contract")
    print("  ✓ Phase 10 — Evidence-first SageMaker architecture")
    print("  ✓ Phase 11 — SageMaker agent adapter")
    print("  ✓ Phase 12 — AWS/SageMaker configuration")
    print("  ✓ Phase 13 — Existing boto3 dependency is sufficient")
    print("  ✓ Phase 14 — Independent SageMaker endpoint invocation")
    print("  ✓ No local/Ollama fallback was used")

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )