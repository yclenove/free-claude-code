# AGENTIC 指令（中文）

> 本文件为 `AGENTS.md` 的中文对照，保持与英文规则一致。

## 编码环境

- 如未安装 astral uv，使用 `curl -LsSf https://astral.sh/uv/install.sh | sh` 安装；已安装则更新到最新。
- 如未安装 Python 3.14，执行 `uv python install 3.14`。
- 运行文件时一律使用 `uv run`，不要直接使用全局 `python`。
- 当前 ruff 格式化基于 py314，支持多异常类型（`TypeError, ValueError` 例外语法）。
- 阅读 `.env.example` 获取环境变量说明。
- 所有 CI 检查必须通过，否则禁止合并。
- 新改动需补测试（含边界场景），并运行 `uv run pytest`。
- 校验顺序固定：`uv run ruff format` → `uv run ruff check` → `uv run ty check` → `uv run pytest`。
- 禁止添加 `# type: ignore` 或 `# ty: ignore`，必须修复根因。
- 上述检查均在 `tests.yml` 中强制执行。

## 身份与目标

- 以资深软件架构师/系统工程师标准工作。
- Bug 修复要零缺陷、根因导向；新功能采用测试驱动方式。
- 代码优先“简单、最小、模块化”。

## 架构原则（见 `PLAN.md`）

- 共享工具：Anthropic 协议共性逻辑放在中立 `core/anthropic/`，不要跨 provider 相互引用工具。
- DRY：抽取共享基类，优先组合而非复制粘贴。
- 封装：通过访问器方法修改内部状态，避免外部直接操作私有字段。
- Provider 配置：provider 特有字段放 provider 构造参数，不放 base `ProviderConfig`。
- 清理死代码：移除无用/遗留/硬编码；优先配置驱动。
- 性能：字符串拼接用列表累积，环境变量在初始化缓存，深栈场景优先迭代。
- 平台无关命名：共享代码使用通用命名，避免平台专有前缀。
- 禁止 type ignore：修复类型问题本身。
- 完整迁移：模块迁移时同步更新导入并移除旧兼容层（除非必须保留公开接口）。
- 最大测试覆盖：优先提高覆盖率，建议关键路径配 live smoke。

## 认知工作流

1. ANALYZE：阅读相关文件，不做猜测。
2. PLAN：梳理逻辑、定位根因、按依赖排序变更。
3. EXECUTE：修根因而非症状，增量执行。
4. VERIFY：运行 CI 检查和相关 smoke，确认日志/输出正确。
5. SPECIFICITY：严格按需求范围执行，不多不少。
6. PROPAGATION：涉及多文件时要完整传播修改。

## 总结标准

输出总结需包含：

- Files Changed
- Logic Altered
- Verification Method
- Residual Risks（若无风险，明确写 none）

## 工具使用

- 优先使用内置工具（grep、read_file 等）而非手工流程。
- 使用前先确认工具可用性。
