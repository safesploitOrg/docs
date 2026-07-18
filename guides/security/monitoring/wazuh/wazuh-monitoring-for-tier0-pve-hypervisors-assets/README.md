# Wazuh Monitoring Alerts (Tier-0 Hypervisors) - Theory

- [Wazuh Monitoring Alerts (Tier-0 Hypervisors)](#wazuh-monitoring-alerts-tier-0-hypervisors)
  - [🧱 What you have now (baseline reality)](#-what-you-have-now-baseline-reality)
  - [✅ Immediate high-value things to enable (do these first)](#-immediate-high-value-things-to-enable-do-these-first)
  - [🔍 Medium-term: turn it into “infrastructure security”](#-medium-term-turn-it-into-infrastructure-security)
  - [🧪 Advanced](#-advanced)
  - [🔗 How this pairs with other tools](#-how-this-pairs-with-other-tools)
  - [⚠️ Common mistakes to avoid](#-common-mistakes-to-avoid)
  - [🧭 Implementation plan](#-implementation-plan)

---

Adding Proxmox VE nodes to Wazuh

Right now, you’ve essentially given yourself **continuous visibility into your hypervisor layer**. That’s powerful *if you use it deliberately*.

Below is a **clear, practical playbook** of what you can do *right now*, ordered from **immediate wins → advanced/enterprise-style use**.

---

## 🧱 What you have now (baseline reality)

By enrolling your Proxmox nodes into Wazuh, you now get:

- Host-based telemetry from **your hypervisors**
- Continuous monitoring (not periodic scans)
- Change detection at the *infrastructure layer* (where things hurt most)

This mirrors how **large estates protect ESXi / hypervisors**.

---

## ✅ Immediate high-value things to enable (do these first)

### 1️⃣ File Integrity Monitoring (FIM) on Proxmox (CRITICAL)

**Why this matters**  
Hypervisors should almost *never* change unexpectedly.

Monitor:

- `/etc/pve/`
- `/etc/network/`
- `/etc/ssh/`
- `/etc/sudoers*`
- `/etc/systemd/`

This gives you:

- Alerts on cluster config changes
- Detection of:

  - Rogue edits
  - Accidental misconfig
  - Post-compromise persistence

> 💡 In prod, this is a **huge audit win**.

---

### 2️⃣ SSH & auth monitoring (very high signal)

Enable rules for:

- Failed SSH logins
- Root login attempts
- Key changes
- sudo usage

What you learn:

- How admins actually use the platform
- Whether access patterns are sane
- Whether automation is behaving as expected

This mirrors **real SOC detection**.

---

### 3️⃣ Package & update monitoring

Track:

- `pve-manager`
- Kernel updates
- ZFS / Ceph packages

Why:

- Hypervisor patching is **high risk**
- Wazuh gives you:

  - Who updated
  - When
  - What changed

This is *change control without tickets*.

---

## 🔍 Medium-term: turn it into “infrastructure security”

### 4️⃣ Proxmox-specific log correlation

Feed these into Wazuh rules:

- `/var/log/pveproxy/access.log`
- `/var/log/pvedaemon.log`
- `/var/log/syslog`

You can detect:

- VM start/stop outside change windows
- Unexpected node joins/leaves
- API token misuse
- Automation mistakes

That’s **real infra security**, not just logs.

---

### 5️⃣ Detect cluster drift (enterprise-grade)

Create alerts for:

- Ceph config changes
- Network bridge changes

In enterprise:

> Drift = outages.

Wazuh becomes your **early warning system**.

---

## 🧪 Advanced

### 6️⃣ Simulate an incident (high learning value)

Try this *intentionally*:

- Modify `/etc/pve/datacenter.cfg`
- Restart a VM outside normal hours
- Add a new SSH key manually

Then:

- Observe alerts
- Tune false positives
- Document response steps

That’s literally **SOC training**.

---

### 7️⃣ Compliance-style reporting (even in a homelab)

Use Wazuh to show:

- “No unauthorised hypervisor config changes”
- “Root login attempts are monitored”
- “Config drift is detected”

This maps cleanly to:

- NIST
- ISO 27001
- CE+

You’re building *audit language*, not just skills.

---

## 🔗 How this pairs with other tools

| **Tool**         | **Role**                |
|:-----------------|:------------------------|
| OpenVAS / Nessus | Finds vulnerabilities   |
| Wazuh            | Detects changes & abuse |
| Proxmox          | Enforces infra          |
| Ansible          | Fixes issues            |
| Terraform        | Keeps consistency       |
| SIEM             | Correlates events       |

You now have:

> discovery → detection → response

That’s actual security maturity.

---

## ⚠️ Common mistakes to avoid

❌ Monitoring *everything* → alert fatigue (signal-to-noise ratio)
❌ Treating hypervisors like normal servers
❌ Ignoring `/etc/pve/` (this is the crown jewel)
❌ Not documenting “expected changes”

---

## 🧭 Implementation plan

**1**

- Enable FIM on `/etc/pve`
- Tune SSH alerts
- Baseline “normal” activity

**2**

- Add Proxmox API & daemon logs
- Simulate changes
- Write a mini runbook

**3**

- Integrate OpenVAS findings
- Correlate:

  - "Vulnerability exists” + “Config changed”
