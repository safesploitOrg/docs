---
description: Designing Active Directory so that a compromised
  workstation and stolen privileged authentication material do not
  automatically become a path to Domain Controller compromise.
published: false
tags: activedirectory, cybersecurity, windows, security
title: "A Domain Admin Password Shouldn't Be Enough: Hardening Active
  Directory Tier 0"
---

# A Domain Admin Password Shouldn't Be Enough: Hardening Active Directory Tier 0

If an attacker compromises an IT workstation, obtains `SYSTEM`, steals a
Domain Admin password, or extracts a valid **Kerberos TGT**...

**should that automatically mean the Domain Controllers are compromised
too?**

In many environments, the practical answer can be:

> **Yes.**

Not simply because the credential was stolen, but because the
compromised endpoint may also have the network path required to use it
against Tier 0.

This article explores a deliberately pessimistic design assumption:

> **Assume the privileged credential is eventually compromised. Design
> the environment so that the credential alone is still insufficient to
> administer Tier 0.**

The objective is simple:

> **A stolen Domain Admin password or Kerberos TGT should not be
> sufficient to turn compromise of `IT-WS01` into compromise of the
> Domain Controllers.**

------------------------------------------------------------------------

## 1. The Problem: When Domain Admin Means Game Over

Consider `IT-WS01`: an ordinary IT workstation with Internet access.

Now assume the workstation is compromised.

<p align="center">
  <img src="https://raw.githubusercontent.com/safesploitOrg/assets/90bfb8f6c2ce17cc6d4c27b6ffb98e5331fb6909/repo/dev.to/ad-tier0-hardening/ad_tier0_hardening.png" alt="Ad Tier0 Hardening" width="800">
</p>

``` text
              IT-WS01
        (COMPROMISED \SYSTEM)
                  │
                  ▼
       DA password / DA TGT
               STOLEN
                  │
                  ▼
        Domain Controller
            COMPROMISED
                  │
                  ▼
      💥 TIER-0 COMPROMISE
```

The problem is not simply that a Domain Admin credential has been
stolen.

The problem is that the compromised endpoint may possess all three
properties required to turn credential theft into Tier-0 compromise:

``` text
Internet-capable endpoint       ✅
Privileged auth material        ✅
DC administrative reachability  ✅

                │
                ▼
      💥 Dangerous combination
```

If malware reaches `SYSTEM`, obtains reusable privileged authentication
material, and can directly reach administrative interfaces on a Domain
Controller, there may be very little separating workstation compromise
from Tier-0 compromise.

So the architecture needs to break that chain.

------------------------------------------------------------------------

## 2. Threat Model: Assume IT-WS01 Is Already Compromised

Instead of beginning with:

> How do we stop `IT-WS01` from ever being compromised?

Start with the worse scenario:

> **Assume we have already lost it.**

Give the attacker almost everything:

``` text
IT-WS01 compromised        ✅
Local SYSTEM               ✅
DA password stolen         ✅
Valid DA Kerberos TGT      ✅
```

Then ask one question:

> **Can the attacker turn those facts into remote administrative
> execution on a Domain Controller?**

The architectural objective is:

``` text
NO
```

This changes the problem considerably.

We are no longer relying solely on password secrecy, endpoint protection
or MFA.

We are asking whether **other independent boundaries survive after
credential compromise**.

------------------------------------------------------------------------

## 3. The Architecture

The proposed model separates normal Active Directory use from Tier-0
administration.

``` text
                     ┌──────────────────────┐
                     │      IT-WS01         │
                     │                      │
                     │ MFA / device policy  │
                     └──────────┬───────────┘
                                │
══════════════ TIER-0 SECURITY BOUNDARY ══════════════
                                │
                     ┌──────────▼───────────┐
                     │   T0-DC-BASTION      │
                     │                      │
                     │  NOT Domain-joined   │
                     │                      │
                     │ Internet ❌          │
                     │ Email    ❌          │
                     │ Admin    ✅          │
                     └──────────┬───────────┘
                                │
                           🔥 Firewall
                                │
                         Admin protocols
                                │
                                ▼
                       ┌────────────────┐
                       │ Domain         │
                       │ Controllers    │
                       └────────────────┘
                                ▲
                                │
                       Required AD services
                                │
                ┌───────────────┴──────────────┐
                │                              │
             IT-WS01                        Servers
           DC Admin ❌                    DC Admin ❌
```

The key idea is not to isolate the Domain Controllers from everything.

Domain members still need Active Directory.

The goal is to isolate **administration of Active Directory**.

> **Using Active Directory is not the same thing as administering Active
> Directory.**

------------------------------------------------------------------------

## 4. Using Active Directory Is Not Administering Active Directory

A domain workstation needs to communicate with Domain Controllers.

Depending on the environment, that can include:

-   DNS
-   Kerberos
-   LDAP / DC Locator
-   SYSVOL / NETLOGON
-   required RPC
-   other explicitly required AD services

What an ordinary workstation does **not** inherently require is
unrestricted remote administration of the Domain Controllers.

The desired distinction is:

