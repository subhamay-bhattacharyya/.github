---
layout: default
title: DMI - Week 03 - Building Safe AI-Assisted Incident Response: Linux Triage with Claude and Bash
hide_hero: true
---

# Building Safe AI-Assisted Incident Response: Linux Triage with Claude and Bash

**By Subhamay Bhattacharyya**

---

## Introduction

As DevOps engineers, we increasingly have access to powerful AI tools that can analyze system state, diagnose problems, and recommend solutions in seconds. But speed comes with a responsibility: ensuring that AI amplifies human capability without removing human control over production systems.

This post documents a hands-on project from the DevOps Micro Internship (DMI) that demonstrates the proper way to integrate AI into incident response workflows. I built a Bash-based health-check script combined with a Claude Code skill, then intentionally simulated an outage to test the complete incident lifecycle: **Gather → Analyze → Human Approve → Verify**.

The key lesson? **AI should diagnose and recommend, but humans must decide and act.**

---

## What We Built

### 1. Bash-Based Health-Check Script

A modular Bash script that performs automated health checks on a Linux system:

```bash
# Example health check structure
check_nginx_process() {
  ps aux | grep nginx | grep -v grep > /dev/null
  if [ $? -eq 0 ]; then
    echo "HEALTHY"
  else
    echo "FAIL"
  fi
}

check_port_80() {
  netstat -tuln | grep :80 | grep LISTEN > /dev/null
  if [ $? -eq 0 ]; then
    echo "HEALTHY"
  else
    echo "FAIL"
  fi
}

check_http_response() {
  curl -s http://localhost > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "HEALTHY"
  else
    echo "FAIL"
  fi
}
```

The script collects raw evidence about system state — nothing more, nothing less.

### 2. Claude Code Skill

A read-only Claude Code skill configured to:

- **Gather:** Execute bash health checks without modification permissions
- **Analyze:** Interpret the evidence and determine system health status
- **Recommend:** Suggest recovery actions based on the diagnosis
- **Guide:** Explain findings in human-readable language

Key configuration:
- `disable-model-invocation: true` — prevents external API calls, keeps analysis local
- Bash + Read + Grep permissions only — no Write, no system modification
- Evidence-driven only — makes recommendations based on facts, not speculation

---

## The Incident Simulation

### Scenario: Nginx Service Stops

**Objective:** Demonstrate the complete incident response workflow by simulating a critical failure.

**Action:** Stop the Nginx service on a lab Ubuntu VM running the DMI Leaderboard application.

```bash
sudo systemctl stop nginx
```

This simulates a real-world outage where the web server becomes unavailable to users.

---

## The Workflow Demonstrated

### Phase 1: Gather Evidence

Bash executes health checks to collect factual data about system state:

**Check 1: Is the Nginx process running?**
```bash
ps aux | grep nginx | grep -v grep
```
**Result:** No process found → FAIL

**Check 2: Is port 80 listening?**
```bash
netstat -tuln | grep :80
```
**Result:** Port 80 not in LISTEN state → FAIL

**Check 3: Can we connect via HTTP?**
```bash
curl http://localhost
```
**Result:** Connection refused → FAIL

**Check 4: What does systemctl report?**
```bash
systemctl status nginx
```
**Result:** Service inactive (dead) → FAIL

**Evidence gathered:** Four independent checks all indicate Nginx is unavailable.

### Phase 2: AI Analysis

Claude examines the evidence and synthesizes a diagnosis:

**Observations:**
- The Nginx process is completely absent — indicates a clean stop, not a crash
- Port 80 shows no listening service — consistent with deliberate shutdown
- HTTP connections are refused — no service is accepting traffic
- systemctl status shows "inactive" — standard state after `systemctl stop`
- No error messages or resource constraints detected

**Root Cause Diagnosis:** Nginx was intentionally stopped via systemctl.

**Confidence Level:** Very high — all four independent checks support the same conclusion.

### Phase 3: Human-Approved Recovery

Claude recommends the recovery command:

```bash
sudo systemctl start nginx
```

**Our Action:** We reviewed this command carefully, understood its implications, and **manually executed it ourselves**.

Why did we not let Claude execute it automatically? Because:
- Production changes require human judgment and accountability
- The human understands business context, timing, and dependencies that AI cannot fully evaluate
- Automatic execution could mask underlying problems or cause cascading failures
- Humans must retain control over critical infrastructure modifications

### Phase 4: Verification

Bash re-executes all health checks to confirm recovery:

**Check 1: Is the Nginx process running?**
```bash
ps aux | grep nginx
```
**Result:** Nginx master and worker processes found → HEALTHY

**Check 2: Is port 80 listening?**
```bash
netstat -tuln | grep :80
```
**Result:** Port 80 in LISTEN state bound to Nginx → HEALTHY

**Check 3: Can we connect via HTTP?**
```bash
curl http://localhost
```
**Result:** HTML content returned successfully → HEALTHY

**Check 4: What does systemctl report?**
```bash
systemctl status nginx
```
**Result:** Service active (running) → HEALTHY

**Overall Status:** All checks passed → System HEALTHY

---

## The Critical Lesson: Why Humans Must Retain Control

This assignment highlighted a crucial principle that every DevOps engineer should understand:

### The Danger of Unrestricted AI Automation

If we allowed AI to automatically restart every failed service, several dangerous scenarios could occur:

#### 1. **Masking Real Problems**

A service might fail because of:
- A security breach that's actively destroying data
- Corrupted configuration files
- Database integrity issues
- Upstream service failures

Automatically restarting the service hides the symptom without treating the disease. The real problem persists and could cause further damage.

#### 2. **Interrupting Planned Maintenance**

An operations engineer might have deliberately stopped Nginx to:
- Apply security patches
- Rebuild configuration
- Migrate data
- Upgrade dependencies

Automatic restart would disrupt this planned work and potentially cause data loss or corruption.

#### 3. **Cascading Failures**

Restarting one service could trigger failures in dependent services:
- If Nginx restarts while a database migration is in progress, active transactions could be corrupted
- If load balancing is improperly configured, restarting a service could overwhelm other nodes
- If upstream API services are unhealthy, restarting a dependent service could amplify failures

#### 4. **Denial of Service Attacks**

An attacker could exploit automatic restart logic by:
- Triggering false health check failures repeatedly
- Causing rapid service restarts that degrade system stability
- Using restart cascades to create outages

### The Solution: Evidence-Driven Analysis + Human Judgment

The proper approach combines:

- **AI Strength:** Rapid evidence gathering and pattern recognition
- **Human Strength:** Judgment, accountability, and context awareness

**The workflow:**
1. **AI gathers evidence** (fast, objective, comprehensive)
2. **AI analyzes patterns** (identifies root cause)
3. **AI recommends actions** (suggests recovery)
4. **Human reviews** (understands context, verifies reasoning)
5. **Human decides** (makes the call based on business needs)
6. **Human executes** (takes responsibility for the action)
7. **AI verifies** (confirms the action worked)

---

## Technical Details: The Agentic Loop

This project demonstrates the complete **Agentic Loop** — a cycle that separates different responsibilities between AI and humans: