# 架构规划（中文）

本文档是 `AGENTS.md` 引用的基础架构说明，记录仓库的依赖方向与迁移目标，确保随着 provider、客户端和 smoke 测试扩展时项目仍保持模块化。

## 当前产品形态

`free-claude-code` 是 Anthropic 兼容代理，并支持可选消息机器人能力：

- `api/`：HTTP 路由、请求编排、模型路由、鉴权、服务生命周期。
- `providers/`：上游模型适配、请求转换、流转换、限流、错误映射。
- `messaging/`：Discord/Telegram 适配、命令处理、树形线程、会话持久化、转录渲染、语音输入。
- `cli/`：包入口和 Claude CLI 子进程会话管理。
- `config/`：环境变量设置与日志配置。
- `smoke/`：可选产品 smoke 场景与契约测试使用的覆盖清单。

## 目标依赖方向

仓库应保持如下依赖顺序（原文示意图见 `PLAN.md`）：

- `config` 提供配置给 `api` / `providers` / `messaging`
- `core.anthropic` 作为中立协议层，被 `api` / `providers` / `messaging` 复用
- `providers` 被 `api` 使用
- `api` 组合 `cli` 与 `messaging`
- `cli` 可与 `messaging` 协同

运行时说明：`api.runtime` 会导入 `cli` 和 `messaging` 完成可选消息栈装配；`messaging` 不反向导入 `cli`（CLI/会话能力由 `api.runtime` 注入）。

实践规则比图更重要：共享协议逻辑必须放到中立 core 模块，不要放在具体 provider 包下。Provider 适配器可以依赖中立协议层，但 API 和 messaging 不应导入 provider 内部实现。

## 契约边界要点

- `api/` 仅可从 `providers` 导入：`providers.base`、`providers.exceptions`、`providers.registry`。
- `core/` 不应依赖 `api`、`messaging`、`cli`、`providers`、`config`、`smoke`。
- `messaging/` 不导入 `api`、`cli`、`smoke`；可通过 `providers.nvidia_nim.voice` 使用 NVIDIA/Riva 离线 ASR。
- 流契约工具位于 `core/anthropic/stream_contracts.py`。
- NIM 配置统一使用 `config.nim.NimSettings`，避免重复 schema。
- provider 默认地址统一放在 `providers/defaults.py`。
- 生产 HTTP handler 必须用 `resolve_provider` + `request.app`（应用级 `ProviderRegistry`），而非进程缓存 helper。
- `api.__all__` 仅暴露 HTTP 模型与 `create_app`。

## 目标模块边界

- `core/anthropic/`：协议辅助、流原语、内容提取、token 估算、请求转换、thinking、tool 辅助、流契约断言。
- `api/runtime.py`：应用组合、可选 messaging 启停、会话恢复与清理。
- `providers/`：provider 描述、凭证解析、传输工厂、限流、上游请求构建、流转换。
- `messaging/`：平台无关编排、命令分发、渲染、语音与持久化。
- `cli/`：Claude CLI 运行配置、子进程管理、用户入口。

## Smoke 覆盖策略

- 默认 CI 保持确定性，只跑 `tests/`：`uv run pytest`。
- 产品 smoke 放在 `smoke/`，通过 `FCC_LIVE_SMOKE=1` 开启。
- 除非明确支持并行，否则 smoke 用 `-n 0`。

合法 skip 类型：

- `missing_env`：缺少凭证、本地服务、二进制或显式开关。
- `upstream_unavailable`：真实 provider/bot API/本地模型服务不可达。

`product_failure` 与 `harness_bug` 属于回归失败。若 `FCC_SMOKE_PROVIDER_MATRIX` 显式选择了 provider，则缺配置应失败而不是跳过。

## 重构规则

- 对外请求/响应形状保持稳定，内部可迁移。
- 模块迁移应一次完成：更新新归属导入并移除旧兼容层（除非明确要保留公开接口）。
- 迁移共享协议或 runtime 代码前，先用聚焦测试锁定行为。
- 校验顺序：`uv run ruff format` → `uv run ruff check` → `uv run ty check` → `uv run pytest`。
