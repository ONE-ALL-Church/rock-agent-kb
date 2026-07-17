# Event Registration Analytics Dashboard

Build a secured read-only Helix dashboard for registration capacity, pace, wait list, optional segmentation, fee choices, demographics, and bounded participant drilldown.

- Recipe ID: `oneall:event-registration-analytics-dashboard`
- Community status: `community-reviewed`
- Version: `1.0.0`
- Source commit: [`8bbd478b3167`](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/8bbd478b31673f25d40fe31ce8ea492be91d16d4/Recipes/event-registration-analytics-dashboard)
- License: [MIT](https://raw.githubusercontent.com/ONE-ALL-Church/RockRMS-OA-Public/8bbd478b31673f25d40fe31ce8ea492be91d16d4/Recipes/event-registration-analytics-dashboard/LICENSE)

## Use Cases

- Give event teams one secured view of capacity, pace, wait list, choices, demographics, and participant context.
- Compare a current registration instance with a prior event at the same number of days before registration closes.
- Add optional mutually exclusive staff and serving segments without presenting local group semantics as universal Rock behavior.

## Adaptation Points

- `registrationInstanceId`: Set the locally verified registration instance. The public configuration uses zero and the endpoint stops until this is supplied.
- `priorRegistrationInstanceId`: Optionally set a comparable prior instance whose end date can anchor same-stage pace comparison.
- `capacityFallback`: Set a fallback only when RegistrationInstance.MaxAttendees is intentionally empty.
- `registrantAttributes`: Map optional registrant campus and discovery-source Attribute IDs after confirming entity scope and display semantics.
- `segmentVerifierGroups`: Configure optional staff and serving-verifier groups, then confirm active non-archived membership is the intended truth source.
- `servingDepartmentHierarchy`: Configure a serving root group and department group type only when the local hierarchy supports that interpretation.
- `feeChoiceScope`: Confirm fee items represent participant choices and optionally restrict displayed fee groups by name.
- `optionLabelSuffixMarker`: Optionally remove a display-only suffix such as a target-audience annotation without modifying fee-item source names.
- `maxRegistrantRows`: Choose a bounded local drilldown cap between 1 and 1000 after measuring database and browser cost.
- `authorization`: Restrict both the Rock page and Lava Application View action to authenticated roles approved for participant operations.

## Implementation

1. Review the immutable README, configuration, Lava source, and static contract before adaptation.
2. Create a secured GET endpoint with ApplicationView security and enable only the Sql Lava command.
3. Set registrationInstanceId, then add optional prior-instance, attribute, segment, hierarchy, and fee configuration only after documenting their local meaning.
4. Render the endpoint through a Lava Application Content block on a staff-authorized page.
5. Run the static contract and test query plans with representative production volume.
6. Validate metric invariants, wait-list behavior, multi-person registrations, optional adapters, authorization personas, and desktop/mobile rendering before launch.

## Validate

1. Run python3 tests/static_contract.py from the recipe directory.
2. Confirm registered people match a known instance total and registrations differ correctly for a multi-person registration.
3. Confirm wait-list people are excluded from confirmed aggregates and remain explicit in the separate metric and drilldown.
4. Confirm mutually exclusive segment counts sum exactly to confirmed people and staff precedence handles a person who also satisfies serving verification.
5. Confirm campus and source values use the intended registrant attributes rather than person or registration campus by accident.
6. Confirm fee-choice counts against known selections and review active versus historical fee behavior.
7. Confirm a serving-verifier holder without an active department lands in the verifier-only bucket and multi-department totals disclose possible duplication.
8. Confirm prior-stage comparison is absent when disabled and aligns by days remaining when configured.
9. Confirm the row cap, empty state, reset, search, campus, segment, and detail controls behave correctly.
10. Confirm unauthorized users cannot open the page or endpoint and an administrator override is not mistaken for intended-role access.
11. Confirm rendered output has no Lava or browser-console errors, clipped labels, or internal vertical scrolling at desktop and mobile widths.

## Security

- Data access: `read_only`
- Authentication: Rock-authenticated staff session
- Authorization: Application-view and page permissions limited to approved registration operations roles
- Handles sensitive data: `true`
- Read-only participant names, attendance intent, staff/serving classification, and registration choices remain sensitive operational data.
- The public reference omits email, phone, addresses, payment details, arbitrary attributes, and free-text registration answers.
- The endpoint enables only Sql and uses GET only while it performs no writes.
- A future write action requires a separate endpoint with authorization, CSRF protection, validation, audit logging, and rollback planning.

## Compatibility

- Tested Rock versions: Not declared
- Last verified: 2026-07-13
- Rock `17`: `expected` - The source pattern targets this model family, but the sanitized package still requires target-instance validation.
- Rock `18`: `expected` - The source pattern targets this model family, but the sanitized package still requires target-instance validation.
- The production pattern was reviewed against the Rock 17/18 model family, but the sanitized package has not been deployed unchanged in every supported release.
- Verify RegistrationInstance, RegistrationRegistrant, RegistrationRegistrantFee, AttributeValue, GroupMember, and Lava SQL behavior against the target release.
- The reference uses SQL Server window functions and STRING_AGG; performance depends on data volume, indexes, compatibility level, and optional hierarchy depth.

## Community Verification

- No consumer verification attestations have been submitted yet.
- Feedback and issues: https://github.com/ONE-ALL-Church/RockRMS-OA-Public/issues

## Reusable Learnings

- Declare metric grain because one Registration can contain multiple RegistrationRegistrant rows.
- Define confirmed and wait-list predicates once, then reconcile every segment and distribution against that population.
- Compare registration pace by days remaining until close rather than calendar date.
- Use explicit classification precedence so staff and serving segments remain mutually exclusive.
- Treat verifier groups and department hierarchies as configurable local truth sources, not as universal Rock behavior.
- Distinguish registrant attribute campus from registration campus and person campus before labeling a chart.
- Interpret fee items as choices only after reviewing the registration template and active or historical behavior.
- Clean display labels without mutating source registration option names.
- A read-only endpoint still requires application and page authorization because participant operations data is sensitive.
- Bound the drilldown and measure query plans before increasing row limits.
- Verify rendered metrics, authorization, errors, and responsive overflow after content readback; a successful file write alone is not proof of a working dashboard.

## Limitations

- The sanitized package requires live testing in each target Rock release and instance configuration.
- Client-side drilldown filtering is intentionally capped and should become server-side pagination for large events.
- BirthYear-derived age bands are approximate and are not exact birthday calculations.
- Fee items are not universally breakout choices; the target registration template determines their meaning.
- Group-based staff, serving, and department classifications are optional local semantics rather than built-in universal Rock definitions.
- Department totals can exceed unique serving people because group membership is many-to-many.
