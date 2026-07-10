# Communication History Active Search

Build a secured read-only Helix communication browser with allowlisted filters, parameterized search, bounded pagination, and aggregate recipient outcomes.

- Recipe ID: `oneall:communication-history-active-search`
- Community status: `community-reviewed`
- Version: `1.0.0`
- Source commit: [`066de269c307`](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/066de269c3071461f8da3702dab917d4d16a07c4/Recipes/communication-history-active-search)
- License: [MIT](https://raw.githubusercontent.com/ONE-ALL-Church/RockRMS-OA-Public/066de269c3071461f8da3702dab917d4d16a07c4/Recipes/communication-history-active-search/LICENSE)

## Use Cases

- Give authorized staff a responsive communication history browser without loading a full page after every filter change.
- Filter communications by Rock status, communication type, subject or name, and bounded pages.
- Review aggregate delivery outcomes without exposing message bodies or recipient-level contact information.

## Adaptation Points

- `defaultStatus`: Choose all, draft, pending approval, approved, or denied for the initial view.
- `defaultPageSize`: Choose a bounded initial page size of 25, 50, or 100.
- `communicationDetailPageId`: Set a locally authorized communication detail page or leave zero to render no record links.
- `applicationSlug`: Update both relative Helix endpoint routes if the application slug differs from the recipe default.
- `authorization`: Restrict the Rock page and both endpoints to authenticated staff roles permitted to view communication activity and outcomes.

## Implementation

1. Review the pinned README, source, configuration, and static test at the immutable commit.
2. Create secured GET list and results endpoints and enable Sql only on the results endpoint.
3. Set local default filters, page size, optional detail page, and relative endpoint routes without introducing production defaults.
4. Render the list endpoint inside a Lava Application Content block on a staff-only Rock page.
5. Preserve parameterized text search, enum allowlists, the 100-row cap, and the exclusion of message and recipient details.
6. Test query plans and response times with realistic communication and recipient volume.

## Validate

1. Run python3 tests/static_contract.py from the recipe directory.
2. Confirm unauthenticated and unauthorized users cannot load the page or either endpoint.
3. Confirm status 3 displays Approved rather than Sent.
4. Confirm status, type, text, and page-size changes reset pagination to page one.
5. Submit quotes, percent characters, underscores, and brackets as search text and confirm they cannot change SQL statement structure.
6. Confirm invalid status and type values fall back to all and invalid page sizes fall back to 25.
7. Confirm no request can return more than 100 rows.
8. Compare aggregate recipient counts with known communications and confirm transient rows and message bodies are absent.
9. Confirm empty results and first, middle, and last pagination states render correctly.

## Security

- Data access: `read_only`
- Authentication: Rock-authenticated staff session
- Authorization: ApplicationView and page permissions limited to approved communication-history roles
- Handles sensitive data: `true`
- The public reference excludes message bodies, SMS text, recipient names, addresses, phone numbers, and recipient-level errors.
- Communication names, schedules, senders, and delivery aggregates remain sensitive staff data.
- The results endpoint uses GET only for read behavior and caps requests at 100 rows.
- Approval, resend, cancel, delete, and other writes require separate endpoints, authorization, CSRF protection, validation, auditing, and rollback.

## Compatibility

- Tested Rock versions: 17, 18
- Last verified: 2026-07-09
- Verify the Communication and CommunicationRecipient enum and field behavior against the target Rock release.
- Performance depends on communication volume, database indexes, search selectivity, and recipient counts.
- The model map identifies communication status 3 as Approved; it must not be relabeled as Sent.

## Reusable Learnings

- Separate the filter shell from the results endpoint so HTMX updates only the changing region.
- Allowlist status, type, and page-size values and bind free text as SQL parameters instead of interpolating sanitized strings.
- Page communication rows before running correlated recipient aggregates so cost scales with the visible page.
- Use the Rock enum name Approved for status 3 and show send and delivery evidence separately.
- Keep the initial operational view narrow and require explicit review before adding message bodies or recipient-level data.
- A read-only endpoint still needs application and page authorization because communication activity is sensitive.

## Limitations

- Subject and name search uses SQL LIKE and may require a different index or search strategy on very large datasets.
- The result count and page query are separate reads and may differ briefly while communications change concurrently.
- The recipe reports aggregate recipient statuses but does not reproduce every official communication analytics feature.
- The reference UI is intentionally minimal and should be adapted to the organization's design system without weakening filter or authorization boundaries.
