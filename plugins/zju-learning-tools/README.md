# ZJU Learning Tools

ZJU Learning Tools is a Windows-first Codex plugin for safely reading 学在浙大 and selected 智云
data and downloading official course resources. It runs locally over stdio. The plugin never sends
your ZJU credentials to Codex and exposes no campus-side write tools.

## Capabilities

- List academic terms, courses, modules, activities and todos.
- Review assignment metadata, submission history, progress, grades and assessment status.
- Read questionnaire, roll-call and discussion metadata without answering or publishing.
- List personal/course resources and download explicitly selected uploads with size/path controls
  and SHA-256 verification.
- Query 智云 class schedules, PPT-page metadata and existing transcripts.

The plugin cannot submit homework or exams, answer questionnaires or roll calls, publish forum
content, spoof attendance, fabricate progress, brush videos, or bypass download controls.

## Task-specific Skills

The plugin routes requests through six independent Skills so an agent loads only the workflow and
safety rules needed for the current task:

- `$zju-auth-session`: runtime diagnosis and user-owned login, status, or logout guidance.
- `$zju-course-planning`: terms, courses, todos, activities, and progress summaries.
- `$zju-assignment-grades`: assignment deadlines, submission history, feedback, and grades.
- `$zju-resource-downloads`: resource discovery, explicit confirmation, bounded download, and hash reporting.
- `$zju-assessments-discussions`: read-only assessment, questionnaire, roll-call, and forum information.
- `$zju-zhiyun-classroom`: Zhiyun class schedules, PPT metadata, and existing transcripts.

Authentication is a shared prerequisite, not an implicit permission expansion. Each data Skill
routes `auth_required` to `$zju-auth-session`; none can perform a remote write.

## Requirements and installation

- Windows 10/11
- [uv](https://docs.astral.sh/uv/) on `PATH`
- Network access to the relevant ZJU services
- A user account authorized to access the requested material

Install this repository as a Codex marketplace, then install `zju-learning-tools`. The runtime is
locked by `runtime/uv.lock`; first use can require downloading those public Python dependencies.

Authenticate in a PowerShell that you opened yourself:

```powershell
powershell -ExecutionPolicy Bypass -File .\plugins\zju-learning-tools\scripts\zju-auth.ps1 login
```

The password is read with hidden terminal input and is not stored. A random encryption key is kept
in Windows Credential Manager; the encrypted, expiring Cookie session is stored under
`%LOCALAPPDATA%\pirate-608\zju-learning-tools\`. The plugin does not read ZLA credentials or
browser Cookies.

Check or clear the session with `status` or `logout`. If CAS adds CAPTCHA/MFA or changes its form,
login fails closed and asks you to use the official site; it does not retry indefinitely.

## Download behavior

The agent must first list resources and receive confirmation of exact upload IDs, filenames, and an
existing absolute destination directory. Downloads do not overwrite existing files (`-v2`, etc.),
are written atomically, and are limited to 250 MiB each, 50 files per batch, and 1 GiB per batch.
Remote filenames and redirects are restricted to prevent path traversal and credential leakage.

Campus APIs used here are unofficial and can change. CI uses only mock servers and sanitized
fixtures; no production campus write test exists.

## Configure this marketplace with an AI

Copy this prompt into Codex:

```text
Add the Git plugin marketplace git@github.com:pirate-608/codex-plugins.git, inspect its marketplace
metadata, install zju-learning-tools from it, and verify that uv is available. Do not ask me for my
ZJU password or cookies. After installation, show me the exact local PowerShell authentication
command and tell me to start a new Codex task before testing zju_doctor.
```

## Licensing

Plugin code is MIT licensed. The isolated `vendor/lazy-core` compatibility component is from
[LAZY v0.2.6](https://github.com/YangShu233-Snow/Learning_at_ZJU_third_client) and remains
LGPL-3.0-only. See `THIRD_PARTY_NOTICES.md` and `UPSTREAM.json`. LAZY's AGPL server is not included.
