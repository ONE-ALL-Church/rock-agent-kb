# Check-In Status Dashboard

A reusable read-only Helix Lava Application pattern that combines an event registration roster, active group-only placements, and the latest qualifying check-in attendance for an operating date.

- Recipe ID: `oneall:check-in-status-dashboard`
- Community status: `community-reviewed`
- Version: `1.0.0`
- Source commit: [`d8ea54fa67ef`](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/d8ea54fa67efe40692689fb009561ff96e88bf42/Recipes/check-in-status-dashboard)
- License: [MIT](https://raw.githubusercontent.com/ONE-ALL-Church/RockRMS-OA-Public/d8ea54fa67efe40692689fb009561ff96e88bf42/Recipes/check-in-status-dashboard/LICENSE)

## Use Cases

- Create an operational roster showing registration, placement, and check-in state in one view.
- Include people manually placed in an event group even when they are not registration registrants.
- Give staff deterministic search and sorting without adding write behavior.

## Adaptation Points

- `registrationInstanceId`: Set this to the target event registration instance after verifying it in the local Rock instance.
- `groupTypeIds`: Set the placement and check-in group type IDs that define the event scope.
- `groupAttributeKeys`: Map optional local group attribute keys such as cabin, bus, and color, or remove unused joins.
- `authorization`: Restrict the Rock page and Lava endpoint to staff roles that need participant roster access.

## Implementation

1. Review the pinned README and source at the immutable commit before adapting it.
2. Create a secured GET endpoint in a Helix Lava Application and add the configuration rigging without numeric defaults.
3. Verify the registration instance, group types, placement behavior, and optional group attribute keys in the target Rock instance.
4. Adapt the result presentation while preserving server-owned filtering, allowlisted sort keys, and deterministic null ordering.
5. Keep the first deployment read-only and omit contact data and registration answers.

## Validate

1. Confirm a registered person appears once and resolves their placement group.
2. Confirm an active non-leader group member without a registration appears as group-only.
3. Confirm waitlist, missing-placement, not-checked-in, and present examples route to separate states.
4. Confirm attendance from another date or unrelated group type does not affect current status.
5. Confirm invalid sort and filter values fall back safely and no write requests are available.
6. Confirm unauthorized users cannot open either the Rock page or endpoint.

## Security

- Data access: `read_only`
- Authentication: Rock-authenticated staff session
- Authorization: Application-view and page permissions limited to event operations roles
- Handles sensitive data: `true`
- The public reference omits phone, email, registration answers, and arbitrary attributes.
- Roster names and attendance remain sensitive operational data even though the endpoint is read-only.
- Any future write action requires authorization, CSRF protection, validation, audit logging, and rollback planning.

## Compatibility

- Tested Rock versions: 17, 18
- Last verified: 2026-06-24
- Verify table, field, Lava command, and Helix endpoint behavior against the target Rock release.
- Local registration and check-in workflows may encode status differently.

## Reusable Learnings

- Union registration and active non-leader placement membership, then deduplicate by person so manual placements remain visible.
- Resolve check-in state from the latest qualifying Attendance joined through AttendanceOccurrence, not from placement alone.
- Treat missing placement and waitlist as operational states rather than collapsing them into not checked in.
- The endpoint returning a result set should own search, filtering, sorting, and null buckets.
- A reusable public recipe should carry code, adaptation points, compatibility, security boundaries, validation, license, and an immutable source pin.

## Limitations

- The pattern does not infer checked-out state because that requires a locally trustworthy checkout signal.
- The reference provides a simple table rather than a complete production interface.
- The SQL must be performance-tested against the size and indexes of the target database.
