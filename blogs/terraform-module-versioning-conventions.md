---
layout: default
title: Terraform Module Versioning Conventions That Actually Work
hide_hero: true
---

## Terraform Module Versioning Conventions That Actually Work

Unversioned Terraform modules are technical debt disguised as convenience. One upstream change breaks three teams silently. Semantic versioning for modules is not optional — it's the difference between infrastructure you can reason about and infrastructure you fear to change.

### Semantic Versioning Means Something

Apply the same rules to modules that you apply to libraries:

- **Patch** (`1.0.1`): bug fix, no interface change
- **Minor** (`1.1.0`): new optional variable, backwards compatible
- **Major** (`2.0.0`): variable renamed, resource recreated, breaking change

Every release gets a git tag. Every module call pins to a tag.

### Conventional Commits Drive the Version

Automate version bumping with conventional commits:

```
feat: add support for S3 intelligent tiering       → minor bump
fix: correct IAM policy for cross-account access   → patch bump
feat!: rename var.bucket_name to var.name          → major bump
```

A GitHub Actions workflow reads the commit log, determines the next version, creates the tag, and publishes release notes. No manual version decisions.

### Module Registry vs Git Tags

For small teams, Git tags are sufficient:

```hcl
module "s3" {
  source  = "github.com/subhamay-bhattacharyya-tf/s3-module?ref=v3.2.1"
}
```

For larger organizations, a private Terraform registry (Terraform Cloud or a self-hosted one) adds discoverability and enforces the version constraint syntax:

```hcl
module "s3" {
  source  = "app.terraform.io/subhamay/s3/aws"
  version = "~> 3.2"
}
```

The `~>` constraint allows patch updates but pins the minor version. Use it for non-breaking updates; require explicit major bumps for breaking changes.

### Testing Before Tagging

Never tag without testing. A minimal module test pipeline:

1. `terraform init` and `terraform validate` on every PR
2. `terraform apply` to a sandbox account on merge to main
3. `terratest` integration test confirms the resource behaves correctly
4. Tag is created only after all tests pass

A module that breaks on `apply` is worse than no module at all.

### Deprecation Policy

When you release a major version, support the previous major for 90 days. Create a GitHub issue tracking which downstream consumers still use the old version. Close the issue when all consumers have migrated. Then archive the old major branch.
