# Source Conflict And Community Intake Review

Reviewed on 2026-06-18 after the editorial quality queue merge.

## Source Conflict Queue

`agent/source-conflicts.jsonl` currently contains 34 rows. These rows are
authority-alignment prompts, not confirmed contradictions.

Current distribution:

- 15 `operational_guidance`
- 9 `release_caveat`
- 6 `risk`
- 4 `implementation_pattern`

Authority tier pairings:

- 28 `community-reviewed` plus `rocku-confirmed`
- 5 `community-reviewed` plus `official`
- 1 `community-reviewed` plus `official` plus `rocku-confirmed`

The queue spans these concepts: `workflows`, `check-in`, `cms-websites`,
`communications`, `security-permissions`, `data-views-reports`, `groups`,
`lava`, `giving-finance`, `developer-resources`, `people-families`,
`platform-configuration`, `event-registration`, `mobile`, `api-integrations`,
and `scheduling-locations`.

Decision: preserve these generated rows. They are useful reminders that agents
should prefer official documentation, source code, release notes, RockU, or live
verification for canonical behavior. Community-reviewed claims may still be
used as implementation examples or discovery context, but they should not
override stronger sources without direct verification.

No public claim approvals or rejections were recorded from this batch because
the rows did not identify a specific claim that should be promoted, suppressed,
or rewritten. If the queue becomes too noisy, improve grouping and severity in
the generator rather than deleting review rows.

## Community Intake

Real community intake status:

- `oneall`: 7 rows submitted under `community-contributions/oneall/`; all 7
  are promoted into `contributions/oneall/bundle.jsonl`.
- `source-suggestions`: no submitted files.

The only unpromoted community bundle is
`community-contributions/simulated-docs-contributor/bundle.jsonl`, with 3 rows:

- `simulated-docs-contributor:lava-security-layering`
- `simulated-docs-contributor:sql-dynamic-data-guardrails`
- `simulated-docs-contributor:checkin-registration-preflight`

Those rows validate structurally and are public-safe as test material, but the
org ID and source record IDs are simulated. Keep them as intake/test fixture
material. Do not promote them into canonical `contributions/` unless a maintainer
explicitly decides simulated material should become real KB content or replaces
the synthetic source references with real reviewed source records.

