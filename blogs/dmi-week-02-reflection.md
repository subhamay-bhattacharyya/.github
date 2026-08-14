---
layout: default
title: DMI - Week 02 - Success Mindset Assignement
hide_hero: true
---

# DMI - Week 01 - Success Mindset Assignement

**By Subhamay Bhattacharyya**

---

Week 2 hit different.

Coming into this week, I thought I had a decent grasp on how Claude Code and agentic workflows work. Turns out, I was only scratching the surface. This week forced me to confront some uncomfortable truths about how I approach learning new tools and frameworks.

## The MCP Reality Check

The biggest revelation was understanding how MCPs (Model Context Providers) actually work in practice. I've spent years building infrastructure as code, automating deployments, and connecting systems—but MCPs felt abstract until I had to debug why a tool wasn't connecting properly.

What I learned: MCPs aren't just "another integration layer." They're the nervous system between Claude and your actual tools. When something breaks, it's not always obvious which component failed. Is it the MCP server? The permissions? The way Claude is invoking it? 

I spent a solid 2 hours troubleshooting a hook integration last Tuesday. Turns out I had the right MCP installed, but hadn't granted the necessary permissions. Simple fix once I understood it, but that gap between knowing something exists and understanding how it actually works is where the real learning happens.

## Skills Changed My Perspective

Then came Skills. I'd heard about them, but I didn't *get* them until I started building one myself.

A Skill is basically a packaged workflow—your own custom prompt and tools bundled together. Instead of Claude suggesting "use this tool," a Skill says "here's your tool, configured and ready." It removes friction.

Building my first Skill forced me to think differently about problems. Not "how do I get Claude to do this," but "how do I make this repeatable and reliable enough that I'd trust it in production?"

That's a different mindset entirely.

## Subagents: The Delegation Problem

Subagents are where things got really interesting—and uncomfortable.

The concept is straightforward: spawn a specialized agent to handle part of a complex task. But knowing when to spawn a subagent versus handling something yourself? That's not a technical decision. That's a judgment call.

I caught myself trying to force subagents into problems that didn't need them. More power isn't always better. Sometimes you need a scalpel, not a bulldozer.

The honest reflection here: I was chasing complexity because it felt more sophisticated. Subagents should be used strategically, not as a reflex.

## Memory: The Tool That Remembers You

This week I also started seriously using Claude's memory system—saving notes about project context, feedback from previous sessions, and decisions that inform future work.

It felt weird at first. "Why am I writing notes to myself that an AI will read?"

But then something clicked. This isn't about the AI remembering—it's about *you* being intentional about what matters. Memory forces you to articulate the why behind decisions. It makes implicit knowledge explicit.

I wrote a memory file about testing preferences after a conversation where I realized I kept repeating the same feedback about test coverage. Now Claude knows my philosophy without me restating it every session.

## The Challenge: Permissions Paralysis

Permissions have been the most frustrating part of Week 2.

Each tool, each system, each MCP requires explicit permission grants. Security-wise, that's excellent. Practically, it means I've had moments where I couldn't get something to work because I forgot to approve access.

There's a balance between safety and friction. I'm learning that balance doesn't mean lowering security—it means understanding your workflow well enough to anticipate what you'll need.

## The Mindset Shift

Here's what I'm sitting with: I've been a builder for years. I know how to write code, provision infrastructure, automate deployments. But agentic development is different. It's not about how fast you can code—it's about how precisely you can think about delegation, context, and feedback loops.

This week humbled me. Not in a bad way. In a "I have a lot to learn and that's exciting" kind of way.

## The System I'm Implementing

Starting this week, I'm implementing a **Decision Log** habit.

Every time I make a significant choice—whether to use a Skill vs. raw Claude, when to spawn a subagent, how to structure a prompt—I'm jotting down a one-line note in a memory file: what I chose, why I chose it, and what I expected to happen.

At the end of each week, I'll review these decisions and note what actually happened. This creates feedback loops around my judgment calls, not just my technical skills.

I've learned that agentic workflows are as much about training yourself to think differently as they are about training your AI.

## Looking Ahead

Week 3 is going to be about connecting these dots. MCPs, Skills, memory, subagents—they're not separate systems. They're pieces of a workflow.

I'm excited about what's next. That's the right place to be.

---
 
P.S. This is part of DevOps Micro Internship (DMI) Cohort 3 with Agentic AI, led by [Pravin Mishra](https://www.linkedin.com/in/pravin-mishra-aws-trainer/). My progress: <https://dmi.pravinmishra.com/s/subhamay-bhattacharyya.html>