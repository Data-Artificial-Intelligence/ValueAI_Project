"""
ValueAI AI Provider Facade Tests

Tests the provider facade without invoking real AI providers.

Coverage:
    - Supported provider definitions
    - Provider resolution
    - Explicit provider precedence
    - Environment/configuration provider selection
    - Whitespace and case normalization
    - Invalid provider handling
    - Local provider dispatch
    - SageMaker provider dispatch
    - No-fallback behavior
    - Query forwarding
    - Local agent_graph delegation
    - Public API availability

IMPORTANT:
    These tests intentionally mock provider dispatch and the
    underlying local agent where appropriate.

    They do NOT:
        - Call Ollama
        - Call Qwen
        - Call AWS
        - Call SageMaker
        - Perform network requests
        - Modify agent_graph.py
        - Modify application configuration
"""


from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch


# ============================================================
# Project Root / Import Path
# ============================================================

# Ensure the project root is available on sys.path when pytest
# is executed directly from the project directory.
#
# This prevents:
#
#     ModuleNotFoundError: No module named 'src'
#
# when running:
#
#     pytest -q tests/test_agent.py
#
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# Third-Party Imports
# ============================================================

import pytest


# ============================================================
# Application Imports
# ============================================================

from src.ai_agent.provider import (
    LOCAL_PROVIDER,
    SAGEMAKER_PROVIDER,
    SUPPORTED_PROVIDERS,
    get_active_provider,
    invoke_agent,
    resolve_provider,
)


# ============================================================
# Provider Constants
# ============================================================


def test_supported_providers_contains_local_and_sagemaker() -> None:
    """Both supported provider names must be registered."""

    assert LOCAL_PROVIDER == "local"
    assert SAGEMAKER_PROVIDER == "sagemaker"

    assert LOCAL_PROVIDER in SUPPORTED_PROVIDERS
    assert SAGEMAKER_PROVIDER in SUPPORTED_PROVIDERS


def test_supported_providers_contains_only_expected_values() -> None:
    """The facade currently supports exactly local and sagemaker."""

    assert SUPPORTED_PROVIDERS == frozenset(
        {
            "local",
            "sagemaker",
        }
    )


# ============================================================
# Provider Resolution
# ============================================================


def test_resolve_provider_without_override_uses_configuration() -> None:
    """
    Without an explicit provider, resolve_provider() must use
    get_ai_provider().
    """

    with patch(
        "src.ai_agent.provider.get_ai_provider",
        return_value="local",
    ) as mock_get_provider:
        result = resolve_provider()

    assert result == "local"

    mock_get_provider.assert_called_once_with()


def test_resolve_provider_explicit_local() -> None:
    """An explicit local provider must resolve to local."""

    assert resolve_provider("local") == "local"


def test_resolve_provider_explicit_sagemaker() -> None:
    """An explicit SageMaker provider must resolve to sagemaker."""

    assert resolve_provider("sagemaker") == "sagemaker"


def test_resolve_provider_is_case_insensitive() -> None:
    """Explicit provider names must be normalized to lowercase."""

    assert resolve_provider("LOCAL") == "local"
    assert resolve_provider("Local") == "local"
    assert resolve_provider("SAGEMAKER") == "sagemaker"
    assert resolve_provider("SageMaker") == "sagemaker"


def test_resolve_provider_strips_whitespace() -> None:
    """Leading and trailing whitespace must be ignored."""

    assert resolve_provider("  local  ") == "local"
    assert resolve_provider("  sagemaker  ") == "sagemaker"


def test_resolve_provider_rejects_empty_override() -> None:
    """An explicitly empty provider must raise ValueError."""

    with pytest.raises(
        ValueError,
        match="AI provider override cannot be empty",
    ):
        resolve_provider("")


def test_resolve_provider_rejects_whitespace_only_override() -> None:
    """A whitespace-only provider must raise ValueError."""

    with pytest.raises(
        ValueError,
        match="AI provider override cannot be empty",
    ):
        resolve_provider("   ")


def test_resolve_provider_rejects_invalid_explicit_provider() -> None:
    """Unsupported explicit providers must raise ValueError."""

    with pytest.raises(
        ValueError,
        match="Unsupported AI provider",
    ):
        resolve_provider("banana")


def test_resolve_provider_rejects_invalid_configured_provider() -> None:
    """Unsupported configured providers must raise ValueError."""

    with patch(
        "src.ai_agent.provider.get_ai_provider",
        return_value="banana",
    ):
        with pytest.raises(
            ValueError,
            match="Unsupported AI provider",
        ):
            resolve_provider()


