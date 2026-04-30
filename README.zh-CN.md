# 🤖 Free Claude Code（中文文档）

通过你自己的 Anthropic 兼容代理，使用 Claude Code CLI、VS Code、JetBrains ACP 或聊天机器人。

[English](README.md) · [中文](README.zh-CN.md)

## 项目简介

Free Claude Code 会把 Claude Code 发出的 Anthropic Messages API 请求，路由到 NVIDIA NIM、OpenRouter、DeepSeek、MiniMax、LM Studio、llama.cpp 或 Ollama。  
它保持 Claude Code 客户端协议不变，同时允许你选择免费、付费或本地模型。

## 你将获得

- Claude Code Anthropic API 请求的即插即用代理。
- 七种后端提供商：NVIDIA NIM、OpenRouter、DeepSeek、MiniMax、LM Studio、llama.cpp、Ollama。
- 按模型分层路由：Opus、Sonnet、Haiku、Fallback 可分别走不同提供商。
- 支持流式输出、工具调用、thinking/reasoning 块以及本地请求优化。
- 可选 Discord/Telegram 机器人封装，支持远程编码会话。
- 可选语音转写（本地 Whisper 或 NVIDIA NIM）。

## 快速开始

### 1) 安装依赖

先安装 [Claude Code](https://github.com/anthropics/claude-code)，再安装 `uv` 与 Python 3.14。

macOS/Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv self update
uv python install 3.14
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv self update
uv python install 3.14
```

### 2) 克隆并配置

```bash
git clone https://github.com/Alishahryar1/free-claude-code.git
cd free-claude-code
cp .env.example .env
```

PowerShell:

```powershell
Copy-Item .env.example .env
```

编辑 `.env` 并选择一个 provider。默认 NVIDIA NIM 示例：

```dotenv
NVIDIA_NIM_API_KEY="nvapi-your-key"
MODEL="nvidia_nim/z-ai/glm4.7"
ANTHROPIC_AUTH_TOKEN="freecc"
```

`ANTHROPIC_AUTH_TOKEN` 可使用任意本地密钥；Claude Code 会把同样值回传给代理。仅在本地私有测试时才建议留空。

### 3) 启动代理

```bash
uv run uvicorn server:app --host 0.0.0.0 --port 8082
```

也可用安装包入口：

```bash
uv tool install git+https://github.com/Alishahryar1/free-claude-code.git
fcc-init
free-claude-code
```

`fcc-init` 会从模板生成 `~/.config/free-claude-code/.env`。

### 4) 启动 Claude Code

将 `ANTHROPIC_BASE_URL` 指向代理根地址（不要追加 `/v1`）。

PowerShell:

```powershell
$env:ANTHROPIC_AUTH_TOKEN="freecc"; $env:ANTHROPIC_BASE_URL="http://localhost:8082"; claude
```

Bash:

```bash
ANTHROPIC_AUTH_TOKEN="freecc" ANTHROPIC_BASE_URL="http://localhost:8082" claude
```

## 选择 Provider

模型格式：

```text
provider_id/model/name
```

`MODEL` 是兜底模型；`MODEL_OPUS`、`MODEL_SONNET`、`MODEL_HAIKU` 分别覆盖对应层级请求。

| Provider | 前缀 | 传输方式 | 密钥 | 默认地址 |
| --- | --- | --- | --- | --- |
| NVIDIA NIM | `nvidia_nim/...` | OpenAI chat 转 Anthropic | `NVIDIA_NIM_API_KEY` | `https://integrate.api.nvidia.com/v1` |
| OpenRouter | `open_router/...` | Anthropic Messages | `OPENROUTER_API_KEY` | `https://openrouter.ai/api/v1` |
| DeepSeek | `deepseek/...` | Anthropic Messages | `DEEPSEEK_API_KEY` | `https://api.deepseek.com/anthropic` |
| MiniMax | `minimax/...` | OpenAI 兼容 chat | `MINIMAX_API_KEY` | `https://api.minimax.chat/v1` |
| LM Studio | `lmstudio/...` | Anthropic Messages | 无 | `http://localhost:1234/v1` |
| llama.cpp | `llamacpp/...` | Anthropic Messages | 无 | `http://localhost:8080/v1` |
| Ollama | `ollama/...` | Anthropic Messages | 无 | `http://localhost:11434` |

### NVIDIA NIM

- 申请 API Key: [build.nvidia.com/settings/api-keys](https://build.nvidia.com/settings/api-keys)
- 示例：

```dotenv
NVIDIA_NIM_API_KEY="nvapi-your-key"
MODEL="nvidia_nim/z-ai/glm4.7"
```

### OpenRouter

- 申请 API Key: [openrouter.ai/keys](https://openrouter.ai/keys)
- 示例：

```dotenv
OPENROUTER_API_KEY="sk-or-your-key"
MODEL="open_router/stepfun/step-3.5-flash:free"
```

### DeepSeek

- 申请 API Key: [platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)
- 示例：

```dotenv
DEEPSEEK_API_KEY="your-deepseek-key"
MODEL="deepseek/deepseek-chat"
```

### MiniMax

- 在 MiniMax 开放平台申请 API Key
- 示例：

```dotenv
MINIMAX_API_KEY="your-minimax-key"
MINIMAX_BASE_URL="https://api.minimax.chat/v1"
MODEL="minimax/MiniMax-M1"
```

### LM Studio

启动本地服务并加载模型后配置：

```dotenv
LM_STUDIO_BASE_URL="http://localhost:1234/v1"
MODEL="lmstudio/your-loaded-model"
```

### llama.cpp

需使用支持 Anthropic `/v1/messages` 的 `llama-server`：

```dotenv
LLAMACPP_BASE_URL="http://localhost:8080/v1"
MODEL="llamacpp/local-model"
```

若 Claude Code 请求返回 HTTP 400，通常要增大 `--ctx-size` 并确认模型能力。

### Ollama

```bash
ollama pull llama3.1
ollama serve
```

```dotenv
OLLAMA_BASE_URL="http://localhost:11434"
MODEL="ollama/llama3.1"
```

## 连接 Claude Code 客户端

### Claude Code CLI

```bash
ANTHROPIC_AUTH_TOKEN="freecc" ANTHROPIC_BASE_URL="http://localhost:8082" claude
```

### VS Code 扩展

在设置中找到 `claude-code.environmentVariables`，添加：

```json
"claudeCode.environmentVariables": [
  { "name": "ANTHROPIC_BASE_URL", "value": "http://localhost:8082" },
  { "name": "ANTHROPIC_AUTH_TOKEN", "value": "freecc" }
]
```

### JetBrains ACP

- Windows: `C:\Users\%USERNAME%\AppData\Roaming\JetBrains\acp-agents\installed.json`
- Linux/macOS: `~/.jetbrains/acp.json`

为 `acp.registry.claude-acp` 设置：

```json
"env": {
  "ANTHROPIC_BASE_URL": "http://localhost:8082",
  "ANTHROPIC_AUTH_TOKEN": "freecc"
}
```

## 可选集成

### Discord / Telegram

支持远程会话、流式进度、分支回复、停止与清理任务。

Discord 最小配置：

```dotenv
MESSAGING_PLATFORM="discord"
DISCORD_BOT_TOKEN="your-discord-bot-token"
ALLOWED_DISCORD_CHANNELS="123456789"
CLAUDE_WORKSPACE="./agent_workspace"
ALLOWED_DIR="C:/Users/yourname/projects"
```

Telegram 最小配置：

```dotenv
MESSAGING_PLATFORM="telegram"
TELEGRAM_BOT_TOKEN="123456789:ABC..."
ALLOWED_TELEGRAM_USER_ID="your-user-id"
CLAUDE_WORKSPACE="./agent_workspace"
ALLOWED_DIR="C:/Users/yourname/projects"
```

常用命令：

- `/stop` 停止任务（回复消息可只停该分支）
- `/clear` 清理会话（可按分支）
- `/stats` 查看会话状态

### 语音笔记

```bash
uv sync --extra voice_local
uv sync --extra voice
uv sync --extra voice --extra voice_local
```

```dotenv
VOICE_NOTE_ENABLED=true
WHISPER_DEVICE="cpu"          # cpu | cuda | nvidia_nim
WHISPER_MODEL="base"
HF_TOKEN=""
```

## 配置参考

以 [`.env.example`](.env.example) 为准。

### 模型路由

```dotenv
MODEL="nvidia_nim/z-ai/glm4.7"
MODEL_OPUS=
MODEL_SONNET=
MODEL_HAIKU=
ENABLE_MODEL_THINKING=true
ENABLE_OPUS_THINKING=
ENABLE_SONNET_THINKING=
ENABLE_HAIKU_THINKING=
```

### Provider 密钥与地址

```dotenv
NVIDIA_NIM_API_KEY=""
OPENROUTER_API_KEY=""
DEEPSEEK_API_KEY=""
MINIMAX_API_KEY=""
MINIMAX_BASE_URL="https://api.minimax.chat/v1"
LM_STUDIO_BASE_URL="http://localhost:1234/v1"
LLAMACPP_BASE_URL="http://localhost:8080/v1"
OLLAMA_BASE_URL="http://localhost:11434"
```

### 限流与超时

```dotenv
PROVIDER_RATE_LIMIT=1
PROVIDER_RATE_WINDOW=3
PROVIDER_MAX_CONCURRENCY=5
HTTP_READ_TIMEOUT=120
HTTP_WRITE_TIMEOUT=10
HTTP_CONNECT_TIMEOUT=10
```

### 安全与诊断

```dotenv
ANTHROPIC_AUTH_TOKEN=
LOG_RAW_API_PAYLOADS=false
LOG_RAW_SSE_EVENTS=false
LOG_API_ERROR_TRACEBACKS=false
LOG_RAW_MESSAGING_CONTENT=false
LOG_RAW_CLI_DIAGNOSTICS=false
LOG_MESSAGING_ERROR_DETAILS=false
```

## 故障排查

- `undefined ... input_tokens` / `$.speed` / malformed response：先更新到最新版本，再检查 `ANTHROPIC_BASE_URL` 是否为 `http://localhost:8082`（非 `/v1`）。
- llama.cpp / LM Studio 返回 400：确认支持 `POST /v1/messages`，并确保上下文窗口与工具能力足够。
- 流式中断：通常是上游断连，降低并发或提高超时后重试。
- VS Code 仍显示登录页：确认环境变量生效后重载扩展，首次可能仍触发一次浏览器登录。

## 工作原理

```text
Claude Code CLI / IDE
        |
        | Anthropic Messages API
        v
Free Claude Code proxy (:8082)
        |
        | provider-specific adapter
        v
NIM / OpenRouter / DeepSeek / LM Studio / llama.cpp / Ollama
```

关键点：

- FastAPI 暴露 `/v1/messages`、`/v1/messages/count_tokens`、`/v1/models` 等兼容接口。
- 路由将 Claude 请求映射到 `MODEL_OPUS` / `MODEL_SONNET` / `MODEL_HAIKU` / `MODEL`。
- 统一规整 thinking、tool call、token usage 和 provider error，保持 Claude Code 端协议稳定。

## 开发

### 项目结构

```text
free-claude-code/
├── server.py
├── api/
├── core/
├── providers/
├── messaging/
├── cli/
├── config/
└── tests/
```

### 开发命令

```bash
uv run ruff format
uv run ruff check
uv run ty check
uv run pytest
```

请按此顺序执行，CI 同步校验。

## 贡献

- 在 [Issues](https://github.com/Alishahryar1/free-claude-code/issues) 提交问题与需求。
- 变更尽量小而聚焦，并补充测试。
- 提交 PR 前运行完整检查链路。

## 许可证

MIT License，见 [LICENSE](LICENSE)。