``` text
Use Active Directory            ✅
Administer Domain Controllers   ❌
```

A simplified network policy therefore looks more like this:

```
  Traffic                Lower tier → DC
  ---------------------- -----------------
  DNS                    ✅ Allow
  Kerberos               ✅ Allow
  LDAP / DC Locator      ✅ Allow
  SYSVOL / NETLOGON      ✅ Allow
  Required RPC           ⚠️ Validate
  RDP administration     ❌ Deny
  WinRM administration   ❌ Deny
  Tier-0 management      ❌ Deny
```

The firewall should not prevent clients from using Active Directory.

It should help separate **using Active Directory from administering
Active Directory**.

------------------------------------------------------------------------

## 5. Identity Is Not the Same as Network Access

A common failure in privileged-access design is allowing several
separate security concepts to collapse into one:

``` text
"Has Domain Admin credentials"
```

But these are different controls:

``` text
Identity
   │
   ├── Who are you?
   │
Authentication material
   │
   ├── Can you prove it?
   │
Administrative workstation
   │
   ├── Where are you connecting from?
   │
Bastion
   │
   ├── Where does administration execute?
   │
Network policy
   │
   ├── Can this system reach the target?
   │
Domain Controller
   │
   └── What are you administering?
```

An attacker possessing a Domain Admin password has compromised an
important security boundary.

An attacker possessing a valid Domain Admin TGT has compromised another.

Neither fact should automatically create an administrative network path
from `IT-WS01` to a Domain Controller.

This is the core idea:

> **A privileged identity should be one requirement for Tier-0
> administration --- not the entire Tier-0 security boundary.**

------------------------------------------------------------------------

## 6. Why MFA Alone Isn't Enough

MFA remains extremely important, but it protects a particular part of
the authentication process.

A simplified flow might look like:

``` text
Password + MFA
      │
      ▼
Authentication
      │
      ▼
Kerberos TGT
      │
      ▼
Service tickets
```

Once reusable authentication material exists, subsequent
Kerberos-authenticated operations do not necessarily replay the original
MFA ceremony.

In other words:

``` text
MFA on RDP
     ≠
MFA on every subsequent
Kerberos operation
```

That distinction matters when the endpoint itself is compromised.

An attacker may not need to interactively RDP into a Domain Controller.

Other administrative mechanisms can exist, including combinations of
SMB, RPC, WMI or WinRM.

So:

> **MFA should be part of the Tier-0 architecture, but it should not be
> the Tier-0 architecture.**

------------------------------------------------------------------------

## 7. The SMB and RPC Problem

This is where firewall design becomes more complicated.

Take TCP/445.

A workstation may legitimately need SMB access to a Domain Controller
for:

``` text
SYSVOL
NETLOGON
```

But administrative activity can also use SMB:

``` text
C$
ADMIN$
```

From the network firewall's perspective, both can simply be:

``` text
TCP/445
```

Similarly, RPC supports legitimate Windows and Active Directory
operations while also participating in powerful remote-management
workflows.

So a simple rule such as:

``` text
Workstations → DC TCP/445 = ALLOW
```

does not express the security intent by itself.

And simply blocking every protocol used for administration may break
legitimate domain functionality.

The answer is defence in depth:

``` text
Network policy
      +
Host firewall
      +
Identity restrictions
      +
Authentication policy
      +
Administrative tiering
```

The firewall is an important boundary.

It is not the only boundary.

------------------------------------------------------------------------

## 8. Keep Tier-0 Credentials Out of Lower Tiers

The threat model deliberately assumes a DA credential or TGT has been
stolen from `IT-WS01`.

But the architecture should also make that situation much harder to
create in the first place.

Administrative identities should be separated by purpose and tier.

For example:

``` text
alice
│
├── alice
│     Standard user
│
├── alice-ws-admin
│     Workstation administration
│
├── alice-srv-admin
│     Server administration
│
└── alice-t0
      Tier-0 administration
```

The intended direction is:

``` text
Tier-0 credential
       │
       ▼
    Tier 0             ✅
```

Not:

``` text
Tier-0 credential
       │
       ▼
Internet-capable
workstation             ❌
```

This also changes how endpoint elevation should be approached.

A pattern such as:

``` text
Download software
       │
       ▼
   UAC prompt
       │
       ▼
Enter Domain Admin
credentials
```

places Tier-0 authentication material onto a lower-trust endpoint.

Workstation administration should instead use controls appropriate to
that tier: dedicated workstation-administrator identities, LAPS where
appropriate, endpoint privilege management, controlled software
deployment and application control.

Most importantly, the policy should not merely be:

> "Administrators should remember not to use Domain Admin here."

Where practical, the enforced rule should be:

> **Domain Admin cannot authenticate here.**

Authentication Policies, Authentication Policy Silos, logon restrictions
and related controls can help enforce that boundary.

------------------------------------------------------------------------

## 9. Why the Bastion Has Its Own Trust Boundary

A hardened domain-joined Tier-0 administrative workstation can be a
valid design.

This architecture deliberately adds another separation:

