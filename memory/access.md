# Access Memory

Seed notes for SSH hosts, key aliases, VPN configs, and access quirks/patterns.

## SSH Hosts

- `velcra-gh-runner.servers.miguel.ms` / `10.3.10.65`: Ubuntu 24.04 LTS LXC `10065` on `pve-02`; SSH verified after base prep. GitHub runner not installed/registered yet.
- `vader.agents.miguel.ms` / `10.3.10.67`: Ubuntu 24.04 LTS GPU LXC `10067` on `pve-02`; SSH verified as both `root` and `openclaw`. `openclaw` has Miguel/Vader SSH keys, sudo, video/render groups, and passwordless sudo at creation time.

## GitHub Runner Access Pattern

- Do not configure or run GitHub Actions runner as `root`; `config.sh` rejects sudo/root with `Must not run with sudo`.
- Use a non-root user such as `github-runner`, own `/home/github-runner/actions-runner`, and run registration as that user.
- Registration tokens pasted into chat/Discord should be treated as exposed and regenerated.
- Give sudo only if workflow requirements justify it; prefer docker group membership if workflows only need Docker.

## Vader OpenClaw Trusted Proxy

- Public access path is `https://vader.miguel.ms` through Caddy at `10.3.10.20`, not direct Gateway exposure.
- Caddy/Vouch authenticated username is `miguel`, so OpenClaw `allowUsers` should include `miguel` for this route.
- Recommended OpenClaw trusted-proxy config values: trusted proxy `10.3.10.20`, user header `x-forwarded-user`, required headers `x-forwarded-proto,x-forwarded-host`.
- Keep Gateway port `18789` reachable only from the reverse proxy for trusted-proxy auth.
