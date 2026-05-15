# Incidents & Outages

---

## 2026-05-12 — Komodo Down Because MongoDB Would Not Start Under Kernel 7

**What happened:** `https://komo.miguel.ms` returned Caddy `502`; `komodo-core-1` was crash-looping because it could not connect to MongoDB at `mongodb.servers.miguel.ms:27017`.

**Root cause:** MongoDB LXC `10036` on `pve-01` was running MongoDB `8.0.21`, which refused to start under Proxmox kernel `7.0.0-3-pve` / Linux 6.19+ compatibility guard. A stale systemd workaround, `GLIBC_TUNABLES=glibc.pthread.rseq=0`, also caused MongoDB `8.3.1` to trip the same guard until cleared.

**Recovery:** Snapshot `pre-mongodb-8-3-1-20260512` was taken, MongoDB apt repo was switched from `8.0` to `8.3`, MongoDB was upgraded to `8.3.1`, and `/etc/systemd/system/mongod.service.d/10-clear-legacy-rseq.conf` was added with `Environment="GLIBC_TUNABLES="`.

**Outcome:** `mongod.service` active, MongoDB `8.3.1`, `dpkg --audit` clean, no failed units, MongoDB listening on `0.0.0.0:27017`, Komodo DB ping succeeded, `komodo` database had 23 collections, Komodo public URL returned HTTP 200, and Komodo API `ListServers` returned 6 servers. FCV was not changed because the Komodo DB user could not read admin-level FCV.

**Lesson:** Before rebooting a Proxmox host for MongoDB kernel incompatibility, check if a newer MongoDB repo can run under the active kernel. Also remove old `GLIBC_TUNABLES=glibc.pthread.rseq=0` workarounds after upgrading MongoDB beyond the affected version.

---

## 2026-05-03 — pve-02 Kernel 7 Boot Panic From Missing Initrd

**What happened:** `pve-02` failed to boot kernel `7.0.0-3-pve` and showed `VFS: Unable to mount root fs on unknown-block(0,0)` on console.

**Root cause:** Proxmox kernel `7.0.0-3-pve` had been installed by `apt-get dist-upgrade`, but NVIDIA DKMS `580.126.09` failed during kernel post-install. `/boot/vmlinuz-7.0.0-3-pve` existed while `/boot/initrd.img-7.0.0-3-pve` did not, so GRUB booted the new kernel without an initrd.

**Recovery:** Booted previous kernel `6.17.13-6-pve`, verified root disk/NVMe health and active GPU state, patched NVIDIA `580.126.09` DKMS source for the kernel `zone_device_page_init()` API change, rebuilt DKMS for `7.0.0-3-pve`, repaired `dpkg`, regenerated initramfs/GRUB, and verified `/boot/initrd.img-7.0.0-3-pve` and GRUB initrd line.

**Outcome:** `pve-02` rebooted cleanly into `7.0.0-3-pve`; RTX 3080 Ti worked with NVIDIA `580.126.09`; `dpkg --audit` clean; no failed units; LXCs `docker-gpu` and `tegclaw` running; GPU passthrough worked inside both LXCs.

**Related test:** NVIDIA official `.run` driver `595.71.05` was extract-only tested and built cleanly against `7.0.0-3-pve` with SHA256 `36203b8960b7e49c8a42f6ba1f5863cde34a05e93d2b24b798af06dd846f6b82`, but was not installed.

**Lesson:** A kernel panic with `unknown-block(0,0)` after a Proxmox kernel upgrade can be a missing-initrd problem caused by DKMS post-install failure, not necessarily disk failure.

---

## 2026-04-26 — Omada Primary Reinstall / Restore

**What happened:** An attempted Omada controller upgrade path briefly left `omadac` broken/half-configured. A clean reinstall with the public `6.2.0.17` package removed existing controller data, so the primary was restored from the 2026-04-25 LXC backup and then upgraded cleanly to `6.2.10.15` from the exact OTA package.

**Recovery:** Restored LXC `10009` from `vzdump-lxc-10009-2026_04_25-05_00_02.tar.zst` onto `local-lvm`, then reinstalled the exact `6.2.10.15` build after snapshotting the container.

**Lesson:** Do not treat Omada "clean reinstall" as a harmless upgrade path; it can erase controller data. Snapshot/backup first, then use the exact target build.

## 2026-03-18 — Omada Cluster Down After Upgrade

