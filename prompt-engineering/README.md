# 🧠 Prompt Engineering

This section defines how designs, tests, and governs prompts for AI-assisted workflows.  
It is intended for internal, automation, and writers contributing to prompt libraries used across DevSecOps, Infrastructure, and Documentation pipelines.

---

## 📘 Purpose

Prompt engineering is treated as **infrastructure-as-text** — prompts are versioned, peer-reviewed, and subject to the same quality and security controls as code.

Goals:
- Build a **reproducible prompt library** (for code, documentation, and automation use).
- Establish **consistent patterns** for clarity, safety, and reusability.
- Encourage **secure-by-default** design — no data leakage, no exposure of secrets.

---

## 📂 Folder Structure

```ini
prompt-engineering/
├── README.md     # This file
├── guides/       # How-tos and design/evaluation guides
├── templates/    # Prompt card templates and checklists
└── examples/     # Demonstrations of prompt workflows
```


### Folder purposes

| Folder | Description |
|--------|--------------|
| **library/** | Production-ready prompts reviewed and approved for use in workflows and automation pipelines. |
| **guides/** | Walkthroughs explaining prompt-design techniques, testing methods, and quality assurance. |
| **templates/** | Standard templates and governance checklists for new prompt submissions. |
| **examples/** | Example prompts and workflows showing chaining, RAG, or evaluation setups. |

---

## 🧩 Prompt Card Specification

Every prompt file must include **YAML frontmatter** at the top followed by markdown content.  
A standard template lives in [`templates/prompt-card-template.md`](../prompt-engineering/templates/prompt-card-template.md).

**Required frontmatter fields:**

| Field | Purpose |
|-------|----------|
| `title` | Human-readable title of the prompt |
| `id` | Unique identifier (`<topic>-<purpose>-vX`) |
| `intent` | Short summary of what the prompt is meant to achieve |
| `tags` | Searchable keywords (e.g. `terraform`, `security`, `ci/cd`) |
| `author` / `owner` | Who wrote and maintains it |
| `model` | Model family it was tested against (e.g. `gpt-5`, `claude-3`, etc.) |
| `temperature` / `max_tokens` | Key model parameters |
| `version` | Semantic version of the prompt |
| `last_reviewed` | ISO date of last validation |
| `safety_reviewed` | `true` or `false` — must be `true` before use in production |

---

## 🔒 Security & Compliance Guidelines

Prompt engineering follows the same rules as code and infrastructure:

1. **Never embed secrets or real data** in prompt examples.  
   - Use `<PLACEHOLDER>` or `<REDACTED>` markers.
2. **Avoid PII, internal hostnames, or system identifiers.**
3. **No prompts should exfiltrate data** or query live environments.
4. **Review every prompt** for:
   - Output correctness and determinism  
   - Data handling (no unintended exposure)  
   - Bias and tone alignment  
   - Model-agnostic performance
5. **All prompts must pass the security checklist** in [`templates/safety-checklist.md`](../prompt-engineering/templates/safety-checklist.md).

---

