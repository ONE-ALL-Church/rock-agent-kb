---
concept_id: obsidian-development
task_id: recipe-cache-a-read-request
title: Recipe: Cache A Read Request
generated: true
---

# Recipe: Cache A Read Request

Concurrent callers share one in-flight request and reuse its result for a bounded period.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Import `cachePromise` from `@Obsidian/Utility/cache`.
2. Choose a key unique to the request and all inputs that affect its result.
3. Wrap the Promise-returning request function.
4. Set an expiration when the one-minute default is inappropriate.
5. Call the wrapper from all consumers.
6. Test concurrent calls and post-expiration behavior. (Caching API Calls)

## Do Not Assume

- The cache is an authorization boundary.
- One key is safe for requests with different inputs.
- The default expiration satisfies the data’s freshness requirement.

## Source Links

- https://community.rockrms.com/developer/obsidian
