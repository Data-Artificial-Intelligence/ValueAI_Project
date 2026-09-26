"""
ValueAI SageMaker AI Provider
================================

SageMaker implementation of the ValueAI evidence-first AI assistant.

Architecture:

    User Question
          |
          v
    sagemaker_agent.py
          |
          v
    Frozen agent_graph evidence router
          |
          v
    agent_tools.py
          |
          v
    Verified Analytical Evidence
          |
          v
    Evidence-First Prompt
          |
          v
    AWS SageMaker Runtime
          |
          v
    Qwen2.5-7B-Instruct
          |
          v
    Final Executive Response

IMPORTANT
---------
src/ai_agent/agent_graph.py is FROZEN.

This module reuses its deterministic evidence retrieval machinery
without modifying the existing LangGraph implementation.

This module does NOT:
    - modify agent_graph.py
    - initialize Ollama
    - initialize ChatOllama
    - retrain analytical models
    - rebuild datasets
    - modify agent_tools.py
    - silently fall back to Local/Ollama
"""

from __future__ import annotations

import json
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from src.ai_agent.agent_graph import (
    SYSTEM_PROMPT,
    retrieve_evidence,
)
from src.utils.config import (
    get_aws_region,
    get_sagemaker_endpoint_name,
    get_sagemaker_max_new_tokens,
    get_sagemaker_temperature,
    get_sagemaker_top_p,
)


# ============================================================
# CONSTANTS
# ============================================================

SAGEMAKER_CONTENT_TYPE = "application/json"
SAGEMAKER_ACCEPT = "application/json"


# ============================================================
# EXCEPTIONS
# ============================================================


class SageMakerConfigurationError(RuntimeError):
    """Raised when SageMaker configuration is incomplete."""


class SageMakerInvocationError(RuntimeError):
    """Raised when SageMaker inference fails."""


class SageMakerResponseError(RuntimeError):
    """Raised when SageMaker returns an unexpected response."""


# ============================================================
# CLIENT
# ============================================================


def _get_runtime_client():
    """
    Create the AWS SageMaker Runtime client.

    AWS credentials are resolved through boto3's normal credential
    chain. No credentials are hard-coded in this application.
    """

    try:
        return boto3.client(
            "sagemaker-runtime",
            region_name=get_aws_region(),
        )

    except Exception as exc:
        raise SageMakerConfigurationError(
            f"Unable to initialize SageMaker Runtime client: {exc}"
        ) from exc


# ============================================================
# EVIDENCE PROMPT
# ============================================================


def _build_evidence_prompt(
    user_query: str,
    evidence_state: dict[str, Any],
) -> str:
    """
    Build the same evidence-first prompt contract used by the
    frozen local ValueAI agent.

    The analytical evidence is retrieved before this function
    constructs the final LLM request.
    """

    evidence = evidence_state.get(
        "evidence",
        {},
    )

    evidence_source = evidence_state.get(
        "evidence_source",
        "none",
    )

    evidence_json = json.dumps(
        evidence,
        indent=2,
        ensure_ascii=False,
    )

    return f"""
VERIFIED ANALYTICAL EVIDENCE
============================

Evidence source:
{evidence_source}

The following JSON was retrieved directly from the ValueAI
analytical artifacts before this response was generated.

Treat this evidence as authoritative.

{evidence_json}


USER QUESTION
=============

{user_query}


RESPONSE REQUIREMENTS
=====================

Answer the user's question using the verified evidence above.

Do not invent quantitative values.

Do not introduce numerical values that are absent from the evidence.

Do not alter the meaning of the evidence.

If the evidence does not establish something, explicitly say so.

Keep observed data, model importance, model predictions, and causal
evidence separate.

If the question concerns SHAP, remember that the supplied SHAP values
are mean absolute SHAP values and therefore provide importance magnitude,
not direction or causation.

If strategic recommendations are requested, provide proposed
interventions only and describe them as hypotheses for evaluation.

Never claim that an intervention will reduce readmissions, costs,
utilization, length of stay, or generate savings unless such evidence
is explicitly supplied.

When the question is a high-risk cluster or strategic business
question, follow the executive response structure in the system
instructions.
"""


# ============================================================
# SAGEMAKER PAYLOAD
# ============================================================


def build_sagemaker_payload(
    prompt: str,
) -> dict[str, Any]:
    """
    Build the JSON payload expected by the SageMaker
    Qwen2.5-7B-Instruct text-generation endpoint.

    Contract:

        {
            "inputs": "...",
            "parameters": {
                "max_new_tokens": ...,
                "temperature": ...,
                "top_p": ...,
                "return_full_text": false
            }
        }
    """

    return {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": get_sagemaker_max_new_tokens(),
            "temperature": get_sagemaker_temperature(),
            "top_p": get_sagemaker_top_p(),
            "return_full_text": False,
        },
    }


# ============================================================
# RESPONSE PARSING
# ============================================================


