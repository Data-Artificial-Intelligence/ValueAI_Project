"""
ValueAI AI Provider Facade

This module provides provider selection without modifying the
existing LangGraph implementation.

Architecture:

    Application
        |
        v
    provider.invoke_agent()
        |
        +-----------------------------+
        |                             |
        v                             v
      local                       sagemaker
        |                             |
        v                             v
    agent_graph.py              SageMaker adapter
    (FROZEN)                    (added later)

The local provider deliberately delegates directly to the
existing, already-validated agent_graph.invoke_agent().

IMPORTANT:
    src/ai_agent/agent_graph.py is intentionally NOT modified
    by this module.
"""

from __future__ import annotations

from typing import Final

from src.ai_agent.agent_graph import (
    invoke_agent as invoke_local_agent,
)
from src.utils.config import get_ai_provider


# ============================================================
# Provider Constants
# ============================================================

LOCAL_PROVIDER: Final[str] = "local"
SAGEMAKER_PROVIDER: Final[str] = "sagemaker"

SUPPORTED_PROVIDERS: Final[frozenset[str]] = frozenset(
    {
        LOCAL_PROVIDER,
        SAGEMAKER_PROVIDER,
    }
)


# ============================================================
# Provider Resolution
# ============================================================


def resolve_provider(
    provider: str | None = None,
) -> str:
    """
    Resolve the AI inference provider.

    Precedence:

        1. Explicit provider argument
        2. VALUEAI_AI_PROVIDER from .env
        3. config.py default

    Args:
        provider:
            Optional explicit provider override.

            Examples:
                "local"
                "sagemaker"

    Returns:
        Normalized provider name.

    Raises:
        ValueError:
            If an unsupported provider is supplied.

    Examples:
        If .env contains:

            VALUEAI_AI_PROVIDER=local

        then:

            resolve_provider()
            -> "local"

            resolve_provider("local")
            -> "local"

            resolve_provider("sagemaker")
            -> "sagemaker"
    """

    # --------------------------------------------------------
    # Explicit runtime override
    # --------------------------------------------------------

    if provider is not None:
        resolved_provider = provider.strip().lower()

        if not resolved_provider:
            raise ValueError(
                "AI provider override cannot be empty."
            )

    # --------------------------------------------------------
    # Environment default
    # --------------------------------------------------------

    else:
        resolved_provider = get_ai_provider()

    # --------------------------------------------------------
    # Validate provider
    # --------------------------------------------------------

    if resolved_provider not in SUPPORTED_PROVIDERS:
        supported = ", ".join(
            sorted(SUPPORTED_PROVIDERS)
        )

        raise ValueError(
            f"Unsupported AI provider: "
            f"'{resolved_provider}'. "
            f"Supported providers: {supported}"
        )

    return resolved_provider


# ============================================================
# Provider Identification
# ============================================================


def get_active_provider(
    provider: str | None = None,
) -> str:
    """
    Return the provider that would be used for an invocation.

    This is a lightweight helper useful for:
        - Streamlit
        - tests
        - logging
        - debugging

    It does not perform inference.

    Args:
        provider:
            Optional explicit provider override.

    Returns:
        Resolved provider name.
    """
    return resolve_provider(provider)


# ============================================================
# Local Provider
# ============================================================


def _invoke_local(
    user_query: str,
):
    """
    Invoke the existing local ValueAI agent.

    IMPORTANT:
        This function delegates directly to the existing
        agent_graph.invoke_agent() implementation.

    No LangGraph logic is duplicated here.
    No prompts are modified here.
    No tools are modified here.
    No evidence logic is modified here.

    Args:
        user_query:
            User's natural-language question.

    Returns:
        Whatever the existing local agent returns.
    """
    return invoke_local_agent(user_query)


# ============================================================
# SageMaker Provider Placeholder
# ============================================================


def _invoke_sagemaker(
    user_query: str,
):
    """
    Invoke the real SageMaker evidence-first provider.

    The import is intentionally lazy so the SageMaker adapter
    is only loaded when SageMaker is actually selected.
    """

    from src.ai_agent.sagemaker_agent import (
        invoke_sagemaker_agent,
    )

    return invoke_sagemaker_agent(
        user_query
    )


# ============================================================
# Public Provider API
# ============================================================


def invoke_agent(
    user_query: str,
    provider: str | None = None,
):
    """
    Invoke the ValueAI AI agent using the selected provider.

    Provider precedence:

        explicit provider argument
                    |
                    v
             .env configuration
                    |
                    v
              provider router

    Supported providers:

        local
            Existing Ollama / Qwen LangGraph agent.

        sagemaker
            AWS SageMaker provider.
            Currently a deliberate placeholder until the
            SageMaker implementation phase.

    Args:
        user_query:
            User's natural-language question.

        provider:
            Optional runtime provider override.

            If omitted:
                VALUEAI_AI_PROVIDER is used.

            If supplied:
                it overrides VALUEAI_AI_PROVIDER.

    Returns:
        The response returned by the selected provider.

    Raises:
        ValueError:
            If the provider is unsupported or empty.

        NotImplementedError:
            If SageMaker is selected before its implementation
            is added.

    Examples:

        # Uses .env
        invoke_agent("What increases readmission risk?")

        # Explicit local override
        invoke_agent(
            "What increases readmission risk?",
            provider="local",
        )

        # Explicit SageMaker override
        invoke_agent(
            "What increases readmission risk?",
            provider="sagemaker",
        )
    """

    resolved_provider = resolve_provider(provider)

    # --------------------------------------------------------
    # Local provider
    # --------------------------------------------------------

    if resolved_provider == LOCAL_PROVIDER:
        return _invoke_local(user_query)

    # --------------------------------------------------------
    # SageMaker provider
    # --------------------------------------------------------

    if resolved_provider == SAGEMAKER_PROVIDER:
        return _invoke_sagemaker(user_query)

    # --------------------------------------------------------
    # Defensive guard
    # --------------------------------------------------------

    # resolve_provider() already validates this, but keeping
    # an explicit guard here protects the dispatch layer if
    # the implementation changes later.
    raise ValueError(
        f"Unsupported AI provider: '{resolved_provider}'. "
        f"Supported providers: "
        f"{', '.join(sorted(SUPPORTED_PROVIDERS))}"
    )


# ============================================================
# Public API
# ============================================================

__all__ = [
    "LOCAL_PROVIDER",
    "SAGEMAKER_PROVIDER",
    "SUPPORTED_PROVIDERS",
    "resolve_provider",
    "get_active_provider",
    "invoke_agent",
]