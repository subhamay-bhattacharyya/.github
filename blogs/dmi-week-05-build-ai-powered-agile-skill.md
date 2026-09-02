---
layout: default
title: DMI - Week 05 - Building an AI-Powered Agile Skill
hide_hero: true
---

# DMI - Week 05 - Building an AI-Powered Agile Skill

**By Subhamay Bhattacharyya**

---
## Introduction

After 19 years building data pipelines, cloud infrastructure, and DevOps tooling, I thought I understood automation. But a recent assignment—building a read-only Jira sprint-health skill using Claude Code and Model Context Protocol (MCP)—taught me something unexpected: **The most powerful automation is the kind that respects human agency.**

This isn't a technical how-to. It's a reflection on why DevOps and Agile are converging in ways that demand we rethink what "automation" actually means.

---

## The Assignment: Sprint Health Reporting

The task was straightforward on the surface:

- Use Jira MCP to read the current active sprint
- Gather issue data (status, story points, assignee, last update)
- Analyze: Calculate velocity, identify at-risk stories, flag missing estimates
- Report findings in a structured way
- Do not modify the board

But here's where it got interesting: **The skill had an explicit constraint—it was read-only by design.**

No create, update, transition, or comment operations. The Scrum Master would never auto-transition a story or add a comment on behalf of the team. The data surfaced would inform decisions, but the decisions remained human.

---

## Why This Matters: The Scrum Master's Paradox

For the first time, I deeply understood why a Scrum Master needs tighter restrictions than almost any other role:

**A Scrum Master's job is facilitation, not execution.**

If I could build a tool that automatically transitioned stories based on elapsed time, or flagged blockers and auto-commented on them, I'd be faster—but I'd destroy team autonomy. I'd be optimizing for speed while breaking the team's self-organization.

This isn't a limitation of my tooling. It's a feature of healthy Agile practice.

---

## The Technical Insight: MCP as a Translation Layer

Building this skill revealed something elegant about the Model Context Protocol:

MCP abstracts away the implementation language. Whether the server is written in Node.js (running via `npx`) or Python (running via `uvx`), Claude Code doesn't care. The protocol defines a standardized interface—tools, resources, and capabilities—that any language can implement.

This matters because **DevOps teams don't speak one language**. We use Go for CLI tools, Python for data processing, JavaScript for orchestration, Terraform for infrastructure. MCP lets these polyglot environments communicate through a common interface.

But more importantly: **The protocol enforces constraints at the interface level, not at runtime.** By declaring certain tools as "allowed" and others as forbidden, we're saying "here's what this AI can do" without relying on the AI to honor a verbal instruction.

This is security through architecture, not through trust.

---

## The Bigger Picture: Gather → Analyze → Human Act → Verify

The assignment mapped to a four-phase framework that I now see everywhere:

1. **Gather** (Automated) - Collect data from systems of record
2. **Analyze** (Automated) - Process and synthesize patterns
3. **Human Act** (Manual) - Decide and execute based on the analysis
4. **Verify** (Manual/Automated) - Confirm outcomes

The temptation in DevOps is to push "Human Act" into automation—to eliminate the human from the loop entirely. Pipeline broke? Auto-rollback. Threshold exceeded? Auto-scale. Deployment failed? Auto-retry.

Sometimes that's right. But not always.

When the decision carries organizational or team consequences, the human phase needs to stay human. Not because humans are smarter at any given decision (they're often not), but because **accountability and ownership require human agency.**

A team that doesn't consciously choose to transition their own stories doesn't learn. A Scrum Master who doesn't raise blockers in standups doesn't coach. A DevOps engineer who doesn't review logs after an auto-remediation doesn't build judgment.

---

## Lessons for My Career in DevOps

This assignment surfaced three truths I'll carry forward:

### 1. **Observability First, Automation Second**

In my data engineering days, I built ETL pipelines that ran autonomously. In cloud infrastructure, I've built self-healing systems. But I've learned that the most impactful work isn't the fastest automation—it's the visibility that lets humans make better decisions faster.

A sprint-health report isn't as flashy as an auto-resolving incident. But it's more valuable because it assumes the team is competent and just needs better information.

### 2. **Constraints Enable Trust**

I've historically thought of constraints as technical limitations to work around. But designing constraints into tools—especially when building AI-powered workflows—is an act of respect.

When I tell someone "Claude can read your Jira board but cannot transition issues," I'm not hobbling the tool. I'm signaling: "I trust your team to own their own work. This tool is here to help you see better, not to replace your judgment."

This feels especially important in the age of AI. Every AI tool should declare its constraints upfront.

### 3. **DevOps and Agile Are Converging Around Feedback Loops**

DevOps has always been about tightening feedback loops—deploy faster, observe better, learn quicker. Agile is fundamentally the same: shorter sprints, more feedback, continuous adaptation.

When you combine them—when you use DevOps observability to feed Agile decision-making—you get something powerful: **Teams that learn at scale.**

The sprint-health skill is a tiny example, but it illustrates the pattern: automate the gather and analyze phases, then intentionally keep the decide-and-act phase human-driven, with clear feedback loops so the team improves over time.

---

## What's Next

I'm completing the DevOps Micro Internship (DMI) Cohort 3, and this assignment has shifted how I think about building tools. I'm more interested now in:

- Building observability layers that surface the right questions
- Designing interfaces that respect team autonomy
- Using AI not to replace human judgment, but to sharpen it
- Creating feedback loops that let teams learn from their decisions

The future of DevOps isn't full automation. It's *augmented* teams—humans with better information, clearer constraints, and stronger feedback loops.

---

## For Fellow DevOps Engineers

If you're building tools for Agile teams, ask yourself these questions:

- **Does this automate a decision, or does it inform one?** If it's the former, who's accountable when it goes wrong?
- **What happens if the human says no?** If your tool doesn't respect the possibility of human override, it's not a tool—it's a tyrant.
- **Does this make my team smarter or just faster?** Speed without learning is brittle.

The best DevOps tooling I've built hasn't been the fastest. It's been the kind that made my teams more autonomous, more accountable, and more capable of learning from their choices.

That's the measure I'm adopting going forward.

---

## Acknowledgments

Thanks to **Pravin Mishra** and the DMI Cohort 3 program for assignments that challenge assumptions rather than just checking boxes. The sprint-health skill forced me to think deeper about what automation is *for*, not just how to build it faster.

---

**Have you thought about combining fixed rules with AI-assisted review in your DevOps workflow? I'd love to hear how you're thinking about automation and human judgment. Drop a comment below.**

#DevOps #GitWorkflow #SecurityEngineering #CICD #ArtificialIntelligence #CloudArchitecture #DMI
P.S. This is part of DevOps Micro Internship (DMI) Cohort 3 with Agentic AI, led by [Pravin Mishra](https://www.linkedin.com/in/pravin-mishra-aws-trainer/). My progress: <https://dmi.pravinmishra.com/s/subhamay-bhattacharyya.html>