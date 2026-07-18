# IAM Authentik vs Keycloak


## High-level

- **Authentik** → 🟢 *Modern, flexible, DevSecOps-friendly IdP*
- **Keycloak** → 🔵 *Enterprise IAM standard (heavyweight)*

👉 Both do AuthN + AuthZ, but they optimise for **different scales and complexity levels**.

---

## Side-by-side comparison (core differences)

| **Category**            | **Authentik**                 | **Keycloak**                             |
|:------------------------|:------------------------------|:-----------------------------------------|
| **🎯 Target**           | SMB / homelab / modern infra  | Enterprise / regulated environments      |
| **🧠 Philosophy**       | Simplicity + flexibility      | Completeness + standardisation           |
| **🔐 AuthN**            | Strong (MFA, passkeys, flows) | Strong (battle-tested, enterprise-grade) |
| **🛂 AuthZ**            | Policy-based (coarse)         | **Fine-grained (UMA, resource-based)**   |
| **🔗 Protocols**        | OIDC, SAML, LDAP, RADIUS      | OIDC, SAML, LDAP, Kerberos               |
| **🧩 Customisation**    | Flow builder (visual)         | Deep config (realms, clients, SPI)       |
| **⚙️ Setup complexity** | Moderate                      | **High (steep learning curve)**          |
| **🧱 Architecture**     | Lightweight/modular           | Heavy, Java-based                        |
| **📈 Scalability**      | Good (SMB–mid)                | **Excellent (enterprise scale)**         |
| **🧑‍🤝‍🧑 Community**        | Growing                       | **Large, mature (Red Hat/CNCF)**         |
| **🧪 UX/Admin UI**      | Modern, clean                 | Functional but dated                     |