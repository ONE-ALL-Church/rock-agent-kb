---
concept_id: engagement-tracking
task_id: recipe-request-and-monitor-assessments
title: Recipe: Request and monitor assessments
generated: true
---

# Recipe: Request and monitor assessments

The intended people receive valid assessment requests and their completion state can be reviewed.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`

## Entities And Tables

- `Person`

## Steps

1. For one person, use Request Assessment from the profile, select one or more assessments and provide the custom message.
2. For many people, use a communication that generates the assessment’s external URL from the public application root and each recipient’s URL-encoded person key.
3. Tell recipients that requests are also available from My Account.
4. Review pending and complete entries on person assessment histories.
5. Cancel an incorrect request only while it remains incomplete.

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment
- https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/manually-track-streaks
- https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/view-assessment-history
- https://community.rockrms.com/documentation/engagement/assessments/administer-assessments/retake-assessments
- https://community.rockrms.com/documentation/engagement/streaks/streak-enrollment/rebuild-streaks-individually
- https://community.rockrms.com/documentation/engagement/assessments/administer-assessments
