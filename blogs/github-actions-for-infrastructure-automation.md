---
layout: default
title: GitHub Actions for Infrastructure Automation at Scale
hide_hero: true
---

## GitHub Actions for Infrastructure Automation at Scale

CI/CD for application code is solved. Infrastructure CI/CD is still where most teams cut corners — manual applies, shared credentials, no drift detection. GitHub Actions, combined with OIDC and reusable workflows, changes that.

### OIDC Instead of Long-Lived Keys

Never store AWS access keys in GitHub secrets. Use OpenID Connect to let GitHub Actions assume an IAM role directly:

```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789012:role/github-actions-deploy
    aws-region: us-east-1
```

The IAM role trust policy restricts which repos and branches can assume it. No keys to rotate, no secrets to leak.

### Reusable Workflow Pattern

Define your Terraform workflow once and call it from every repo:

```yaml
# .github/workflows/terraform.yml (in the shared repo)
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      working_directory:
        required: true
        type: string
```

Individual repos call it with two lines. Consistency at zero maintenance cost.

### Plan on PR, Apply on Merge

The standard gate: `terraform plan` runs on every pull request and posts the diff as a comment. `terraform apply` runs only after the PR merges to main. This keeps humans in the loop without blocking automation.

### Drift Detection

Schedule a nightly workflow that runs `terraform plan` against every environment and opens a GitHub issue if drift is detected. Infrastructure that drifts silently is infrastructure that will surprise you at the worst time.

### Semantic Versioning for Modules

Tag every module release. Workflows pin to a specific version:

```hcl
source = "github.com/subhamay-bhattacharyya-tf/s3-module?ref=v2.1.0"
```

Unpinned modules are a supply chain risk. Pin everything; upgrade deliberately.
