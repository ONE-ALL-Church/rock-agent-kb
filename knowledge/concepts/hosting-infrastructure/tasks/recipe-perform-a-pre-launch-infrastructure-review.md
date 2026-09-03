---
concept_id: hosting-infrastructure
task_id: recipe-perform-a-pre-launch-infrastructure-review
title: Recipe: Perform a pre-launch infrastructure review
generated: true
---

# Recipe: Perform a pre-launch infrastructure review

A go/no-go record separates verified readiness from unresolved conditions.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Confirm the exact Rock, Windows, IIS, and SQL versions against current requirements.
2. Confirm topology and PCI-required web/database separation.
3. Inspect SQL network exposure and allowed TCP 1433 sources.
4. Validate HTTPS for internal and external Rock sites.
5. Confirm backup ownership, retention, and a tested restore path.
6. Confirm patch ownership and supported Rock branch.
7. Verify SMTP through a controlled delivery test.
8. Confirm file-storage behavior, especially across multiple nodes.
9. Confirm the single job-running node for Rock 19 farms.
10. Exercise representative public, administrative, check-in, reporting, and integration journeys.
11. Record unresolved gaps and assign owners.
12. Stop before launch if a security, payment-processing, recovery, certificate, or critical-path dependency remains unverified.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-rock
- https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-your-rock-context
- https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1003s
