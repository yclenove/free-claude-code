## 2026-05-13
- Summary: 补充仓库忽略规则，排除会话痕迹目录、IDE 本地配置与审计草稿文件，避免误提交到远端。
- Affected: `.gitignore`, `CHANGELOG.md`
- Impact: 工作区保持干净状态，后续提交与同步不会携带本地临时文件。

## 2026-05-13
- Summary: 合并远端 fork `origin/main`（含 Xiaomi MiMo provider）到已同步上游的本地 `main`，统一 provider 目录、runtime 启动校验与 smoke 默认值；`AppRuntime.startup` 对 `fcc_skip_startup_model_validation` 使用 `getattr` 以兼容测试用 `SimpleNamespace`。
- Affected: `config/provider_catalog.py`, `providers/registry.py`, `providers/defaults.py`, `config/settings.py`, `api/runtime.py`, `.env.example`, `README.md`, `smoke/lib/config.py`, `smoke/README.md`, `api/admin_config.py`, `tests/providers/test_registry.py`, `tests/contracts/test_smoke_config.py`, `tests/config/test_config.py`, `tests/contracts/test_feature_manifest.py`, `CHANGELOG.md`
- Impact: 单一 `main` 线同时包含上游 Kimi/Wafer/OpenCode 与 fork 的 MiniMax、小米 MiMo；`uv run pytest` 全绿。

## 2026-05-13
- Summary: 将上游 `Alishahryar1/free-claude-code` 的 `main` 合并入 fork，保留 MiniMax 与中文 `.env.example` 说明，并接入 Kimi、Wafer、OpenCode Zen；OpenRouter free CLI 默认模型改为带 `open_router/` 前缀以避免与 `minimax` provider 前缀歧义。
- Affected: `.env.example`, `README.md`, `config/provider_catalog.py`, `config/settings.py`, `providers/registry.py`, `api/admin_config.py`, `smoke/lib/config.py`, `smoke/README.md`, `tests/config/test_config.py`, `tests/contracts/test_smoke_config.py`, `tests/providers/test_registry.py`, `CHANGELOG.md`
- Impact: 与上游功能对齐且保留 fork 独有 provider；smoke/OpenRouter 矩阵与 Admin 配置字段同步；全量 `uv run pytest` 通过。

## 2026-04-28
- Summary: 完成项目核心文档双语化，新增中文文档并在主 README 增加中英文入口。
- Affected: `README.md`, `README.zh-CN.md`, `PLAN.zh-CN.md`, `smoke/README.zh-CN.md`, `AGENTS.zh-CN.md`, `CLAUDE.zh-CN.md`
- Impact: 中文读者可直接使用完整中文文档，英文文档保持不变；降低上手成本并提升团队协作可读性。

## 2026-04-28
- Summary: 将 `.env.example` 的注释说明全面翻译为中文，便于本地配置时直接理解各变量用途。
- Affected: `.env.example`
- Impact: 保持变量名与默认值不变，仅提升可读性与配置效率，不影响运行逻辑。

## 2026-04-28
- Summary: 为 `.env` 配置 NVIDIA NIM 的高质量分层模型路由，并设置桌面网关鉴权 token，默认关闭 thinking 以降低额度消耗。
- Affected: `.env`
- Impact: Claude Desktop 可直接以 `freecc` 鉴权接入本地代理；Opus/Sonnet/Haiku 请求分别映射到更优先质量或性价比模型，响应链路已验证可用。

## 2026-04-28
- Summary: 针对 NVIDIA NIM 响应慢的问题，将默认/sonnet/haiku 路由切换到低延迟 `step-3.5-flash`。
- Affected: `.env`
- Impact: 降低日常问答首答与总耗时；保留 `MODEL_OPUS` 高质量路由不变，按需继续用于复杂任务。

## 2026-04-28
- Summary: 将模型路由调整为“高质量 + 低延迟 + 代码能力”组合：Opus 用 `deepseek-v4-pro`，Sonnet 用 `glm5`，Haiku/默认用 `deepseek-v4-flash`。
- Affected: `.env`
- Impact: 复杂编码任务优先高质量模型，日常请求保持低延迟；兼顾代码能力与交互速度。

## 2026-04-28
- Summary: 基于实测延迟将 Sonnet/Haiku/默认模型回切到 `step-3.5-flash`，保留 Opus 为 `deepseek-v4-pro`。
- Affected: `.env`
- Impact: 日常交互与代码任务显著提速，同时保留高质量 Opus 入口用于复杂场景。

## 2026-04-28
- Summary: 新增 MiniMax 官方 API key 直连 provider（`minimax/...`），并同步接入配置、注册表、smoke 配置、测试与中英文文档。
- Affected: `config/provider_catalog.py`, `config/settings.py`, `providers/defaults.py`, `providers/registry.py`, `providers/minimax/__init__.py`, `providers/minimax/client.py`, `providers/minimax/request.py`, `.env.example`, `smoke/lib/config.py`, `tests/providers/test_registry.py`, `tests/providers/test_minimax.py`, `tests/config/test_config.py`, `tests/contracts/test_feature_manifest.py`, `tests/contracts/test_smoke_config.py`, `README.md`, `README.zh-CN.md`, `smoke/README.md`, `CHANGELOG.md`
- Impact: 可直接使用 `MINIMAX_API_KEY` 与 `MINIMAX_BASE_URL` 走官方链路，减少依赖 NIM 托管路径带来的延迟不确定性，并保持现有 provider 架构一致性。
