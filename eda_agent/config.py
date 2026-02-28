from __future__ import annotations

from dataclasses import dataclass, field
import json
import os
from typing import Any


@dataclass(frozen=True)
class OpenAIConfig:
    model: str = "gemini-3.1-pro-preview"
    api_key: str | None = None
    base_url: str | None = "https://generativelanguage.googleapis.com/v1beta/openai/"
    organization: str | None = None
    reasoning_effort: str | None = None
    request_timeout: float | None = 60.0
    stream: bool = False
    generate_kwargs: dict[str, Any] = field(default_factory=dict)


def load_openai_config(
    *,
    model: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
    organization: str | None = None,
    reasoning_effort: str | None = None,
    request_timeout: float | None = None,
    stream: bool | None = None,
    temperature: float | None = None,
    top_p: float | None = None,
    max_completion_tokens: int | None = None,
    extra_body: dict[str, Any] | str | None = None,
) -> OpenAIConfig:
    env_model = os.environ.get("OPENAI_MODEL")
    env_key = os.environ.get("OPENAI_API_KEY")
    env_base_url = os.environ.get("OPENAI_BASE_URL")

    # Support for Gemini API
    if not env_key:
        env_key = os.environ.get("GEMINI_API_KEY")
        if env_key:
            if not env_base_url:
                env_base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
            if not env_model:
                env_model = "gemini-3.1-pro-preview"
    env_org = os.environ.get("OPENAI_ORGANIZATION")
    env_timeout = os.environ.get("OPENAI_TIMEOUT")
    env_extra_body = os.environ.get("OPENAI_EXTRA_BODY")

    parsed_timeout: float | None = None
    if request_timeout is not None:
        parsed_timeout = float(request_timeout)
    elif env_timeout:
        try:
            parsed_timeout = float(env_timeout)
        except ValueError as exc:
            raise ValueError("OPENAI_TIMEOUT must be a number (seconds).") from exc

    generate_kwargs: dict[str, Any] = {}
    if temperature is not None:
        generate_kwargs["temperature"] = temperature
    if top_p is not None:
        generate_kwargs["top_p"] = top_p
    if max_completion_tokens is not None:
        generate_kwargs["max_completion_tokens"] = max_completion_tokens
    extra_body_value = extra_body if extra_body is not None else env_extra_body
    if extra_body_value is not None:
        if isinstance(extra_body_value, str):
            extra_body_value = extra_body_value.strip()
            if extra_body_value:
                try:
                    extra_body_value = json.loads(extra_body_value)
                except json.JSONDecodeError as exc:
                    raise ValueError("OPENAI_EXTRA_BODY must be valid JSON.") from exc
            else:
                extra_body_value = None
        if extra_body_value is not None and not isinstance(extra_body_value, dict):
            raise ValueError("OPENAI_EXTRA_BODY must be a JSON object.")
    if extra_body_value:
        generate_kwargs["extra_body"] = extra_body_value

    return OpenAIConfig(
        model=model or env_model or OpenAIConfig.model,
        api_key=api_key or env_key,
        base_url=base_url or env_base_url,
        organization=organization or env_org,
        reasoning_effort=reasoning_effort,
        request_timeout=parsed_timeout if parsed_timeout is not None else OpenAIConfig.request_timeout,
        stream=OpenAIConfig.stream if stream is None else stream,
        generate_kwargs=generate_kwargs,
    )
