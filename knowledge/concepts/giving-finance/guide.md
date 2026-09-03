---
id: authored-giving-finance
title: Giving And Finance
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "e6563f7e6f51e7d1155719235f03d507f9a5ef36496c68d354c4bfcb787e696b"
---

# Giving And Finance

## Agent Summary

Treat giving as an end-to-end financial journey, not as a single transaction screen. For audits and troubleshooting, trace the path from the public giving action through the payment gateway, Rock financial transaction, transaction details, account designations, batch, receipt or contribution statement, and the reporting definition consuming the data. This is the guide’s primary operational rule and is supported by approved claim `claim:43ded9f19d576e7c826d`, including a bounded read-only verification of Rock’s transaction, detail, account, and reporting surfaces. [Giving Journey](https://community.rockrms.com/rocku/finance/giving-journey-1)

Keep these distinctions explicit:

- A transaction records the overall financial event; one or more transaction details allocate its amount to financial accounts.
- A gateway processes payment information, while Rock records the financial and ministry context.
- A batch groups transactions for control, reconciliation, and general-ledger integration.
- A receipt is associated with an individual processed transaction; a contribution statement is generated from a template and a defined population, period, transaction set, account set, and giving-unit configuration.
- Giving Analytics, Giving Journey, and Giving Alerts interpret giving patterns. They are not substitutes for exact transaction reconciliation.
- Pledges represent commitments over a stated period and are not themselves proof that payments were received.
- Security must be applied both to finance administration and to every report, data view, page, or external dashboard that exposes finance data.

Before changing a workflow or report, examine the donor experience and the back-office record path together. Approved claim `claim:cf2e3f3d823a4bf03441` identifies the donor experience, transaction record, account designation, follow-up, and reporting as separate concerns that should be evaluated together. Its applicability to a particular installation still requires configuration and version review. [Giving Journey](https://community.rockrms.com/rocku/finance/giving-journey-1)

## Scope And Boundaries

This guide covers evidence-supported operations for transactions, scheduled transactions, payment gateways, online and text giving, batches, contribution statements, pledges, giving units, businesses, fundraising transactions, giving automation, alerts, analytics, finance reporting, and finance security. The documented product behavior in the pack is primarily scoped to Rock v19.0. [Finance documentation](https://community.rockrms.com/documentation/church-management/finance)

Related concepts remain in their owning guides:

- Use the people and groups concepts for person matching, family structure, group membership, and broader record stewardship.
- Use the event-registration concept for registration configuration. The relevant finance boundary is that one registration can contain multiple registrants, while account, fee, and payment information is managed separately; reports must deliberately choose registration, registrant, payment, or transaction-detail grain. This is approved claim `claim:8236f070927c9ba07547`, scoped to v19.0. [Manage Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations)
- Use the workflows concept for general workflow design. This guide covers only the finance events that may initiate or feed a workflow.
- Use the reporting concept for general data-view, SQL, visualization, and dashboard engineering.
- Use the security concept for organization-wide authorization design.

No installation-specific gateway, account, batch schedule, statement template, job schedule, page authorization, plugin, or provider behavior is assumed here. When those values determine the answer, inspect them in the target installation and record the result under live verification.

## Mental Model

Rock’s foundational finance model begins with a person or other authorized record making a financial transaction. A simple transaction may have one detail; a transaction allocated to multiple purposes has multiple detail records. Each detail points to the account that identifies what that portion of the transaction is for. Transactions from a similar period can then be grouped into a batch, and batch totals can be carried to a general-ledger system while Rock retains transaction-level history. Pledges are separate commitments to give an amount during a stated period. [Intro to Financial Components](https://community.rockrms.com/documentation/church-management/finance/financial-components/intro-to-financial-components)

For an online card or bank-account payment, Rock acts as the transaction-entry system and sends payment information to the configured gateway. The gateway passes the transaction into the external processing chain; approved funds ultimately move through the merchant and banking systems. Rock’s record and the provider’s settlement are therefore related but not interchangeable evidence. [Intro to Payment Gateways](https://community.rockrms.com/documentation/church-management/finance/payment-gateways/intro-to-payment-gateways)

Use this operational chain when investigating finance behavior:

1. Identify the public or staff entry surface and its block settings.
2. Establish the authorized person or business and the intended giving unit.
3. Determine whether the event is one-time, scheduled, registration-related, fundraising-related, or another payment type.
4. Verify gateway acceptance or later scheduled processing.
5. Find the Rock transaction.
6. Inspect every transaction detail and its account.
7. Locate the batch and compare transaction, control, account, and currency totals.
8. Check receipt and statement inclusion rules separately.
9. Reproduce the report with its exact date, account, transaction-type, currency, giving-unit, and time-grain definitions.

This sequence implements approved claim `claim:43ded9f19d576e7c826d`; it does not imply that any specific organization’s transaction was inspected. [Giving Journey](https://community.rockrms.com/rocku/finance/giving-journey-1)

## Transactions

Rock’s online-giving tools distinguish one-time transactions from scheduled transactions. A one-time transaction is a single gift on a particular date. A scheduled transaction recurs according to a schedule. The same tools can also be used for payments other than donations, so an agent must verify the transaction type and purpose instead of inferring “contribution” from the page’s appearance. [Intro to Online Giving](https://community.rockrms.com/documentation/church-management/finance/online-giving/intro-to-online-giving)

A transaction may allocate money across several accounts. Always inspect the detail records before declaring that a gift went to the wrong fund or before summing a report. A transaction-level result and a detail-level result answer different questions; joining them without controlling the grain can duplicate transaction-level values. Rock’s official financial-component model documents the transaction-to-detail-to-account relationship. [Intro to Financial Components](https://community.rockrms.com/documentation/church-management/finance/financial-components/intro-to-financial-components)

The Utility Payment Entry block is documented as a flexible transaction-entry surface for online giving, on-site giving, scheduled transactions, fundraising, and text giving. Its settings can select a gateway, enable ACH or credit cards, establish a batch-name prefix and transaction source, expose eligible accounts, use account hierarchy or campus mapping, allow scheduled transactions, enable business or anonymous giving, select a receipt communication, and set the transaction type. Those are configuration capabilities, not proof of how a particular page is configured. [Advanced Utility Payment Entry Block Settings](https://community.rockrms.com/documentation/church-management/finance/advanced-finance/advanced-utility-payment-entry-block-settings)

For fundraising, the documented default is a Contribution transaction whose account comes from the opportunity group setting. Fundraising donations are tied to the fundraising opportunity’s Group Member; the documentation expressly distinguishes that linkage from event-registration finance linkage. Do not infer that a fundraising gift is financially attached to a registration. [Fundraising Financial Transactions](https://community.rockrms.com/documentation/church-management/finance/fundraising-groups/fundraising-financial-transactions)

A community recipe demonstrates an optional pattern in which a permitted URL value sets a custom financial transaction attribute, allowing reporting distinctions without creating a separate financial account for every purpose. Treat this as a community implementation example, not standard Rock behavior. Confirm finance-team agreement, installed block behavior, attribute placement, URL allow-listing, input safety, and reporting grain before adopting it. [Custom Financial Transaction Attributes recipe](https://community.rockrms.com/recipes/254)

## Payment Gateways

Gateway configuration is available under `Admin Tools > Settings > Financial Gateways` in the v19.0 documentation. Relevant settings include gateway type, active state, batch schedule, batch time offset, and provider-dependent mode. A gateway may require provider credentials, and it must also be selected on the applicable giving page after configuration. [Configure a Gateway](https://community.rockrms.com/documentation/church-management/finance/payment-gateways/configure-a-gateway)

Do not treat the gateway’s `Active` flag as a universal stop switch. The documentation warns that making a gateway inactive does not prevent charges for registrations where that gateway is already assigned. Similarly, a gateway’s mode can mean live versus test for one provider and hosted versus unhosted for another. Interpret the value according to the installed gateway type and provider documentation. [Configure a Gateway](https://community.rockrms.com/documentation/church-management/finance/payment-gateways/configure-a-gateway)

The supplied documentation advises against converting Rock’s Test Gateway into a live gateway merely by changing its type and adding real configuration. Preserve a clear separation between test and production payment paths. [Configure a Gateway](https://community.rockrms.com/documentation/church-management/finance/payment-gateways/configure-a-gateway)

A gateway migration has two independent tasks:

1. Route new gifts away from the old gateway by changing the Give Now block setting.
2. Move existing scheduled givers by presenting a transfer experience on Manage Giving Profiles.

For the documented Scheduled Transaction List Lava block, a gateway filter can restrict the displayed profiles, while a transfer-to gateway can turn the edit action into a transfer action. The new form copies relevant details; after the replacement transaction is completed, the old scheduled transaction is deleted. Verify the installed Rock version before relying on these block names or settings. [Transfer Gateways](https://community.rockrms.com/documentation/church-management/finance/payment-gateways/transfer-gateways)

## Online Giving And Receipts

The documented Give Now journey has entry, confirmation, and final stages. The entry surface collects giving and payment information, the optional confirmation stage lets the person review it, and the final stage presents the completion result. Block settings determine gateways, eligible payment types, accounts, transaction source, batch prefix, and receipt communication. [Giving Pages](https://community.rockrms.com/documentation/church-management/finance/online-giving/giving-pages)

For a same-day one-time online gift, Rock sends the payment to the gateway immediately. If the gateway accepts it, Rock immediately creates a transaction and adds it to an Online Transaction batch. An existing batch is used only when it is open, its prefix matches the Utility Payment Entry configuration, and the current time falls within the batch’s date range; otherwise Rock creates a batch for the current day. A future-dated one-time gift is processed like a scheduled transaction. [Use Batches for Online Giving](https://community.rockrms.com/documentation/church-management/finance/online-giving/use-batches-for-online-giving)

Scheduled transactions follow a different timing path: their resulting transactions must be downloaded later from the gateway. Therefore, the presence of a scheduled giving profile is not evidence that a particular payment has been processed or synchronized into Rock. [Use Batches for Online Giving](https://community.rockrms.com/documentation/church-management/finance/online-giving/use-batches-for-online-giving)

A transaction receipt and a contribution statement must be tested separately. On the Give Now surface, a receipt email is sent only when an applicable receipt template is configured. A successful gateway response or visible Rock transaction does not, by itself, prove that a receipt was configured, queued, or delivered. [Giving Pages](https://community.rockrms.com/documentation/church-management/finance/online-giving/giving-pages)

The Giving History page can filter the logged-in user’s transactions by date and account and can display summary totals and the matching transaction list. When business giving is enabled, individual and business histories can be selected separately. These public-history results are still subject to installed block settings and version behavior. [Giving Pages](https://community.rockrms.com/documentation/church-management/finance/online-giving/giving-pages)

## Text Giving

Text Giving requires a one-time setup experience backed by a Utility Payment Entry block and an SMS Pipeline. After setup, a person can send a configured keyword and amount. Setup, help, maximum-amount, refund, missing-amount, and failure responses are configurable. [Intro to Text Giving](https://community.rockrms.com/documentation/church-management/finance/text-giving/intro-to-text-giving)

The documented configuration includes giving and setup keywords, a maximum gift amount, financial account, setup page, refund keyword, processing delay, response templates, and optional saving of responses as communication records. If the financial account setting is blank, the person’s Text Giving account can be used; account selection may also interact with the Utility Payment Entry block’s campus mapping. [Configure Text Giving](https://community.rockrms.com/documentation/church-management/finance/text-giving/configure-text-giving)

A text refund works only within the configured processing delay. The delay exists because the transaction has not yet been sent through the gateway. If the delay is blank or zero, the text-refund function is disabled. Failure messaging also differs by timing: delayed processing relies on the Charge Future Transactions job’s SMS configuration, while immediate-processing failures use the SMS Pipeline response. [Configure Text Giving](https://community.rockrms.com/documentation/church-management/finance/text-giving/configure-text-giving)

Do not diagnose Text Giving solely from the inbound SMS. Inspect the matched person, registration/setup state, configured keyword, parsed amount, maximum, financial account, processing delay, gateway path, relevant job configuration, and saved communication history where enabled.

## Batches

Batches group transactions, preserve detailed history, and support transfer of summarized totals into a general-ledger process. In Rock v19.0 they are managed under `Finance > Batches`. [Batches](https://community.rockrms.com/documentation/church-management/finance/financial-components/batches)

A batch provides several independent controls and observations:

- Transaction total versus control amount.
- Transaction-item count versus control count.
- Variances for amount and count.
- Totals by financial account.
- Totals by currency type.
- Optional accounting code, notes, and batch attributes.
- Transaction-level or transaction-detail-level grids.
- An audit log of changes.

When one transaction is split across accounts, use the transaction-detail view to inspect each allocation. Do not attempt to resolve an account variance from a transaction-only list. [Batches](https://community.rockrms.com/documentation/church-management/finance/financial-components/batches)

Automated batches can temporarily have `Pending` status while transactions download. Rock prevents changing that status until the download completes; after completion the status changes to `Open`. A pending automated batch is therefore not ready for ordinary processing or manual status correction. [Batches](https://community.rockrms.com/documentation/church-management/finance/financial-components/batches)

Teller Import transactions may have amounts and accounts without contributor names. Those items require transaction matching; the account filter can be limited to accounts represented by the imported file. Treat matching and reconciliation as separate controls: identifying the giver does not prove that amounts, details, accounts, and control totals balance. [Batches](https://community.rockrms.com/documentation/church-management/finance/financial-components/batches)

Reopening a closed batch has separate entity-level security because reopening can disrupt coordination with the financial clearing process. The documented authorization is attached to `Rock.Model.FinancialBatch` through Entity Administration. Do not reopen or delete a batch merely because a finance page is visible to the operator. [Batches](https://community.rockrms.com/documentation/church-management/finance/financial-components/batches)

## Statements

Rock v19.0 documents a Windows-based Statement Generator downloaded from `Admin Tools > Settings > External Applications > Rock Statement Generator`. Login is limited to members of Finance Administration, Finance Worker, or Rock Administration. The supplied documentation states a Windows 7-or-newer requirement, but current operating-system support must be verified before installation. [Set Up the Statement Generator Software](https://community.rockrms.com/documentation/church-management/finance/contribution-statements/set-up-the-statement-generator-software)

A statement run should explicitly define:

1. The population: all eligible individuals, a data-view-filtered population, or one individual.
2. Whether inactive individuals and businesses are included.
3. The contribution template.
4. The relevant period and template-controlled transaction rules.
5. Output location, filename, sort, chapter size, and split behavior.
6. Minimum contribution amount and paper-statement suppression strategy.
7. Whether the generated summary agrees with the intended run.

The generator saves a summary of results alongside generated statements. That summary is evidence about generation, not evidence that files were printed, mailed, posted, or delivered. [Set Up the Statement Generator Software](https://community.rockrms.com/documentation/church-management/finance/contribution-statements/set-up-the-statement-generator-software)

Contribution templates under `Finance > Financial Settings > Contribution Templates` control both generated and web statement content. Their settings can restrict accounts, distinguish cash from non-cash currency types, filter refunded or same-day-corrected transactions, choose transaction types, optionally include pledge accounts, configure pledge inclusion rules, and define the report, footer, logo, and PDF settings. Pledges are not shown by default. [Use Contribution Statement Templates](https://community.rockrms.com/documentation/church-management/finance/contribution-statements/use-contribution-statement-templates)

Giving-unit configuration can materially alter statement results. By default, giving is summarized by family. `Combine Giving With` can associate a person’s giving with a selected family; leaving it blank marks the person for separate individual giving. Review this setting before concluding that a spouse’s gifts are absent, duplicated, or assigned to the wrong statement. [Family Giving](https://community.rockrms.com/documentation/church-management/finance/track-giving/family-giving)

The Statement Generator’s documented suppression attribute supports opt-out and opt-in strategies. Under the default described behavior, a `Yes` value for any giving-group member suppresses the family’s printed statement. Changing the attribute default and clearing existing values can alter the strategy, but any bulk update is an installation-specific data change and is outside this guide’s safe read-only verification boundary. [Set Up the Statement Generator Software](https://community.rockrms.com/documentation/church-management/finance/contribution-statements/set-up-the-statement-generator-software)

## Giving Units, Businesses, And Pledges

Person, family, and business attribution must be chosen deliberately. The person profile’s Contributions tab can show Giving Overview, scheduled transactions, pledges, yearly totals, transaction history, and reassignment tools. The supplied v19.0 documentation limits this tab to Finance Administration, Finance Worker, and Rock Administration by default. [View Giving on Person Profile](https://community.rockrms.com/documentation/church-management/finance/track-giving/view-giving-on-person-profile)

Business giving is enabled out of the box according to the v19.0 documentation and can be disabled in the Give Now Contributions block settings. When enabled, an associated person can give as the business, and the giving surfaces can expose the individual and business histories separately. Businesses retain historical financial records and cannot simply be deleted. [Intro to Businesses](https://community.rockrms.com/documentation/church-management/finance/businesses/intro-to-businesses)

Pledges record a commitment over a stated period. Statement templates include pledge data only when pledge accounts are selected, and their pledge filters independently determine such matters as child-account and non-cash inclusion. Do not equate pledge amount, received transaction amount, or statement-displayed pledge progress without verifying the applicable rules. [Intro to Financial Components](https://community.rockrms.com/documentation/church-management/finance/financial-components/intro-to-financial-components) [Use Contribution Statement Templates](https://community.rockrms.com/documentation/church-management/finance/contribution-statements/use-contribution-statement-templates)

## Giving Automation, Journey, And Alerts

Giving Automation settings drive much of the Giving Overview and are used by the Giving Automation job. The documented settings include whether automation is enabled, which days update giving-group classifications, included transaction types, and included accounts. Event-registration payments can be included in calculations, but the documentation states that they do not apply to Giving Alerts. [Giving Automation](https://community.rockrms.com/documentation/church-management/finance/track-giving/giving-automation)

Giving Journey classifies people into six stages: Non-Giver, New Giver, Consistent Giver, Occasional Giver, Lapsed Giver, and Former Giver. Evaluation proceeds from the top of the configured list until a match is found, making rule order significant. The conditions are customizable, and the update schedule need not run every day. Current stage, previous stage, and change date are stored as person attributes, while changes to the current stage are written to history. [Giving Journey](https://community.rockrms.com/documentation/church-management/finance/track-giving/giving-journey)

Giving Alerts are either Gratitude or Follow-up alerts and can be filtered or configured by criteria including campus and financial account. An alert may start a workflow, create a connection request, notify account participants, send a bus event, or notify a configured group. When a workflow is started, the authorized person on the financial transaction is the workflow initiator. Deleting the transaction that triggered an alert also deletes the alert. [Use Giving Alerts](https://community.rockrms.com/documentation/church-management/finance/track-giving/use-giving-alerts)

Treat these classifications as configured operational signals, not universal pastoral conclusions. Before changing them, compare the donor-facing journey, underlying transaction records, account filters, update schedule, and downstream follow-up behavior. This boundary is supported by approved claim `claim:cf2e3f3d823a4bf03441`. [Giving Journey](https://community.rockrms.com/rocku/finance/giving-journey-1)

## Reporting And Reconciliation

Giving Analytics supports chart and detail modes with filters for date range, giving-unit totals, data view, account eligibility, currency type, transaction source, and account. Its details are organized by giving unit, and return modes can represent givers, adults, children, or whole families. [Giving Analytics](https://community.rockrms.com/documentation/church-management/finance/track-giving/giving-analytics)

Giving Analytics is oriented toward people and ministry weeks rather than exact dollars grouped by transaction date. The default documented week runs Monday through Sunday, and contributions are associated with a Sunday date for this analysis. Consequently, its totals may not align with a transaction-date ledger calculation. Use transaction and detail records for exact reconciliation, and use Giving Analytics for its documented people-and-pattern purpose. [Giving Analytics](https://community.rockrms.com/documentation/church-management/finance/track-giving/giving-analytics)

Rock’s specialized finance reports also have distinct meanings. For example, the Transaction Fee Report filters by account and date and separates total, credit-card, and ACH fees. The Volunteer Generosity report relates volunteer service to whether people gave; it does not report their exact donation amounts. [Transaction Fee Report](https://community.rockrms.com/documentation/church-management/finance/finance-reports/transaction-fee-report) [Volunteer Generosity](https://community.rockrms.com/documentation/church-management/finance/finance-reports/volunteer-generosity)

For custom SQL reporting, approved claims `claim:797a78b9477adb5e5c0f` and `claim:c6565b995e9651232990` support window functions when a transaction-detail row must retain aggregate context. `SUM(...) OVER (PARTITION BY TransactionId)` can expose a transaction total beside each detail row without collapsing the details as `GROUP BY` would. Approved claim `claim:ca7b59ed2770c8682356` supports ranking functions such as row number, rank, dense rank, and n-tile for sequence or bucket analysis. These patterns were verified by bounded read-only queries against `FinancialTransactionDetail` in one connected Rock SQL Server, but table availability, permissions, and the target report’s grain still require local verification. [SQL Window Functions](https://www.triumph.tech/resources/sql-window-functions)

When embedding Power BI or a similar external report, secure the Rock page and blocks and separately verify the external platform’s licensing and authorization. Approved claim `claim:60d40983fd53c0173dd9` confirms the operational need to pair both layers. Its bounded Rock verification found page, block, and authorization surfaces; it did not verify external BI licensing. [Community media source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz)

## Security And Administration

The v19.0 finance roles separate routine processing from configuration:

- `RSR - Finance Worker` can view and edit basic finance information such as transactions and batches but cannot modify core finance configuration such as accounts.
- `RSR - Finance Administration` can view and edit finance information, including configuration.

Finance pages, the person Contributions tab, check-scanner login, finance data-view filters, and report creation are protected. However, a created data view or report can be run by anyone who has view permission to that object. Secure the output object, not merely the ability to create it. [Security for Finance](https://community.rockrms.com/documentation/church-management/finance/advanced-finance/security-for-finance)

Reopening or deleting batches, initiating refunds, and filtering a transaction list by person have additional securable actions. Visibility of the containing page does not prove authorization for these operations. [Security for Finance](https://community.rockrms.com/documentation/church-management/finance/advanced-finance/security-for-finance)

Apply least privilege and verify authorization as the affected user. For external dashboards, test both Rock-side access and provider-side identity and licensing. Never infer effective access solely from role membership, page placement, or an administrator’s successful test.

## Version And Authority Caveats

Most official documentation in this pack is marked v19.0. Confirm the installed Rock version, block generation, gateway package, provider capabilities, and local configuration before applying paths or setting names.

The pack includes these narrower version signals:

- Rock v18.1 release notes report new mobile Financial Batch Detail and Financial Batch List blocks supporting batch viewing and related batch operations. This does not establish that an installation has deployed or authorized them. [Rock release notes](https://www.rockrms.com/releasenotes)
- Rock v18.3 release notes report fixes to Giving History API behavior involving blank `Combine Giving With` values and exclusion of family giving. Interpret older API results with the exact patch version in mind. [Rock release notes](https://www.rockrms.com/releasenotes)
- The supplied release-note excerpt identifies Rock v20.0 as alpha and describes contribution-statement block conversion, redesign and renaming of the public scheduled-transaction list, removal of a legacy TextToGiveSettings block, and other finance changes. These are upcoming or alpha behaviors, not the v19.0 baseline. [Rock release notes](https://www.rockrms.com/releasenotes)

The immutable source excerpts in the pack come from commit `471fd303d111b2e46218228dbc1e93dba8856fa3` on the `develop` branch. They can clarify implementation but do not prove the installed schema or configuration. For example, the analytical source model describes a record as a transaction-plus-detail combination, so one multi-account transaction can produce multiple analytical source records. That supports careful grain selection but remains a source-code observation. [AnalyticsSourceFinancialTransaction at the supplied commit](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Reporting/AnalyticsSourceFinancialTransaction/AnalyticsSourceFinancialTransaction.cs)

Community media, recipes, and SQL patterns are examples or reviewed operational guidance rather than official product guarantees. Live verification cited by approved claims was bounded and read-only; it demonstrates that the described surfaces or SQL patterns existed in the reviewed instance, not that every installation has identical data or configuration.

## Troubleshooting Decision Tree

### A gateway accepted a payment, but no Rock transaction is visible

1. Confirm whether the gift was same-day one-time, future-dated one-time, or scheduled. Same-day one-time gifts create a Rock transaction after gateway acceptance; future-dated and recurring gifts follow scheduled processing.
2. Verify the exact giving page and gateway selected by its block.
3. For scheduled processing, inspect the applicable download or charge process and its timing rather than expecting an immediate transaction.
4. Search using the authorized person or business, transaction date range, source, amount, and account without assuming a single account detail.
5. If the gateway shows a payment but Rock remains empty, stop before creating a manual duplicate. Preserve the provider reference and investigate synchronization. [Use Batches for Online Giving](https://community.rockrms.com/documentation/church-management/finance/online-giving/use-batches-for-online-giving)

### A transaction is in the wrong batch or no expected batch exists

1. Inspect the transaction’s originating block and batch-name prefix.
2. Inspect the gateway’s batch schedule and time offset.
3. Check whether the candidate batch was open.
4. Compare the transaction time with the batch start and end times.
5. For automated downloads, determine whether the batch is still pending.
6. Do not rename or move financial records until the expected grouping rule and downstream reconciliation impact are understood. [Configure a Gateway](https://community.rockrms.com/documentation/church-management/finance/payment-gateways/configure-a-gateway) [Use Batches for Online Giving](https://community.rockrms.com/documentation/church-management/finance/online-giving/use-batches-for-online-giving)

### A batch has an amount, count, account, or currency variance

1. Compare transaction total with control amount.
2. Compare transaction count with control count.
3. Switch to transaction-detail rows when transactions split across accounts.
4. Compare totals by account and currency type.
5. Review unmatched imported transactions and contributor matching separately.
6. Review the batch audit log for edits.
7. Stop before closing, reopening, deleting, or exporting the batch if the variance is unresolved. [Batches](https://community.rockrms.com/documentation/church-management/finance/financial-components/batches)

### A statement omits a gift, includes an unexpected gift, or combines the wrong people

1. Confirm the statement period and selected population.
2. Inspect `Combine Giving With` and whether the person gives individually or with a family.
3. Confirm the authorized person or business on the transaction.
4. Inspect the template’s account, transaction-type, currency-type, refund, and same-day-correction filters.
5. Inspect pledge settings separately from received contributions.
6. Check minimum contribution and paper-suppression settings.
7. Generate a single-person test and compare it with the source transaction details before changing production templates. [Family Giving](https://community.rockrms.com/documentation/church-management/finance/track-giving/family-giving) [Use Contribution Statement Templates](https://community.rockrms.com/documentation/church-management/finance/contribution-statements/use-contribution-statement-templates)

### Giving Analytics does not match a transaction-date total

1. Identify whether the question concerns exact dollars, transaction details, people, or giving patterns.
2. Compare the same account, transaction-type, currency, and giving-unit filters.
3. Account for Giving Analytics’ ministry-week and Sunday-date grouping.
4. Check whether family combining changes the displayed giving unit.
5. Use transaction-detail reporting for ledger reconciliation; retain Giving Analytics for people-and-pattern analysis. [Giving Analytics](https://community.rockrms.com/documentation/church-management/finance/track-giving/giving-analytics)

### Giving Overview, Journey, or alerts appear stale or incorrect

1. Confirm Giving Automation is enabled.
2. Inspect the job’s latest completed run and configured update days.
3. Verify included transaction types and accounts.
4. For Giving Journey, inspect rule order because the first matching stage wins.
5. For alerts, inspect campus, account, alert type, and downstream workflow or connection settings.
6. Recalculate or change configuration only after the source transactions and expected inclusion rules are established. [Giving Automation](https://community.rockrms.com/documentation/church-management/finance/track-giving/giving-automation) [Giving Journey](https://community.rockrms.com/documentation/church-management/finance/track-giving/giving-journey)

### Text Giving setup, processing, refund, or failure messaging does not work

1. Confirm the SMS Pipeline received the message and matched the intended person.
2. Check the giving or setup keyword and amount parsing.
3. Confirm registration/setup and the Utility Payment Entry configuration.
4. Verify the selected account, gateway, and maximum amount.
5. Inspect Processing Delay Minutes before testing a text refund.
6. If delayed processing is enabled, inspect the Charge Future Transactions job’s SMS sender; otherwise inspect the pipeline’s failure response.
7. If response saving is enabled, use communication history to trace the automated reply. [Configure Text Giving](https://community.rockrms.com/documentation/church-management/finance/text-giving/configure-text-giving)

### Users can see finance data they should not see, or cannot see an embedded dashboard

1. Test the Rock page, block, data view, and report as the affected user.
2. Distinguish Finance Worker from Finance Administration permissions.
3. Check object-level view permissions even if report creation is protected.
4. For embedded BI, verify Rock authorization and external identity, licensing, and report permissions independently.
5. Stop when one layer remains unverified; do not describe the dashboard as secured or available based on the other layer alone. [Security for Finance](https://community.rockrms.com/documentation/church-management/finance/advanced-finance/security-for-finance) [Community media source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz)

## Agent Task Recipes

### Recipe: Trace a public gift end to end

**Outcome:** Account for a gift from donor action through its Rock records and reporting treatment.

1. Record the entry surface, date, intended person or business, amount, and intended account without collecting payment secrets.
2. Inspect the page’s gateway, transaction type, source, account, batch-prefix, and receipt settings.
3. Determine whether processing is immediate, future-dated, or recurring.
4. Confirm gateway outcome using a safe provider reference.
5. Locate the Rock transaction and inspect all transaction details.
6. Confirm the account on each detail and the sum of the allocations.
7. Locate the batch and compare status, totals, control values, account totals, and currency totals.
8. Check receipt configuration and evidence independently.
9. Reproduce any report or statement with its exact inclusion rules.
10. Record which links were observed and which remain unverified.

**Inspect:**

- Authorized person or business.
- Transaction type and source.
- Detail-level account allocations.
- Batch status and variances.
- Giving-unit configuration.
- Report or statement grain.

**Do not assume:**

- Gateway acceptance proves Rock synchronization.
- A transaction has only one account.
- A receipt was sent.
- A report uses transaction-date grain.

**Stop when:**

- Resolving the discrepancy would require a refund, new transaction, account reassignment, batch reopening, or other financial write without authorization.

This recipe operationalizes approved claim `claim:43ded9f19d576e7c826d`. [Giving Journey](https://community.rockrms.com/rocku/finance/giving-journey-1)

### Recipe: Validate an online giving page before launch

**Outcome:** Establish that the page’s configuration expresses the intended finance path.

1. Identify the installed Rock version and exact Utility Payment Entry or legacy block.
2. Verify the gateway and whether its mode represents test/live or hosted/unhosted.
3. Confirm enabled payment methods.
4. Confirm transaction type, source, accounts, campus mapping, and scheduled-giving option.
5. Confirm batch prefix and gateway batch timing.
6. Confirm business, anonymous, CAPTCHA, confirmation-page, and receipt settings as applicable.
7. Execute an authorized non-production test.
8. Verify the gateway result, Rock transaction, details, account, batch, receipt behavior, and visible giving history.

**Do not assume:**

- A gateway named “Test” is harmless if it has been reconfigured.
- An active gateway is selected by the page.
- A successful confirmation page proves downstream records.

**Stop when:**

- Only a production charge could complete the test and production authorization has not been granted.

[Advanced Utility Payment Entry Block Settings](https://community.rockrms.com/documentation/church-management/finance/advanced-finance/advanced-utility-payment-entry-block-settings) [Configure a Gateway](https://community.rockrms.com/documentation/church-management/finance/payment-gateways/configure-a-gateway)

### Recipe: Reconcile an online batch

**Outcome:** Explain every batch total and variance at the correct grain.

1. Confirm batch status; wait for an automated pending batch to complete.
2. Record the transaction total, control amount, and amount variance.
3. Record transaction count, control count, and count variance.
4. Review transaction details for split-account gifts.
5. Compare account and currency totals.
6. Resolve unmatched imported items through the intended matching workflow.
7. Review the audit log for edits.
8. Compare the reconciled batch total with the external settlement or general-ledger handoff according to the organization’s documented process.

**Stop when:**

- The batch remains out of balance.
- External settlement timing is not known.
- Reopening or modifying a closed batch would be required.

[Batches](https://community.rockrms.com/documentation/church-management/finance/financial-components/batches)

### Recipe: Generate and validate contribution statements

**Outcome:** Produce a reviewable statement set whose population and finance rules are explicit.

1. Verify Statement Generator compatibility, user role, and Rock version.
2. Select the population and decide how inactive people and businesses are handled.
3. Review family and individual giving-unit settings for exceptions.
4. Copy or select a contribution template.
5. Verify accounts, currency types, transaction types, refund rules, same-day corrections, and pledge settings.
6. Set period, minimum contribution, suppression behavior, sort, split, and output settings.
7. Generate single-person samples representing family, individual, business, refund, non-cash, and pledge scenarios that actually apply.
8. Compare each sample with underlying transaction details.
9. Run the full generation.
10. Preserve and review the generated summary separately from printing or delivery.

**Do not assume:**

- Generated means delivered.
- Family membership alone determines the giving unit.
- Pledges appear by default.
- Web and PDF output are visually identical.

[Set Up the Statement Generator Software](https://community.rockrms.com/documentation/church-management/finance/contribution-statements/set-up-the-statement-generator-software) [Use Contribution Statement Templates](https://community.rockrms.com/documentation/church-management/finance/contribution-statements/use-contribution-statement-templates)

### Recipe: Build a detail-preserving finance report

**Outcome:** Show each account allocation with transaction-level context without accidental row collapse.

1. Define whether the output grain is transaction, transaction detail, giving unit, person, family, registration, registrant, or batch.
2. Begin with the entity that represents that grain.
3. For detail-level reporting, retain one row per financial transaction detail.
4. Use `OVER (PARTITION BY TransactionId)` when transaction totals or detail counts must appear beside each detail.
5. Add ranking functions only when the report requires sequence, rank, or buckets.
6. Test a transaction split across multiple accounts.
7. Compare the sum of detail rows with the expected transaction and batch totals.
8. Secure the report and every page or dashboard that exposes it.

**Do not assume:**

- `GROUP BY` and a window function preserve the same rows.
- One registration equals one registrant.
- One transaction equals one account allocation.
- A report creator’s permission protects report viewers.

This recipe is supported by approved claims `claim:797a78b9477adb5e5c0f`, `claim:c6565b995e9651232990`, `claim:ca7b59ed2770c8682356`, and `claim:8236f070927c9ba07547`. [SQL Window Functions](https://www.triumph.tech/resources/sql-window-functions) [Manage Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations)

### Recipe: Transfer scheduled giving to a new gateway

**Outcome:** Route new gifts to the new provider while giving existing scheduled donors a controlled transfer path.

1. Verify the installed block generation and gateway-provider support.
2. Configure and test the new gateway without modifying the Test Gateway into a live gateway.
3. Change the Give Now surface so new profiles use the new gateway.
4. Configure the Manage Giving Profiles surface to identify old-gateway profiles and offer transfer.
5. Test the transfer with an authorized non-production profile.
6. Verify creation of the replacement profile and deletion of the old profile only after completion.
7. Track remaining old-gateway profiles without exposing payment data.
8. Keep the old gateway available only as required by the migration and provider plan.

**Do not assume:**

- Changing Give Now migrates existing schedules.
- Making the old gateway inactive stops every assigned charge.
- Gateway-held payment credentials can be exported.

[Transfer Gateways](https://community.rockrms.com/documentation/church-management/finance/payment-gateways/transfer-gateways) [Configure a Gateway](https://community.rockrms.com/documentation/church-management/finance/payment-gateways/configure-a-gateway)

## Known Gaps And Live Verification

The evidence pack does not establish the following for any target installation:

- Installed Rock version, patch level, or v20 migration state.
- Installed gateway packages, provider features, credentials, settlement schedule, licensing, or PCI scope.
- Actual giving-page, text-giving, batch, account, receipt, statement, automation, report, or security configuration.
- Whether scheduled transactions and processed-payment counts are synchronized from the provider.
- Whether jobs completed successfully or whether communications were delivered.
- Whether custom transaction attributes, community recipes, mobile batch blocks, analytics tables, or external BI embeds are installed and in use.
- Whether an observed discrepancy can be reproduced.
- Whether a statement set was printed, mailed, published, or received.

Use a separate, bounded, read-only review for these questions. Confirm version and plugin state, inspect configuration, reproduce with approved test data, and use existence or count checks that avoid exposing donor information. Do not publish raw SQL output, payment references, person identifiers, organization-specific IDs, or private transaction evidence.

The supplied live verification supports only the public-safe conclusions attached to approved claims: relevant finance and authorization surfaces existed in the reviewed instance, and the stated window-function patterns executed against its financial transaction details. It does not establish universal schema, configuration, external licensing, or current status.

## Source Map

### Approved claim spine

- `claim:43ded9f19d576e7c826d` — trace the full public-action-to-transaction-detail-account-receipt-reporting path. [Giving Journey](https://community.rockrms.com/rocku/finance/giving-journey-1)
- `claim:cf2e3f3d823a4bf03441` — evaluate donor experience and back-office records together before changing giving workflows. [Giving Journey](https://community.rockrms.com/rocku/finance/giving-journey-1)
- `claim:60d40983fd53c0173dd9` — pair Rock authorization with external BI licensing and permissions. [Community media source](https://community.rockrms.com/community-hubs/2KmggZ0dmR/media/kdlEdprmjz)
- `claim:797a78b9477adb5e5c0f`, `claim:c6565b995e9651232990`, and `claim:ca7b59ed2770c8682356` — window and ranking functions for detail-preserving Rock SQL reporting. [SQL Window Functions](https://www.triumph.tech/resources/sql-window-functions)
- `claim:8236f070927c9ba07547` — registration, registrant, account, fee, and payment grain must be selected explicitly. [Manage Event Registrations](https://community.rockrms.com/documentation/church-management/event-calendar/event-registrations/manage-event-registrations)

### Official v19.0 documentation

- [Finance](https://community.rockrms.com/documentation/church-management/finance)
- [Intro to Financial Components](https://community.rockrms.com/documentation/church-management/finance/financial-components/intro-to-financial-components)
- [Batches](https://community.rockrms.com/documentation/church-management/finance/financial-components/batches)
- [Intro to Online Giving](https://community.rockrms.com/documentation/church-management/finance/online-giving/intro-to-online-giving)
- [Giving Pages](https://community.rockrms.com/documentation/church-management/finance/online-giving/giving-pages)
- [Use Batches for Online Giving](https://community.rockrms.com/documentation/church-management/finance/online-giving/use-batches-for-online-giving)
- [Configure a Gateway](https://community.rockrms.com/documentation/church-management/finance/payment-gateways/configure-a-gateway)
- [Transfer Gateways](https://community.rockrms.com/documentation/church-management/finance/payment-gateways/transfer-gateways)
- [Configure Text Giving](https://community.rockrms.com/documentation/church-management/finance/text-giving/configure-text-giving)
- [Family Giving](https://community.rockrms.com/documentation/church-management/finance/track-giving/family-giving)
- [Giving Automation](https://community.rockrms.com/documentation/church-management/finance/track-giving/giving-automation)
- [Giving Journey](https://community.rockrms.com/documentation/church-management/finance/track-giving/giving-journey)
- [Use Giving Alerts](https://community.rockrms.com/documentation/church-management/finance/track-giving/use-giving-alerts)
- [Giving Analytics](https://community.rockrms.com/documentation/church-management/finance/track-giving/giving-analytics)
- [Set Up the Statement Generator Software](https://community.rockrms.com/documentation/church-management/finance/contribution-statements/set-up-the-statement-generator-software)
- [Use Contribution Statement Templates](https://community.rockrms.com/documentation/church-management/finance/contribution-statements/use-contribution-statement-templates)
- [Security for Finance](https://community.rockrms.com/documentation/church-management/finance/advanced-finance/security-for-finance)

### Versioned and implementation evidence

- [Rock Core Release Notes](https://www.rockrms.com/releasenotes)
- [AnalyticsSourceFinancialTransaction at immutable commit `471fd303d111b2e46218228dbc1e93dba8856fa3`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Reporting/AnalyticsSourceFinancialTransaction/AnalyticsSourceFinancialTransaction.cs)

### Community example

- [Custom Financial Transaction Attributes](https://community.rockrms.com/recipes/254) — optional community reporting pattern, not official default behavior.