def test_resolve_provider_explicit_override_has_precedence() -> None:
    """
    An explicit provider must override the configured provider.
    """

    with patch(
        "src.ai_agent.provider.get_ai_provider",
        return_value="local",
    ) as mock_get_provider:
        result = resolve_provider("sagemaker")

    assert result == "sagemaker"

    # Configuration must not be consulted when an explicit
    # provider is supplied.
    mock_get_provider.assert_not_called()


# ============================================================
# Active Provider
# ============================================================


def test_get_active_provider_uses_resolve_provider() -> None:
    """
    get_active_provider() must delegate to resolve_provider().

    Because provider.py calls:

        resolve_provider(provider)

    and provider defaults to None, the expected call is:

        resolve_provider(None)
    """

    with patch(
        "src.ai_agent.provider.resolve_provider",
        return_value="local",
    ) as mock_resolve:
        result = get_active_provider()

    assert result == "local"

    mock_resolve.assert_called_once_with(None)


def test_get_active_provider_accepts_explicit_override() -> None:
    """get_active_provider() must support explicit overrides."""

    with patch(
        "src.ai_agent.provider.resolve_provider",
        return_value="sagemaker",
    ) as mock_resolve:
        result = get_active_provider("sagemaker")

    assert result == "sagemaker"

    mock_resolve.assert_called_once_with("sagemaker")


# ============================================================
# Local Provider Dispatch
# ============================================================


def test_invoke_agent_dispatches_to_local_provider() -> None:
    """
    provider='local' must dispatch to _invoke_local().
    """

    expected_response = "local provider response"

    with patch(
        "src.ai_agent.provider._invoke_local",
        return_value=expected_response,
    ) as mock_local, patch(
        "src.ai_agent.provider._invoke_sagemaker",
    ) as mock_sagemaker:

        result = invoke_agent(
            "What increases readmission risk?",
            provider="local",
        )

    assert result == expected_response

    mock_local.assert_called_once_with(
        "What increases readmission risk?"
    )

    mock_sagemaker.assert_not_called()


def test_invoke_agent_explicit_local_overrides_configuration() -> None:
    """
    An explicit local provider must override a configured
    SageMaker provider.
    """

    expected_response = "local response"

    with patch(
        "src.ai_agent.provider.get_ai_provider",
        return_value="sagemaker",
    ), patch(
        "src.ai_agent.provider._invoke_local",
        return_value=expected_response,
    ) as mock_local, patch(
        "src.ai_agent.provider._invoke_sagemaker",
    ) as mock_sagemaker:

        result = invoke_agent(
            "Explain the high-risk cluster.",
            provider="local",
        )

    assert result == expected_response

    mock_local.assert_called_once_with(
        "Explain the high-risk cluster."
    )

    mock_sagemaker.assert_not_called()


# ============================================================
# Local Provider → agent_graph Delegation
# ============================================================


def test_invoke_local_delegates_to_existing_agent_graph() -> None:
    """
    The local provider must delegate directly to the existing
    agent_graph.invoke_agent implementation.

    The real local agent is mocked, so this test does not invoke
    Ollama or Qwen.
    """

    expected_response = "existing local graph response"

    user_query = (
        "Does AVG_DAYS_BETWEEN_INPATIENT_CLAIMS "
        "increase or decrease readmission risk?"
    )

    with patch(
        "src.ai_agent.provider.invoke_local_agent",
        return_value=expected_response,
    ) as mock_local_agent:

        # Import the private adapter only for this delegation test.
        from src.ai_agent.provider import _invoke_local

        result = _invoke_local(user_query)

    assert result == expected_response

    mock_local_agent.assert_called_once_with(user_query)


# ============================================================
# SageMaker Provider Dispatch
# ============================================================


def test_invoke_agent_dispatches_to_sagemaker_provider() -> None:
    """
    provider='sagemaker' must dispatch to _invoke_sagemaker().
    """

    expected_response = "sagemaker provider response"

    with patch(
        "src.ai_agent.provider._invoke_sagemaker",
        return_value=expected_response,
    ) as mock_sagemaker, patch(
        "src.ai_agent.provider._invoke_local",
    ) as mock_local:

        result = invoke_agent(
            "What increases readmission risk?",
            provider="sagemaker",
        )

    assert result == expected_response

    mock_sagemaker.assert_called_once_with(
        "What increases readmission risk?"
    )

    mock_local.assert_not_called()


