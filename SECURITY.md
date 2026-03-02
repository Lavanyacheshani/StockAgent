# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in StockAgent, please report it responsibly.

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, please email: **lavanyacheshani5@gmail.com**

Include the following in your report:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **Acknowledgement**: Within 48 hours
- **Initial Assessment**: Within 1 week
- **Fix & Disclosure**: Coordinated with the reporter

## Security Best Practices for Users

1. **Never commit `.env` files** — Use `.env.example` as a template and keep secrets out of version control.
2. **Rotate API keys regularly** — Especially if they may have been exposed.
3. **Use environment variables or a secrets manager** — Never hardcode API keys in source code.
4. **Run Docker containers as non-root** — The provided Dockerfile already does this.
5. **Restrict CORS origins in production** — Update `server.py` to allow only your frontend domain.
6. **Keep dependencies updated** — Use `renovate.json` (already configured) or Dependabot for automated updates.
7. **Pin Docker base images** — Use digest-pinned images in production Dockerfiles.
