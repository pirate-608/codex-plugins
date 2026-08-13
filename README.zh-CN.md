# pirate-608 Codex 插件市场

[English](README.md) | 简体中文

一个公开的 Codex 插件市场，提供 Unity、CAD、Adobe、LaTeX、Ren'Py、Calibre、Windows 文件搜索与安全受控的浙大课程工作流。

## 添加插件市场

~~~sh
codex plugin marketplace add git@github.com:pirate-608/codex-plugins.git
~~~

如果当前网络无法使用 SSH，可以改用 HTTPS：

~~~sh
codex plugin marketplace add https://github.com/pirate-608/codex-plugins.git
~~~

使用稳定的插件 ID 和市场名称安装插件，例如：

~~~sh
codex plugin add unity-mcp@pirate-608-codex-plugins
~~~

## 让 AI 自动配置

复制下面的提示词并发送给 Codex 或其他编程智能体：

~~~text
请帮我自动配置下面这个 Codex 插件市场：

- SSH 仓库：git@github.com:pirate-608/codex-plugins.git
- HTTPS 备用地址：https://github.com/pirate-608/codex-plugins.git
- 预期市场名称：pirate-608-codex-plugins

请自主完成配置：
1. 执行操作前，先检查本机 Codex CLI 及其 plugin marketplace 帮助，确认当前版本支持的命令。
2. 列出已配置的市场。如果这个完全相同的市场已经存在，使用当前 CLI 支持的 marketplace upgrade
   命令刷新它，不要重复添加。
3. 如果尚未配置，优先使用 SSH 地址添加；如果 SSH 连接或认证失败，自动改用 HTTPS 地址重试。
4. 保留所有无关的插件市场和设置。除非我明确要求，否则不要安装任何单独插件。
5. 验证该市场已经可用且名称为 pirate-608-codex-plugins，然后使用 plugin list 命令列出其中
   可用的插件 ID。
6. 最后报告执行过的命令和配置结果。仅当认证、授权或缺少必要依赖导致无法继续时再询问我，
   且不要输出任何凭据或 token。
~~~

## 插件列表

| 插件 ID | 显示名称 | 用途 |
| --- | --- | --- |
| unity-mcp | Unity MCP | Unity 项目配置、2D/3D、玩法、UI、VFX、调试、优化与构建发布 |
| renpy-visual-novel-dev | Ren'Py Visual Novel Development | 受控创作、Codex 原生素材生成与运行时视觉测试 |
| latex-workflows | LaTeX Workflows | LaTeX 编译、故障排查与验证 |
| solidworks-automation | SolidWorks Automation | SolidWorks COM 与 MCP 自动化 |
| autocad-mcp-codex | AutoCAD MCP | 通过 MCP 完成 AutoCAD 绘图与检查 |
| adobe-photoshop | Adobe Photoshop | Photoshop 文档与图层工作流 |
| adobe-premiere | Adobe Premiere Pro | Premiere Pro 视频编辑工作流 |
| adobe-after-effects | Adobe After Effects | After Effects 合成与动画工作流 |
| calibre-library-tools | Calibre Library Tools | Calibre 书库分析与维护 |
| everything-search | Everything Search | 通过 voidtools ES 快速查找本地 Windows 文件和文件夹 |
| zju-learning-tools | ZJU Learning Tools | 浙大课程查询、受限 CLI 回退、受控下载与确认后的普通作业提交 |

## 运行要求

每个插件会声明自己的运行时集成。根据插件不同，主机可能需要安装对应桌面应用，以及
Python、uv/uvx、Node.js/npx 或位于 PATH 中的 PowerShell。仓库不包含商业桌面软件和用户凭据。

Everything Search 仅支持 Windows，需要用户自行安装并运行 Everything，同时确保 `es.exe` 位于
PATH，或通过 `EVERYTHING_ES_PATH` 指定其路径。插件不会捆绑或自动启动这些程序。

ZJU Learning Tools 面向 Windows 且需要 `uv`。认证必须由用户在本地 PowerShell 中通过隐藏
输入完成，凭据不会进入 Codex。0.3.0 仍只有普通作业提交这一项远端写入：默认关闭，必须由用户
本地启用、核对锁定的文件哈希预览并逐次重新确认。MCP 传输不可用时，可通过独立加密会话的
tronclass-cli 受限回退完成固定查询与单文件下载，但绝不回退提交。使用前请阅读插件 README。

### Ren'Py 图片与运行时工作流

Ren'Py 插件使用 Codex 内置图片生成能力制作背景、CG、立绘和 UI 素材，因此默认流程不需要
Gemini、Nano Banana、`GEMINI_API_KEY` 或 `OPENAI_API_KEY`。项目素材会先在本地完成尺寸、
透明度和命名规范化，并写入项目侧 manifest，再由内置 Ren'Py MCP 注册和验证。如果内置图片
能力不可用，工作流只接受用户提供的素材，不会静默切换图片服务商。

实时截图、场景检查、布局测量和运行时控制可选使用采用 MIT 许可证的 RenForge 0.7.0。
`uvx` 会在首次使用时下载这个固定版本，因此届时需要网络；即使 RenForge 无法启动，内置的
创作 MCP 和静态诊断仍然可以使用。

## 仓库结构

- .agents/plugins/marketplace.json：Git 插件市场目录。
- plugins/<plugin-id>/.codex-plugin/plugin.json：各插件的清单。
- 各插件的 skills、MCP 启动器、脚本、图标和上游说明均放在对应插件目录中。

## 许可证

本仓库汇集了采用不同许可证的插件和内置上游组件。具体条款与署名请查看各插件清单，以及
对应的 LICENSE、NOTICE、UPSTREAM.json 或 vendor 目录。简要清单见 [NOTICE.md](NOTICE.md)。