def test_invoke_agent_configured_sagemaker_dispatches_to_sagemaker() -> None:
    """
    When configuration selects SageMaker, invocation must
    dispatch to SageMaker.
    """

    expected_response = "configured sagemaker response"

    with patch(
        "src.ai_agent.provider.get_ai_provider",
        return_value="sagemaker",
    ), patch(
        "src.ai_agent.provider._invoke_sagemaker",
        return_value=expected_response,
    ) as mock_sagemaker, patch(
        "src.ai_agent.provider._invoke_local",
    ) as mock_local:

        result = invoke_agent(
            "Analyze readmission risk."
        )

    assert result == expected_response

    mock_sagemaker.assert_called_once_with(
        "Analyze readmission risk."
    )

    mock_local.assert_not_called()


def test_invoke_agent_explicit_sagemaker_overrides_local_configuration() -> None:
    """
    An explicit SageMaker provider must override a configured
    local provider.
    """

    expected_response = "explicit sagemaker response"

    with patch(
        "src.ai_agent.provider.get_ai_provider",
        return_value="local",
    ), patch(
        "src.ai_agent.provider._invoke_sagemaker",
        return_value=expected_response,
    ) as mock_sagemaker, patch(
        "src.ai_agent.provider._invoke_local",
    ) as mock_local:

        result = invoke_agent(
            "Analyze average days between inpatient claims.",
            provider="sagemaker",
        )

    assert result == expected_response

    mock_sagemaker.assert_called_once_with(
        "Analyze average days between inpatient claims."
    )

    mock_local.assert_not_called()


# ============================================================
# No-Fallback Contract
# ============================================================


def test_sagemaker_failure_does_not_fallback_to_local() -> None:
    """
    CRITICAL CONTRACT:

    If SageMaker fails, the provider facade must NOT silently
    fall back to the local Ollama/Qwen provider.
    """

    sagemaker_error = RuntimeError(
        "SageMaker endpoint unavailable"
    )

    with patch(
        "src.ai_agent.provider._invoke_sagemaker",
        side_effect=sagemaker_error,
    ) as mock_sagemaker, patch(
        "src.ai_agent.provider._invoke_local",
    ) as mock_local:

        with pytest.raises(
            RuntimeError,
            match="SageMaker endpoint unavailable",
        ):
            invoke_agent(
                "What increases readmission risk?",
                provider="sagemaker",
            )

    mock_sagemaker.assert_called_once_with(
        "What increases readmission risk?"
    )

    mock_local.assert_not_called()


def test_sagemaker_not_implemented_does_not_fallback_to_local() -> None:
    """
    CRITICAL CONTRACT:

    Until SageMaker is implemented, its deliberate
    NotImplementedError must propagate directly.

    The facade must not fall back to Local/Ollama.
    """

    with patch(
        "src.ai_agent.provider._invoke_sagemaker",
        side_effect=NotImplementedError(
            "SageMaker provider not implemented"
        ),
    ) as mock_sagemaker, patch(
        "src.ai_agent.provider._invoke_local",
    ) as mock_local:

        with pytest.raises(
            NotImplementedError,
            match="SageMaker provider not implemented",
        ):
            invoke_agent(
                "Test SageMaker routing.",
                provider="sagemaker",
            )

    mock_sagemaker.assert_called_once_with(
        "Test SageMaker routing."
    )

    mock_local.assert_not_called()


def test_local_provider_failure_does_not_fallback_to_sagemaker() -> None:
    """
    A Local provider failure must not silently switch to
    SageMaker.
    """

    local_error = RuntimeError(
        "Local Ollama unavailable"
    )

    with patch(
        "src.ai_agent.provider._invoke_local",
        side_effect=local_error,
    ) as mock_local, patch(
        "src.ai_agent.provider._invoke_sagemaker",
    ) as mock_sagemaker:

        with pytest.raises(
            RuntimeError,
            match="Local Ollama unavailable",
        ):
            invoke_agent(
                "Test local routing.",
                provider="local",
            )

    mock_local.assert_called_once_with(
        "Test local routing."
    )

    mock_sagemaker.assert_not_called()


# ============================================================
# Query Forwarding
# ============================================================


def test_local_query_is_forwarded_unchanged() -> None:
    """The Local provider must receive the exact user query."""

    user_query = (
        "Does AVG_DAYS_BETWEEN_INPATIENT_CLAIMS increase "
        "or decrease readmission risk?"
    )

    with patch(
        "src.ai_agent.provider._invoke_local",
        return_value="response",
    ) as mock_local:

        invoke_agent(
            user_query,
            provider="local",
        )

    mock_local.assert_called_once_with(user_query)


def test_sagemaker_query_is_forwarded_unchanged() -> None:
    """The SageMaker provider must receive the exact user query."""

    user_query = (
        "Explain the relationship between TOTAL_ADMISSIONS "
        "and readmission risk."
    )

    with patch(
        "src.ai_agent.provider._invoke_sagemaker",
        return_value="response",
    ) as mock_sagemaker:

        invoke_agent(
            user_query,
            provider="sagemaker",
        )

    mock_sagemaker.assert_called_once_with(user_query)


