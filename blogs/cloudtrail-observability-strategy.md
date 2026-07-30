---
layout: default
title: A Practical CloudTrail Observability Strategy
hide_hero: true
---

## A Practical CloudTrail Observability Strategy

CloudTrail is enabled by default in most accounts, then ignored. Logs pile up in S3 and nobody looks at them until an incident forces it. A real observability strategy means acting on CloudTrail data continuously, not retroactively.

### Centralize First

All CloudTrail logs should flow to a dedicated log archive account — an S3 bucket that workload accounts can write to but never delete from. Use S3 Object Lock in compliance mode with a 7-year retention period. This makes logs tamper-proof even if a workload account is compromised.

```hcl
resource "aws_s3_bucket_object_lock_configuration" "trail" {
  bucket = aws_s3_bucket.log_archive.id

  rule {
    default_retention {
      mode = "COMPLIANCE"
      years = 7
    }
  }
}
```

### Encrypt with a Customer-Managed Key

The default CloudTrail encryption is fine for compliance checkboxes. For real security, use a CMK in the security account:

- Key policy allows CloudTrail to encrypt
- Key policy allows log archive S3 to decrypt for reading
- Workload account roles cannot decrypt — they can write logs but not read them

### What to Alert On

Don't alert on everything — alert fatigue is real. Start with high-signal events:

- Root account login (any account)
- Changes to SCPs or OU structure
- IAM role creation with `*` actions
- Security group rules opening `0.0.0.0/0` on port 22 or 3389
- CloudTrail being stopped or deleted

Route these through EventBridge → SNS → PagerDuty. Everything else goes to S3 for later analysis.

### Athena for Ad-Hoc Queries

When you need to investigate an incident, Athena over the centralized S3 bucket is your fastest path:

```sql
SELECT eventtime, useridentity.arn, eventname, sourceipaddress
FROM cloudtrail_logs
WHERE eventtime > '2029-01-01'
  AND errorcode IS NULL
  AND eventname IN ('AssumeRole', 'GetSecretValue', 'DeleteBucket')
ORDER BY eventtime DESC
LIMIT 100;
```

Partition the table by account ID and date so queries stay cheap even across years of logs.
