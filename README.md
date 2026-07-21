# 📚 safesploitOrg / docs

A **public** documentation hub for the `safesploitOrg` ecosystem — containing design decisions, best practices, runbooks (public-safe), and cross-repo knowledge.  
This is the **"why" and "how"** behind projects, without exposing sensitive implementation details.

---

## 📖 Purpose

This repository exists to:

- Provide a **single source of truth** for project knowledge and design context.
- Maintain **cross-repo documentation** for workflows that span Terraform, Ansible, Kubernetes, security tooling, and more.
- Share **public-safe best practices** and compliance mappings for DevSecOps, cloud, and infrastructure.
- Act as the **onboarding hub** for contributors and collaborators.

> 💡 **Rule:** If it explains, justifies, or guides — but is not directly deployable code — it belongs here.

---

## 🗂 Repository Structure

```txt
docs/
├── .github/workflows/
├── architecture/              # High-level diagrams (redacted)
├── assets/                    # Images/diagrams (no secrets in images)
├── best-practices/            # Org-wide patterns (Terraform, Ansible, CI/CD)
├── compliance/                # NIST/Cyber Essentials+ mappings (sanitised)
├── guides/                    # How-tos & walkthroughs
├── postmortems/               # Public-safe lessons learned
├── repo/                      # One page per code repo (public summary)
│   ├── homelab/               # safesploitOrg/homelab prompt path
│   ├── ansible-configs.md
│   ├── terraform-configs.md
│   └── <more>.md
├── runbooks/                  # Manual/ops procedures (public-safe only)
├── security/                  # Security baselines (no sensitive detail)
├── templates/                 # Re-usable doc templates
└── README.md
```
