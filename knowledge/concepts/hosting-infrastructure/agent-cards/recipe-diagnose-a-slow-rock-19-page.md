---
concept_id: hosting-infrastructure
task_id: recipe-diagnose-a-slow-rock-19-page
title: Recipe: Diagnose a slow Rock 19 page
generated: true
---

# Recipe: Diagnose a slow Rock 19 page

A repeatable diagnosis identifies either a page component or a broader infrastructure constraint.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Page`
- `DataView`
- `Block`

## Entities And Tables

- `Page`
- `DataView`
- `Block`

## Steps

1. Capture the affected URL, user context, time, and expected behavior.
2. Run the v19 Page Load Time diagnostic.
3. Identify the slowest page components.
4. Repeat the test to determine whether the result is stable.
5. Correlate it with IIS, CPU, database, storage, network, and provider telemetry.
6. Inspect snapshot isolation and supported read-only-context opportunities.
7. Record whether the cause is component-specific, database-related, capacity-related, intermittent, or unresolved.
8. Stop when the evidence supports a bounded next action.
9. Confirm the Rock version. In v19, capture the Page Load Time diagnostic trace for the affected page.
10. Identify whether one block or component dominates the trace.
11. Reproduce at a known time and record whether the issue is constant, intermittent, or load-dependent.
12. Inspect IIS application-pool startup, idle timeout, preload, recycling, and dynamic-compression settings.
13. Determine whether the page invokes Data Views, Reports, analytics, plugins, APIs, or long-running database operations.
14. Inspect whether snapshot isolation is enabled and whether supported read workloads are eligible for `RockContextReadOnly` or `RockContextAnalytics`. Install Rock
15. Compare the symptom with CPU, database, network, and provider telemetry.
16. Stop when the slow component or infrastructure constraint is identified with repeatable evidence; do not prescribe a web farm solely from the symptom.

## Do Not Assume

- A slow page proves the server is undersized.
- A clean trace rules out intermittent infrastructure issues.
- Adding web nodes fixes database or custom-code constraints.
- Stop when the slow component or infrastructure constraint is identified with repeatable evidence; do not prescribe a web farm solely from the symptom.

## Source Links

- https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/install-rock
- https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-your-rock-context
- https://community.rockrms.com/documentation/supporting-rock/hosting/internal-hosting/configure-internet-information-services-iis
- https://community.rockrms.com/documentation/supporting-rock/hosting/scale-rock/configure-a-rock-web-farm
- https://www.youtube.com/watch?v=c-wycR9HEuQ&t=1003s