**Trigger:** Vader upgraded both Omada controllers (omada-lxc-controller + omada-bkp-controller) from 6.2.0.12 to 6.2.0.15.

**Root cause (multi-layered):**
1. The `.deb` was downloaded from the TP-Link community **beta/pre-release** thread, not the official release page. Miguel's intended build came from the OTA CDN (`ota-download.tplinkcloud.com`) — checksums turned out identical, but the source was wrong practice.
2. The upgrade installer on the **primary** ran with no TTY and silently failed on first attempt (whiptail dialog). Fixed with `DEBIAN_FRONTEND=noninteractive dpkg -i`.
3. After upgrade, the **backup controller** had **MongoDB 8.0.19** (repo already configured for 8.0 on that LXC), while the **primary** still ran MongoDB 7.0.30.
4. MongoDB wire protocol version mismatch (7.0 = wire 21, 8.0 = wire 25) → replset heartbeats rejected → backup fell back out of HSB mode to standalone.
5. During repair attempts, the backup's mongod repeatedly started with `--bind_ip 127.0.0.1` (standalone fallback) instead of `--bind_ip 0.0.0.0 --replSet omadaCluster_8507` — because the 5-minute secondary init timeout expired before the primary was ready.

**Resolution:**
1. Added MongoDB 8.0 repo to primary (`/etc/apt/sources.list.d/mongodb-org-8.0.list`)
2. Upgraded primary's MongoDB from 7.0.30 → 8.0.20
3. Restarted primary (tpeap stop/start) — picked up MongoDB 8.x, started with replSet config
4. Restarted backup cleanly — both nodes now on MongoDB 8.x, cluster identity check passed
5. Both nodes reconnected: node 1 (primary, 10.3.10.9) + node 2 (secondary, 10.3.10.10) healthy

**Lessons:**
- Never install pre-release/beta Omada builds on production (rule from Miguel)
- Check MongoDB version alignment BEFORE upgrading Omada controllers — especially when nodes have different repo configs
- Always upgrade primary first, then backup — they must be version-aligned for replset
- The `tpeap start` output "Waiting to initialize the secondary node" with eventual timeout → fallback to standalone is the symptom of this MongoDB mismatch

**Komodo API note:** The API keys in `~/.openclaw/.env` were stale. Use `source /home/openclaw/.openclaw/workspace/secrets/komodo.env` for current keys (KOMODO_KEY / KOMODO_SECRET).

---

## 2026-04-13 to 2026-04-14 — Omada v6.2.10.11 Upgrade Failure (Backup Controller)

**Trigger:** Upgrade both Omada controllers from v6.2.0.17 to v6.2.10.11 (released 2026-04-03).

**What happened:**
1. **Primary (omada-lxc-controller, 10.3.10.9):** Upgraded successfully. v6.2.10.11 Build 20260403150649 fully operational, web UI responsive, 4 EAPController processes running.
2. **Backup (omada-bkp-controller, 10.3.10.10):** Upgrade completed but secondary initialization hung on "Waiting to initialize the secondary node" timeout. HSB (Hot-Standby) cluster mode failed to initialize.

**Root cause (unresolved):**
- v6.2.10.11 appears to have an HSB secondary initialization issue on the backup hardware/configuration
- Attempted fixes:
  - Cleared HSB state → didn't help; init script hardcoded for HSB backup mode
  - Edited `/etc/hosts` to ensure primary hostname resolution → didn't resolve the timeout issue
  - Multiple service restart attempts → secondary always timed out on initialization
  - Resource check: 4GB RAM, 15GB disk — adequate, not a constraint

**Resolution:**
- After 1+ hour of troubleshooting, backup controller deemed unrecoverable on v6.2.10.11
- **Decision:** Decommission backup controller (2026-04-14)
- Primary is fully operational and can handle full network load standalone

**Outcome:**
- Network remains OPERATIONAL (primary fully functional)
- High availability broken (single point of failure on primary)
- To restore HA: either downgrade backup to 6.2.0.17 (known working) or wait for 6.2.10.x patch

**Lessons:**
- v6.2.10.11 HSB initialization has a known compatibility issue on secondary hardware
- Check Omada release notes for known v6.2.10.11 HSB bugs before upgrading production clusters
- Rapid backup of a working config (v6.2.0.17) after successful primary upgrade would have prevented extended downtime

---

# Incidents

Delays, cancellations, disruptions, and recovery preferences.
