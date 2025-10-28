# 🔒 Prompt Safety & Compliance Checklist

This checklist ensures every prompt meets secure-by-default, compliant, and ethical standards before approval.  
All prompts **must pass** every “Required” item before they can be merged or used in production workflows.

---

## 📋 Metadata

| Field             | Value                 |
| ------------------ | --------------------- |
| **Prompt ID**      | `<prompt-id-here>`    |
| **Prompt Title**   | `<prompt-title-here>` |
| **Author**         | `<author-name>`       |
| **Reviewer(s)**    | `<security-reviewer>`, `<domain-reviewer>` |
| **Date Reviewed**  | `<YYYY-MM-DD>`        |
| **Review Result**  | ✅ Approved / ❌ Rejected / ⚠️ Revision required |

---

## ✅ Security Checklist

> These are mandatory controls to verify that the prompt does not leak data, contain secrets, or violate any internal policies.

| #  | Check                                                                 | Required | Status | Notes |
|----|-----------------------------------------------------------------------|-----------|--------|-------|
| **1** | No hard-coded secrets, keys, or tokens present                     | ✅ | ☐ |  |
| **2** | No real hostnames, IPs, domains, or internal infrastructure identifiers | ✅ | ☐ |  |
| **3** | No personal or sensitive data (PII, PHI, credentials) in examples  | ✅ | ☐ |  |
| **4** | Prompts do not request or encourage data exfiltration              | ✅ | ☐ |  |
| **5** | Output handling is deterministic, non-destructive, and free of bias | ✅ | ☐ |  |
| **6** | Model-specific behaviour documented (temperature, max tokens, etc.) | ✅ | ☐ |  |
| **7** | Clear user intent and expected structure of response defined        | ✅ | ☐ |  |
| **8** | Proper frontmatter fields present and valid (`id`, `tags`, `version`, `safety_reviewed`) | ✅ | ☐ |  |
| **9** | Example inputs and outputs contain only sanitised data             | ✅ | ☐ |  |
| **10** | Licencing/ownership of referenced material is compliant           | ✅ | ☐ |  |

---

## 🧩 Compliance & Governance

> Confirms alignment with external standards (Cyber Essentials+, NIST 800-53) and internal governance.

| #  | Check                                                               | Required | Status | Notes |
|----|---------------------------------------------------------------------|-----------|--------|-------|
| **1** | Prompt aligns with **Cyber Essentials+** and **NIST 800-53** confidentiality principles | ✅ | ☐ |  |
| **2** | Prompt supports **least-privilege** and **minimal disclosure** design | ✅ | ☐ |  |
| **3** | No vendor lock-in or proprietary data dependencies                | ✅ | ☐ |  |
| **4** | Language, tone, and context are appropriate for workplace/public use | ✅ | ☐ |  |
| **5** | Prompt complies with ethical AI guidelines and OpenAI policy      | ✅ | ☐ |  |
| **6** | Legal review (if applicable) completed for publication or public sharing | ⚙️ Optional | ☐ |  |

---

## 🧪 Functional Validation

> Ensures the prompt behaves as intended and produces reproducible, safe outputs.

| #  | Test                                                               | Required | Status | Notes |
|----|--------------------------------------------------------------------|-----------|--------|-------|
| **1** | Prompt runs successfully in test harness / dev LLM endpoint     | ⚙️ Optional | ☐ |  |
| **2** | Outputs match expected structure (as defined in prompt card)    | ✅ | ☐ |  |
| **3** | Determinism validated for low-temperature prompts               | ✅ | ☐ |  |
| **4** | Stress-tested with edge-case inputs                             | ⚙️ Optional | ☐ |  |
| **5** | Version incremented after any material change                   | ✅ | ☐ |  |

---

## 🧭 Reviewer Sign-Off

| Role                  | Name              | Signature / Initials | Date |
|-----------------------|------------------|----------------------|------|
| **Security Reviewer** |                  |                      |      |
| **Domain Reviewer**   |                  |                      |      |
| **Maintainer** _(opt)_|                  |                      |      |

---

## 🗂️ Notes & Actions

Use this section for comments, follow-ups, or known limitations.

- Example: Needs test coverage for Terraform IAM policies.
- Example: Requires approval for public release under Apache 2.0.


---

### ✅ Approval Criteria

A prompt can be marked **`safety_reviewed: true`** in its frontmatter when:

1. All **Required** items above are ✅ checked.  
2. Both reviewers have signed off.  
3. The prompt has been tested for correctness and reproducibility.

---

### 🧠 Reminder

> Prompts are **code** — they can leak data, execute actions, and shape model behaviour.  
> Review them with the same diligence as infrastructure or application code.

---

_Revision 1.0 — 2025-10-28_  
_Maintained by: @safesploit_
