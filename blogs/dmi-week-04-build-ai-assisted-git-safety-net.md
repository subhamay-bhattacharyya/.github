---
layout: default
title: DMI - Week 04 - Building AI-Assisted Git Safety Net
hide_hero: true
---

# DMI - Week 04 - Building Safe AI-Assisted Git Safety Net

**By Subhamay Bhattacharyya**

---

# Building Smarter Git Safety: Why Fixed Rules + AI-Assisted Review Beat Either Alone

When I started Week 4 of the DevOps Micro Internship, I thought the assignment was about Git hooks. By the end, I realized it was really about something deeper: how to combine automation and human judgment to build systems that are both fast *and* intelligent.

## The Problem: One Layer Isn't Enough

Before this week, I had a naive view of security in DevOps: write a rule, enforce it everywhere, call it done. But real security isn't that simple.

Here's what happened: I committed code that *technically* passed my pre-commit hook (no secrets detected, files under 1MB), but I left a debug `echo` statement in the script and forgot to document why I changed the function signature. The hook didn't catch any of that.

I realized I needed two very different kinds of checks working together.

## What I Built: A Two-Layer Safety System

### Layer 1: Fixed Rules (`hooks/pre-commit`)

The pre-commit hook is a deterministic gatekeeper:

```bash
if git diff --cached -- "$file" | grep -qE 'AKIA[0-9A-Z]{16}|-----BEGIN (RSA|OPENSSH|PRIVATE) KEY-----'; then
  echo "BLOCKED: possible secret in $file"
  blocked=1
fi
```

**What it catches:**
- AWS Access Keys (AKIA prefix + 16 alphanumeric characters)
- Private key headers (RSA, OpenSSH, PEM)
- Oversized files (>1MB)

**Why it works:**
- **Speed** — Runs in milliseconds on every commit
- **Reliability** — Pattern matching is deterministic; no false negatives on known formats
- **Shared enforcement** — Tracked in the repo, so every contributor gets the same baseline
- **Stops obvious mistakes** — Prevents accidental credential leaks before they hit the server

**Its limits:**
- Only catches known patterns
- Misses poorly-named variables that store secrets
- Can't understand intent or context
- No semantic analysis

### Layer 2: AI-Assisted Review (`/pr-ready`)

The `/pr-ready` Claude Code skill analyzes staged changes with semantic understanding:

```markdown
1. Inspect staged changes (git diff --cached)
2. Flag semantic issues:
   - Debug statements (console.log, echo, print)
   - TODO/FIXME left in code
   - Mixed concerns (unrelated changes in one commit)
   - Missing documentation
3. Draft PR title and description with context
```

**What it catches:**
- Debug `echo` statements I left in scripts
- Missing change notes in documentation
- Commits that mix refactoring with new features
- Incomplete or unclear change descriptions

**Why it works:**
- **Context-aware** — Understands what "debug statement" means, not just pattern matching
- **Explanatory** — Drafts PR descriptions that explain *why* I changed something
- **Catches what humans forget** — The things that slip past pattern matching
- **Educational** — Shows me issues and suggests improvements

**Its limits:**
- Slower than fixed rules
- Can hallucinate or miss subtle issues
- Requires human judgment to act on
- Not meant to commit or push code

## The Key Insight: Neither Alone Is Enough

Here's what I discovered:

| Aspect | Fixed Rules | AI Review |
|--------|-------------|-----------|
| **Speed** | ⚡ Instant | 🐢 Seconds |
| **Catches patterns** | ✅ Yes | ✅ Yes |
| **Understands context** | ❌ No | ✅ Yes |
| **Can act alone** | ✅ Yes | ❌ No |
| **False positives** | 🟡 Few | 🟡 Some |
| **False negatives** | ⚠️ Many | 🟡 Few |

**The hook** stops obvious disasters fast. **The AI** catches what I forgot to think about. Together, they form a two-layer defense that's better than either alone.

