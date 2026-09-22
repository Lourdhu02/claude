# Security

## Reporting a security issue

If you find a security vulnerability in this course — for example, a code example that exposes an API key in a way that could lead to accidental sharing, or a lab that encourages an unsafe pattern — please report it privately.

**Preferred way**: Open a private issue on the repo if GitHub private reporting is available, or email the maintainer at the address listed in the repo settings.

**What to include**:
- What the issue is
- Why it's a security concern
- A suggested fix, if you have one

**What to expect**:
- Acknowledgment within a few days
- A fix or a response with next steps

## Public issues

For non-security bugs — a lab that doesn't run, a confusing explanation, a typo — open a public issue. See [CONTRIBUTING.md](./CONTRIBUTING.md).

## Security in the course content

The course uses `python-dotenv` to load the API key from a `.env` file that is `.gitignore`d. The `.env.example` file contains a placeholder, not a real key. Students are instructed not to commit their `.env`.

If you notice a code example or lab that contradicts this — for example, one that hardcodes a key or prints it to the console — that's exactly the kind of thing a security report is for.
