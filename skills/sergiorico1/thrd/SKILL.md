---
name: thrd
description: "Automate email account provisioning and management via the thrd.email API. Use to: (1) Instantly provision new email accounts (tenant name optional), (2) Retrieve API keys and inbox details, (3) Poll for inbound emails, (4) Send/Reply to emails (idempotency required), (5) Track outbound status, and (6) Generate Stripe checkout links for plan upgrades."
---

# Thrd Email Skill

This skill allows you to manage email accounts for AI agents using the [thrd.email](https://thrd.email) infrastructure.

## Workflows

### Provision a New Email Account
To create a new email account, run the onboarding script:
```bash
python3 scripts/onboard.py [tenant_name]
```

### Upgrade Plan (Billing)
To upgrade your current tenant to a higher Tier (Limited or Verified), use the checkout script:
```bash
python3 scripts/checkout.py <plan_name>
```
Forward the resulting Stripe URL to your human owner for payment.

### Manage Emails and Track Delivery
For detailed API usage (polling, sending, replying, and checking delivery status), see [references/api.md](references/api.md).

## Tools
- `scripts/onboard.py`: Instant provisioning of a new email inbox.
- `scripts/checkout.py`: Generate a Stripe Checkout URL for upgrades.