## What I Learned About Automation and Human Judgment

### 1. Fixed Rules Are Speed Bumps, Not Substitutes

The pre-commit hook can't understand intent. It stops patterns, not problems. A poorly-named variable like `api_key = "secret_value"` would slip right through, because it doesn't match `AKIA[0-9A-Z]{16}`.

**Lesson:** Deterministic rules are essential for speed and consistency, but they're incomplete.

### 2. AI Is a Reviewer, Not a Gatekeeper

Claude can analyze my code, spot issues, and suggest improvements—but it shouldn't commit or push on my behalf. Why? Because I'm accountable for what goes into Git.

```bash
# These stay under human control:
git commit   # Only I decide to commit
git push     # Only I decide to push  
gh pr create # Only I open the PR
```

**Lesson:** AI assists; humans decide and act.

### 3. Humans Must Stay in the Loop

When the pre-commit hook flagged my fake AWS key, I decided whether to remove it. When `/pr-ready` flagged my debug echo statement, I decided how to fix it. When the AI drafted my PR description, I reviewed and tweaked it before pushing.

This boundary is critical. It ensures accountability, catches AI mistakes, and prevents automation from running wild.

**Lesson:** The best security systems have humans in them—not because humans are infallible, but because humans are accountable.

### 4. Two Layers Beat One

A system with only the pre-commit hook would pass a commit with:
- No secrets ✅
- No debug statements ❌ (not caught)
- Clear change notes ❌ (not checked)

A system with only AI review would be slow and require manual verification of every commit.

Together, they work: the hook is the fast guard, the AI is the thoughtful reviewer.

**Lesson:** Layered defense catches more than any single layer alone.

## The Bigger Picture: DevOps and Enterprise Reality

This assignment mirrors how real DevOps teams work:

- **Automation** handles the routine: CI/CD pipelines, policy enforcement, pattern detection, infrastructure-as-code validation
- **Humans** handle judgment: code review, architectural decisions, exception handling, accountability
- **Tools** bridge the gap: pre-commit hooks, linters, AI assistants, monitoring alerts

The goal isn't to remove humans from the process. It's to give them better guards, better information, and better tools so they can focus on judgment instead of busywork.

## Takeaways for Building Secure Systems

1. **Combine deterministic rules with intelligent analysis.** Rules catch known patterns fast; intelligence catches context.
2. **Keep humans in the loop for action.** Automation can suggest, but humans must commit, push, and own decisions.
3. **Layer your defenses.** One guard isn't enough; multiple layers catch different kinds of issues.
4. **Make security cheap.** Pre-commit hooks run in milliseconds; if they're expensive, developers will disable them.
5. **Educate as you enforce.** When `/pr-ready` flags an issue, it explains why—so I learn, not just comply.

## What's Next

This week gave me a template for thinking about automation and safety. I'm now looking at:
- How to extend the hook with custom rules for my team
- Using `/pr-ready` as part of a broader PR review workflow
- Documenting security patterns so new contributors understand the why, not just the what

---

## Wrapping Up

Building secure systems isn't about removing humans. It's about giving them better tools, better information, and clear boundaries so they can make better decisions faster.

A fixed rule stops obvious mistakes. An AI catches what you forgot. A human owns the result. Together, they're stronger than any one alone.

---

**Have you thought about combining fixed rules with AI-assisted review in your DevOps workflow? I'd love to hear how you're thinking about automation and human judgment. Drop a comment below.**

#DevOps #GitWorkflow #SecurityEngineering #CICD #ArtificialIntelligence #CloudArchitecture #DMI
P.S. This is part of DevOps Micro Internship (DMI) Cohort 3 with Agentic AI, led by [Pravin Mishra](https://www.linkedin.com/in/pravin-mishra-aws-trainer/). My progress: <https://dmi.pravinmishra.com/s/subhamay-bhattacharyya.html>