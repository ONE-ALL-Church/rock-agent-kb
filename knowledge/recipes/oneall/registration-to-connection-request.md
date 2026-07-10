# Registration-to-Connection Request Transfer Workflow

Create a Connection Request for each selected registration registrant, preserve source traceability, copy registration campus explicitly, and transfer reviewed attributes through native Rock workflow actions.

- Recipe ID: `oneall:registration-to-connection-request`
- Community status: `community-reviewed`
- Version: `1.0.0`
- Source commit: [`03efbb093c02`](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/03efbb093c024d31ae4df3b6e6af56bdbbcafe00/Recipes/registration-to-connection-request)
- License: [MIT](https://raw.githubusercontent.com/ONE-ALL-Church/RockRMS-OA-Public/03efbb093c024d31ae4df3b6e6af56bdbbcafe00/Recipes/registration-to-connection-request/LICENSE)

## Use Cases

- Move application or intake registration data into a Connection Board for staff follow-up.
- Create one Connection Request per registrant while preserving a traceable source Registration ID.
- Carry the registration's selected campus and reviewed registrant attributes into the follow-up process.

## Adaptation Points

- `workflowIdentity`: Choose a stable workflow name and organization-owned ForeignKey prefix; preserve the prefix across reruns and upgrades.
- `connectionOpportunityAndStatus`: Set local Connection Opportunity and Status GUIDs after reviewing board behavior and permissions.
- `sourceRegistrationTargetAttributeKey`: Create and configure an Integer Connection Request attribute used to store Registration.Id.
- `registrationCampus`: Keep explicit Registration.Campus propagation or replace it only after documenting another authoritative campus source.
- `commentsSourceAttribute`: Choose the registrant attribute that may populate Connection Request comments, or remove the mapping when comments are inappropriate.
- `attributeMappings`: Map only reviewed registration registrant attributes to compatible Connection Request attributes and add normalization where field types differ.
- `duplicatePolicy`: Choose skip, reviewed update, or intentional additional request behavior before any retry or backfill.
- `authorizationAndRetention`: Restrict the deploy surface and resulting Connection data, then set retention and reporting access appropriate to copied answers.

## Implementation

1. Review the immutable README, mapping contract, Lava deploy, SQL verifier, and static test before adaptation.
2. Create the target Connection Request attributes and complete every required value in the deploy's ADAPTATION REQUIRED block.
3. Run the deploy from a temporary administrator-only Lava Application endpoint with only RockEntity, RockEntityModify, and read-only Sql enabled.
4. Run the deploy twice and require stable reuse plus zero invalid Create Connection Request references.
5. Review the workflow in Rock, then assign it manually as the registration template's Registrant Workflow.
6. Submit a marked test registration through the real registration experience and run the read-only verifier.
7. Document retry and backfill duplicate behavior before processing any existing registrants.

## Validate

1. Run python3 tests/static_contract.py from the recipe directory.
2. Confirm the deploy stops while local opportunity, status, or target attribute configuration is missing.
3. Run the deploy twice and confirm exactly one managed WorkflowType, one Start activity, nine workflow attributes, and stable managed actions remain.
4. Confirm every Create Connection Request setting GUID resolves to an attribute qualified to the deployed WorkflowType.
5. Submit one marked test registrant and confirm exactly one Connection Request has the expected person, opportunity, status, and comments.
6. Confirm ConnectionRequest.CampusId equals Registration.CampusId, including a deliberate null-campus case.
7. Confirm the source registration attribute stores RegistrationRegistrant.RegistrationId and the mapped target value matches its source.
8. Run tests/verify-transfer.sql with a read-only principal and confirm MatchingRequestCount is one and CampusMatches is true.
9. Manually retry only under the documented duplicate policy and verify no unintended duplicate is created.

## Security

- Data access: `writes`
- Authentication: Rock-authenticated administrator for deployment; runtime launch follows the registration submission and workflow context configured by Rock.
- Authorization: Deployment is limited to trusted administrators, while Connection Type, page, attribute, workflow, and reporting permissions limit resulting data to approved staff.
- Handles sensitive data: `true`
- The deployment endpoint changes Rock configuration and should be disabled or removed after use.
- Runtime writes use native Create Connection Request and Set Entity Attribute actions; SQL in the package is read-only lookup and verification.
- Registration answers can contain pastoral, contact, care, or other sensitive information; copy only fields staff need.
- Do not persist a full admin URL because it leaks environment routing and becomes stale across hosts.
- The reference does not delete or merge existing requests and must not be used as a bulk cleanup tool.

## Compatibility

- Tested Rock versions: 17, 18
- Last verified: 2026-07-09
- The pattern is based on multiple production registration workflows and a corrected end-to-end implementation, but the sanitized package has not been deployed unchanged in a generic Rock instance.
- Verify system action classes, action-setting keys, field types, and registration trigger behavior against the target release.
- The public deploy dynamically resolves system entity, field type, and action-setting IDs rather than copying local numeric IDs.

## Reusable Learnings

- Registrant-scoped automation should use the template's Registrant Workflow and consume RegistrationRegistrantId rather than guessing from registrar or person context.
- Create Connection Request falls back to the person's primary campus when no Campus Attribute is configured, so registration campus must be wired explicitly when it is authoritative.
- Capture the created request in a workflow attribute before later native actions copy request attributes.
- Store the source Registration ID and construct local links when rendering instead of persisting environment-specific URLs.
- Use stable ForeignKeys and re-query canonical IDs after every modify operation so rerunnable deploys do not depend on transient return objects.
- Validate that all action-setting attribute GUIDs belong to the same WorkflowType; stale cross-workflow references can survive copied configuration.
- Keep deployment SQL read-only and use native Rock actions for runtime writes.
- Treat retries and backfills as a separate reviewed workflow because unconditionally rerunning Create Connection Request can create duplicates.

## Limitations

- The sanitized deployment has not been executed unchanged against every supported Rock release or plugin combination.
- The native registration trigger is expected to launch once per new registrant; manual reruns and backfills require an explicit duplicate policy.
- The example includes one generic mapped value and must be extended carefully for additional fields and field-type normalization.
- Connection Request attribute qualifiers vary by local Connection configuration and must be created and permissioned before deployment.
- An empty registration campus remains empty; the recipe intentionally does not substitute the person's primary campus.
