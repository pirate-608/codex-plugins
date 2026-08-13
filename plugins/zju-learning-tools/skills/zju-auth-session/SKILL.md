---
name: zju-auth-session
description: Diagnose and manage the private local authentication session for ZJU Learning Tools. Use when the user asks to set up, log in to, log out of, check, repair, or troubleshoot 学在浙大/ZJU access, or when another ZJU tool returns auth_required or a runtime readiness error.
---

# ZJU Auth Session

Keep credential entry outside the agent. Use only `zju_doctor` and `zju_auth_status` for diagnosis.

## Diagnose

1. Call `zju_doctor` to check Windows, `uv`, the locked runtime, the credential store, and session-file readiness.
2. Call `zju_auth_status` to report whether a session exists, when it expires, and only the masked account suffix.
3. Translate structured failures without exposing raw exceptions or secret material.

## Ask the user to authenticate

Resolve `<plugin-root>` as the directory two levels above this skill directory. Tell the user to run the appropriate command in a PowerShell they opened themselves:

```powershell
powershell -ExecutionPolicy Bypass -File <plugin-root>/scripts/zju-auth.ps1 login
powershell -ExecutionPolicy Bypass -File <plugin-root>/scripts/zju-auth.ps1 status
powershell -ExecutionPolicy Bypass -File <plugin-root>/scripts/zju-auth.ps1 logout
```

Never run `login` through an agent-controlled shell. Never ask for or accept a password, Cookie, CAS ticket, Bearer token, session file, encryption key, or copied browser/ZLA credential in chat, tool arguments, environment variables, or configuration.

If login reports CAPTCHA, MFA, or an upstream-form change, stop and direct the user to the official site. Do not loop, scrape browser credentials, or weaken validation. After the user finishes login, ask them to retry `zju_auth_status`; do not claim success before checking.

## Boundaries

Authentication authorizes only the plugin's read-only queries and bounded official downloads. It never authorizes submission, posting, attendance, progress fabrication, or raw API access.
