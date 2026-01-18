# NetNTLMv1 Is Now Cryptographically Dead

## Overview
In 2025, Google/Mandiant released **8.6 TB of pre-computed rainbow tables** targeting the NetNTLMv1 authentication protocol.  
The dataset covers over **1.1 quadrillion password permutations**, reducing NetNTLMv1 credential recovery to a **commodity operation** achievable in under **12 hours on consumer-grade hardware**.

This release was explicitly intended to **accelerate protocol deprecation** by eliminating the remaining cost and complexity barriers to exploitation.

**NetNTLMv1 should now be considered functionally equivalent to plaintext authentication.**

---

## What Changed
Prior to this release, NetNTLMv1 was widely acknowledged as weak but often tolerated due to:
- Legacy system compatibility
- Perceived attacker effort
- Lack of widespread exploitation tooling

The public release of these tables removes those assumptions entirely:
- Passive network capture → offline cracking
- No brute-force, rate limits, or lockouts
- Minimal expertise required
- Low-cost hardware barrier

This shifts NetNTLMv1 from a *legacy risk* to a **clear security liability**.

---

## Security Impact
Any environment that still permits NetNTLMv1 is exposed to:
- Credential compromise via captured handshakes
- Lateral movement using recovered hashes
- Service account exposure
- Undetectable offline attacks

High-risk scenarios include:
- Flat networks
- Legacy SMB configurations
- Shared or long-lived service accounts
- Environments without enforced SMB signing
- Devices that silently negotiate NTLM fallback

---

## Defensive Actions

### Immediate
- Disable **NTLMv1** entirely
- Enforce **NTLMv2 only**
- Enable and enforce **SMB signing**
- Audit NTLM authentication usage

### Short-Term
- Identify systems still negotiating NTLMv1
- Isolate or replace legacy devices
- Rotate credentials used in NTLM-authenticated sessions

### Long-Term
- Remove NTLM where Kerberos is viable
- Migrate to certificate-based authentication where possible
- Treat NTLM as a deprecated protocol, not a compatibility feature

---

## Governance & Compliance Relevance
This issue directly impacts:
- NIST SP 800-53 (IA, AC)
- Cyber Essentials / CE+
- MITRE ATT&CK (Credential Access, Lateral Movement)
- Enterprise identity and access management policies

Allowing NetNTLMv1 in 2025+ environments should be considered a **policy failure**, not a technical limitation.

---

## Reference
Google Cloud Storage (NetNTLMv1 tables):

https://console.cloud.google.com/storage/browser/net-ntlmv1-tables/tables

