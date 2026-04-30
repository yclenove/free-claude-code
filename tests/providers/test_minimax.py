from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from providers.minimax import MINIMAX_DEFAULT_BASE, MiniMaxProvider


class MockMessage:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content


class MockRequest:
    def __init__(self, **kwargs):
        self.model = "MiniMax-M1"
        self.messages = [MockMessage("user", "Hello")]
        self.max_tokens = 100
        self.temperature = 0.5
        self.top_p = 0.9
        self.system = "System prompt"
        self.stop_sequences = ["STOP"]
        self.tools = []
        self.thinking = MagicMock()
        self.thinking.enabled = True
        for key, value in kwargs.items():
            setattr(self, key, value)


@pytest.fixture(autouse=True)
def mock_rate_limiter():
    with patch("providers.openai_compat.GlobalRateLimiter") as mock:
        instance = mock.get_scoped_instance.return_value
        instance.wait_if_blocked = AsyncMock(return_value=False)

        async def _passthrough(fn, *args, **kwargs):
            return await fn(*args, **kwargs)

        instance.execute_with_retry = AsyncMock(side_effect=_passthrough)
        yield instance


@pytest.mark.asyncio
async def test_init_uses_default_base(provider_config):
    config = provider_config.model_copy(update={"base_url": ""})
    with patch("providers.openai_compat.AsyncOpenAI") as mock_openai:
        provider = MiniMaxProvider(config)
    assert provider._base_url == MINIMAX_DEFAULT_BASE
    mock_openai.assert_called_once()


@pytest.mark.asyncio
async def test_build_request_body(provider_config):
    provider = MiniMaxProvider(provider_config)
    req = MockRequest()
    body = provider._build_request_body(req)

    assert body["model"] == "MiniMax-M1"
    assert body["temperature"] == 0.5
    assert len(body["messages"]) == 2  # system + user
    assert body["messages"][0]["role"] == "system"