def parse_sagemaker_response(
    response_body: str,
) -> str:
    """
    Parse a SageMaker text-generation response.

    Primary expected format:

        [
            {
                "generated_text": "..."
            }
        ]

    A dictionary form is also supported for compatibility.
    """

    try:
        parsed = json.loads(
            response_body
        )

    except json.JSONDecodeError as exc:
        raise SageMakerResponseError(
            "SageMaker returned a response that is not valid JSON."
        ) from exc

    generated_text: str | None = None

    # --------------------------------------------------------
    # Standard Hugging Face / JumpStart format
    # --------------------------------------------------------

    if isinstance(parsed, list) and parsed:

        first = parsed[0]

        if isinstance(first, dict):

            value = first.get(
                "generated_text"
            )

            if isinstance(value, str):
                generated_text = value

            # Some serving configurations may return:
            # {"generation": {"content": "..."}}
            if generated_text is None:

                generation = first.get(
                    "generation"
                )

                if isinstance(
                    generation,
                    dict,
                ):

                    content = generation.get(
                        "content"
                    )

                    if isinstance(
                        content,
                        str,
                    ):
                        generated_text = content

    # --------------------------------------------------------
    # Dictionary format
    # --------------------------------------------------------

    elif isinstance(parsed, dict):

        value = parsed.get(
            "generated_text"
        )

        if isinstance(value, str):
            generated_text = value

        if generated_text is None:

            generation = parsed.get(
                "generation"
            )

            if isinstance(
                generation,
                dict,
            ):

                content = generation.get(
                    "content"
                )

                if isinstance(
                    content,
                    str,
                ):
                    generated_text = content

        if generated_text is None:

            choices = parsed.get(
                "choices"
            )

            if isinstance(
                choices,
                list,
            ) and choices:

                first_choice = choices[0]

                if isinstance(
                    first_choice,
                    dict,
                ):

                    text = first_choice.get(
                        "text"
                    )

                    if isinstance(
                        text,
                        str,
                    ):
                        generated_text = text

    if not generated_text:
        raise SageMakerResponseError(
            "SageMaker returned JSON, but no generated text "
            "could be extracted from the response."
        )

    return generated_text.strip()


# ============================================================
# RAW SAGEMAKER INVOCATION
# ============================================================


def invoke_sagemaker_endpoint(
    prompt: str,
) -> str:
    """
    Invoke the configured SageMaker endpoint directly.

    This function performs inference only.

    It does NOT perform evidence retrieval.
    """

    if not prompt or not prompt.strip():
        raise ValueError(
            "SageMaker prompt cannot be empty."
        )

    endpoint_name = get_sagemaker_endpoint_name()

    payload = build_sagemaker_payload(
        prompt.strip()
    )

    runtime_client = _get_runtime_client()

    try:

        response = runtime_client.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType=SAGEMAKER_CONTENT_TYPE,
            Accept=SAGEMAKER_ACCEPT,
            Body=json.dumps(
                payload
            ).encode("utf-8"),
        )

    except ClientError as exc:

        error = exc.response.get(
            "Error",
            {},
        )

        error_code = error.get(
            "Code",
            "Unknown",
        )

        error_message = error.get(
            "Message",
            str(exc),
        )

        raise SageMakerInvocationError(
            "SageMaker endpoint invocation failed. "
            f"Code: {error_code}. "
            f"Message: {error_message}"
        ) from exc

    except BotoCoreError as exc:

        raise SageMakerInvocationError(
            f"AWS SDK error while invoking SageMaker: {exc}"
        ) from exc

    except Exception as exc:

        raise SageMakerInvocationError(
            f"Unexpected SageMaker invocation error: {exc}"
        ) from exc

    body = response.get(
        "Body"
    )

    if body is None:
        raise SageMakerResponseError(
            "SageMaker response did not contain a response body."
        )

    try:

        response_body = body.read().decode(
            "utf-8"
        )

    except Exception as exc:

        raise SageMakerResponseError(
            f"Unable to read SageMaker response body: {exc}"
        ) from exc

    return parse_sagemaker_response(
        response_body
    )


# ============================================================
# EVIDENCE-FIRST SAGEMAKER AGENT
# ============================================================


def invoke_sagemaker_agent(
    user_query: str,
) -> str:
    """
    Run the complete ValueAI SageMaker evidence-first workflow.

    Flow:

        user query
             |
             v
        deterministic evidence retrieval
             |
             v
        verified analytical evidence
             |
             v
        evidence-first prompt
             |
             v
        SageMaker Qwen
             |
             v
        final response

    There is intentionally NO fallback to the local Ollama agent.
    """

    if not user_query or not user_query.strip():
        raise ValueError(
            "User query cannot be empty."
        )

    normalized_query = user_query.strip()

    # --------------------------------------------------------
    # Retrieve deterministic ValueAI evidence.
    #
    # This reuses the frozen evidence machinery from
    # agent_graph.py.
    # --------------------------------------------------------

    evidence_state = retrieve_evidence(
        {
            "user_query": normalized_query,
        }
    )

    prompt = _build_evidence_prompt(
        normalized_query,
        evidence_state,
    )

    # --------------------------------------------------------
    # Send evidence-grounded prompt to SageMaker.
    # --------------------------------------------------------

    return invoke_sagemaker_endpoint(
        prompt
    )


__all__ = [
    "SageMakerConfigurationError",
    "SageMakerInvocationError",
    "SageMakerResponseError",
    "build_sagemaker_payload",
    "parse_sagemaker_response",
    "invoke_sagemaker_endpoint",
    "invoke_sagemaker_agent",
]