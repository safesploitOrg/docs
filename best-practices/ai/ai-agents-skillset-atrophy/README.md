# AI Can Write Code Faster Than I Can Understand It — Here’s My Rule for Fixing That


  - [🧠 1. The Uncomfortable Moment After a Productive AI Session](#key-1-the-uncomfortable-moment-after-a-productive-ai-session)
  - [🧠 2. The Problem: AI Can Create Knowledge Debt](#key-2-the-problem-ai-can-create-knowledge-debt)
  - [🔍 3. Review Is Not the Same as Consolidation](#key-3-review-is-not-the-same-as-consolidation)
  - [🛠️ 4. My Rule: 2 Hours Generation, 1 Hour Consolidation](#key-4-my-rule-2-hours-generation-1-hour-consolidation)
  - [🧩 5. What Counts as Consolidation?](#key-5-what-counts-as-consolidation)
    - [1. Read the Code Manually](#key-1-read-the-code-manually)
    - [2. Run the Tests Yourself](#key-2-run-the-tests-yourself)
    - [3. Modify One Thing Without AI](#key-3-modify-one-thing-without-ai)
    - [4. Document the Architecture in My Own Words](#key-4-document-the-architecture-in-my-own-words)
    - [5. Use AI as a Tutor, Not a Generator](#key-5-use-ai-as-a-tutor-not-a-generator)
  - [✅ 6. The AI Agent Consolidation Checklist](#key-6-the-ai-agent-consolidation-checklist)
  - [⚠️ 7. When AI Writes Infrastructure, “Mostly Understand It” Is Not Good Enough](#key-7-when-ai-writes-infrastructure-mostly-understand-it-is-not-good-enough)
  - [🎯 8. The Portfolio Angle: AI-Assisted Is Fine, AI-Owned Is Not](#key-8-the-portfolio-angle-ai-assisted-is-fine-ai-owned-is-not)
  - [🚩 9. Warning Signs That AI Is Becoming Harmful](#key-9-warning-signs-that-ai-is-becoming-harmful)
  - [🔁 10. A Healthier AI-Agent Workflow](#key-10-a-healthier-ai-agent-workflow)
  - [Final Reflection](#final-reflection)

---

## The TL;DR Version

AI coding agents are useful.

But if the codebase improves faster than your understanding, you create a new problem:

> Knowledge debt.

My current rule is simple:

> For every 2 hours of AI-agent generation, I spend 1 hour manually consolidating the result.

That means reading, testing, documenting, and modifying the code myself before moving on.

AI can accelerate the work.

But I still need to own the result.

---

## 🧠 1. The Uncomfortable Moment After a Productive AI Session

I had a strange moment after spending around 7 hours with Codex modernising an old PHP/MySQL project.

On paper, the session had gone well:

- ✅ the repo was cleaner
- ✅ the architecture was better
- ✅ tests existed
- ✅ CI/CD existed
- ✅ Docker support existed

This was exactly what I wanted.

But there was one uncomfortable problem:

> I did not fully understand what had just been built.

That is the strange part of AI-assisted development.

You can look at your own repository and see progress everywhere, while also feeling a gap underneath it.

```text
Repository progress
      ↓
Cleaner structure
More automation
More tests
Better tooling
      ↓
But weaker ownership
```

That was the moment I realised the real risk was not that AI had written bad code.

The risk was that AI had written useful code before I had properly caught up.

This article is not anti-AI.

The problem is not AI.

The problem is unreviewed acceleration.

If the output grows faster than your understanding, you do not just gain productivity.

**You also create knowledge debt.**

---

## 🧠 2. The Problem: AI Can Create Knowledge Debt

Before AI coding agents, progress was slower.

That was frustrating, but it had one advantage:

> I usually understood most of what I had written, because I had struggled through it manually.

With AI, the relationship changes.

The codebase can improve faster than your understanding.

That creates a new kind of debt:

> AI-generated code can reduce technical debt in the repository while increasing knowledge debt in the engineer.

Knowledge debt looks like this:

|  **Symptom**                           |  **What it means**                       |
|:---------------------------------------|:-----------------------------------------|
| 🐛 I cannot confidently debug it       | I do not understand the failure modes    |
| 🧠 I cannot explain the design         | I do not understand the trade-offs       |
| 🔁 I need AI for every change          | I have become dependent                  |
| 🧪 I do not understand the tests       | I do not know what is actually protected |
| 🎤 I cannot explain it in an interview | It is not portfolio-ready                |

That last point matters.

A portfolio project is only valuable if I can explain it under questioning.

If I cannot describe the architecture, trade-offs, tests, risks, and changes I personally validated, then it is not really my project yet. It is AI-assisted output sitting in my repository.

**That does not mean AI should not be used.**

It means AI usage needs discipline.

---

## 🔍 3. Review Is Not the Same as Consolidation

This is the distinction I had to make:

> Review checks the output.  
> Consolidation protects the engineer.

They are related, but they are not the same thing.

|  **Review asks**                |  **Consolidation asks**                  |
|:--------------------------------|:-----------------------------------------|
| Does this code look acceptable? | Can I work with this code independently? |
| Do the tests pass?              | Do I understand what the tests prove?    |
| Does the diff look reasonable?  | Can I explain why the change works?      |
| Is anything obviously broken?   | Can I debug it without AI?               |
| Can this be merged?             | Do I actually own this?                  |

A review might catch obvious problems.

**Consolidation goes deeper.**

It means manually rebuilding ownership after AI has accelerated the output:

- reading the code properly
- tracing execution paths
- running tests yourself
- modifying something by hand
- documenting the architecture
- explaining what changed without relying on AI

That is the difference.

**Review is quality control.**

**Consolidation is skill protection.**

---

## 🛠️ 4. My Rule: 2 Hours Generation, 1 Hour Consolidation

My current rule is simple:

> For every 2 hours of AI-agent generation, I spend 1 hour manually consolidating the result.

That means if I spend 7 hours using Codex, I owe the project roughly 3 hours of consolidation.

This is not punishment.

It is skill protection.

The goal is not to slow everything down for the sake of it.

The goal is to make sure the speed does not come at the cost of ownership.

The 2:1 ratio gives me enough AI usage to benefit from acceleration, but enough manual work to keep my understanding from falling too far behind.

AI can help me move faster.

But I still need to remain the engineer responsible for the result.

---

## 🧩 5. What Counts as Consolidation?

Consolidation is not passive reading.

It is active ownership.

|  **Step**    |  **What I do**              |  **Why it matters**                             |
|:-------------|:----------------------------|:------------------------------------------------|
| **1**        | Read the code manually      | Understand the actual implementation            |
| **2**        | Run the tests myself        | Understand what is protected                    |
| **3**        | Modify one thing without AI | Prove I can work independently                  |
| **4**        | Document the architecture   | Turn vague understanding into clear explanation |
| **5**        | Use AI as a tutor           | Reduce knowledge debt instead of creating more  |

---

<details>
<summary>Expand on Consolidation</summary>

### 1. Read the Code Manually

The first step is simple, but easy to skip.

Read the code.

Not just the summary.

Not just the AI explanation.

The actual code.

I want to understand:

- what files were added
- what files were modified
- what the new entrypoints are
- what abstractions were introduced
- what assumptions the code makes
- what could break

The goal is to trace at least one full execution path from start to finish.

For example:

```text
Request comes in
   ↓
Route/controller handles it
   ↓
Service layer processes logic
   ↓
Repository/database layer is called
   ↓
Response is returned
```

If I cannot trace the flow, I do not understand the change yet.

---

### 2. Run the Tests Yourself

It is not enough to see that CI passed.

I want to run the tests locally and understand what they actually prove.

Questions I ask:

- What behaviour is protected?
- What behaviour is still untested?
- Are these tests meaningful?
- Are they testing business logic, infrastructure behaviour, or implementation details?
- Could the tests pass while the system is still broken?

This matters because AI can generate tests that look convincing but only prove shallow behaviour.

A passing test suite is useful.

But a test suite I understand is much more valuable.

---

### 3. Modify One Thing Without AI

This is the most important anti-atrophy step.

I force myself to make at least one small manual change.

Examples:

- add one unit test manually
- rename a method and fix references manually
- improve one validation rule
- refactor one function by hand
- adjust a Dockerfile without asking AI
- update a GitHub Actions workflow manually

This proves that I am not just observing the code.

I can actually work with it.

My rule is:

> If I cannot safely modify the code without AI, I do not fully own it yet.

That does not mean I will never use AI again on that project.

It means I should be capable without it.

AI should be acceleration, not dependency.

---

### 4. Document the Architecture in My Own Words

This is where vague understanding becomes clear understanding.

After a large AI-assisted change, I try to write a short explanation of:

- what the old architecture looked like
- what the new architecture looks like
- why the change was made
- how data flows through the system
- where tests and CI/CD fit
- what risks were reduced
- what risks still remain

For example:

```text
Before:
- Logic, database access, and rendering were tightly coupled.
- Testing was difficult because most behaviour depended on direct database access.
- The project had limited separation between application concerns.

After:
- Services handle business logic.
- Repositories handle persistence.
- Tests protect critical behaviours.
- CI/CD validates changes before merge.
- Docker provides a more reproducible development environment.
```

This is especially important for portfolio projects.

If I cannot document it, I probably cannot explain it properly in an interview.

And if I cannot explain it in an interview, the project is not doing its job.

---

### 5. Use AI as a Tutor, Not a Generator

During consolidation, I try not to ask:

> Add the next feature.

Instead, I ask:

> Explain this file line by line.

> What assumptions does this code make?

> Where could this fail?

> What tests are missing?

> What would you ask me in a code review?

That changes the role of AI.

It stops being a code factory and becomes a reviewer, tutor, and sparring partner.

This is where AI becomes very useful for learning.

The same tool that can create knowledge debt can also help reduce it, depending on how it is used.

</details>

---

## ✅ 6. The AI Agent Consolidation Checklist

After a long AI-agent session, I do not want to rely on vibes.

I want a repeatable checklist.

The goal is simple:

> Before I generate more code, I need to prove I understand what was already generated.

```text
## AI Agent Consolidation Checklist

### 🔍 Scope Review
- [ ] I reviewed every file changed by the AI.
- [ ] I understand the purpose of each new file.
- [ ] I understand the main execution flow.
- [ ] I identified any code I do not yet understand.

### 🧪 Test Review
- [ ] I ran the test suite locally.
- [ ] I understand what each test validates.
- [ ] I added or modified at least one test manually.
- [ ] I identified the highest-risk untested behaviour.

### 🛠️ Manual Ownership
- [ ] I made at least one small manual code change.
- [ ] I can explain why the change works.
- [ ] I can revert or debug the change without AI.

### 📝 Documentation
- [ ] I documented the architecture in my own words.
- [ ] I wrote a before/after summary.
- [ ] I updated README or project notes if needed.

### 🎯 Portfolio Readiness
- [ ] I can explain the change in an interview.
- [ ] I can explain what AI helped with.
- [ ] I can explain what I personally reviewed or changed.
- [ ] I can describe what I learned.
```

This checklist is not about slowing AI down for no reason.

It is about converting generated output into owned knowledge.

> AI generation creates output.  
> Human consolidation creates skill.

---

## ⚠️ 7. When AI Writes Infrastructure, “Mostly Understand It” Is Not Good Enough

My principle is simple:

> AI can draft infrastructure and automation, but humans must own the blast radius.

When infrastructure is codified, code review is not just about correctness.

It is about operational safety.

---

This rule matters for application code.

But it matters even more when the “code” changes infrastructure, operating systems, identity, networking, or security controls.

Why?

Because the blast radius changes.

With application code, partial understanding can create:

- 🐛 bugs
- 🔓 weak validation
- 🧪 shallow tests
- 🧱 poor abstractions

That is bad.

But with infrastructure and IT automation, partial understanding can change the environment itself.

```text
AI-generated automation
      ↓
Terraform / Ansible / PowerShell / Bash / Kubernetes / CI/CD
      ↓
Cloud resources, servers, laptops, networks, identities, policies
      ↓
Real infrastructure or OS-level changes
      ↓
Potential production impact
```

That is a very different risk profile.

A bad helper function might break a feature.

A bad infrastructure script might:

- 🌐 expose a private subnet
- 🔥 open the wrong firewall rule
- 🔑 over-permission an IAM role
- 💀 break routing
- 🚀 deploy into the wrong environment
- 🧨 give a pipeline more access than it should have
- 🪟 modify dangerous Windows registry paths
- 💻 remove or corrupt files needed for boot (bricking laptops, desktops, or servers)

For example, imagine asking AI to produce a PowerShell script to harden Windows registry settings.

On the surface, that sounds useful.

But if I do not understand every registry path, service change, permission change, and file operation, that script could move from “hardening” to “breaking the operating system” for thousands of devices very quickly.

```text
AI-generated hardening script
      ↓
Registry / services / permissions / system files
      ↓
Applied across endpoints or servers
      ↓
Boot failure, broken login, disabled services, outage
```

That is why “mostly understood” is not good enough for infrastructure or systems automation.

The minimum standard should be:

> If this code can change infrastructure, identity, networking, security, operating system behaviour, or data access, I need to understand exactly what it does before I run it.

For IaC and IT automation, consolidation is not just a learning exercise.

It is an operational safety control.

> Application code:  
> Can I understand the behaviour?
>
> Infrastructure and systems automation:  
> Can I understand the blast radius?

---

## 🎯 8. The Portfolio Angle: AI-Assisted Is Fine, AI-Owned Is Not

I do not think there is anything wrong with using AI in portfolio projects.

In modern engineering, avoiding AI completely may become unrealistic.

The issue is not whether AI helped.

The issue is whether I still own the result.

There is a big difference between these two positions:

|  **Weak framing**               |  **Strong framing**                                        |
|:--------------------------------|:-----------------------------------------------------------|
| “AI built this for me.”         | “I used AI to accelerate parts of the implementation.”     |
| “I accepted what it generated.” | “I reviewed, tested, modified, and documented the result.” |
| “The project works.”            | “I can explain how and why it works.”                      |
| “I need AI to change it.”       | “I can work on it independently.”                          |

That distinction matters.

Employers may increasingly expect engineers to use AI tools, but they still value:

- judgement
- debugging ability
- architecture understanding
- security awareness
- ownership

A stronger portfolio description would be:

```text
AI-assisted legacy modernisation project.

Used Codex to accelerate scaffolding and refactoring,
while retaining ownership through 
- manual review
- tests
- CI/CD validation
- documentation
- post-generation consolidation
```

That is honest.

It does not pretend AI was not involved.

But it also shows engineering discipline.

**I do not want to hide AI usage.**

**I want to prove that I used it properly.**

---

## 🚩 9. Warning Signs That AI Is Becoming Harmful

AI becomes harmful when it replaces the struggle that creates understanding.

For me, these are the warning signs:

|  **Warning sign**                                      |  **What it suggests**                            |
|:-------------------------------------------------------|:-------------------------------------------------|
| 🚫 I accept code I cannot explain                      | I am trusting output instead of understanding it |
| 🧯 I cannot debug without asking AI                    | I do not understand the failure modes            |
| ➕ I keep adding features instead of reviewing changes | I am stacking knowledge debt                     |
| 🧪 The tests pass, but I do not know what they prove   | I may have false confidence                      |
| 🧱 I cannot draw the architecture from memory          | I do not understand the system shape             |
| 😬 I feel anxious when AI is unavailable               | AI has become a dependency                       |
| 📚 I stop reading documentation                        | I am outsourcing learning                        |
| 🧠 I stop forming my own design opinions               | I am losing engineering judgement                |

That is when AI stops being an accelerator and starts becoming a dependency.

The danger is not that AI makes you productive.

The danger is that it can make you look productive while quietly weakening your understanding.

That is the trap I am trying to avoid.

---

## 🔁 10. A Healthier AI-Agent Workflow

The workflow I am **not aiming for**:

```text
Prompt → accept → prompt again → accept again
```

That is how *knowledge debt* stacks up.

A healthier loop looks like this:

```text
Human defines architecture and constraints
      ↓
AI drafts implementation
      ↓
Human reviews the diff
      ↓
Human runs tests and tools
      ↓
Human manually changes one part
      ↓
Human documents the result
      ↓
AI is used as reviewer / tutor
      ↓
Next generation cycle begins
```

The shorter version:

```text
Design manually
      ↓
Generate selectively
      ↓
Review deeply
      ↓
Test automatically
      ↓
Document clearly
      ↓
Own the result
```

This gives AI a useful place in the workflow.

It is not banned.

It is not blindly trusted.

It is used deliberately.

That is the difference.

---

## Final Reflection

AI agents are not going away.

And honestly, I do not want them to.

They are useful.

They can accelerate boring work, suggest patterns, create tests, explain unfamiliar code, and help modernise old projects faster than I could manually.

But speed has a cost if I do not deliberately consolidate afterwards.

My current rule is simple:

> For every 2 hours of AI-generated progress, I spend 1 hour rebuilding ownership.

That means:

- reading the code
- running the tests
- documenting the architecture
- making at least one manual change
- proving I can explain the result

The goal is not to code slower.

**The goal is to make sure I am still an engineer, not just the person pressing accept.**

AI should accelerate my learning curve, not outsource it.