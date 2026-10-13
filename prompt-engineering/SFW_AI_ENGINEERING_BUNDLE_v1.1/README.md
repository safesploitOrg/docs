# 📊 SFW v1.1 — Engineering Standards Quality Assessment

**Assessment scope:** `SFW_AI_ENGINEERING_STANDARD_v1.1.md` (v1.1.0)

Ratings evaluate the quality, completeness and practical usefulness of the **written standard itself**, not the implementation maturity of projects adopting it. Scores are indicative editorial assessments, not independent certification or verified compliance results.

| Skill / Discipline | Rating | What SFW v1.1 Covers Well | Areas for Further Improvement |
|---|---|---|---|
| 🧭 Requirements & Planning | 8.5/10 | Five-phase engineering workflow, scope identification, acceptance criteria, risk classification and Definition of Done | Formal requirements traceability, acceptance-test mapping and change-impact analysis |
| 🏗️ Software Architecture | 8.5/10 | Separation of concerns, modular design, dependency isolation, interface boundaries, ADRs and architecture documentation | More explicit dependency-direction rules and architecture conformance checks |
| 🧩 Code Quality & Maintainability | 8.5/10 | DRY principles, coding conventions, static analysis, scoped changes, defensive error handling and regression prevention | Language-specific quality thresholds, complexity limits and measurable maintainability criteria |
| 🔐 Security-by-Design | 9/10 | Trust boundaries, least privilege, secure defaults, privacy, input validation, authentication, authorisation, cryptography and SSRF prevention | More explicit security-requirement-to-verification traceability |
| 🎯 Threat Modelling | 8.5/10 | Required T2 threat reviews covering assets, actors, attack surfaces, trust boundaries, abuse cases, controls and residual risk | Standard threat-model template, reassessment triggers and clearer risk-scoring guidance |
| 🧪 Unit Testing | 9/10 | Deterministic tests, positive and negative cases, edge conditions, security boundaries, regression testing and independent reference validation | Quantifiable critical-path coverage expectations and mutation-testing guidance |
| 🔗 Integration Testing | 8.5/10 | Real database/runtime boundaries, authentication, HTTP, filesystem, migrations, dependencies and representative environments | More explicit contract-testing, environment reproducibility and test-data lifecycle guidance |
| 🌐 End-to-End Testing | 9/10 | Critical user journeys, Playwright, negative scenarios, browser matrices, release gates and prohibition of silently disabled tests | Flaky-test management procedures and clearer prioritisation of essential user journeys |
| ♿ Accessibility & Browser Compatibility | 9/10 | Chromium, Firefox, WebKit, representative viewports, axe, keyboard navigation, focus, reduced motion, zoom and WCAG 2.2 AA guidance | More precise accessibility acceptance criteria, manual audit records and real-device test requirements |
| 🔍 Security Testing / SAST | 8.5/10 | SAST, dependency auditing, secret detection, malicious-input tests, fuzzing, security regression tests and scanner enforcement | More explicit DAST/API testing guidance and security-tool coverage validation |
| ⬅️ Shift-Left Security | 9/10 | Threat modelling before implementation, secure coding, local pre-commit checks, CI-aligned checks and early security regression testing | Mandatory traceability between identified threats, preventive controls and automated tests |
| ⚙️ CI/CD Engineering | 9/10 | Automated validation, reproducible dependency installation, testing stages, least-privilege workflows, artifact integrity and controlled deployments | Reference pipeline examples and reusable verification patterns for each project profile |
| 🚦 CI/CD Security Enforcement | 9/10 | Fail-closed gates, severity/exploitability thresholds, vulnerability baselines, blocking findings, exceptions and evidence-based verification | Machine-readable policy examples, automated exception expiry and gate-enforcement test procedures |
| 📦 Software Supply-Chain Security | 8.5/10 | Lockfiles, dependency audits, SBOMs, GitHub Actions pinning, dependency provenance, signing considerations and SLSA references | Stronger requirements for signed provenance, artifact verification and dependency integrity at higher risk tiers |
| 🐳 Containerisation & Runtime Hardening | 7.5/10 | Non-root execution, minimal capabilities, container vulnerability scanning, restricted network exposure and secure runtime principles | Explicit seccomp, read-only filesystems, rootless execution, resource limits, image-digest pinning and runtime security checks |
| 🚀 Release Engineering | 9/10 | Immutable artifact promotion, tested revisions, release approvals, changelogs, deployment checks, rollback and T2 human sign-off | Progressive delivery strategies, rollback rehearsals and explicit promotion between environments |
| 📡 Shift-Right / Observability | 8/10 | Health checks, structured logs, metrics, traces, actionable alerts, security telemetry and operational feedback loops | SLI/SLO definitions, error budgets, alert-quality measures and clearer operational readiness criteria |
| 🚨 Incident Response & Vulnerability Management | 8.5/10 | Vulnerability triage, remediation deadlines, secret rotation, incident feedback, recovery, risk acceptance and security regression prevention | Incident severity classification, communication procedures, evidence preservation and vulnerability disclosure timelines |
| 🤖 AI-Assisted Software Engineering | 9/10 | Structured AI workflows, code inspection, implementation constraints, independent validation, evidence-based reporting and mandatory completion reports | Standardised evidence artifacts, repeatable AI-output evaluation and agent-performance regression testing |
| 🛡️ AI Agent Security & Permissions | 9.5/10 | Prompt-injection resistance, instruction precedence, untrusted-source handling, scoped authorisation, privileged-action restrictions and human approval boundaries | Explicit agent sandboxing, execution audit trails and automated enforcement of tool/action permissions |
| ♻️ Legacy Modernisation & Technical Debt | 9/10 | Legacy baselines, introduced-regression separation, existing risk assessment, time-bounded exceptions, debt ownership and remediation deadlines | Formal technical-debt prioritisation, migration milestones and measurable debt-reduction indicators |
| 📚 Documentation & Knowledge Management | 9/10 | Canonical documentation, AGENTS.md, architecture records, testing guides, SECURITY.md, operations runbooks, changelogs and documentation ownership | Automated documentation validation, link checking, freshness checks and drift detection |
| ⚖️ Engineering Governance & Risk Management | 9/10 | Project profiles, T0–T2 risk tiers, MUST/SHOULD/MAY requirements, exception management, review cycles, release approvals and controlled policy changes | More objective risk-scoring criteria, auditable approval templates and machine-readable governance rules |
| 👥 Code Review & Human Oversight | 8/10 | Human T2 release approval, reviewable changes, branch protection expectations, AI self-approval restrictions and owner-controlled exceptions | Explicit independent-review criteria, CODEOWNERS guidance, reviewer independence and formal review-evidence requirements |

## Overall Assessment

**SFW v1.1 provides a strong, security-focused engineering standard** covering the full software development lifecycle, from requirements and architecture through implementation, verification, release and operational maintenance.

Its strongest areas are security-by-design, AI agent governance, automated testing requirements, CI/CD security enforcement, documentation and risk-based controls.

The most significant opportunities for improvement are container-specific hardening, operational observability, measurable assurance criteria and formal independent-review processes.

**Assessment limitation:** A high rating indicates that the document provides substantial and actionable guidance. It does not establish that any adopting repository satisfies those requirements. Actual compliance must be demonstrated through implementation, execution evidence and enforced controls.

**Interpretation:** SFW v1.1 is an engineering policy, not a complete implementation manual. It deliberately leaves some technology-specific configuration to individual repositories. A score below 10/10 does not necessarily mean a mandatory feature is missing; it may indicate that guidance could be more precise, measurable or operationally useful.
