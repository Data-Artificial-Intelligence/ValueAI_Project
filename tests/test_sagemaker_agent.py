"""
ValueAI — SageMaker Agent Contract Tests
==========================================

Tests for:

    src.ai_agent.sagemaker_agent

These tests DO NOT:
    - call AWS
    - call SageMaker
    - call Ollama
    - call the live endpoint
    - create AWS resources
    - modify the frozen agent_graph.py
    - require a running SageMaker endpoint

They verify:

    1. SageMaker payload construction
    2. SageMaker response parsing
    3. Invalid response handling
    4. Empty prompt validation
    5. AWS runtime client initialization
    6. SageMaker ClientError translation
    7. SageMaker BotoCoreError translation
    8. Missing response body handling
    9. Response body read/decode handling
    10. Evidence-first prompt construction
    11. Evidence retrieval before SageMaker invocation
    12. User-query normalization
    13. Empty user-query validation
    14. No silent local/Ollama fallback
    15. Complete evidence-first SageMaker agent flow

Run:

    pytest -q tests/test_sagemaker_agent.py

Run with verbose output:

    pytest -v tests/test_sagemaker_agent.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import BotoCoreError, ClientError


# ============================================================
# PROJECT ROOT / IMPORT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# APPLICATION IMPORTS
# ============================================================

from src.ai_agent import sagemaker_agent


from src.ai_agent.sagemaker_agent import (
    SAGEMAKER_ACCEPT,
    SAGEMAKER_CONTENT_TYPE,
    SageMakerConfigurationError,
    SageMakerInvocationError,
    SageMakerResponseError,
    _build_evidence_prompt,
    build_sagemaker_payload,
    invoke_sagemaker_agent,
    invoke_sagemaker_endpoint,
    parse_sagemaker_response,
)


# ============================================================
# TEST DATA
# ============================================================

TEST_PROMPT = (
    "What increases readmission risk?"
)

TEST_QUERY = (
    "Explain the main readmission risk drivers."
)

TEST_GENERATED_TEXT = (
    "ValueAI SageMaker response"
)

TEST_EVIDENCE_STATE = {
    "evidence": {
        "readmission_rate": 0.23,
        "high_risk_cluster": {
            "size": 1250,
            "readmission_rate": 0.41,
        },
    },
    "evidence_source": "verified analytical artifacts",
}


# ============================================================
# HELPERS
# ============================================================


def make_streaming_body(
    content: str,
) -> MagicMock:
    """
    Create a fake SageMaker StreamingBody-like object.
    """

    body = MagicMock()

    body.read.return_value = content.encode(
        "utf-8"
    )

    return body


def make_client_error(
    code: str = "ValidationException",
    message: str = "Test SageMaker error",
) -> ClientError:
    """
    Create a deterministic boto3 ClientError for testing.
    """

    return ClientError(
        {
            "Error": {
                "Code": code,
                "Message": message,
            }
        },
        "InvokeEndpoint",
    )


# ============================================================
# PAYLOAD TESTS
# ============================================================


def test_sagemaker_payload_contains_inputs() -> None:
    """
    The payload must preserve the supplied prompt.
    """

    payload = build_sagemaker_payload(
        TEST_PROMPT
    )

    assert isinstance(
        payload,
        dict,
    )

    assert payload["inputs"] == TEST_PROMPT


def test_sagemaker_payload_contains_generation_parameters() -> None:
    """
    The payload must contain the generation parameters required
    by the SageMaker Qwen endpoint.
    """

    payload = build_sagemaker_payload(
        TEST_PROMPT
    )

    parameters = payload.get(
        "parameters"
    )

    assert isinstance(
        parameters,
        dict,
    )

    assert "max_new_tokens" in parameters
    assert "temperature" in parameters
    assert "top_p" in parameters
    assert "return_full_text" in parameters


def test_sagemaker_payload_return_full_text_is_false() -> None:
    """
    ValueAI expects only the generated completion rather than
    the original prompt being returned as part of the response.
    """

    payload = build_sagemaker_payload(
        TEST_PROMPT
    )

    assert (
        payload["parameters"]["return_full_text"]
        is False
    )


def test_sagemaker_payload_uses_configured_generation_values() -> None:
    """
    Generation settings must come from the ValueAI configuration
    helpers rather than being hard-coded inside the payload builder.
    """

    with patch(
        "src.ai_agent.sagemaker_agent.get_sagemaker_max_new_tokens",
        return_value=777,
    ), patch(
        "src.ai_agent.sagemaker_agent.get_sagemaker_temperature",
        return_value=0.25,
    ), patch(
        "src.ai_agent.sagemaker_agent.get_sagemaker_top_p",
        return_value=0.91,
    ):

        payload = build_sagemaker_payload(
            TEST_PROMPT
        )

    parameters = payload["parameters"]

    assert parameters["max_new_tokens"] == 777
    assert parameters["temperature"] == 0.25
    assert parameters["top_p"] == 0.91
    assert parameters["return_full_text"] is False


# ============================================================
# RESPONSE PARSING TESTS
# ============================================================


def test_parse_sagemaker_response_parses_jumpstart_format() -> None:
    """
    Verify the primary Hugging Face / JumpStart response format:

        [
            {
                "generated_text": "..."
            }
        ]
    """

    raw_response = json.dumps(
        [
            {
                "generated_text": TEST_GENERATED_TEXT
            }
        ]
    )

    result = parse_sagemaker_response(
        raw_response
    )

    assert result == TEST_GENERATED_TEXT


def test_parse_sagemaker_response_strips_whitespace() -> None:
    """
    Generated text should be returned without surrounding
    whitespace.
    """

    raw_response = json.dumps(
        [
            {
                "generated_text": (
                    "   ValueAI response   "
                )
            }
        ]
    )

    result = parse_sagemaker_response(
        raw_response
    )

    assert result == "ValueAI response"


def test_parse_sagemaker_response_parses_dictionary_format() -> None:
    """
    Dictionary responses containing generated_text should
    also be accepted.
    """

    raw_response = json.dumps(
        {
            "generated_text": TEST_GENERATED_TEXT
        }
    )

    result = parse_sagemaker_response(
        raw_response
    )

    assert result == TEST_GENERATED_TEXT


def test_parse_sagemaker_response_parses_generation_content_list() -> None:
    """
    Verify compatibility with:

        [
            {
                "generation": {
                    "content": "..."
                }
            }
        ]
    """

    raw_response = json.dumps(
        [
            {
                "generation": {
                    "content": TEST_GENERATED_TEXT
                }
            }
        ]
    )

    result = parse_sagemaker_response(
        raw_response
    )

    assert result == TEST_GENERATED_TEXT


def test_parse_sagemaker_response_parses_generation_content_dict() -> None:
    """
    Verify compatibility with:

        {
            "generation": {
                "content": "..."
            }
        }
    """

    raw_response = json.dumps(
        {
            "generation": {
                "content": TEST_GENERATED_TEXT
            }
        }
    )

    result = parse_sagemaker_response(
        raw_response
    )

    assert result == TEST_GENERATED_TEXT


def test_parse_sagemaker_response_parses_choices_text() -> None:
    """
    Verify compatibility with a choices/text response shape.
    """

    raw_response = json.dumps(
        {
            "choices": [
                {
                    "text": TEST_GENERATED_TEXT
                }
            ]
        }
    )

    result = parse_sagemaker_response(
        raw_response
    )

    assert result == TEST_GENERATED_TEXT


def test_parse_sagemaker_response_rejects_invalid_json() -> None:
    """
    Invalid JSON must produce SageMakerResponseError.
    """

    with pytest.raises(
        SageMakerResponseError,
        match="not valid JSON",
    ):
        parse_sagemaker_response(
            "this is not json"
        )


def test_parse_sagemaker_response_rejects_unrecognized_shape() -> None:
    """
    Valid JSON without generated text must be rejected.
    """

    raw_response = json.dumps(
        {
            "unexpected": "response"
        }
    )

    with pytest.raises(
        SageMakerResponseError,
        match="no generated text",
    ):
        parse_sagemaker_response(
            raw_response
        )


def test_parse_sagemaker_response_rejects_empty_generated_text() -> None:
    """
    Empty generated text is not a valid SageMaker response.
    """

    raw_response = json.dumps(
        [
            {
                "generated_text": ""
            }
        ]
    )

    with pytest.raises(
        SageMakerResponseError,
        match="no generated text",
    ):
        parse_sagemaker_response(
            raw_response
        )


def test_parse_sagemaker_response_rejects_empty_list() -> None:
    """
    An empty JSON list must be rejected.
    """

    with pytest.raises(
        SageMakerResponseError,
        match="no generated text",
    ):
        parse_sagemaker_response(
            "[]"
        )


# ============================================================
# EVIDENCE PROMPT TESTS
# ============================================================


def test_evidence_prompt_contains_user_query() -> None:
    """
    The final evidence-first prompt must contain the user's
    actual question.
    """

    prompt = _build_evidence_prompt(
        TEST_QUERY,
        TEST_EVIDENCE_STATE,
    )

    assert TEST_QUERY in prompt


def test_evidence_prompt_contains_evidence_source() -> None:
    """
    The prompt must identify where the evidence came from.
    """

    prompt = _build_evidence_prompt(
        TEST_QUERY,
        TEST_EVIDENCE_STATE,
    )

    assert (
        "verified analytical artifacts"
        in prompt
    )


def test_evidence_prompt_contains_evidence_json() -> None:
    """
    The analytical evidence must be embedded in the prompt.
    """

    prompt = _build_evidence_prompt(
        TEST_QUERY,
        TEST_EVIDENCE_STATE,
    )

    assert (
        "readmission_rate"
        in prompt
    )

    assert (
        "high_risk_cluster"
        in prompt
    )

    assert (
        "0.23"
        in prompt
    )

    assert (
        "1250"
        in prompt
    )


def test_evidence_prompt_contains_evidence_first_instructions() -> None:
    """
    The prompt must retain the evidence-first safeguards.
    """

    prompt = _build_evidence_prompt(
        TEST_QUERY,
        TEST_EVIDENCE_STATE,
    )

    assert (
        "Treat this evidence as authoritative."
        in prompt
    )

    assert (
        "Do not invent quantitative values."
        in prompt
    )

    assert (
        "Do not introduce numerical values"
        in prompt
    )

    assert (
        "If the evidence does not establish something"
        in prompt
    )


def test_evidence_prompt_contains_shap_safeguard() -> None:
    """
    The prompt must distinguish SHAP importance magnitude from
    direction and causation.
    """

    prompt = _build_evidence_prompt(
        TEST_QUERY,
        TEST_EVIDENCE_STATE,
    )

    assert (
        "mean absolute SHAP values"
        in prompt
    )

    assert (
        "not direction or causation"
        in prompt
    )


def test_evidence_prompt_contains_strategy_safeguard() -> None:
    """
    Strategic recommendations must be framed as hypotheses
    rather than guaranteed outcomes.
    """

    prompt = _build_evidence_prompt(
        TEST_QUERY,
        TEST_EVIDENCE_STATE,
    )

    assert (
        "hypotheses for evaluation"
        in prompt
    )

    assert (
        "Never claim that an intervention will reduce"
        in prompt
    )


# ============================================================
# RAW ENDPOINT VALIDATION TESTS
# ============================================================


def test_invoke_sagemaker_endpoint_rejects_empty_prompt() -> None:
    """
    Empty prompts must fail before AWS is contacted.
    """

    with pytest.raises(
        ValueError,
        match="prompt cannot be empty",
    ):
        invoke_sagemaker_endpoint("")


def test_invoke_sagemaker_endpoint_rejects_whitespace_prompt() -> None:
    """
    Whitespace-only prompts must fail before AWS is contacted.
    """

    with pytest.raises(
        ValueError,
        match="prompt cannot be empty",
    ):
        invoke_sagemaker_endpoint(
            "   "
        )


def test_invoke_sagemaker_endpoint_does_not_call_aws_for_empty_prompt() -> None:
    """
    Confirm that invalid input fails before creating the runtime
    client.
    """

    with patch(
        "src.ai_agent.sagemaker_agent._get_runtime_client"
    ) as mock_client:

        with pytest.raises(
            ValueError,
            match="prompt cannot be empty",
        ):
            invoke_sagemaker_endpoint(
                "   "
            )

    mock_client.assert_not_called()


# ============================================================
# RUNTIME CLIENT TESTS
# ============================================================


def test_runtime_client_uses_configured_region() -> None:
    """
    The SageMaker Runtime client must use get_aws_region().
    """

    fake_client = MagicMock()

    with patch(
        "src.ai_agent.sagemaker_agent.get_aws_region",
        return_value="us-east-1",
    ), patch(
        "src.ai_agent.sagemaker_agent.boto3.client",
        return_value=fake_client,
    ) as mock_boto_client:

        result = sagemaker_agent._get_runtime_client()

    assert result is fake_client

    mock_boto_client.assert_called_once_with(
        "sagemaker-runtime",
        region_name="us-east-1",
    )


def test_runtime_client_wraps_initialization_error() -> None:
    """
    Runtime-client initialization failures must become the
    application's configuration error.
    """

    with patch(
        "src.ai_agent.sagemaker_agent.boto3.client",
        side_effect=Exception(
            "Unable to initialize AWS client"
        ),
    ):

        with pytest.raises(
            SageMakerConfigurationError,
            match="Unable to initialize SageMaker Runtime client",
        ):
            sagemaker_agent._get_runtime_client()


# ============================================================
# ENDPOINT INVOCATION TESTS
# ============================================================


def test_invoke_sagemaker_endpoint_sends_expected_request() -> None:
    """
    Verify the actual invoke_endpoint contract without calling AWS.
    """

    runtime_client = MagicMock()

    runtime_client.invoke_endpoint.return_value = {
        "Body": make_streaming_body(
            json.dumps(
                [
                    {
                        "generated_text": TEST_GENERATED_TEXT
                    }
                ]
            )
        )
    }

    with patch(
        "src.ai_agent.sagemaker_agent._get_runtime_client",
        return_value=runtime_client,
    ), patch(
        "src.ai_agent.sagemaker_agent.get_sagemaker_endpoint_name",
        return_value="valueai-qwen25-7b",
    ):

        result = invoke_sagemaker_endpoint(
            TEST_PROMPT
        )

    assert result == TEST_GENERATED_TEXT

    runtime_client.invoke_endpoint.assert_called_once()

    call_kwargs = (
        runtime_client.invoke_endpoint.call_args.kwargs
    )

    assert (
        call_kwargs["EndpointName"]
        == "valueai-qwen25-7b"
    )

    assert (
        call_kwargs["ContentType"]
        == SAGEMAKER_CONTENT_TYPE
    )

    assert (
        call_kwargs["Accept"]
        == SAGEMAKER_ACCEPT
    )

    payload = json.loads(
        call_kwargs["Body"].decode(
            "utf-8"
        )
    )

    assert payload["inputs"] == TEST_PROMPT

    assert (
        payload["parameters"]["return_full_text"]
        is False
    )


def test_invoke_sagemaker_endpoint_strips_prompt_before_sending() -> None:
    """
    invoke_sagemaker_endpoint() should normalize the prompt
    using strip() before constructing the payload.
    """

    runtime_client = MagicMock()

    runtime_client.invoke_endpoint.return_value = {
        "Body": make_streaming_body(
            json.dumps(
                [
                    {
                        "generated_text": "OK"
                    }
                ]
            )
        )
    }

    with patch(
        "src.ai_agent.sagemaker_agent._get_runtime_client",
        return_value=runtime_client,
    ), patch(
        "src.ai_agent.sagemaker_agent.get_sagemaker_endpoint_name",
        return_value="valueai-qwen25-7b",
    ):

        result = invoke_sagemaker_endpoint(
            "   hello world   "
        )

    assert result == "OK"

    call_kwargs = (
        runtime_client.invoke_endpoint.call_args.kwargs
    )

    payload = json.loads(
        call_kwargs["Body"].decode(
            "utf-8"
        )
    )

    assert (
        payload["inputs"]
        == "hello world"
    )


def test_invoke_sagemaker_endpoint_translates_client_error() -> None:
    """
    boto3 ClientError must become SageMakerInvocationError.
    """

    runtime_client = MagicMock()

    runtime_client.invoke_endpoint.side_effect = (
        make_client_error(
            code="ModelError",
            message="The model failed",
        )
    )

    with patch(
        "src.ai_agent.sagemaker_agent._get_runtime_client",
        return_value=runtime_client,
    ), patch(
        "src.ai_agent.sagemaker_agent.get_sagemaker_endpoint_name",
        return_value="valueai-qwen25-7b",
    ):

        with pytest.raises(
            SageMakerInvocationError,
            match="ModelError",
        ) as exc_info:

            invoke_sagemaker_endpoint(
                TEST_PROMPT
            )

    assert (
        "The model failed"
        in str(exc_info.value)
    )


def test_invoke_sagemaker_endpoint_translates_botocore_error() -> None:
    """
    boto3/botocore failures must become SageMakerInvocationError.
    """

    runtime_client = MagicMock()

    runtime_client.invoke_endpoint.side_effect = (
        BotoCoreError()
    )

    with patch(
        "src.ai_agent.sagemaker_agent._get_runtime_client",
        return_value=runtime_client,
    ), patch(
        "src.ai_agent.sagemaker_agent.get_sagemaker_endpoint_name",
        return_value="valueai-qwen25-7b",
    ):

        with pytest.raises(
            SageMakerInvocationError,
            match="AWS SDK error",
        ):

            invoke_sagemaker_endpoint(
                TEST_PROMPT
            )


def test_invoke_sagemaker_endpoint_translates_unexpected_error() -> None:
    """
    Unexpected runtime-client failures must also be translated
    into SageMakerInvocationError.
    """

    runtime_client = MagicMock()

    runtime_client.invoke_endpoint.side_effect = (
        RuntimeError(
            "Unexpected test failure"
        )
    )

    with patch(
        "src.ai_agent.sagemaker_agent._get_runtime_client",
        return_value=runtime_client,
    ), patch(
        "src.ai_agent.sagemaker_agent.get_sagemaker_endpoint_name",
        return_value="valueai-qwen25-7b",
    ):

        with pytest.raises(
            SageMakerInvocationError,
            match="Unexpected SageMaker invocation error",
        ):

            invoke_sagemaker_endpoint(
                TEST_PROMPT
            )


def test_invoke_sagemaker_endpoint_rejects_missing_body() -> None:
    """
    A successful boto3 call without Body is still an invalid
    SageMaker response.
    """

    runtime_client = MagicMock()

    runtime_client.invoke_endpoint.return_value = {}

    with patch(
        "src.ai_agent.sagemaker_agent._get_runtime_client",
        return_value=runtime_client,
    ), patch(
        "src.ai_agent.sagemaker_agent.get_sagemaker_endpoint_name",
        return_value="valueai-qwen25-7b",
    ):

        with pytest.raises(
            SageMakerResponseError,
            match="did not contain a response body",
        ):

            invoke_sagemaker_endpoint(
                TEST_PROMPT
            )


def test_invoke_sagemaker_endpoint_handles_body_read_failure() -> None:
    """
    Failure while reading the StreamingBody must become
    SageMakerResponseError.
    """

    body = MagicMock()

    body.read.side_effect = (
        RuntimeError(
            "Body read failed"
        )
    )

    runtime_client = MagicMock()

    runtime_client.invoke_endpoint.return_value = {
        "Body": body
    }

    with patch(
        "src.ai_agent.sagemaker_agent._get_runtime_client",
        return_value=runtime_client,
    ), patch(
        "src.ai_agent.sagemaker_agent.get_sagemaker_endpoint_name",
        return_value="valueai-qwen25-7b",
    ):

        with pytest.raises(
            SageMakerResponseError,
            match="Unable to read SageMaker response body",
        ):

            invoke_sagemaker_endpoint(
                TEST_PROMPT
            )


def test_invoke_sagemaker_endpoint_handles_invalid_response_json() -> None:
    """
    Invalid response JSON must be rejected after the endpoint
    invocation succeeds.
    """

    runtime_client = MagicMock()

    runtime_client.invoke_endpoint.return_value = {
        "Body": make_streaming_body(
            "not valid json"
        )
    }

    with patch(
        "src.ai_agent.sagemaker_agent._get_runtime_client",
        return_value=runtime_client,
    ), patch(
        "src.ai_agent.sagemaker_agent.get_sagemaker_endpoint_name",
        return_value="valueai-qwen25-7b",
    ):

        with pytest.raises(
            SageMakerResponseError,
            match="not valid JSON",
        ):

            invoke_sagemaker_endpoint(
                TEST_PROMPT
            )


# ============================================================
# COMPLETE EVIDENCE-FIRST AGENT TESTS
# ============================================================


def test_invoke_sagemaker_agent_rejects_empty_query() -> None:
    """
    Empty user queries must be rejected before evidence retrieval
    or SageMaker invocation.
    """

    with patch(
        "src.ai_agent.sagemaker_agent.retrieve_evidence"
    ) as mock_retrieve, patch(
        "src.ai_agent.sagemaker_agent.invoke_sagemaker_endpoint"
    ) as mock_invoke:

        with pytest.raises(
            ValueError,
            match="User query cannot be empty",
        ):

            invoke_sagemaker_agent(
                ""
            )

    mock_retrieve.assert_not_called()
    mock_invoke.assert_not_called()


def test_invoke_sagemaker_agent_rejects_whitespace_query() -> None:
    """
    Whitespace-only queries must be rejected.
    """

    with patch(
        "src.ai_agent.sagemaker_agent.retrieve_evidence"
    ) as mock_retrieve, patch(
        "src.ai_agent.sagemaker_agent.invoke_sagemaker_endpoint"
    ) as mock_invoke:

        with pytest.raises(
            ValueError,
            match="User query cannot be empty",
        ):

            invoke_sagemaker_agent(
                "   "
            )

    mock_retrieve.assert_not_called()
    mock_invoke.assert_not_called()


def test_invoke_sagemaker_agent_normalizes_user_query() -> None:
    """
    Leading/trailing whitespace must be removed before evidence
    retrieval.
    """

    evidence_state = {
        "evidence": {
            "example": "verified"
        },
        "evidence_source": "test",
    }

    with patch(
        "src.ai_agent.sagemaker_agent.retrieve_evidence",
        return_value=evidence_state,
    ) as mock_retrieve, patch(
        "src.ai_agent.sagemaker_agent.invoke_sagemaker_endpoint",
        return_value="Final response",
    ) as mock_invoke:

        result = invoke_sagemaker_agent(
            "   Explain readmission risk.   "
        )

    assert result == "Final response"

    mock_retrieve.assert_called_once_with(
        {
            "user_query": (
                "Explain readmission risk."
            )
        }
    )

    mock_invoke.assert_called_once()


def test_invoke_sagemaker_agent_retrieves_evidence_before_invocation() -> None:
    """
    The architecture requires:

        user query
            ↓
        retrieve evidence
            ↓
        build evidence prompt
            ↓
        SageMaker

    This test verifies that evidence retrieval happens before
    SageMaker invocation.
    """

    call_order: list[str] = []

    evidence_state = {
        "evidence": {
            "readmission_rate": 0.23
        },
        "evidence_source": "verified analytical artifacts",
    }

    def fake_retrieve(
        state: dict,
    ) -> dict:

        call_order.append(
            "retrieve_evidence"
        )

        return evidence_state

    def fake_invoke(
        prompt: str,
    ) -> str:

        call_order.append(
            "invoke_sagemaker_endpoint"
        )

        assert (
            "readmission_rate"
            in prompt
        )

        assert (
            "0.23"
            in prompt
        )

        return "SageMaker answer"

    with patch(
        "src.ai_agent.sagemaker_agent.retrieve_evidence",
        side_effect=fake_retrieve,
    ), patch(
        "src.ai_agent.sagemaker_agent.invoke_sagemaker_endpoint",
        side_effect=fake_invoke,
    ):

        result = invoke_sagemaker_agent(
            TEST_QUERY
        )

    assert result == "SageMaker answer"

    assert call_order == [
        "retrieve_evidence",
        "invoke_sagemaker_endpoint",
    ]


def test_invoke_sagemaker_agent_passes_evidence_into_prompt() -> None:
    """
    The prompt sent to SageMaker must contain the retrieved
    analytical evidence.
    """

    evidence_state = {
        "evidence": {
            "high_risk_cluster_size": 1250,
            "readmission_rate": 0.41,
        },
        "evidence_source": (
            "verified analytical artifacts"
        ),
    }

    with patch(
        "src.ai_agent.sagemaker_agent.retrieve_evidence",
        return_value=evidence_state,
    ), patch(
        "src.ai_agent.sagemaker_agent.invoke_sagemaker_endpoint",
        return_value="Answer",
    ) as mock_invoke:

        result = invoke_sagemaker_agent(
            "Analyze the high-risk cluster."
        )

    assert result == "Answer"

    mock_invoke.assert_called_once()

    prompt = (
        mock_invoke.call_args.args[0]
    )

    assert (
        "high_risk_cluster_size"
        in prompt
    )

    assert (
        "1250"
        in prompt
    )

    assert (
        "0.41"
        in prompt
    )

    assert (
        "verified analytical artifacts"
        in prompt
    )


def test_invoke_sagemaker_agent_returns_sagemaker_response() -> None:
    """
    The final return value must be exactly the response returned
    by the SageMaker invocation layer.
    """

    evidence_state = {
        "evidence": {
            "example": "verified"
        },
        "evidence_source": "test",
    }

    expected_response = (
        "This is the generated SageMaker response."
    )

    with patch(
        "src.ai_agent.sagemaker_agent.retrieve_evidence",
        return_value=evidence_state,
    ), patch(
        "src.ai_agent.sagemaker_agent.invoke_sagemaker_endpoint",
        return_value=expected_response,
    ):

        result = invoke_sagemaker_agent(
            TEST_QUERY
        )

    assert result == expected_response


# ============================================================
# NO-FALLBACK TESTS
# ============================================================


def test_invoke_sagemaker_agent_does_not_fallback_when_sagemaker_fails() -> None:
    """
    SageMaker failure must propagate.

    There must be no hidden fallback to:
        - Ollama
        - ChatOllama
        - local Qwen
        - another provider
    """

    evidence_state = {
        "evidence": {
            "example": "verified"
        },
        "evidence_source": "test",
    }

    with patch(
        "src.ai_agent.sagemaker_agent.retrieve_evidence",
        return_value=evidence_state,
    ), patch(
        "src.ai_agent.sagemaker_agent.invoke_sagemaker_endpoint",
        side_effect=SageMakerInvocationError(
            "SageMaker unavailable"
        ),
    ) as mock_invoke:

        with pytest.raises(
            SageMakerInvocationError,
            match="SageMaker unavailable",
        ):

            invoke_sagemaker_agent(
                TEST_QUERY
            )

    mock_invoke.assert_called_once()


def test_invoke_sagemaker_agent_does_not_silently_replace_evidence() -> None:
    """
    The SageMaker agent must use the exact evidence returned by
    retrieve_evidence rather than silently substituting another
    source.
    """

    evidence_state = {
        "evidence": {
            "test_value": 987654
        },
        "evidence_source": "deterministic-test-source",
    }

    with patch(
        "src.ai_agent.sagemaker_agent.retrieve_evidence",
        return_value=evidence_state,
    ), patch(
        "src.ai_agent.sagemaker_agent.invoke_sagemaker_endpoint",
        return_value="Answer",
    ) as mock_invoke:

        invoke_sagemaker_agent(
            TEST_QUERY
        )

    prompt = (
        mock_invoke.call_args.args[0]
    )

    assert (
        "987654"
        in prompt
    )

    assert (
        "deterministic-test-source"
        in prompt
    )


# ============================================================
# ERROR PROPAGATION TESTS
# ============================================================


def test_invoke_sagemaker_agent_propagates_response_errors() -> None:
    """
    Response parsing errors must not be swallowed by the agent.
    """

    evidence_state = {
        "evidence": {
            "example": "verified"
        },
        "evidence_source": "test",
    }

    with patch(
        "src.ai_agent.sagemaker_agent.retrieve_evidence",
        return_value=evidence_state,
    ), patch(
        "src.ai_agent.sagemaker_agent.invoke_sagemaker_endpoint",
        side_effect=SageMakerResponseError(
            "Invalid SageMaker response"
        ),
    ):

        with pytest.raises(
            SageMakerResponseError,
            match="Invalid SageMaker response",
        ):

            invoke_sagemaker_agent(
                TEST_QUERY
            )


def test_invoke_sagemaker_agent_propagates_configuration_errors() -> None:
    """
    SageMaker configuration errors must propagate rather than
    triggering a local fallback.
    """

    evidence_state = {
        "evidence": {
            "example": "verified"
        },
        "evidence_source": "test",
    }

    with patch(
        "src.ai_agent.sagemaker_agent.retrieve_evidence",
        return_value=evidence_state,
    ), patch(
        "src.ai_agent.sagemaker_agent.invoke_sagemaker_endpoint",
        side_effect=SageMakerConfigurationError(
            "SageMaker configuration is invalid"
        ),
    ):

        with pytest.raises(
            SageMakerConfigurationError,
            match="SageMaker configuration is invalid",
        ):

            invoke_sagemaker_agent(
                TEST_QUERY
            )


# ============================================================
# PUBLIC API TEST
# ============================================================


def test_sagemaker_agent_public_api_exports_expected_functions() -> None:
    """
    Verify that the module's public API remains available.
    """

    expected_exports = {
        "SageMakerConfigurationError",
        "SageMakerInvocationError",
        "SageMakerResponseError",
        "build_sagemaker_payload",
        "parse_sagemaker_response",
        "invoke_sagemaker_endpoint",
        "invoke_sagemaker_agent",
    }

    assert set(
        sagemaker_agent.__all__
    ) == expected_exports

    for name in expected_exports:
        assert hasattr(
            sagemaker_agent,
            name,
        )


# ============================================================
# CONSTANT TESTS
# ============================================================


def test_sagemaker_content_type_is_json() -> None:
    """
    SageMaker endpoint input/output contract must use JSON.
    """

    assert (
        SAGEMAKER_CONTENT_TYPE
        == "application/json"
    )

    assert (
        SAGEMAKER_ACCEPT
        == "application/json"
    )