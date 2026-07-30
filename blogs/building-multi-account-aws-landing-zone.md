---
layout: default
title: Building a Multi-Account AWS Landing Zone from Scratch
hide_hero: true
---

## Building a Multi-Account AWS Landing Zone from Scratch

Most teams treat AWS accounts like a single shared sandbox. By the time they realize the risks, they're already dealing with blast-radius incidents and compliance headaches. A proper landing zone solves this before it becomes a problem.

### Why Multiple Accounts

An AWS organization with well-defined account boundaries gives you security isolation, cost visibility, and blast-radius containment by default. Dev workloads can't accidentally reach prod. A runaway Lambda in staging doesn't affect billing clarity in production. IAM mistakes stay contained.

### The OU Structure

Start with a simple Organizational Unit hierarchy:

- **Root**
  - Management (billing and org management only)
  - Security (audit, log archive)
  - Infrastructure (shared services, networking)
  - Workloads
    - Production
    - Non-Production

Keep the management account empty of workloads. Treat it as a locked room — only org-level automation and billing should touch it.

### SCPs as Guardrails

Service Control Policies are the backbone of a landing zone. Apply them at the OU level, not the account level, so new accounts inherit them automatically.

Key policies to start with:

- Deny any action outside approved regions
- Deny disabling CloudTrail
- Deny leaving the organization
- Require IMDSv2 on all EC2 instances

### Terraform Module Structure

```hcl
module "landing_zone" {
  source  = "github.com/subhamay-bhattacharyya-tf/aws-landing-zone"
  version = "1.4.0"

  organization_id     = var.org_id
  root_email_domain   = "example.com"
  log_retention_days  = 365
  enable_guardduty    = true
}
```

A single module call should provision the org structure, SCPs, and baseline security services. Everything else builds on top.

### What Comes Next

Once the landing zone is stable, layer in account vending (automated account creation via Service Catalog), centralized logging into a log archive account, and IAM Identity Center for single sign-on. Each piece is independent — you don't need all of them on day one.
