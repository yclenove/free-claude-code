"""MiniMax provider implementation (official API key via OpenAI-compatible endpoint)."""

from __future__ import annotations

from typing import Any

from providers.base import ProviderConfig
from providers.defaults import MINIMAX_DEFAULT_BASE
from providers.openai_compat import OpenAIChatTransport

from .request import build_request_body


class MiniMaxProvider(OpenAIChatTransport):
    """MiniMax provider using OpenAI-compatible chat-completions transport."""

    def __init__(self, config: ProviderConfig):
        super().__init__(
            config,
            provider_name="MINIMAX",
            base_url=config.base_url or MINIMAX_DEFAULT_BASE,
            api_key=config.api_key,
        )

    def _build_request_body(
        self, request: Any, thinking_enabled: bool | None = None
    ) -> dict[str, Any]:
        return build_request_body(
            request,
            thinking_enabled=self._is_thinking_enabled(request, thinking_enabled),
        )