> **Production Active Directory is not the authority controlling entry
> into the Tier-0 bastion.**

Conceptually:

``` text
Independent authentication
          │
          ▼
      T0-BASTION
          │
          ▼
Production Active Directory
```

That creates an important security property.

If an attacker steals production AD authentication material:

``` text
DA password stolen             ✅
DA Kerberos TGT stolen         ✅

Authenticate to T0-BASTION?    ❌
```

The credential that has been compromised is not automatically the
credential required to cross the administrative ingress boundary.

However:

> **Non-domain-joined does not mean secure.**

A bastion capable of administering Domain Controllers is itself
effectively a Tier-0 asset.

It therefore needs controls appropriate to that trust level: strong
authentication, MFA, patching, endpoint protection, application control,
logging, configuration management, restricted networking, secrets
management and tested recovery.

The useful security property comes from the **independent trust
boundary**, not simply from removing the machine from the production
domain.

------------------------------------------------------------------------

## 10. Replay the Attack

Now return to the attack from Section 1.

We deliberately give the attacker everything assumed in the threat
model:

``` text
IT-WS01 compromised       ✅
SYSTEM                    ✅
DA password               ✅
DA Kerberos TGT           ✅
```

In the original model, the attack path might look like:

``` text
IT-WS01
   │
   ▼
SYSTEM
   │
   ▼
DA password / TGT
   │
   ▼
Administrative path to DC
   │
   ▼
Remote execution
   │
   ▼
💥 Tier-0 compromise
```

Now replay it against the hardened architecture:

``` text
              IT-WS01
        (COMPROMISED \SYSTEM)
                  │
                  ▼
       DA password / DA TGT
               STOLEN
                  │
                  ▼
          TIER-0 BOUNDARY
                  │
                  ❌
                  │
               BLOCKED
```

Why?

``` text
Tier-0 credential should exist on IT-WS01?  ❌
Tier-0 identity allowed to log on there?    ❌
Direct RDP path to DC?                      ❌
Direct WinRM path to DC?                    ❌
General DC administrative path?             ❌
Production AD credential unlocks bastion?   ❌
```

The attacker has compromised the privileged identity.

That is serious.

But they have **not automatically compromised every other boundary
around Tier 0**.

------------------------------------------------------------------------

## 11. Prove the Controls Work

Architecture diagrams are useful.

Failed attack attempts are better.

The design should be validated from the perspective of an attacker.

  -----------------------------------------------------------------------
  Attempt                             Security result
  ----------------------------------- -----------------------------------
  `IT-WS01` + DA password → DC        🛡️ BLOCKED
  administration                      

  `IT-WS01` + stolen DA TGT → DC      🛡️ BLOCKED
  administration                      

  Production AD identity →            🛡️ BLOCKED
  `T0-BASTION`                        

  Approved Tier-0 environment →       ✅ ALLOWED
  approved DC administration          
  -----------------------------------------------------------------------

The most important test can be reduced to one question:

> **Assume I completely own a domain workstation and possess a valid
> Domain Admin TGT. Can I turn those two facts into remote code
> execution on a Domain Controller?**

The architectural objective is still:

``` text
NO
```

Testing should also verify that normal domain functionality continues to
work.

A security design that successfully protects the Domain Controllers by
breaking authentication, Group Policy or other required domain
functionality is not a successful design.

------------------------------------------------------------------------

## 12. The End State

The original problem is the concentration of several dangerous
properties on the same endpoint.

### Before

``` text
IT-WS01

Internet access                 ✅
DA/TGT                          ✅
DC administrative reachability  ✅

                 │
                 ▼
       💥 TIER-0 COMPROMISE
```

The proposed architecture separates those properties.

### After

``` text
IT-WS01          T0-BASTION           DC
────────         ──────────           ────────
Internet ✅      Internet ❌          Internet ❌
DA/TGT ❌        DA use ✅            Tier-0 ✅
DC admin ❌      DC admin ✅          Admin target
```

That separation matters.

Compromising `IT-WS01` no longer automatically provides Tier-0
credentials.

Possessing production AD authentication material does not automatically
provide access to the bastion.

And ordinary production systems do not have the same administrative
network path to the Domain Controllers as the Tier-0 environment.

------------------------------------------------------------------------

## Conclusion

The goal is not to make Domain Admin compromise harmless.

A stolen Domain Admin password or Kerberos TGT remains a serious
incident requiring containment, credential revocation or rotation,
investigation and recovery.

The goal is to stop this:

``` text
Domain Admin compromised
           =
Domain Controllers compromised
```

Instead, Tier-0 administration should require multiple independent
conditions:

``` text
Privileged identity
        +
Approved authentication origin
        +
Trusted Tier-0 environment
        +
Independent administrative ingress
        +
Permitted network path
        =
Tier-0 administration
```

If `IT-WS01` is completely compromised and an attacker steals a valid
Domain Admin TGT, another boundary should still stand between that
compromise and administrative execution on a Domain Controller.

That is the security property this architecture is designed to create:

> **Do not make possession of a privileged identity equivalent to
> possession of Tier 0.**
