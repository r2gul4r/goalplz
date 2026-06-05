# Security Policy

Goalplz is a local Codex plugin and prompt package. It should not require secrets, production credentials, paid API calls, or production writes to install or verify.

## Reporting a Vulnerability

If GitHub private vulnerability reporting is enabled for this repository, use it.

If it is not enabled, open a minimal public issue that describes the affected area without posting exploit details, credentials, tokens, private logs, or sensitive local paths.

## Security Expectations

Goalplz should:

- Preserve Codex approval gates for paid API calls, deploys, production writes, dependency installs, and destructive actions.
- Avoid weakening authentication, authorization, validation, or sandbox boundaries.
- Avoid logging secrets or sensitive personal data.
- Treat `/goalplz` as a prompt-routing convenience, not as permission to bypass user approval.

## Non-Goals

Goalplz is not a security scanner, sandbox escape tool, credential manager, or production deployment system.
