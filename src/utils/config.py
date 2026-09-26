"""
ValueAI Application Configuration

Centralized configuration management for the ValueAI project.

Responsibilities:
    - Load environment variables from .env
    - Validate supported configuration values
    - Expose provider configuration
    - Provide safe defaults for development

This module intentionally does NOT:
    - Initialize Ollama
    - Initialize Qwen
    - Initialize SageMaker
    - Modify the LangGraph agent
    - Perform model inference

Provider-specific inference logic belongs in:
    src/ai_agent/provider.py
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Final

from dotenv import load_dotenv


# ============================================================
# Project Paths
# ============================================================

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parents[2]
ENV_FILE: Final[Path] = PROJECT_ROOT / ".env"


# ============================================================
# Environment Loading
# ============================================================

# Load .env if it exists.
#
# override=False is intentional:
# an explicitly supplied system environment variable takes
# precedence over the value stored in .env.
load_dotenv(ENV_FILE, override=False)


# ============================================================
# Supported Values
# ============================================================

SUPPORTED_AI_PROVIDERS: Final[frozenset[str]] = frozenset(
    {
        "local",
        "sagemaker",
    }
)


# ============================================================
# Generic Environment Helpers
# ============================================================


def _get_env(
    name: str,
    default: str | None = None,
) -> str | None:
    """
    Read an environment variable and normalize whitespace.

    Args:
        name:
            Environment variable name.

        default:
            Value returned when the variable is not defined.

    Returns:
        The stripped environment variable value, or default.
    """
    value = os.getenv(name, default)

    if value is None:
        return None

    return value.strip()


def _get_required_env(name: str) -> str:
    """
    Read a required environment variable.

    Args:
        name:
            Environment variable name.

    Returns:
        Non-empty environment variable value.

    Raises:
        ValueError:
            If the variable is missing or empty.
    """
    value = _get_env(name)

    if not value:
        raise ValueError(
            f"Required environment variable '{name}' is not set."
        )

    return value


# ============================================================
# AI Provider Configuration
# ============================================================


def get_ai_provider() -> str:
    """
    Return the configured default AI inference provider.

    Supported providers:
        - local
        - sagemaker

    The value is normalized to lowercase.

    Returns:
        The configured provider name.

    Raises:
        ValueError:
            If the configured provider is unsupported.

    Examples:
        >>> get_ai_provider()
        'local'
    """
    provider = _get_env(
        "VALUEAI_AI_PROVIDER",
        default="local",
    )

    if provider is None:
        provider = "local"

    provider = provider.lower()

    if provider not in SUPPORTED_AI_PROVIDERS:
        supported = ", ".join(sorted(SUPPORTED_AI_PROVIDERS))

        raise ValueError(
            f"Unsupported AI provider: '{provider}'. "
            f"Supported providers: {supported}"
        )

    return provider


# ============================================================
# Local LLM Configuration
# ============================================================


def get_local_llm_provider() -> str:
    """
    Return the configured local LLM provider.

    Defaults to:
        ollama
    """
    return _get_env(
        "VALUEAI_LOCAL_LLM_PROVIDER",
        default="ollama",
    ) or "ollama"


def get_local_llm_model() -> str:
    """
    Return the configured local LLM model.

    Defaults to:
        qwen2.5:7b
    """
    return _get_env(
        "VALUEAI_LOCAL_LLM_MODEL",
        default="qwen2.5:7b",
    ) or "qwen2.5:7b"


def get_ollama_base_url() -> str:
    """
    Return the Ollama server base URL.

    Defaults to:
        http://localhost:11434
    """
    return _get_env(
        "VALUEAI_OLLAMA_BASE_URL",
        default="http://localhost:11434",
    ) or "http://localhost:11434"


# ============================================================
# AWS / SageMaker Configuration
# ============================================================


def get_aws_region() -> str:
    """
    Return the AWS region used by ValueAI.

    Defaults to:
        us-east-1

    This function only reads configuration.
    It does not create an AWS client.
    """
    return _get_env(
        "AWS_REGION",
        default="us-east-1",
    ) or "us-east-1"


def get_sagemaker_endpoint_name() -> str:
    """
    Return the configured SageMaker endpoint name.

    Raises:
        ValueError:
            If no endpoint name has been configured.

    This is intentionally only validated when SageMaker
    configuration is actually requested.
    """
    return _get_required_env(
        "VALUEAI_SAGEMAKER_ENDPOINT_NAME"
    )


def get_sagemaker_model_id() -> str:
    """
    Return the SageMaker JumpStart model ID expected by ValueAI.

    This is metadata/configuration for the deployed endpoint.
    The runtime invocation itself only requires the endpoint name.
    """
    return (
        _get_env(
            "VALUEAI_SAGEMAKER_MODEL_ID",
            default="huggingface-llm-qwen2-5-7b-instruct",
        )
        or "huggingface-llm-qwen2-5-7b-instruct"
    )


def get_sagemaker_max_new_tokens() -> int:
    """
    Maximum number of tokens generated by the SageMaker endpoint.
    """
    value = _get_env(
        "VALUEAI_SAGEMAKER_MAX_NEW_TOKENS",
        default="512",
    )

    try:
        parsed = int(value or "512")
    except ValueError as exc:
        raise ValueError(
            "VALUEAI_SAGEMAKER_MAX_NEW_TOKENS must be an integer."
        ) from exc

    if parsed <= 0:
        raise ValueError(
            "VALUEAI_SAGEMAKER_MAX_NEW_TOKENS must be greater than zero."
        )

    return parsed


def get_sagemaker_temperature() -> float:
    """
    Temperature used by the SageMaker text-generation endpoint.
    """
    value = _get_env(
        "VALUEAI_SAGEMAKER_TEMPERATURE",
        default="0.0",
    )

    try:
        parsed = float(value or "0.0")
    except ValueError as exc:
        raise ValueError(
            "VALUEAI_SAGEMAKER_TEMPERATURE must be a number."
        ) from exc

    if parsed < 0:
        raise ValueError(
            "VALUEAI_SAGEMAKER_TEMPERATURE cannot be negative."
        )

    return parsed


def get_sagemaker_top_p() -> float:
    """
    Top-p value used by the SageMaker text-generation endpoint.
    """
    value = _get_env(
        "VALUEAI_SAGEMAKER_TOP_P",
        default="1.0",
    )

    try:
        parsed = float(value or "1.0")
    except ValueError as exc:
        raise ValueError(
            "VALUEAI_SAGEMAKER_TOP_P must be a number."
        ) from exc

    if parsed <= 0 or parsed > 1:
        raise ValueError(
            "VALUEAI_SAGEMAKER_TOP_P must be greater than 0 and <= 1."
        )

    return parsed

# ============================================================
# Application Configuration
# ============================================================


def get_environment() -> str:
    """
    Return the current ValueAI environment.

    Defaults to:
        development
    """
    return _get_env(
        "VALUEAI_ENVIRONMENT",
        default="development",
    ) or "development"


def get_log_level() -> str:
    """
    Return the configured application log level.

    Defaults to:
        INFO
    """
    return (
        _get_env(
            "VALUEAI_LOG_LEVEL",
            default="INFO",
        )
        or "INFO"
    ).upper()


# ============================================================
# Configuration Summary
# ============================================================


def get_config_summary() -> dict[str, str]:
    return {
        "environment": get_environment(),
        "ai_provider": get_ai_provider(),
        "local_llm_provider": get_local_llm_provider(),
        "local_llm_model": get_local_llm_model(),
        "ollama_base_url": get_ollama_base_url(),
        "aws_region": get_aws_region(),
        "sagemaker_model_id": get_sagemaker_model_id(),
        "sagemaker_endpoint_name": (
            get_sagemaker_endpoint_name()
            if os.getenv("VALUEAI_SAGEMAKER_ENDPOINT_NAME")
            else "<not configured>"
        ),
        "sagemaker_max_new_tokens": str(
            get_sagemaker_max_new_tokens()
        ),
        "sagemaker_temperature": str(
            get_sagemaker_temperature()
        ),
        "sagemaker_top_p": str(
            get_sagemaker_top_p()
        ),
        "log_level": get_log_level(),
    }


# ============================================================
# Module-Level Validation
# ============================================================

# Validate the provider as soon as the configuration module
# is imported.
#
# This means an invalid value such as:
#
#     VALUEAI_AI_PROVIDER=banana
#
# fails immediately with a clear configuration error.
#
# We deliberately do NOT validate the SageMaker endpoint here,
# because local inference must remain usable even when
# SageMaker has not yet been configured.
get_ai_provider()