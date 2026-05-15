# Decisions

Seed notes for key decisions made with Miguel.

## 2026-05-13 — Email checks use gog only

- Miguel instructed: never use Codex Gmail connector/tools, MCP Gmail tools, or other Codex-provided email tools to check email.
- Use `gog` only.
- If `gog` is unavailable, unauthenticated, or cannot select the required account, stop and report the blocker instead of falling back.

## 2026-05-13 — Do not patch installed OpenClaw code without approval

- After an installed Control UI bundle patch was rolled back, Miguel clarified: never change installed OpenClaw code, global package files, module files, generated dist files, or bundled UI assets without explicit approval.
- Product-code fixes must be proposed first with target files and rollback plan.

## 2026-05-13 — SSH defaults and config maintenance

- Default SSH user for infrastructure hosts is usually `root`.
- If `root` is not allowed, Miguel will instruct otherwise or the verified `.ssh/config` entry should record the exception.
- Miguel explicitly allowed ongoing maintenance of `/home/openclaw/.ssh/config` as host access is verified.

## 2026-05-14 — No blanket infrastructure delegation rule

- Miguel clarified that the old rule requiring infrastructure delegation is obsolete.
- Vader handles infrastructure requests directly when tools, access, and permission make it safe.
- Config or service changes still need explicit approval before applying.

# Infrastructure Decisions

---

## 2026-05-13 — Use Existing Vouch Auth for Vader OpenClaw Trusted Proxy

**Decision:** Put `vader.miguel.ms` behind the existing Caddy + Vouch/Synology authentication path and configure OpenClaw for trusted-proxy auth using Caddy-provided headers.

**Why:** Synology DSM Reverse Proxy alone cannot safely pass the currently logged-in DSM user as a dynamic identity header. The existing Vouch path already validates identity and emits `X-Vouch-User`; Caddy can map that to the conventional `X-Forwarded-User` header for OpenClaw.

**What changed:**
- `/etc/caddy/sites/miguel.ms/vader.caddy` proxies `vader.miguel.ms` to `vader.agents.miguel.ms:18789`.
- Normal paths use Vouch auth; `/hooks` bypasses auth.
- Caddy forwards `X-Forwarded-User`, `X-Forwarded-Proto`, `X-Forwarded-Host`, `X-Vouch-User`, and `X-OpenClaw-Scopes`.

**OpenClaw values:** trusted proxy IP `10.3.10.20`, user header `x-forwarded-user`, required headers `x-forwarded-proto,x-forwarded-host`, allowed user `miguel`.

**Outcome:** Caddy reload succeeded; unauthenticated root path redirects to Vouch; `/hooks` reaches OpenClaw without Vouch redirect.

---

## 2026-05-12 — Recover Komodo by Upgrading MongoDB to 8.3.1

**Decision:** Upgrade MongoDB LXC `10036` from MongoDB `8.0.21` to `8.3.1` instead of rebooting `pve-01` into the previous kernel.

**Why:** MongoDB `8.0.21` would not start under kernel `7.0.0-3-pve` / Linux 6.19+, but a no-install smoke test showed MongoDB `8.3.1` could run under the active kernel. Upgrading the LXC avoided a disruptive Proxmox host reboot.

**What changed:** Snapshot `pre-mongodb-8-3-1-20260512` was taken, the MongoDB apt repo was changed from `8.0` to `8.3`, MongoDB upgraded to `8.3.1`, and the stale `GLIBC_TUNABLES=glibc.pthread.rseq=0` systemd workaround was cleared.

**Outcome:** MongoDB and Komodo recovered; Komodo public URL returned HTTP 200 and Komodo API `ListServers` returned 6 servers.

---

## 2026-05-03 — Keep NVIDIA 580.126.09 on pve-02 for Kernel 7

**Decision:** Keep the existing NVIDIA `580.126.09` DKMS driver on `pve-02` after patching it for kernel `7.0.0-3-pve`; do not install NVIDIA `.run` driver `595.71.05` yet.

**Why:** The patched `580.126.09` stack built cleanly, repaired the missing initrd, and worked after reboot on kernel 7. The `595.71.05` `.run` driver was viable in an extract-only build test, but installing it would let the NVIDIA installer own the live GPU stack and affect GPU LXC workloads.

**Outcome:** `pve-02` booted `7.0.0-3-pve` cleanly with NVIDIA `580.126.09`; GPU access passed in `docker-gpu` and `tegclaw`. `595.71.05` remains a fallback candidate if packaged deliberately or required later.

---

## 2026-04-14 — Decommission Omada Backup Controller

**Decision:** After v6.2.10.11 upgrade failure, decommission omada-bkp-controller (LXC 10010, IP 10.3.10.10).

**Why:** The backup controller failed HSB secondary initialization timeout after upgrade to v6.2.10.11. Despite 1+ hour of troubleshooting (HSB state clear, hostname resolution, multiple restarts), the secondary could not initialize. v6.2.10.11 appears to have a known compatibility issue on secondary hardware. Primary is fully operational and can handle full network load standalone.

**What changed:**
- LXC 10010 deleted from pve-02
- IP 10.3.10.10 released to phpIPAM
- DNS record omada-bkp-controller.network.miguel.ms removed
- Omada cluster now single-node (omada-lxc-controller at 10.3.10.9, v6.2.10.11)

**Impact:**
- Network remains operational (primary fully functional)
- High availability broken — single point of failure
- Can be restored: downgrade backup to v6.2.0.17 (known working) or wait for v6.2.10.x patch

**Rationale:** Spending more time on an unproven fix for an unstable build carried more risk than accepting a temporary single-node state. The primary is stable and handles load well. Decommissioning removes confusion and frees LXC resources.

---

## 2026-04-26 — Omada Primary Upgrade to 6.2.10.15

**Decision:** Upgrade `omada-lxc-controller` to `Omada Controller v6.2.10.15 Build 20260417100356` using the exact TP-Link OTA package after taking LXC snapshot `pre-omada-6-2-10-15-20260426`.

**Why:** The public download page lagged behind the requested build and exposed only `6.2.0.17`. The exact OTA package was available and matched the requested version, so the safer path was snapshot first, then install the exact build on the restored primary.

**Outcome:** Primary controller is now running `v6.2.10.15`; service health and ports verified after install.

---

## 2026-05-11 — Omada Primary Upgrade to 6.2.10.17

**Decision:** Upgrade `omada-lxc-controller` to `Omada Controller v6.2.10.17 Build 20260428102045` using Miguel's exact TP-Link OTA package URL after taking LXC snapshot `pre-omada-6-2-10-17-20260511`.

**Why:** Miguel requested the exact OTA `.deb`. Prior Omada upgrades showed the OTA package URL is safer than relying on the public download page when TP-Link release metadata lags or exposes mismatched builds.

**Outcome:** Primary controller is running `v6.2.10.17`; package `omadac 6.2.10.17` is installed cleanly, Java and embedded MongoDB are running, ports 8043/8088/8843/29811-29814 are listening, HTTP redirects to HTTPS, HTTPS returns 200, and `dpkg --audit` is clean.

---
