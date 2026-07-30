---
layout: default
title: Designing IAM Identity Center Permission Sets That Scale
hide_hero: true
---

## Designing IAM Identity Center Permission Sets That Scale

IAM Identity Center (formerly AWS SSO) is the right way to manage human access across a multi-account AWS organization. But most implementations start with too-broad permission sets and never tighten them. Here's how to design them to scale.

### The Three-Tier Model

Resist the urge to create a permission set per team. Instead, model access in three tiers:

| Tier | Permission Set | Who |
|------|---------------|-----|
| 1 | `ReadOnly` | Everyone by default |
| 2 | `PowerUser` | Engineers working in non-prod |
| 3 | `AdministratorAccess` | Senior engineers, prod break-glass only |

Most work happens at tier 2. Tier 3 access to production should require a JIRA ticket and auto-expire after 8 hours.

### Attribute-Based Access Control

Use ABAC to reduce the number of permission sets you need to maintain. Tag IAM Identity Center users with their team:

```json
{
  "Condition": {
    "StringEquals": {
      "aws:PrincipalTag/Team": "${aws:ResourceTag/Team}"
    }
  }
}
```

Engineers can only touch resources tagged with their own team. One permission set covers all teams.

### Terraform Management

Manage permission sets in code:

```hcl
resource "aws_ssoadmin_permission_set" "power_user" {
  name             = "PowerUser"
  instance_arn     = local.sso_instance_arn
  session_duration = "PT8H"
  relay_state      = "https://console.aws.amazon.com/"
}
```

Every assignment — which group gets which permission set in which account — is a Terraform resource. Drift is impossible because the nightly plan run catches it.

### Break-Glass Access

Even with a solid permission set structure, you need an emergency access path. Keep one `BreakGlass` permission set that grants full admin. It should be:

- Unassigned by default
- Assignable only via an automated runbook that requires two approvals
- Logged via CloudTrail with an SNS alert on any use
