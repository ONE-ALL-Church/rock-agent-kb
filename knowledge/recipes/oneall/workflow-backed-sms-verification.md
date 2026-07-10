# Workflow-Backed SMS Verification for Anonymous Rock Forms

Optionally recognize an existing person during an anonymous Rock form using an exact unique match, persisted workflow challenge, bounded SMS code, Rock modify-command state writes, and an idempotent final action.

- Recipe ID: `oneall:workflow-backed-sms-verification`
- Community status: `community-reviewed`
- Version: `1.1.0`
- Source commit: [`7211f1d5a024`](https://github.com/ONE-ALL-Church/RockRMS-OA-Public/tree/7211f1d5a024a164fdf883575585fb23b6a79f5d/Recipes/workflow-backed-sms-verification)
- License: [MIT](https://raw.githubusercontent.com/ONE-ALL-Church/RockRMS-OA-Public/7211f1d5a024a164fdf883575585fb23b6a79f5d/Recipes/workflow-backed-sms-verification/LICENSE)

## Superseded Contribution Patterns

- `oneall:anonymous-sms-verification-strict-match-and-session-recheck`

## Use Cases

- Optionally recognize a returning person during an anonymous registration or request form.
- Prefill or associate a final form action only after phone-possession verification.
- Keep short-lived verification state server-side without trusting browser-provided person identifiers.

## Adaptation Points

- `verificationWorkflowTypeGuid`: Set the GUID of the dedicated verification workflow type after creating and reviewing its attributes and actions.
- `intendedAction`: Choose a stable local action key that prevents a verified challenge from being reused on another form or operation.
- `mobilePhoneTypeValueId`: Set the local DefinedValue ID used for mobile phone numbers and verify that messaging-enabled semantics match the target instance.
- `matchFields`: Review first/nickname, last name, email, mobile number, messaging-enabled state, and birthdate as an exact-match policy appropriate for the form risk.
- `limits`: Set expiration, verification attempts, per-person sends, per-source sends, and upstream anonymous traffic controls.
- `authorizationAndCsrf`: Configure POST-only endpoint security, anti-CSRF behavior, TLS, monitoring, and staff-only access to workflow or communication review surfaces.

## Implementation

1. Review the immutable README, workflow contract, source, and static test before adapting the recipe.
2. Create a dedicated verification workflow and configure its SMS action to clear the plain Code attribute immediately after delivery.
3. Create POST-only start, check, and final-submit endpoints with only the required Lava commands and anti-CSRF behavior; enable Sql and WorkflowActivate for start, then Sql and ModifyWorkflow for check and final submission.
4. Keep endpoint SQL query-only and use ModifyWorkflow for Attempts, Verified, and ConsumedAt state changes.
5. Supply every local configuration value without introducing fallback production IDs or routes.
6. Integrate the final-submit recheck immediately before the protected form action, use only its server-resolved alias context, and make the protected operation idempotent with protectedActionIdempotencyKey.
7. Add anonymous traffic controls, monitoring, retention decisions, privacy review, and an accessible non-SMS path before launch.

## Validate

1. Run python3 tests/static_contract.py from the recipe directory.
2. Confirm one exact eligible match sends one code while zero or multiple matches send none.
3. Confirm all start responses have the same status, message, timing envelope where practical, and field shape.
4. Confirm invalid, expired, over-attempt, wrong-action, already-verified, and consumed challenges fail safely.
5. Race two final submissions and confirm both receive the same protectedActionIdempotencyKey while the protected operation produces only one business result.
6. Scan every Lava source file and confirm no SQL UPDATE, INSERT, DELETE, or MERGE statement is present.
7. Inspect browser responses and confirm no person ID, alias ID, or alias GUID is present.
8. Confirm per-person, per-source, resend, and upstream anonymous traffic limits work through the real proxy path.
9. Confirm the plain Code workflow value is cleared and review any rendered SMS retained in communication history.
10. Confirm the protected final action cannot run by submitting only browser fields without a valid server-side challenge.

## Security

- Data access: `writes`
- Authentication: Anonymous form request plus possession of the SMS destination; this is not account authentication or identity proofing.
- Authorization: The challenge may authorize only its configured intended form action; workflow and communication administration remain restricted to appropriate staff roles.
- Handles sensitive data: `true`
- Zero or multiple person matches fail closed, and every start response uses the same browser-visible shape.
- The browser never receives the matched person ID, alias ID, or alias GUID.
- The final endpoint rechecks expiration, verification, intended action, and the best-effort consumed marker on the server, then supplies an idempotency key to the protected operation.
- All SQL in the reference endpoints is query-only; Attempts, Verified, and ConsumedAt are written through ModifyWorkflow.
- A six-digit code hash reduces accidental exposure but does not resist an attacker who can read the database; database controls, rate limits, expiration, and retention remain required.
- SMS is vulnerable to interception and redirection and must not be described as strong identity proofing or phishing-resistant MFA.

## Compatibility

- Tested Rock versions: Not declared
- Last verified: 2026-07-10
- Rock `17`: `expected` - Reviewed against the Rock 17 model family; verify in the target instance.
- Rock `18`: `expected` - Reviewed against the Rock 18 model family; verify in the target instance.
- The originating implementation informed this rewrite, but the hardened public package requires live verification in each target instance.
- Verify WorkflowActivate and ModifyWorkflow command access, query-only SQL behavior, SQL Server CRYPT_GEN_RANDOM support, endpoint CSRF behavior, proxy-aware client IP handling, protected-action idempotency, and SMS retention before launch.
- The package was reviewed against the Rock 17/18 model family.

## Community Verification

- No consumer verification attestations have been submitted yet.
- Feedback and issues: https://github.com/ONE-ALL-Church/RockRMS-OA-Public/issues

## Reusable Learnings

- Treat anonymous recognition as a persisted, bounded server challenge rather than as a browser state transition.
- Fail closed on ambiguous person matches instead of selecting the oldest or lowest-ID candidate.
- Return an opaque session for every start request so browser response structure does not reveal whether a person exists.
- Never let a browser-supplied person or alias identifier establish verified applicant context.
- Bind each challenge to an intended action, enforce expiration and attempt limits, and make the final protected operation idempotent with the challenge session.
- Use query-only SQL for complex challenge lookup and hashing while routing workflow state changes through ModifyWorkflow.
- Separate the short-lived delivery code from durable audit state and make communication retention an explicit decision.

## Limitations

- SMS possession is not complete identity proofing, account authentication, or phishing-resistant MFA.
- The public package is a reference integration and has not been live-tested unchanged in a generic Rock instance.
- Exact match fields can exclude legitimate people with stale or shared data and require an accessible fallback.
- Context.Request.UserHostAddress may identify a reverse proxy unless the target environment provides a trusted client-address mechanism.
- ModifyWorkflow does not provide atomic compare-and-set behavior; concurrent final requests can both pass the recheck, so the protected operation must reject a repeated protectedActionIdempotencyKey or return the first result.
- A strict exactly-once requirement needs a purpose-built Rock action or API with an application-layer transaction; this reference intentionally contains no SQL writes.
