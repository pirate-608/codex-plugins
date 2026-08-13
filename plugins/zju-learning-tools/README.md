# ZJU Learning Tools

ZJU Learning Tools is a Windows-first Codex plugin for safely reading 学在浙大 and selected 智云
data, downloading official course resources, and optionally submitting already reviewed files to
ordinary homework. It runs locally over stdio and never sends ZJU credentials to Codex.

## Capabilities

- List academic terms, courses, modules, activities and todos.
- Review assignment metadata, submission history, progress, grades and assessment status.
- Read questionnaire, roll-call and discussion metadata without answering or publishing.
- List personal/course resources and download explicitly selected uploads with size/path controls
  and SHA-256 verification.
- Query 智云 class schedules, PPT-page metadata and existing transcripts.
- Submit reviewed files to one ordinary-homework activity through a disabled-by-default,
  prepare/confirm/commit transaction with SHA-256 locking and write-back verification.

The plugin cannot submit exams, quizzes, classroom exercises or questionnaires, answer roll calls,
publish forum content, withdraw prior submissions, spoof attendance, fabricate progress, brush
videos, schedule/batch submissions, retry uncertain writes, or bypass download controls.

## Task-specific Skills

The plugin routes requests through seven independent Skills so an agent loads only the workflow and
safety rules needed for the current task:

- `$zju-auth-session`: runtime diagnosis and user-owned login, status, or logout guidance.
- `$zju-course-planning`: terms, courses, todos, activities, and progress summaries.
- `$zju-assignment-grades`: assignment deadlines, submission history, feedback, and grades.
- `$zju-assignment-submission`: gated preparation and one-time submission of reviewed homework files.
- `$zju-resource-downloads`: resource discovery, explicit confirmation, bounded download, and hash reporting.
- `$zju-assessments-discussions`: read-only assessment, questionnaire, roll-call, and forum information.
- `$zju-zhiyun-classroom`: Zhiyun class schedules, PPT metadata, and existing transcripts.

Authentication is a shared prerequisite, not an implicit permission expansion. Only
`$zju-assignment-submission` can invoke the two fixed assignment-write tools; every other Skill is
read-only with respect to campus systems.

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

## Assignment submission

Assignment submission is disabled after installation. To authorize files from one or more local
directories, run this yourself in an interactive PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\plugins\zju-learning-tools\scripts\zju-write-access.ps1 enable -Root D:\path\to\reviewed-homework
```

The script displays the exact scope and requires typing `ENABLE ASSIGNMENT SUBMISSION`. It writes a
local policy under `%LOCALAPPDATA%\pirate-608\zju-learning-tools\`; it does not store a password.
Use `status` to inspect the policy or `disable` to remove it.

Each attempt is two phase:

1. `zju_prepare_assignment_submission` re-reads the assignment and personal submission history,
   validates the deadline and ordinary-homework type, hashes every explicit file, and returns a
   120-second preview. It performs no remote write.
2. After the user reviews account suffix, assignment, prior attempts, file paths/sizes/SHA-256,
   comment, deadline, and payload hash, a separate explicit confirmation permits exactly one
   `zju_commit_assignment_submission` call.
3. Commit revalidates the account, capability, assignment revision, deadline, paths, sizes, and
   hashes; uploads files; submits once; then reads submission history back for verification.

Approvals are process-local, expire, and cannot be reused. A local atomic ledger blocks identical
duplicates across restarts. If a timeout or ambiguous failure occurs after a write may have begun,
the result is `submission_state_unknown`: inspect the official page and do not retry automatically.
The plugin never turns generated work directly into a submission within the same autonomous flow.

## Download behavior

The agent must first list resources and receive confirmation of exact upload IDs, filenames, and an
existing absolute destination directory. Downloads do not overwrite existing files (`-v2`, etc.),
are written atomically, and are limited to 250 MiB each, 50 files per batch, and 1 GiB per batch.
Remote filenames and redirects are restricted to prevent path traversal and credential leakage.

Campus APIs used here are unofficial and can change. CI uses only mock servers and sanitized
fixtures; no production campus write test exists. Real submission should first be tried by the user
with a small, non-critical ordinary-homework attachment after reviewing the official page.

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