# ============================================================
# Explicit Provider Normalization During Invocation
# ============================================================


def test_invoke_agent_accepts_uppercase_local() -> None:
    """invoke_agent() must inherit provider normalization."""

    expected_response = "local response"

    with patch(
        "src.ai_agent.provider._invoke_local",
        return_value=expected_response,
    ) as mock_local:

        result = invoke_agent(
            "Test uppercase provider.",
            provider="LOCAL",
        )

    assert result == expected_response

    mock_local.assert_called_once_with(
        "Test uppercase provider."
    )


def test_invoke_agent_accepts_uppercase_sagemaker() -> None:
    """invoke_agent() must inherit SageMaker normalization."""

    expected_response = "sagemaker response"

    with patch(
        "src.ai_agent.provider._invoke_sagemaker",
        return_value=expected_response,
    ) as mock_sagemaker:

        result = invoke_agent(
            "Test uppercase provider.",
            provider="SAGEMAKER",
        )

    assert result == expected_response

    mock_sagemaker.assert_called_once_with(
        "Test uppercase provider."
    )


def test_invoke_agent_accepts_whitespace_around_provider() -> None:
    """
    invoke_agent() must strip whitespace from explicit
    provider names.
    """

    expected_response = "local response"

    with patch(
        "src.ai_agent.provider._invoke_local",
        return_value=expected_response,
    ) as mock_local:

        result = invoke_agent(
            "Test whitespace provider.",
            provider="  LOCAL  ",
        )

    assert result == expected_response

    mock_local.assert_called_once_with(
        "Test whitespace provider."
    )


def test_invoke_agent_rejects_invalid_provider() -> None:
    """invoke_agent() must reject unsupported providers."""

    with pytest.raises(
        ValueError,
        match="Unsupported AI provider",
    ):
        invoke_agent(
            "Test invalid provider.",
            provider="invalid_provider",
        )


def test_invoke_agent_rejects_empty_provider() -> None:
    """invoke_agent() must reject an empty provider override."""

    with pytest.raises(
        ValueError,
        match="AI provider override cannot be empty",
    ):
        invoke_agent(
            "Test empty provider.",
            provider="",
        )


def test_invoke_agent_rejects_whitespace_only_provider() -> None:
    """
    invoke_agent() must reject a provider containing only
    whitespace.
    """

    with pytest.raises(
        ValueError,
        match="AI provider override cannot be empty",
    ):
        invoke_agent(
            "Test whitespace-only provider.",
            provider="   ",
        )


# ============================================================
# Configuration Precedence
# ============================================================


def test_environment_local_is_used_when_no_override_exists() -> None:
    """
    When the configured provider is local and no explicit
    provider is supplied, the local provider must be selected.
    """

    expected_response = "environment local response"

    with patch(
        "src.ai_agent.provider.get_ai_provider",
        return_value="local",
    ) as mock_get_provider, patch(
        "src.ai_agent.provider._invoke_local",
        return_value=expected_response,
    ) as mock_local, patch(
        "src.ai_agent.provider._invoke_sagemaker",
    ) as mock_sagemaker:

        result = invoke_agent(
            "Test environment local selection."
        )

    assert result == expected_response

    mock_get_provider.assert_called_once_with()

    mock_local.assert_called_once_with(
        "Test environment local selection."
    )

    mock_sagemaker.assert_not_called()


def test_environment_sagemaker_is_used_when_no_override_exists() -> None:
    """
    When the configured provider is SageMaker and no explicit
    provider is supplied, SageMaker must be selected.
    """

    expected_response = "environment sagemaker response"

    with patch(
        "src.ai_agent.provider.get_ai_provider",
        return_value="sagemaker",
    ) as mock_get_provider, patch(
        "src.ai_agent.provider._invoke_sagemaker",
        return_value=expected_response,
    ) as mock_sagemaker, patch(
        "src.ai_agent.provider._invoke_local",
    ) as mock_local:

        result = invoke_agent(
            "Test environment SageMaker selection."
        )

    assert result == expected_response

    mock_get_provider.assert_called_once_with()

    mock_sagemaker.assert_called_once_with(
        "Test environment SageMaker selection."
    )

    mock_local.assert_not_called()


# ============================================================
# Public API Smoke Tests
# ============================================================


def test_public_provider_api_is_callable() -> None:
    """
    Basic smoke test confirming the primary public facade
    functions are available and callable.
    """

    assert callable(resolve_provider)
    assert callable(get_active_provider)
    assert callable(invoke_agent)