# ZJU Learning Tools

ZJU Learning Tools 是面向 Windows Codex 的本地插件，用于安全查询“学在浙大”和部分智云
课堂数据，并下载用户有权访问的官方课程资料。插件通过本地 stdio MCP 运行，统一认证密码
不会进入 Codex 上下文，也不提供任何校园系统远端写入工具。

## 能力

- 查询学年、学期、课程、章节、活动和待办。
- 查看作业元数据、本人提交历史、课程进度、成绩和测验状态。
- 只读查看问卷、签到通知和讨论，不答题、不签到、不发帖。
- 列出课程/个人资源，按用户明确选择下载，并校验路径、大小和 SHA-256。
- 查询智云课堂日程、已有 PPT 页面元数据和转写结果。

插件不能提交作业或考试、填写问卷、代签或枚举签到码、发布讨论、伪造位置/设备/进度、
刷视频或绕过下载限制。

## 按任务拆分的 Skills

插件包含六个相互独立的 Skill，使 Agent 只加载当前任务所需的工作流与安全约束：

- `$zju-auth-session`：运行环境诊断，以及由用户本人完成的登录、状态检查和登出指导。
- `$zju-course-planning`：学期、课程、待办、活动与进度整理。
- `$zju-assignment-grades`：作业截止时间、本人提交历史、反馈与成绩查询。
- `$zju-resource-downloads`：资源定位、明确确认、限量下载与哈希汇总。
- `$zju-assessments-discussions`：只读查询测验、问卷、签到通知与课程讨论。
- `$zju-zhiyun-classroom`：智云课堂日程、PPT 元数据与已有转写。

认证只是各查询流程的共同前置条件，不会扩大权限。数据 Skill 遇到 `auth_required` 时会转到
`$zju-auth-session`，所有 Skill 都不能执行远端写入。

## 要求与安装

- Windows 10/11
- `PATH` 中已有 [uv](https://docs.astral.sh/uv/)
- 能访问相应浙大服务的网络
- 本人账号对目标课程和文件具有访问权限

将本仓库添加为 Codex 插件市场，再安装 `zju-learning-tools`。运行时依赖由
`runtime/uv.lock` 锁定；首次使用可能需要下载公开 Python 依赖。

请在你本人打开的 PowerShell 中执行登录：

```powershell
powershell -ExecutionPolicy Bypass -File .\plugins\zju-learning-tools\scripts\zju-auth.ps1 login
```

密码使用终端隐藏输入且不会保存。随机会话加密密钥保存在 Windows Credential Manager，
加密且会过期的 Cookie 会话位于
`%LOCALAPPDATA%\pirate-608\zju-learning-tools\`。插件不会读取已安装 ZLA 或浏览器的凭据。

将参数换成 `status` 或 `logout` 可检查或清除会话。CAS 出现验证码、二次认证或表单变化时，
登录会安全停止并提示使用官方页面，不会无限重试。

## 下载规则

Agent 必须先列出资源，并得到用户对上传 ID、文件名和现有绝对目标目录的明确确认。默认不覆盖
同名文件，而是生成 `-v2` 等版本；文件经同目录临时文件写入后原子改名。限制为单文件
250 MiB、每批 50 个、每批总计 1 GiB，并阻止路径穿越、UNC、ADS、重解析点和非白名单重定向。

校园 API 没有公开契约，可能随时变化。CI 仅使用 Mock 服务与脱敏 fixture，不会对生产校园
域名执行写测试。

## 让 AI 自动配置插件市场

复制以下 Prompt 给 Codex：

```text
请添加 Git 插件市场 git@github.com:pirate-608/codex-plugins.git，检查其中的市场元数据，安装
zju-learning-tools，并确认本机 uv 可用。不要向我索要浙大密码或 Cookie。安装完成后，给出需要
由我本人在本地 PowerShell 执行的认证命令，并提醒我新建一个 Codex 任务后再测试 zju_doctor。
```

## 许可证

插件自有代码使用 MIT。隔离的 `vendor/lazy-core` 兼容组件来自
[LAZY v0.2.6](https://github.com/YangShu233-Snow/Learning_at_ZJU_third_client)，继续使用
LGPL-3.0-only。详见 `THIRD_PARTY_NOTICES.md` 和 `UPSTREAM.json`。未引入 LAZY 的 AGPL Server。
