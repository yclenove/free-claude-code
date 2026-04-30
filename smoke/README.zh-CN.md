# 产品端到端 Smoke 测试（中文）

`smoke/` 仅用于本地场景。它可以启动子进程、调用真实 provider、访问本地模型服务，并可选发送/删除机器人消息。  
可重复、无副作用的契约测试应放在 `tests/`，并确保 `uv run pytest` 始终通过。

## 分类

- `smoke/prereq/`：连通性前置检查（服务、路由、鉴权、CLI 脚本、provider ping、本地 `/models`、机器人权限）。
- `smoke/product/`：端到端产品场景，功能级 smoke 覆盖来源于这里。
- `smoke/features.py`：权威功能映射（feature -> subfeature -> scenario -> env -> expected behavior -> failure class）。

## 本地必跑命令

```powershell
uv run pytest smoke --collect-only -q
uv run pytest smoke -n 0 -s --tb=short
```

第二条命令在未设置 `FCC_LIVE_SMOKE=1` 时会全部跳过，但仍会把 skip 结果写入 `.smoke-results/`。

## 运行产品 Smoke

```powershell
$env:FCC_LIVE_SMOKE = "1"
uv run pytest smoke -n 0 -s --tb=short
```

Provider E2E 会按“已配置 provider”分别运行，不依赖 `MODEL`、`MODEL_OPUS`、`MODEL_SONNET`、`MODEL_HAIKU`。  
可用 `FCC_SMOKE_MODEL_<PROVIDER>` 覆盖模型，例如：`FCC_SMOKE_MODEL_DEEPSEEK=deepseek-v4-pro`。  
若未配置 provider smoke 模型，live smoke 默认以 `missing_env` 失败；除非显式设置 `FCC_ALLOW_NO_PROVIDER_SMOKE=1`。

## 目标集合

默认目标不发送真实机器人消息，也不会加载语音后端：

- `api`：messages、count_tokens、errors、`/stop`、optimizations
- `auth`：x-api-key、bearer、anthropic-auth-token、无效/缺失鉴权
- `cli`：`fcc-init`、服务入口、Claude CLI 自适应 thinking、会话清理
- `clients`：VS Code 与 JetBrains 协议载荷
- `config`：环境优先级、移除环境迁移、代理/超时
- `extensibility`：provider registry 与平台工厂
- `messaging`：伪造 Discord/Telegram 全流程、命令、树形会话、持久化、语音取消
- `providers`：多轮文本、thinking 历史、tools、断连、错误
- `tools`：强制 tool_use 与 tool_result 延续
- `rate_limit`：断连清理与后续请求
- `lmstudio` / `llamacpp` / `ollama`：本地模型路由与代理消息链路

有副作用目标需显式开启：

- `telegram`：getMe/send/edit/delete/可选手动入站
- `discord`：频道访问/send/edit/delete/可选手动入站
- `voice`：通过本地 Whisper 或 NVIDIA NIM 做语音转写

## 示例

```powershell
$env:FCC_LIVE_SMOKE = "1"
$env:FCC_SMOKE_PROVIDER_MATRIX = "open_router,nvidia_nim,deepseek,lmstudio,llamacpp,ollama"
uv run pytest smoke/product -n 0 -s --tb=short
```

```powershell
$env:FCC_LIVE_SMOKE = "1"
$env:FCC_SMOKE_TARGETS = "ollama"
$env:OLLAMA_BASE_URL = "http://localhost:11434"
uv run pytest smoke/prereq smoke/product -n 0 -s --tb=short
```

## 环境变量

- `FCC_ENV_FILE`：显式 dotenv 路径。
- `FCC_LIVE_SMOKE=1`：开启 live smoke。
- `FCC_ALLOW_NO_PROVIDER_SMOKE=1`：允许无 provider 的 live smoke（用于测试框架调试）。
- `FCC_SMOKE_TARGETS`：逗号分隔目标，或 `all`。
- `FCC_SMOKE_PROVIDER_MATRIX`：逗号分隔 provider 前缀。
- `FCC_SMOKE_MODEL_*`：provider 级别 smoke 模型覆盖。
- `FCC_SMOKE_TIMEOUT_S`：请求/子进程超时，默认 `45`。
- `FCC_SMOKE_CLAUDE_BIN`：Claude CLI 可执行名，默认 `claude`。
- `FCC_SMOKE_TELEGRAM_CHAT_ID` / `FCC_SMOKE_DISCORD_CHANNEL_ID`：消息收发目标。
- `FCC_SMOKE_INTERACTIVE=1`：开启 Telegram/Discord 手动入站检查。
- `FCC_SMOKE_RUN_VOICE=1`：允许加载语音转写后端。

## Windows 与嵌套 `uv run`

从仓库根目录按统一方式运行：`uv run pytest smoke`。  
子进程会复用测试进程的同一 Python 解释器，而不是嵌套 `uv run`，避免 Windows 锁文件替换问题。

## 失败分类

smoke 产物写入 `.smoke-results/`，并会对名称含 `KEY`、`TOKEN`、`SECRET`、`WEBHOOK`、`AUTH` 的环境值做脱敏。

- `missing_env`：缺少凭证、二进制、provider 配置、本地服务或 opt-in 开关。
- `upstream_unavailable`：真实 provider / bot API / 本地模型服务不可达。
- `product_failure`：应用接受场景但返回错误形状、崩溃、状态泄漏或违反产品契约。
- `harness_bug`：smoke 测试或驱动本身假设错误。

`product_failure` 与 `harness_bug` 视为失败。  
`missing_env` 与 `upstream_unavailable` 通常视为跳过；但若用户在 `FCC_SMOKE_PROVIDER_MATRIX` 显式选中某 provider，则“选中但缺失”应失败。
