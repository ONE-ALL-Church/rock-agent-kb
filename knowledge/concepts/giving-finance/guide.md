---
id: authored-giving-finance
title: Giving And Finance
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Giving And Finance

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Giving And Finance index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Stable method rows: `../../model-map/stable-methods.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Pre-alpha/upcoming method rows: `../../model-map/latest-methods.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Rock RMS finance is the system area that records, classifies, processes, reconciles, reports, and communicates financial activity. In practice, agents working in this area usually deal with five operational surfaces:

1. **Giving entry and payment capture**: online giving, text giving, scheduled gifts, manual entry, check scanning, imported giving, and gateway-backed payments.
2. **Financial recordkeeping**: transactions, transaction details, payment details, accounts, batches, pledges, businesses, refunds, and non-cash assets.
3. **Reconciliation and controls**: open and closed batches, control amounts, item counts, gateway deposits, audit history, payment reversals, and statement exclusions.
4. **Donor-facing output**: receipts, giving history, contribution statements, public account names, household combine-giving logic, and opt-out behavior.
5. **Analytics and automation**: giving analytics, BI models, giving unit facts, giving alerts, recurring-giving prompts, pledge reporting, and external giving imports.

The official Rock finance training index frames the finance area around accounts, batches, transactions, scheduled transactions, refunds, businesses, online giving, check matching, pledges, analytics, benevolence, contribution statements, settings, fundraising groups, giving journey, giving overview, giving alerts, and text giving ([RockU Finance](https://community.rockrms.com/rocku/finance)). The most complete official written source in this pack is *Rock Solid Finances*, which includes chapters for financial components, transactions, batches, accounts, pledges, payment gateways, statement generation, giving analytics, benevolence, security, and version-specific updates ([Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15)).

For agent work, the critical mental model is this:

- A **FinancialTransaction** is the transaction header: who authorized it, when it happened, what payment method/gateway/source was used, and which batch contains it.
- A **FinancialTransactionDetail** is the allocation line: which financial account received which amount. One transaction can have multiple details.
- A **FinancialPaymentDetail** stores payment-specific metadata such as currency type, credit-card type, check information, and gateway-related payment details.
- A **FinancialBatch** is the reconciliation container. Since older Rock versions, all transactions are expected to belong to a batch according to the version notes in *Rock Solid Finances* ([Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15)).
- A **FinancialAccount** is the fund, ledger-facing account, campaign, or payment destination used by transaction details, scheduled transaction details, pledges, receipts, and statement filters.
- A **FinancialScheduledTransaction** is the recurring or future payment plan header. It has detail rows that mirror account allocations and may sync state with the gateway.
- A **FinancialPledge** records an intended giving commitment to an account over a date range; pledge analytics compare pledge targets with actual gifts.
- A **giving unit** is the reporting unit used for family or household giving analytics. It is related to Person, PersonAlias, family groups, and Rock's combine-giving settings.

Agents should not treat finance data as just a table query problem. Finance work touches security, legal/tax communication, gateway state, family merge history, payment processor behavior, reporting performance, and user trust. Before changing configuration or data, inspect the live instance for:

- Rock version and enabled finance blocks.
- Account tax deductibility and public names.
- Gateway plugin, payment processor, and recurring profile sync behavior.
- Batch status, control amount, item count, and deposit date conventions.
- Whether a transaction is a gift, payment, refund, reversal, pledge payment, imported record, or test record.
- Whether statements are generated from the desktop Statement Generator, online statement blocks, APIs, saved settings, or custom reports.
- Whether a person is an individual or business record and whether gifts are combined with household members.

When facts are not fully established by the source pack, this guide names what to verify in a live Rock instance instead of pretending every installation behaves the same.

## 2. Scope And Terminology

This guide covers Rock RMS giving and finance concepts that agents need for real operational work. It includes:

- Accounts.
- Transactions and transaction details.
- Payment details.
- Batches.
- Scheduled transactions.
- Refunds and reversals.
- Businesses.
- Online giving.
- Text giving.
- Check matching and check scanning.
- Pledges.
- Contribution statements and receipts.
- Giving analytics and BI reporting.
- Benevolence and fundraising-adjacent finance flows.
- Security, reporting, workflow, Lava, API, mobile, and source-code landmarks.

This guide does not replace legal, tax, accounting, or payment-card compliance advice. Rock stores and presents financial records, but each organization must verify its contribution receipting language, tax-deductible account policies, refund practices, retention rules, and PCI/payment gateway responsibilities with qualified advisors.

Key terms:

**Account**
A Rock `FinancialAccount`. It is the destination for a transaction detail. Accounts may be tax-deductible or not, may have public names for donor-facing receipts, and may be nested or categorized depending on the instance. RockU includes accounts as a core finance training topic ([Accounts](https://community.rockrms.com/rocku/finance/accounts)).

**Transaction**
A Rock `FinancialTransaction`. It is the header record for a financial event. It commonly references an authorized person alias, a batch, a payment detail, a transaction type, a source, and transaction date fields. RockU treats transactions as a core finance area ([Transactions](https://community.rockrms.com/rocku/finance/transactions)).

**Transaction Detail**
A Rock `FinancialTransactionDetail`. It is the allocation line under a transaction. A single donor payment can be split between multiple accounts, producing multiple detail rows. The analytics source model explicitly states that the analytics source record represents a combination of `FinancialTransaction` and `FinancialTransactionDetail`, so a single transaction with multiple accounts becomes multiple analytic records ([AnalyticsSourceFinancialTransaction.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsSourceFinancialTransaction/AnalyticsSourceFinancialTransaction.cs)).

**Payment Detail**
A Rock payment metadata record associated with the transaction. It stores currency and payment-specific information such as cash/check/card type, gateway details, and check metadata. The dev SQL seed scripts in the source pack show payment-detail variables for currency type, credit-card type, gateway, and MICR-related fields ([Populate_FinancialTransactions_Contributions.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Populate_FinancialTransactions_Contributions.sql)).

**Batch**
A Rock `FinancialBatch`. It groups financial transactions for control, reconciliation, deposit, and posting workflows. RockU includes batches as a central finance training item ([Batches](https://community.rockrms.com/rocku/finance/batches)). The official finance documentation notes version-era changes around transactions needing to be in batches and later updates around batch blocks, audit logs, automated batches, teller import, and financial batch attributes ([Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15)).

**Gateway**
A configured payment processor integration. Gateways process cards/ACH and often own recurring profile state. The official finance book includes payment gateways as a dedicated configuration area and release-note history references gateway-specific behavior ([Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15)).

**Scheduled Transaction**
A recurring or future payment profile in Rock, typically represented by `FinancialScheduledTransaction` plus one or more scheduled transaction detail rows. RockU has scheduled-transaction training ([Scheduled Transactions](https://community.rockrms.com/rocku/finance/scheduled-transactions)). Source snippets for payment-plan support show that scheduled transaction payment plans can track frequency, number of payments, amount per payment, start date, planned amount, processed payments, and remaining payments, with caveats when gateway sync is incomplete ([PaymentPlan.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlan.cs)).

**Contribution**
A gift transaction type. In source snippets, the contribution defined value GUID appears in finance statement and transaction population SQL, which agents can use as a landmark but should verify in the live instance before hardcoding IDs ([spFinance_ContributionStatementQuery.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.4/202104291818024_GroupSalutation_spFinance_ContributionStatementQuery.sql)).

**Receipt**
A donor-facing confirmation after a payment or gift. Receipts may be system emails, gateway confirmations, or custom communication templates. A community recipe shows one pattern for differentiating gift language from payment language by account tax deductibility, but because recipes are not official and may not follow best practice, agents should treat it as an example rather than policy ([Giving Receipt System Email Shortcodes](https://community.rockrms.com/recipes/510/giving-receipt-system-email-shortcodes)).

**Contribution Statement**
A periodic donor statement, usually annual or date-range based. It is generated by Rock's statement tools or statement APIs using configured accounts, transaction types, currency types, household rules, addresses, and filters. RockU covers contribution statements ([Contribution Statements](https://community.rockrms.com/rocku/finance/contribution-statements)), and the source pack includes Statement Generator transaction settings from Rock source ([FinancialStatementTemplateTransactionSetting.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Applications/Wpf/StatementGenerator/Client/FinancialStatementTemplateTransactionSetting.cs)).

**Pledge**
A commitment to give to a financial account over a date range. RockU includes pledges ([Pledges](https://community.rockrms.com/rocku/finance/pledges)); release notes mention a v19.1 finance change adding a giving date range filter to the Financial Pledge Analytics block and renaming the existing date filter to Pledge Date Range for clarity ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

**Business**
A Rock person-like record with business record type. Businesses can give and receive contribution detail in Rock finance. RockU includes businesses as a finance topic ([Businesses](https://community.rockrms.com/rocku/finance/businesses)). Statement SQL in the source pack explicitly checks whether the selected `PersonId` has a business record type when preparing contribution-statement output ([spFinance_ContributionStatementQuery.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.4/202104291818024_GroupSalutation_spFinance_ContributionStatementQuery.sql)).

**Giving Unit**
A reporting concept that often aligns with a family/household but is more precise than "family" because it can account for combine-giving choices and historical membership. Rock analytics files distinguish authorized family keys from giving unit keys ([AnalyticsFactFinancialTransaction.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsFactFinancialTransaction/AnalyticsFactFinancialTransaction.cs)).

## 3. Giving And Finance Mental Model

Rock finance is easiest to reason about as a pipeline:

1. **Intent**: A donor, business, attendee, or system decides to give or pay. The intent may originate from online giving, text giving, mobile, a registration payment, an imported external system, a check, a cash envelope, a benevolence flow, or a manual finance office entry.
2. **Identity**: Rock associates the financial action with a person alias, business, saved account, or fallback person. This link is essential for receipts, statements, analytics, follow-up, and household combining.
3. **Payment method**: The payment is cash, check, credit card, ACH, non-cash asset, or another configured currency type. Payment detail captures method-specific metadata.
4. **Allocation**: The payment amount is split into one or more transaction details, each pointing to a financial account.
5. **Processing**: If a gateway is involved, Rock and the gateway exchange authorization, recurring profile, transaction code, settlement, reversal, and failure state.
6. **Batching**: The transaction lands in a batch. Batches provide control totals, deposit dates, status, and reconciliation workflow.
7. **Communication**: The payer may receive a receipt. Later, eligible gifts may appear on contribution statements.
8. **Reporting**: Finance teams use lists, reports, data views, analytics views, BI exports, giving overview blocks, and pledge analytics.
9. **Care and engagement**: Giving patterns may drive giving alerts, giving journey, recurring-giving prompts, pastoral care, stewardship workflows, or segmentation.

This pipeline explains most troubleshooting. If a transaction is missing from a statement, start by asking where it fell out of the pipeline:

- Was the transaction created?
- Is it the correct transaction type?
- Does it have details?
- Are the details tied to selected accounts?
- Are those accounts tax-deductible or included in statement settings?
- Is the authorized person alias correct?
- Is the donor excluded by combine-giving settings or statement filters?
- Was the transaction corrected, refunded, reversed, or hidden by statement template rules?
- Is the date range using transaction date, batch date, or another reporting date?
- Is the report using raw finance tables, analytics source tables, a stale BI model, or a saved statement generator setting?

The source-code analytics model reinforces that reporting often happens at the transaction-detail grain, not only the transaction header grain. `AnalyticsSourceFinancialTransaction` is generated from transaction plus detail, so split gifts become multiple rows in analytics ([AnalyticsSourceFinancialTransaction.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsSourceFinancialTransaction/AnalyticsSourceFinancialTransaction.cs)). Agents should therefore avoid summing transaction headers when the question is account-specific.

## 4. Source Authority And How To Use This Guide

Use sources in this order:

1. **Official Rock documentation and release notes**: Highest authority for intended behavior, version changes, block names, and supported configuration. In this pack that includes *Rock Solid Finances* and Rock Core Release Notes ([Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15), [Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
2. **Rock source code**: Best for entity relationships, exact property names, generated APIs, internal service caveats, analytics table grain, and statement generator settings. Source files are authoritative for a branch but may represent develop branch rather than the installed version ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)).
3. **RockU training**: Good for operational orientation and topic coverage, but the hydrated excerpts in this pack contain mostly titles and durations rather than transcripts. Use RockU as topic confirmation and a source pointer, not as the only evidence ([RockU Finance](https://community.rockrms.com/rocku/finance)).
4. **Developer/mobile docs**: Good for block-level configuration, especially newer mobile finance blocks. The Financial Batch List and Financial Batch Detail mobile docs include block settings and version availability ([Financial Batch List](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-list), [Financial Batch Detail](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-detail)).
5. **Community recipes**: Useful examples for workflows, Lava, SQL, imports, and customization patterns, but not core-team-reviewed. Recipes explicitly warn that contributed content may not follow best practices or may affect performance/security, so agents must validate before adoption ([Syncing Planning Center Giving into Rock RMS](https://community.rockrms.com/recipes/521/syncing-planning-center-giving-into-rock-rms), [Automate asking Regular Givers to Set up Recurring Giving](https://community.rockrms.com/recipes/122), [Custom Financial Transaction Attributes](https://community.rockrms.com/recipes/254)).
6. **Third-party resources**: Helpful context, especially for performance and analytics, but lower authority than official docs/source. Triumph's Giving Unit Analytics resource points to the performance value of analytics source giving-unit tables, but this pack did not hydrate a detailed excerpt, so verify in official docs or the live schema before relying on details ([Giving Unit Analytics](https://www.triumph.tech/resources/giving-unit-analytics)).

How agents should use this guide:

- Treat entity and workflow descriptions as a practical map.
- Treat exact IDs, GUIDs, block settings, and version caveats as verification prompts unless the current live instance has been checked.
- Prefer read-only inspection before making changes.
- Use the Model Map, Entity Type list, SQL schema, block settings, and source version to confirm installed behavior.
- For donor-facing or accounting-sensitive changes, require human review.

## 5. Core Configuration And Data Model

### Financial Accounts

Financial accounts are the backbone of giving classification. They answer: "What fund, campaign, ministry, fee, or destination did this money go to?"

Operational fields to inspect in a live Rock instance:

- `Name`: internal account name.
- `PublicName`: donor-facing name used in some receipt/statement contexts. Release notes state that in v18.1 the Send Payment Receipts process was updated so Giving Receipt System Emails use an account's public name when available, falling back to account name when not available ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- `IsTaxDeductible`: whether gifts to the account should generally be treated as deductible for statement/receipt language. Verify local policy; this flag is not legal advice.
- Account hierarchy/category: used for finance navigation and reporting organization.
- Active/inactive status: determines whether the account is available for future entry. Historical transactions may still point to inactive accounts.
- Campus or fund-specific attributes if the instance uses them.
- External ledger codes or account numbers if configured through attributes or integrations.

Do not create a new financial account for every one-off campaign without evaluating reporting requirements. A community recipe demonstrates one alternative: use Financial Transaction attributes and URL parameters on the Transaction Entry block to capture campaign-specific metadata while keeping account sprawl under control ([Custom Financial Transaction Attributes](https://community.rockrms.com/recipes/254)). This is a useful pattern, but agents must verify whether leadership, finance, statement generation, pledge reporting, and accounting exports need separate accounts rather than attributes.

### Financial Gateways

Financial gateways are configured payment processor integrations. They affect:

- Online giving.
- Scheduled transactions.
- Refunds.
- Hosted payment fields.
- Tokenized saved payment methods.
- Gateway downloads/imports.
- Reversal notifications.
- Payment-plan edits.
- ACH/card failure handling.

The official finance documentation includes payment gateways as a major chapter and has version notes about gateway transfer handling, reversal notification workflows, NMI gateway behavior, and downloading transaction options ([Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15)). Release notes also mention gateway-adjacent fixes, including a Utility Payment Entry block CAPTCHA issue that could wipe hosted gateway iframe payment information in v19.1 ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Before changing gateway configuration, inspect:

- Gateway entity/plugin type.
- Test vs production mode.
- API credentials and tokenization settings.
- Webhook/reversal notification endpoints.
- Scheduled transaction sync behavior.
- Saved account support.
- Whether payment plans and recurring schedules are managed in Rock, the gateway, or both.
- Whether external systems create gifts directly in Rock or only in the processor.

If a scheduled transaction exists in the gateway but not Rock, Rock-only reports may conclude that the donor does not have recurring giving. A community recurring-giving recipe warns about exactly this kind of mismatch: if recurring profiles do not sync into Rock, automation may contact donors who already have recurring gifts elsewhere ([Automate asking Regular Givers to Set up Recurring Giving](https://community.rockrms.com/recipes/122)).

### Defined Values

Finance depends heavily on defined types and values. Common examples include:

- Transaction type, such as Contribution.
- Currency type, such as Cash, Check, Credit Card, ACH, Non-Cash Asset.
- Credit card type.
- Transaction source.
- Payment frequency, such as one-time, weekly, biweekly, twice monthly, monthly, quarterly, twice yearly, yearly.
- Non-cash asset types.

The statement SQL source snippet shows constants for Family group type, Adult/Child roles, contribution transaction type, and business record type ([spFinance_ContributionStatementQuery.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.4/202104291818024_GroupSalutation_spFinance_ContributionStatementQuery.sql)). Payment-plan source shows Rock has defined-value GUID handling for frequencies including biweekly, first-and-fifteenth, monthly, one-time, quarterly, twice monthly, twice yearly, weekly, and yearly ([PaymentPlanConfigurationService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlanConfigurationService.cs)).

Agents should never assume local integer IDs for defined values. Use GUIDs, Model Map, Entity Type records, or live joins to resolve IDs.

### Entity Attributes

Rock finance entities can be extended with entity attributes. The source pack includes official finance documentation version notes about custom financial account attributes and financial batch attributes ([Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15)). A community recipe demonstrates custom Financial Transaction attributes and shows a practical workflow:

- Create an Entity Attribute for the `Financial Transaction` entity.
- Configure a Transaction Entry block to set the attribute from a URL parameter.
- Report later on transactions by account and attribute ([Custom Financial Transaction Attributes](https://community.rockrms.com/recipes/254)).

Use attributes when the data is descriptive metadata, not an accounting destination. Use accounts when finance needs separate ledger treatment, tax treatment, statement selection, pledge tracking, or accounting export mapping.

### Blocks And Pages

Finance behavior is often block-driven. Agents should inspect block settings, not only database rows.

Common block/page surfaces:

- Transaction Entry.
- Transaction List.
- Transaction Detail.
- Batch List.
- Batch Detail.
- Scheduled Transaction List/Detail.
- Giving History.
- Giving Overview.
- Giving Analytics.
- Pledge Analytics.
- Statement Generator/online statement blocks.
- Giving Receipt system email.
- Utility Payment Entry.
- Mobile Financial Batch List.
- Mobile Financial Batch Detail.

Release notes mention specific block behavior changes, including Transaction List fixes for account summary and move-to-batch visibility, Pledge Analytics date filter changes, and statement generation fixes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

When an agent is asked why finance behavior changed, inspect:

- Rock version.
- Block type and whether it is WebForms, Obsidian, or mobile.
- Block attribute values.
- Page route and query parameters.
- Security on page, block, account, and entity.
- Whether a lava template, shortcode, workflow action, or plugin overrides core behavior.

## 6. Primary Entities And Relationships

### Transaction Header, Detail, And Payment Detail

A transaction is not the same as an account allocation. The practical relationship is:

- `FinancialTransaction`
  - has one `FinancialPaymentDetail` or payment-detail reference in common implementations.
  - has many `FinancialTransactionDetail` records.
  - belongs to one `FinancialBatch` in normal financial flows.
  - references `AuthorizedPersonAliasId` for the person/business credited or associated with the transaction.
  - references `ProcessedByPersonAliasId` or similar fields in some workflows.
  - uses transaction type and source defined values.

- `FinancialTransactionDetail`
  - belongs to one `FinancialTransaction`.
  - references one `FinancialAccount`.
  - contains the amount for that account allocation.
  - may have summary/metadata fields depending on version.

Analytics source files confirm that financial analytics are detail-grain: one source record represents the combination of transaction and transaction detail ([AnalyticsSourceFinancialTransaction.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsSourceFinancialTransaction/AnalyticsSourceFinancialTransaction.cs)). That is the rule agents should follow for account-level reporting.

### Batches And Transactions

A batch is the reconciliation and posting container. The dev seed SQL in the pack shows `FinancialBatch` fields such as name, start date/time, status, control amount, and GUID being populated for test data ([Populate_FinancialTransactions_Contributions.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Populate_FinancialTransactions_Contributions.sql)). Official docs note that older updates introduced batch audit log details, automated batch documentation, teller import transactions, and financial batch attributes ([Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15)).

Batch relationships agents should inspect:

- Batch to transaction: each transaction should be assigned to a batch for reconciliation.
- Batch to campus: if the instance uses campus-specific deposits or mobile batch filtering.
- Batch status: open, pending, closed, or other configured values depending on version.
- Control amount and item count: expected total and count.
- Actual sum and count: calculated from transaction details.
- Accounting/export state: if external accounting integration exists.
- Audit history: who changed amount, status, transaction membership, or control fields.

Mobile finance docs show newer mobile batch management is becoming more capable. The Financial Batch List block can filter by status/campus and can allow adding batches; the Financial Batch Detail block supports viewing/editing batches and check scanning through Azure Document Intelligence ([Financial Batch List](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-list), [Financial Batch Detail](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-detail)).

### Scheduled Transactions And Payment Plans

Scheduled transactions are distinct from completed transactions. A scheduled transaction is an instruction/profile for future processing. Completed gifts created from that profile become normal financial transactions.

Source-code landmarks show an internal payment-plan model around scheduled transactions:

- `PaymentPlan` includes the scheduled transaction GUID, amount per payment, active status, number of payments, processed count, remaining count, planned amount, and comments that gateway sync can make processed/remaining/planned values inaccurate if payments have not synced back to Rock ([PaymentPlan.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlan.cs)).
- `PaymentPlanConfiguration` copies start date, frequency, and number of payments into a `FinancialScheduledTransaction`; it also copies payment-plan information into scheduled transaction details ([PaymentPlanConfiguration.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlanConfiguration.cs)).
- `PaymentFrequencyConfiguration` stores the payment frequency and maximum number of payments for that frequency ([PaymentFrequencyConfiguration.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentFrequencyConfiguration.cs)).
- These payment-plan classes are marked internal API, so plugin authors should not treat them as stable public extension contracts ([PaymentPlan.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlan.cs)).

Agents troubleshooting scheduled giving should inspect:

- `FinancialScheduledTransaction`.
- `FinancialScheduledTransactionDetail`.
- Gateway profile/token IDs.
- Active/inactive status.
- Start date and next payment date.
- Frequency defined value.
- Number of payments if the profile is a payment plan.
- Whether the donor changed the profile at gateway, in Rock, or through a mobile/web block.
- Recent gateway download/sync jobs.
- Exception logs and communication receipts.

### Pledges

Pledges represent commitments, not money received. Pledge reporting compares pledged amount and date range against qualifying transactions.

Inspect:

- `FinancialPledge`.
- `PersonAliasId` or giving-unit/person linkage.
- `AccountId`.
- `StartDate` and `EndDate`.
- `TotalAmount`.
- Whether the pledge is individual, family, or campaign-specific in local reporting.
- Which transaction types/accounts/date ranges count toward fulfillment.

A community pledge-analysis recipe shows one common operational need: reporting pledges active on a selected date, filtering by account, and calculating whether giving is on pace based on elapsed time and tolerance ([Pledge Analysis Page](https://community.rockrms.com/recipes/90)). Treat the recipe as an example; for production, verify live pledge table fields, data view filters, and performance.

Release notes add an important version caveat: v19.1 added a Giving Date Range filter to the Financial Pledge Analytics block and renamed the prior date filter to Pledge Date Range ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). Agents comparing old screenshots or reports to v19.1+ should check which date filter is being used.

### People, PersonAlias, Businesses, Families, And Giving Units

Finance almost always uses `PersonAliasId`, not just `PersonId`, because Rock preserves identity through merges and alternate aliases. The dev SQL snippets join `FinancialTransaction.AuthorizedPersonAliasId` to `PersonAlias`, then to `Person`, and use `Person.GivingId` for test data frequency patterns ([Populate_FinancialTransactions_Contribution_UsingFrequency.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Populate_FinancialTransactions_Contribution_UsingFrequency.sql)).

For statements and analytics, family membership and giving unit logic matter. The statement stored procedure source references family group type, adult and child roles, location types, contribution transaction type, and business record type ([spFinance_ContributionStatementQuery.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.4/202104291818024_GroupSalutation_spFinance_ContributionStatementQuery.sql)). Analytics fact source distinguishes current family, historical family at transaction time, and giving unit key ([AnalyticsFactFinancialTransaction.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsFactFinancialTransaction/AnalyticsFactFinancialTransaction.cs)).

Agents must inspect live person/family/giving settings before answering questions such as:

- "Why did this spouse's gift appear on the statement?"
- "Why is a child listed in the salutation?"
- "Why does giving history include/exclude other household members?"
- "Why does the API show family giving instead of individual giving?"

Release notes include a v18.3 fix for Giving History API behavior: when "Combine Giving With" was blank, the API incorrectly returned family giving instead of only the individual's authorized giving; another fix addressed missing contributions from an individual's other records when family giving was excluded ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). This is a major caveat for agents working across versions.

## 7. Common Giving And Finance Workflows

### Online Giving

Online giving typically follows this path:

1. The giver opens a Transaction Entry or giving block.
2. The page identifies the person or allows guest entry.
3. The giver chooses amount, account(s), frequency, and payment method.
4. Rock submits payment data through a gateway or hosted gateway iframe.
5. The gateway authorizes or rejects the payment.
6. Rock creates transaction, details, payment detail, and batch membership.
7. Rock sends a receipt or confirmation.
8. If recurring, Rock creates or updates a scheduled transaction and gateway profile.

RockU includes online giving as a core finance topic ([Online Giving](https://community.rockrms.com/rocku/finance/online-giving)). The official finance documentation includes advanced Transaction Entry block settings and payment gateway configuration references ([Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15)). A community recipe demonstrates a Transaction Entry advanced pattern: presetting a transaction attribute from a URL parameter so special campaign data can be captured without creating many accounts ([Custom Financial Transaction Attributes](https://community.rockrms.com/recipes/254)).

Operational checks:

- Confirm the page's Transaction Entry block settings.
- Confirm allowed accounts.
- Confirm gateway is correct for the environment.
- Confirm account public names and tax deductibility.
- Confirm receipt system email and Lava merge fields.
- Confirm whether scheduled giving uses Rock-managed profiles or gateway-managed profiles.
- Confirm transaction source values for online giving.
- Confirm batch creation logic and whether online gifts land in automated batches.

### Text Giving

Text giving is a compact interface to the same finance backbone. RockU includes text giving as a finance topic ([Text Giving](https://community.rockrms.com/rocku/finance/text-giving)). Release notes include a v19.1 fix for Text-to-Give failure handling: after an automated transaction attempt fails and the giver is notified, the pending transaction is deleted so batch detail and transaction list totals are not distorted by leftover pending records ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

When troubleshooting text giving:

- Inspect the SMS provider and text-giving configuration.
- Check pending transaction state.
- Compare transaction list totals to batch detail totals.
- Look for failure communications.
- Check exception logs around gateway failures.
- Verify whether the installed version includes the pending-transaction cleanup fix.
- Confirm account keywords and default account mapping.

### Manual Entry And Check Processing

Manual entry includes cash, checks, non-cash assets, and office-entered card/ACH gifts. RockU includes check matching and batches as finance topics ([Check Matching](https://community.rockrms.com/rocku/finance/check-matching), [Batches](https://community.rockrms.com/rocku/finance/batches)). The official finance book's version notes mention transaction date behavior when scanning checks, Canon check-reader driver recommendations, check scanning software updates, and batch block/audit-log changes ([Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15)).

Newer mobile functionality matters here. The Financial Batch Detail mobile developer doc says the block can integrate with Azure Document Intelligence to scan checks, extract MICR data, and allocate funds to accounts. Its configuration includes Transaction Detail Page, Accounts, Document Intelligence API Key, Document Intelligence Endpoint, Accounts Allocation Required, Required Control Amount, and Required Control Item Count ([Financial Batch Detail](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-detail)). Release notes say Financial Batch Detail and Financial Batch List were added to support check scanning, batch creation, detail viewing, and modifications in v18.1 mobile ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Manual/check workflow checks:

- Confirm batch exists and is open.
- Confirm transaction date convention.
- Confirm payment detail currency type is Check/Cash/Non-Cash as appropriate.
- For check matching, verify MICR hash/matching data and person alias linkage.
- Confirm item count and control amount.
- Confirm split allocations sum to total.
- Confirm non-cash asset type if applicable.
- Confirm batch status after reconciliation.

### Scheduled Giving And Recurring Giving

Recurring giving is not just a repeated transaction. It is a relationship between Rock, gateway profile, donor identity, payment method token, schedule frequency, allocation details, and future processing state.

RockU covers scheduled transactions ([Scheduled Transactions](https://community.rockrms.com/rocku/finance/scheduled-transactions)). Source-code payment-plan classes show that payment-plan calculations depend on currency precision, amount, frequency, allowed frequencies, start/end dates, minimum/maximum payment counts, and whether payment counts are limited by end date ([PaymentPlanConfigurationOptions.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlanConfigurationOptions.cs), [PaymentPlanConfigurationService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlanConfigurationService.cs)).

Recurring-giving operational checks:

- Is the scheduled transaction active?
- Does the gateway profile still exist?
- Does the saved payment method/token still work?
- Is the frequency valid and supported by the gateway?
- Is the next payment date in the future?
- Are the scheduled transaction details tied to active accounts?
- Has the donor's person alias changed through merge?
- Did Rock receive gateway callbacks/downloads?
- Are failed transactions leaving pending records?
- Are receipts sent for scheduled payments?
- Are payment-plan counts accurate, or did gateway sync lag make them stale?

A community recipe for encouraging regular givers to set up recurring giving uses giving history and absence of active `FinancialScheduledTransaction` records as criteria, but it warns that external recurring systems that do not sync profiles to Rock can create false positives ([Automate asking Regular Givers to Set up Recurring Giving](https://community.rockrms.com/recipes/122)). Agents should repeat that warning in any automation design.

### Refunds And Reversals

RockU includes refunds as a finance topic ([Refunds](https://community.rockrms.com/rocku/finance/refunds)). The official finance book has release history around payment reversal notification workflows and gateway-specific reversal handling ([Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15)).

Refund/reversal troubleshooting must distinguish:

- A gateway refund that returned money to the payer.
- A Rock correction that offsets a transaction.
- A failed ACH/card transaction that never settled.
- A pending transaction that should be removed.
- A statement setting that hides refunded or corrected transactions.
- A batch correction made after deposit.

Statement Generator transaction settings include `HideRefundedTransactions` and `HideCorrectedTransactionOnSameData`, which directly affect whether refunded/corrected items appear on statements ([FinancialStatementTemplateTransactionSetting.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Applications/Wpf/StatementGenerator/Client/FinancialStatementTemplateTransactionSetting.cs)).

### Businesses

Businesses are person-like records that can be associated with contributions. RockU has a finance video for businesses ([Businesses](https://community.rockrms.com/rocku/finance/businesses)). Statement SQL checks whether a requested person is a business using a business record type defined value ([spFinance_ContributionStatementQuery.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.4/202104291818024_GroupSalutation_spFinance_ContributionStatementQuery.sql)).

Operational checks for business gifts:

- Confirm the record type is Business.
- Confirm the business has the correct address and contacts.
- Confirm authorized person alias belongs to the business record when appropriate.
- Confirm statement salutation/address behavior.
- Confirm recurring giving for businesses if used.
- Confirm whether gifts should be credited to the business, an individual, or both for relationship history.

### External Giving Imports

External systems such as Planning Center Giving may need to sync into Rock. The community recipe in the pack describes a workflow-based Planning Center import that uses a Rock REST key, Rock-side attributes, Planning Center personal access token, fund/account mapping, webhooks, person matching/creation, and API requests to create financial records ([Syncing Planning Center Giving into Rock RMS](https://community.rockrms.com/recipes/521/syncing-planning-center-giving-into-rock-rms)). Because this is a community recipe and not core-team-reviewed, it should be treated as a pattern, not a complete integration standard.

For any external import, agents should require:

- Idempotency key to prevent duplicate transactions.
- Source system transaction ID stored in an attribute or integration table.
- Explicit fund-to-account mapping.
- Person/business matching rules.
- Gateway/payment method mapping.
- Batch naming and deposit-date policy.
- Error logging and retry policy.
- Reconciliation report between external source and Rock.
- API key least privilege and rotation plan.
- Test environment validation before production.

## 8. Transactions Deep Dive

### Transaction Grain

The most common reporting bug is using the wrong grain.

Use transaction header grain when the question is:

- How many payments occurred?
- Who authorized the payment?
- What gateway transaction code was used?
- Which batch contains the payment?
- What was the total payment amount?
- What was the payment method?

Use transaction detail grain when the question is:

- How much went to this account?
- Which funds received money?
- How much tax-deductible giving occurred?
- Which pledge/account was fulfilled?
- What should appear on a statement by account?
- What should be exported to ledger accounts?

Rock's analytics source model makes the grain explicit: one analytics source financial record represents the `FinancialTransaction` and `FinancialTransactionDetail` combination, and a multi-account transaction produces multiple records ([AnalyticsSourceFinancialTransaction.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsSourceFinancialTransaction/AnalyticsSourceFinancialTransaction.cs)).

### Transaction Dates

Rock finance may expose several dates:

- Transaction date/time.
- Transaction date key, often `YYYYMMDD` for analytics.
- Sunday date, used in some reporting patterns.
- Batch start/end date.
- Deposit/settlement date.
- Gateway authorization/settlement date.
- Created/modified date.

The dev SQL frequency script updates `TransactionDateTime`, `TransactionDateKey`, and `SundayDate` together for test contribution data ([Populate_FinancialTransactions_Contribution_UsingFrequency.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Populate_FinancialTransactions_Contribution_UsingFrequency.sql)). That source is a test tool, not production guidance, but it shows these fields matter together.

Before changing dates or comparing totals, inspect which date the report uses. This is especially important for:

- Year-end giving.
- Statements.
- Deposits.
- Pledge fulfillment.
- Giving analytics.
- BI exports.
- Gateway settlement reconciliation.

### Transaction Types

The common transaction type for gifts is Contribution. Transaction type defined values are used in statement queries, analytics, and reports. Source snippets show the contribution GUID being used as a constant in statement and data-generation SQL ([spFinance_ContributionStatementQuery.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.4/202104291818024_GroupSalutation_spFinance_ContributionStatementQuery.sql), [Populate_FinancialTransactions_Contributions.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Dev%20Tools/Sql/Populate_FinancialTransactions_Contributions.sql)).

Do not assume every payment is a contribution. Registration payments, event fees, product payments, and non-deductible account payments may use finance infrastructure but should not necessarily appear on contribution statements. For donor-facing receipt language, a community shortcode recipe uses account tax deductibility to choose gift vs payment language, but this must be reviewed for local policy and multi-account edge cases ([Giving Receipt System Email Shortcodes](https://community.rockrms.com/recipes/510/giving-receipt-system-email-shortcodes)).

### Transaction Sources

Transaction source indicates origin: online, mobile, text, check scanner, teller import, external import, registration, manual entry, etc. Official finance documentation version notes mention a Transaction Source option and transactions created using Teller Import ([Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15)). Analytics fact source includes `TransactionSource` as a field ([AnalyticsFactFinancialTransaction.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsFactFinancialTransaction/AnalyticsFactFinancialTransaction.cs)).

Agents should use transaction source for operational filtering but not as the only determinant of tax treatment or statement eligibility.

### Transaction Attributes

Financial transaction attributes can capture metadata beyond core fields. A community recipe shows using a URL parameter to preset a transaction attribute from the Transaction Entry block ([Custom Financial Transaction Attributes](https://community.rockrms.com/recipes/254)). This can support fundraiser names, campaign subcategories, external IDs, donor intent labels, or internal reporting tags.

Guardrails:

- Do not use attributes as a substitute for accounts when accounting separation is required.
- Do not store sensitive payment data in attributes.
- Use defined-value fields when values need normalization.
- Document any URL parameter behavior.
- Include attributes in reports explicitly; they will not automatically alter statements or ledger exports.

### Transaction Security

Finance transaction access should be tightly scoped. Agents should inspect:

- Page security.
- Block security.
- Entity security.
- Account security.
- REST API key permissions.
- Lava command enablement.
- Report/data view permissions.
- Mobile block access.
- Finance team roles.

The official finance documentation version notes mention additional security actions in the Security for Finance chapter ([Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15)). Recipes involving REST keys and Lava entity commands should be reviewed carefully because finance data is sensitive ([Syncing Planning Center Giving into Rock RMS](https://community.rockrms.com/recipes/521/syncing-planning-center-giving-into-rock-rms), [Giving Receipt System Email Shortcodes](https://community.rockrms.com/recipes/510/giving-receipt-system-email-shortcodes)).

## 9. Statements Deep Dive

### Statement Inputs

A contribution statement is the result of multiple filters and settings:

- Date range.
- Account selection.
- Transaction type selection.
- Currency types for cash gifts.
- Currency types for non-cash gifts.
- Whether to hide refunded transactions.
- Whether to hide corrected transactions on the same date.
- Person or group selection.
- Data view selection.
- Address requirements.
- Combine-giving settings.
- Business vs individual handling.
- Template content.
- Custom messages.
- Public account names.

The Statement Generator transaction settings source includes `AccountSelectionOption`, `CurrencyTypesForCashGiftGuids`, `CurrencyTypesForNonCashGuids`, `HideCorrectedTransactionOnSameData`, `HideRefundedTransactions`, `SelectedAccountIds`, and `TransactionTypeGuids` ([FinancialStatementTemplateTransactionSetting.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Applications/Wpf/StatementGenerator/Client/FinancialStatementTemplateTransactionSetting.cs)). The generated client counterpart exposes the same settings ([Rock.Client FinancialStatementTemplateTransactionSetting.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Client/CodeGenerated/FinancialStatementTemplateTransactionSetting.cs)).

### Statement Recipients

Statement recipient logic depends on people, groups, addresses, businesses, and combine-giving rules. The older statement stored procedure source returns mailing address and custom-message data, not the transaction rows themselves, and notes that the Statement Generator utility uses the procedure plus REST transaction queries ([spFinance_ContributionStatementQuery.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.4/202104291818024_GroupSalutation_spFinance_ContributionStatementQuery.sql)). That procedure is marked obsolete in favor of Statement Generator/REST endpoints in the source snippet, so agents should verify the installed statement path.

Inspect live:

- Statement generator settings.
- Person/Business selected.
- Family group membership.
- Adult/child roles.
- Mailing address availability.
- Combine Giving With field/settings.
- Whether household member opted out.
- Saved settings from prior statement runs.
- Data view filters.

Release notes mention a v18.1 fix where Statement Generator could fail for a single individual if a Data View had been used previously and the person was not part of that view ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). Agents diagnosing single-person statement generation should check version and saved Data View state.

Release notes also mention a fix where Contribution Statements included the name of a household member who opted out of Combine Giving in the salutation even though that member's transactions were not included ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). This is a version-sensitive salutation issue.

### Statement Eligibility

Start with [Contribution Statements](https://community.rockrms.com/rocku/finance/contribution-statements) and the current [Statement Generator transaction settings](https://github.com/SparkDevNetwork/Rock/blob/develop/Applications/Wpf/StatementGenerator/Client/FinancialStatementTemplateTransactionSetting.cs); eligibility is the intersection of the selected people, accounts, transaction and currency types, dates, statuses, and household-giving rules.

A gift may be excluded from statements because:

- The transaction type is not included.
- The account is not selected.
- The account is not tax-deductible and the template/report excludes it.
- The currency type is excluded.
- The transaction is refunded or corrected and settings hide it.
- The transaction date is outside range.
- The authorized person alias is wrong.
- The gift is under a business instead of an individual, or vice versa.
- Combine-giving settings exclude it.
- The statement run used a Data View that excludes the person.
- The transaction is pending/failed/test.
- The report uses stale analytics data or an old BI extract.

Agents should inspect statement settings before editing financial records.

### Receipts Vs Statements

Receipts are usually immediate confirmations. Statements are periodic contribution summaries. They can use different templates, settings, and language.

A community recipe shows a receipt customization where the email subject/body changes based on whether the first account is tax-deductible ([Giving Receipt System Email Shortcodes](https://community.rockrms.com/recipes/510/giving-receipt-system-email-shortcodes)). That pattern has limitations:

- It assumes first account controls the whole receipt.
- Split transactions can mix deductible and non-deductible accounts.
- It depends on Lava entity access.
- It must be reviewed for spelling, legal language, and local policy.
- It may need to use account public name after the v18.1 receipt public-name change.

Use receipt customization only after confirming the system email, merge objects, available fields, Lava commands, and account policy.

## 10. Batches Deep Dive

### Batch Purpose

A batch is the finance office's control surface. It answers:

- Which transactions are grouped together?
- What should the total be?
- How many items should be present?
- Has the group been reviewed?
- Has it been closed?
- Does it reconcile to cash/check/gateway deposits?
- Who changed it?

RockU includes batch training ([Batches](https://community.rockrms.com/rocku/finance/batches)). Official docs mention batch audit logs, batch blocks, automated batches, financial batch attributes, and transactions from teller import ([Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15)).

### Batch Fields To Inspect

In a live instance, inspect:

- Name.
- Status.
- Batch start date/time.
- Batch end date/time.
- Control amount.
- Control item count.
- Campus.
- Accounting system code or export metadata if configured.
- Created/modified audit fields.
- Attribute values.
- Transaction count.
- Transaction detail sum.
- Payment method mix.
- Gateway deposit or settlement reference.

The mobile Financial Batch Detail block has settings for Required Control Amount and Required Control Item Count, indicating those controls can be required in mobile batch workflows ([Financial Batch Detail](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-detail)).

### Batch Status

Batch statuses vary by version/configuration, but operationally agents should distinguish:

- **Open**: transactions can still be added/edited.
- **Pending/review**: possibly awaiting count/amount reconciliation.
- **Closed**: expected to be final and reconciled.
- **Exported/posted**: if custom integration tracks ledger export.

Do not move or edit closed batches without finance approval. Release notes mention a Transaction List block fix where "Move Transactions To Batch" was incorrectly displayed on transaction details when it should only appear from the main transaction list ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). If users report seeing or not seeing move-to-batch actions, check version and block context.

### Automated Batches

Online/gateway transactions often go into automated batches by date/source/gateway. Official docs version notes mention automated batch documentation ([Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15)). Agents should verify local rules:

- One batch per day?
- One batch per gateway settlement?
- One batch per campus?
- One batch per payment method?
- One batch per source?
- Are failed/pending transactions included?
- How are refunds/reversals batched?

### Check Scanning And Mobile Batch Processing

The Financial Batch Detail mobile block can integrate with Azure Document Intelligence for check scanning and MICR extraction. Required configuration includes API key, endpoint, allowed accounts, transaction detail page, and control amount/item-count requirements ([Financial Batch Detail](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-detail)). Financial Batch List includes settings such as status filter, allow add, detail page, campus filtering, display campus types/statuses, page load size, item template, post-save action, and styling ([Financial Batch List](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-list)).

Agents implementing mobile batch workflows should verify:

- Rock core version and mobile shell version.
- Whether mobile blocks are available in the installed build.
- Azure Document Intelligence credentials.
- Network access from mobile app to Rock and Azure.
- Account allocation requirements.
- Campus filtering.
- Security roles for finance users.
- Test check images and MICR extraction accuracy.
- Audit trail and reconciliation with desktop finance pages.

Release notes identify the mobile batch blocks as v18.1 additions for check scanning, batch creation, detail viewing, and modifications ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

## 11. Related Rock Areas: People, Groups, Workflows, Security, Reporting

### People

Person and PersonAlias are central to giving. Incorrect identity linkage causes:

- Missing giving history.
- Wrong donor statement.
- Duplicate donor records.
- Business gifts attached to people.
- Household combine-giving surprises.
- Recurring profiles not visible to the right user.

Inspect:

- Person aliases.
- Giving ID.
- Merged records.
- Family group membership.
- Business record type.
- Contact information and addresses.
- Deceased/inactive status if reports filter it.
- Giving history page and API output.

### Groups

Family groups determine household context. The statement SQL source references family group type and adult/child roles ([spFinance_ContributionStatementQuery.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.4/202104291818024_GroupSalutation_spFinance_ContributionStatementQuery.sql)). Analytics source differentiates current family from historical family at transaction time and giving unit ([AnalyticsFactFinancialTransaction.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsFactFinancialTransaction/AnalyticsFactFinancialTransaction.cs)).

Fundraising groups are also finance-adjacent; RockU includes fundraising group training ([Fundraising Group](https://community.rockrms.com/rocku/finance/fundraising-group)). Agents should inspect group type, group attributes, member roles, account/campaign mapping, and donation page settings before modifying fundraising behavior.

### Workflows

Finance workflows commonly handle:

- Giving alerts.
- Recurring-giving invitations.
- Payment reversal notifications.
- External imports.
- Benevolence requests.
- Receipt customization.
- Failed payment follow-up.
- Pledge reminders.
- Batch review notifications.

RockU includes giving alerts ([Giving Alerts](https://community.rockrms.com/rocku/finance/giving-alerts)) and benevolence ([Benevolence](https://community.rockrms.com/rocku/finance/benevolence)). The external Planning Center recipe uses workflow actions and REST API calls to create financial records, illustrating how powerful and risky finance workflows can be ([Syncing Planning Center Giving into Rock RMS](https://community.rockrms.com/recipes/521/syncing-planning-center-giving-into-rock-rms)).

Workflow guardrails:

- Use least-privilege API keys.
- Store external IDs for idempotency.
- Log every skipped/failed record.
- Never email donors from an unverified Data View.
- Avoid direct SQL writes for production finance.
- Use dry-run/test mode where possible.
- Require finance signoff before enabling scheduled automation.

### Security

Finance security is multi-layered:

- Finance pages.
- Finance blocks.
- Financial accounts.
- Entity attributes.
- Reports.
- Data views.
- REST endpoints.
- Lava commands.
- Mobile app pages.
- Gateway credentials.
- Workflow actions.
- System emails.

The official finance documentation has security-specific updates for finance ([Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15)). Community recipes involving REST keys, SQL, and Lava entity commands are useful but must be reviewed against the installed security model ([Syncing Planning Center Giving into Rock RMS](https://community.rockrms.com/recipes/521/syncing-planning-center-giving-into-rock-rms), [Giving Receipt System Email Shortcodes](https://community.rockrms.com/recipes/510/giving-receipt-system-email-shortcodes)).

### Reporting

Reporting spans:

- Core reports.
- Data Views.
- Dynamic Data blocks.
- Giving Analytics blocks.
- Giving Overview.
- Giving Journey.
- Giving Alerts.
- BI models and Power BI.
- Analytics source/fact tables.
- SQL views.
- Model Map.
- REST APIs.

RockU includes Giving Analytics, Giving Overview, Giving Journey, and BI Financial Transaction Report ([Giving Analytics](https://community.rockrms.com/rocku/finance/giving-analytics), [Giving Overview](https://community.rockrms.com/rocku/finance/giving-overview), [Giving Journey](https://community.rockrms.com/rocku/finance/giving-journey-1), [BI Financial Transaction Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-financial-transaction-report)). The Giving Journey lesson is useful training context for evaluating donor experience alongside transaction records, account detail, receipts, giving alerts, and reporting definitions; verify exact setup in the live instance ([Giving Journey](https://community.rockrms.com/rocku/finance/giving-journey-1)). The BI Financial Transaction Report source record includes a Power BI template link in the training page ([BI Financial Transaction Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-financial-transaction-report)).

Agents should ask whether a report should use live transactional tables or analytics tables. Analytics tables can be faster and semantically richer, but may need refresh jobs and may expose detail-grain rows.

## 12. Administration And Operational Guardrails

### Change Control

Finance changes should be treated like production changes even when they are "just block settings." Require:

- Ticket/request context.
- Finance owner approval.
- Test transaction or staging validation.
- Version check.
- Rollback plan.
- Audit of affected pages/blocks/reports.
- Statement/receipt impact check.
- Security review if permissions, APIs, Lava, or workflows are involved.

### Account Governance

Before adding/changing accounts:

- Confirm accounting/ledger mapping.
- Confirm tax deductibility.
- Confirm public name.
- Confirm statement inclusion.
- Confirm pledge/campaign behavior.
- Confirm whether attributes would be better.
- Confirm whether old transactions need reclassification.
- Confirm whether online giving pages expose the account.

The custom transaction attribute recipe is a useful reminder that account sprawl is not always the right solution ([Custom Financial Transaction Attributes](https://community.rockrms.com/recipes/254)).

### Gateway Governance

Before changing gateways:

- Export/list active scheduled transactions.
- Confirm saved payment token portability.
- Confirm payment reversal webhooks.
- Confirm receipt behavior.
- Confirm automated batch behavior.
- Confirm test mode vs production mode.
- Confirm fees, settlement, and refund handling.
- Communicate donor impact if profiles must be re-created.

The official finance documentation notes gateway-transfer handling and gateway download configuration updates in its version history ([Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15)).

### Batch Controls

Finance teams should define:

- Who can create batches.
- Who can edit transactions in open batches.
- Who can close batches.
- Whether control amount and item count are required.
- How deposits map to batches.
- How online batches are named.
- How refunds/reversals are grouped.
- How batch discrepancies are resolved.
- Whether mobile batch processing is allowed.

Mobile block settings can enforce control amount/item count requirements in the mobile batch detail experience ([Financial Batch Detail](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-detail)).

### Receipt And Statement Controls

Before changing receipts/statements:

- Review legal/tax language.
- Confirm organization name and contact details.
- Confirm account public names.
- Confirm tax-deductible flags.
- Test split transactions.
- Test business gifts.
- Test refunded/corrected transactions.
- Test household combine-giving edge cases.
- Test single individual statement generation.
- Check installed version for known fixes.

Release notes around v18.1 and v18.3 include statement and giving-history fixes that can materially change donor-facing output ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

## 13. Developer, API, Lava, And Source-Code Landmarks

### Source Repository

The Rock source repository is the primary source-code landmark for models, services, migrations, generated clients, Obsidian blocks, and developer contracts ([SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock)).

Important files from this pack:

- Payment plans and scheduled transactions:
  - [PaymentPlan.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlan.cs)
  - [PaymentPlanConfiguration.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlanConfiguration.cs)
  - [PaymentPlanConfigurationOptions.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlanConfigurationOptions.cs)
  - [PaymentPlanConfigurationService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlanConfigurationService.cs)
  - [PaymentFrequencyConfiguration.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentFrequencyConfiguration.cs)
- Analytics:
  - [AnalyticsBaseFinancialTransaction.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsBaseFinancialTransaction/AnalyticsBaseFinancialTransaction.cs)
  - [AnalyticsSourceFinancialTransaction.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsSourceFinancialTransaction/AnalyticsSourceFinancialTransaction.cs)
  - [AnalyticsFactFinancialTransaction.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsFactFinancialTransaction/AnalyticsFactFinancialTransaction.cs)
- Statements:
  - [FinancialStatementTemplateTransactionSetting.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Applications/Wpf/StatementGenerator/Client/FinancialStatementTemplateTransactionSetting.cs)
  - [Rock.Client FinancialStatementTemplateTransactionSetting.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Client/CodeGenerated/FinancialStatementTemplateTransactionSetting.cs)
  - [spFinance_ContributionStatementQuery.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.4/202104291818024_GroupSalutation_spFinance_ContributionStatementQuery.sql)
- Reporting filters:
  - [FinancialTransaction TotalAmountFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/FinancialTransaction/TotalAmountFilter.cs)
  - [FinancialTransactionDetail AccountFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/FinancialTransactionDetail/AccountFilter.cs)
  - [FinancialScheduledTransactionDetail AccountFilter.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataFilter/FinancialScheduledTransactionDetail/AccountFilter.cs)

### API Considerations

Rock exposes many entities through REST or generated APIs, but finance API behavior is version-sensitive. Analytics fact/source models in the pack are generated as read-only REST endpoints with entity security disabled in their attributes ([AnalyticsFactFinancialTransaction.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsFactFinancialTransaction/AnalyticsFactFinancialTransaction.cs), [AnalyticsSourceFinancialTransaction.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsSourceFinancialTransaction/AnalyticsSourceFinancialTransaction.cs)). That does not mean arbitrary users can access them; actual access depends on API authentication, route security, and Rock configuration. Verify in the live instance.

The Giving History API has known version fixes in v18.3 around combine-giving behavior and performance ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). Agents building mobile/profile giving history should verify installed version before diagnosing discrepancies.

External integration recipes often use REST API keys. The Planning Center import recipe uses a Rock REST key to create financial records and includes setup steps for API key creation ([Syncing Planning Center Giving into Rock RMS](https://community.rockrms.com/recipes/521/syncing-planning-center-giving-into-rock-rms)). In production, use least privilege, store secrets securely, and prefer supported endpoints/services.

### Lava Considerations

Finance Lava can be powerful and risky. Community examples include:

- Transaction Entry block URL parameter to set Financial Transaction attributes ([Custom Financial Transaction Attributes](https://community.rockrms.com/recipes/254)).
- Receipt shortcodes using `financialaccount` entity access and account tax deductibility ([Giving Receipt System Email Shortcodes](https://community.rockrms.com/recipes/510/giving-receipt-system-email-shortcodes)).
- Pledge analysis pages using Dynamic Data and SQL/Lava patterns ([Pledge Analysis Page](https://community.rockrms.com/recipes/90)).

Guardrails:

- Verify enabled Lava commands.
- Avoid exposing sensitive fields.
- Do not run arbitrary SQL in public blocks.
- Cache carefully.
- Test with split gifts and businesses.
- Confirm account security behavior if using `securityenabled:'false'` patterns from recipes.
- Have finance review donor-facing output.

### Mobile Developer Landmarks

The mobile finance docs in this pack identify:

- Financial Batch List: available as mobile v7.0 / core v17.4, with settings for post-save action, item template, status, allow add, detail page, campus filters, page load size, and styling ([Financial Batch List](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-list)).
- Financial Batch Detail: mobile v7.0 / core v18, with settings for transaction detail page, accounts, Azure Document Intelligence API key/endpoint, account allocation requirement, required control amount, required control item count, and styling ([Financial Batch Detail](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-detail)).

Release notes identify the batch mobile blocks as v18.1 additions for check scanning and batch management ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)). Verify current installed versions because developer docs and release notes can use different version labels for mobile shell and core.

## 14. Reporting, Analytics, And Model Map

### Transactional Tables Vs Analytics Tables

Use transactional tables when you need current operational truth:

- `FinancialTransaction`.
- `FinancialTransactionDetail`.
- `FinancialPaymentDetail`.
- `FinancialBatch`.
- `FinancialAccount`.
- `FinancialScheduledTransaction`.
- `FinancialScheduledTransactionDetail`.
- `FinancialPledge`.

Use analytics tables/views when you need faster aggregated reporting, giving-unit context, date dimensions, historical/current family keys, first-transaction flags, days-since-last metrics, BI extracts, or trend reporting. Source files define `AnalyticsSourceFinancialTransaction` as a real source table and `AnalyticsFactFinancialTransaction` as a SQL view based on that source ([AnalyticsBaseFinancialTransaction.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsBaseFinancialTransaction/AnalyticsBaseFinancialTransaction.cs), [AnalyticsFactFinancialTransaction.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsFactFinancialTransaction/AnalyticsFactFinancialTransaction.cs)).

The analytics base model includes fields such as transaction key, transaction date key, authorized person key, authorized current person key, days since last transaction of type, and first transaction of type flags ([AnalyticsBaseFinancialTransaction.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsBaseFinancialTransaction/AnalyticsBaseFinancialTransaction.cs)). The analytics fact model includes transaction type, transaction source, schedule type, processed-by person key, authorized family key, current family key, and giving unit key ([AnalyticsFactFinancialTransaction.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsFactFinancialTransaction/AnalyticsFactFinancialTransaction.cs)).

### Giving Analytics

RockU lists Giving Analytics and Giving Overview as finance training areas ([Giving Analytics](https://community.rockrms.com/rocku/finance/giving-analytics), [Giving Overview](https://community.rockrms.com/rocku/finance/giving-overview)). Official finance documentation version notes mention a new Giving Analytics chapter and updated screenshots/options ([Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15)).

Agents should inspect:

- Block settings.
- Date range.
- Account filters.
- Campus filters.
- Giving unit logic.
- Analytics refresh jobs.
- Security.
- Version-specific block changes.

### BI Financial Transaction Reporting

RockU includes BI Financial Transaction Report training and references a Power BI template ([BI Financial Transaction Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-financial-transaction-report)). For BI work, verify:

- BI job schedule.
- Data warehouse/model refresh state.
- Which finance entities are included.
- Whether data is detail-grain or aggregate.
- Whether giving-unit analytics are used.
- Whether report filters match finance statement filters.
- Whether security is enforced in embedded reports.

### Model Map Usage

For any live task, use the Model Map or live schema to confirm:

- Entity names.
- Navigation properties.
- Field names and types.
- Defined value relationships.
- Attribute entity types.
- Whether an entity is hidden from reporting.
- REST endpoint generation status.
- Version differences.

This guide uses source-code snippets from the develop branch. Installed Rock versions may differ.

## 15. Version And Release Caveats

Important version caveats from the source pack:

- **Rock v4.0-era finance documentation**: official docs note that all transactions must be in a batch and include updates around check scanning, batch blocks, batch audit log, Giving Analytics, Benevolence, Pledge Analytics, and Transaction Source ([Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15)).
- **Rock v7.0-era finance documentation**: official docs mention gateway transfer handling, giving envelopes, business contribution detail page, scheduled transaction screenshots, payment gateway downloading transaction options, financial batch attributes, advanced Transaction Entry settings, Statement Generator saved settings, finance security actions, teller import transactions, automated batches, and online contribution statement block names ([Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15)).
- **Rock v12.5 analytics context**: a third-party resource points to Giving Unit Analytics performance improvements in v12.5, but this pack lacks a hydrated detailed excerpt; verify in official docs or live schema before relying on exact table behavior ([Giving Unit Analytics](https://www.triumph.tech/resources/giving-unit-analytics)).
- **Rock v16.10 community receipt recipe**: receipt shortcode example uses account tax deductibility and Lava entity access; treat as a community pattern, not official behavior ([Giving Receipt System Email Shortcodes](https://community.rockrms.com/recipes/510/giving-receipt-system-email-shortcodes)).
- **Rock v17.0 community Planning Center recipe**: external giving sync pattern uses REST keys, attributes, workflow, webhook processing, and API record creation; validate security/idempotency/performance before production ([Syncing Planning Center Giving into Rock RMS](https://community.rockrms.com/recipes/521/syncing-planning-center-giving-into-rock-rms)).
- **Mobile v7.0 / Core v17.4**: Financial Batch List developer docs specify this version pairing for the batch list block ([Financial Batch List](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-list)).
- **Mobile v7.0 / Core v18**: Financial Batch Detail developer docs specify this version pairing and Azure Document Intelligence check scanning configuration ([Financial Batch Detail](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-detail)).
- **Rock v18.1**: release notes mention Financial Batch Detail/List mobile blocks for check scanning and batch management; Statement Generator single-individual fix after Data View use; Giving Receipt emails using account public name when available ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- **Rock v18.3**: release notes mention Giving History API fixes around Combine Giving With and includeGivingGroup behavior, plus performance fixes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
- **Rock v19.1**: release notes mention Pledge Analytics date-filter changes, Utility Payment Entry CAPTCHA/hosted iframe fix, Text-to-Give failed pending transaction cleanup, Contribution Statement salutation fix for combine-giving opt-out, Giving History API performance, Transaction List account summary fix, and Move Transactions To Batch visibility fix ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

Agents should always verify current installed version. The release notes page in this pack was hydrated on 2026-06-03 and included v19.1 beta and v18.3 alpha headings; production availability may differ by installation ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

## 16. Implementation Playbooks

### Playbook: Add A New Giving Account

Use [Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15) for account semantics and [Online Giving](https://community.rockrms.com/rocku/finance/online-giving) for public availability; confirm statement, pledge, gateway, batch, and accounting consequences before creating the account.

1. Confirm the business purpose with finance.
2. Decide whether this needs a true account or a transaction attribute.
3. Define internal name, public name, tax deductibility, parent/category, active status, campus constraints, and accounting code.
4. Confirm whether it should appear on online giving, mobile giving, statements, pledge analytics, and reports.
5. Create in a test environment if possible.
6. Add to Transaction Entry block account list if needed.
7. Add to statement account selection or saved settings if needed.
8. Add to pledge campaign reports if needed.
9. Test a small transaction.
10. Verify receipt language uses the intended public name.
11. Verify batch allocation and reporting.
12. Document owner and review date.

### Playbook: Configure Online Giving

1. Verify gateway is configured and tested.
2. Confirm account list and default account.
3. Confirm transaction type/source.
4. Confirm receipt email/template.
5. Confirm scheduled-giving options and allowed frequencies.
6. Confirm saved payment method/token behavior.
7. Confirm security for public/anonymous users.
8. Confirm batch creation behavior.
9. Test one-time card, ACH if enabled, split gift, failed card, and recurring profile.
10. Inspect resulting transaction, details, payment detail, batch, receipt, and scheduled transaction.
11. Confirm statement eligibility.

### Playbook: Enable Mobile Batch Check Scanning

1. Verify installed Rock core/mobile versions support the blocks.
2. Add/configure Financial Batch List and Financial Batch Detail pages.
3. Configure Financial Batch List settings: status, allow add, detail page, campus filters, page load size, and item template as needed ([Financial Batch List](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-list)).
4. Configure Financial Batch Detail settings: transaction detail page, accounts, Azure Document Intelligence API key/endpoint, account allocation requirement, required control amount, and required control item count ([Financial Batch Detail](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-detail)).
5. Scope security to finance users only.
6. Test creating a batch.
7. Test scanning checks.
8. Verify MICR matching and person matching.
9. Verify account allocation.
10. Verify control amount and item count behavior.
11. Verify audit and reconciliation on desktop finance pages.

### Playbook: Build A Giving Analytics Report

Use [Giving Analytics](https://community.rockrms.com/rocku/finance/giving-analytics) for the operational reporting surface and [BI Financial Transaction Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-financial-transaction-report) for the BI path; reconcile any derived result to live transaction-detail and batch totals.

1. Define the question: donor count, gift count, account totals, first-time givers, lapsed givers, recurring donors, pledge progress, campus giving, or giving units.
2. Choose grain: transaction, transaction detail, person, family, giving unit, month, account.
3. Choose source: live transaction tables, analytics source/fact, BI model, or Data View.
4. Verify analytics refresh if using analytics tables.
5. Include account filters and transaction type filters.
6. Use detail grain for account totals.
7. Use giving-unit fields for household analytics.
8. Validate totals against the Transaction List and batch totals.
9. Document date field used.
10. Review security before publishing.

### Playbook: Import Giving From An External System

1. Identify source system, API, webhook model, and historical import needs.
2. Define idempotency key and storage location.
3. Map source funds to Rock accounts.
4. Map payment methods to Rock currency types.
5. Define person/business matching rules.
6. Define fallback handling for unmatched donors.
7. Define batch naming, dates, and control totals.
8. Create least-privilege API credentials.
9. Build in staging.
10. Test duplicates, refunds, failed payments, split gifts, business gifts, and anonymous gifts.
11. Reconcile source totals to Rock totals.
12. Review security and error logs.
13. Enable production with monitoring.

The Planning Center community recipe provides a detailed example pattern, but agents should strengthen it with production-grade idempotency, least privilege, and reconciliation controls ([Syncing Planning Center Giving into Rock RMS](https://community.rockrms.com/recipes/521/syncing-planning-center-giving-into-rock-rms)).

## 17. Troubleshooting Decision Tree

### A Gift Is Missing From A Person's Giving History

1. Search for the transaction by amount/date/gateway code.
2. Confirm it exists in `FinancialTransaction`.
3. Confirm `AuthorizedPersonAliasId` points to the expected person/business.
4. Confirm transaction type is included in giving history.
5. Confirm transaction details exist.
6. Confirm date range.
7. Confirm account filters.
8. Confirm combine-giving/API include-family behavior.
9. Check Rock version for v18.3 Giving History API fixes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
10. If using analytics or BI, refresh/rebuild and compare to live transaction tables.

### A Gift Is Missing From A Statement

1. Confirm the transaction is a contribution or selected transaction type.
2. Confirm detail account is selected/included.
3. Confirm transaction date is inside statement date range.
4. Confirm currency type is selected.
5. Confirm refunded/corrected settings.
6. Confirm authorized person/business.
7. Confirm combine-giving settings.
8. Confirm address requirements.
9. Confirm Data View settings from the statement run.
10. Check v18.1 single-individual statement fix if relevant ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
11. Check v19.1 salutation/combine-giving opt-out fix if names are wrong ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).

### Batch Total Does Not Match

1. Confirm control amount.
2. Sum transaction details in the batch.
3. Count transactions and compare item count.
4. Look for pending/failed text-giving records.
5. Check refunds/reversals.
6. Check split gifts and negative corrections.
7. Check moved transactions.
8. Check whether Transaction List block account summary settings are honored in this version.
9. Check v19.1 Text-to-Give pending cleanup and Transaction List fixes ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
10. Review batch audit history.

### Recurring Gift Did Not Run

1. Confirm scheduled transaction is active.
2. Confirm next payment date/frequency.
3. Confirm gateway profile exists and is active.
4. Confirm saved payment token is valid.
5. Confirm gateway/download jobs.
6. Check exception logs.
7. Check donor communication logs.
8. Confirm account details are valid/active.
9. If payment plan counts look wrong, verify gateway sync because source comments warn counts may be inaccurate when payments have not synced ([PaymentPlan.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlan.cs)).
10. Confirm whether donor changed profile outside Rock.

### Receipt Language Is Wrong

1. Identify the system email/template.
2. Inspect merge fields available for the receipt.
3. Inspect account `PublicName` and `IsTaxDeductible`.
4. Check v18.1 public-name behavior for Giving Receipt System Emails ([Rock Core Release Notes](https://www.rockrms.com/releasenotes)).
5. Test split transactions.
6. Test non-deductible payments.
7. Review custom Lava/shortcodes.
8. If using community shortcode patterns, review them for security and multi-account behavior ([Giving Receipt System Email Shortcodes](https://community.rockrms.com/recipes/510/giving-receipt-system-email-shortcodes)).
9. Get finance/legal review.

### External Import Created Duplicates

1. Identify source transaction IDs.
2. Search Rock transaction attributes/integration table for source IDs.
3. Confirm idempotency logic.
4. Confirm webhook retry behavior.
5. Confirm workflow re-entry paths.
6. Confirm batch naming and dates.
7. Void/remove duplicates only with finance approval.
8. Add duplicate detection before re-enabling automation.

## 18. Agent Task Recipes

### Recipe: Read-Only Finance Record Inspection

Use when asked, "What happened to this gift?"

Inspect:

- Transaction header.
- Transaction details.
- Payment detail.
- Batch.
- Authorized person alias and person/business.
- Account(s).
- Gateway transaction code.
- Receipt communication.
- Statement eligibility.
- Audit history.
- Exceptions.

Return:

- Transaction ID/GUID.
- Donor identity.
- Date/time.
- Total amount and detail allocations.
- Payment method.
- Batch status.
- Receipt status.
- Statement eligibility and blockers.
- Recommended next action.

### Recipe: Statement Eligibility Explanation

Use when asked, "Why is this not on the year-end statement?"

Inspect:

- Statement settings.
- Transaction date.
- Transaction type.
- Detail accounts.
- Currency type.
- Refund/correction state.
- Person/business linkage.
- Combine-giving fields.
- Address.
- Data View and saved settings.
- Rock version.

Return:

- Included/excluded verdict.
- Exact exclusion reason.
- What setting or data row controls it.
- Whether correction is data cleanup, statement setting, or expected behavior.
- Whether finance review is required.

### Recipe: Safe Account Cleanup Assessment

Use when asked to deactivate or merge accounts.

Inspect:

- Historical transactions by account.
- Scheduled transaction details.
- Pledges.
- Online giving block settings.
- Statement saved settings.
- Reports/Data Views.
- External fund mappings.
- Attributes/integrations.
- Security.

Return:

- Whether account can be deactivated.
- What still references it.
- Whether transactions should remain historical.
- Migration plan if allocations must move.
- Risks to statements and reporting.

### Recipe: Giving Automation Review

Use when asked to email, alert, or segment donors by giving behavior.

Inspect:

- Data View criteria.
- Transaction source and type filters.
- Account filters.
- Date logic.
- Scheduled transaction visibility.
- Gateway sync completeness.
- Exclusions and opt-outs.
- Communication approval.
- Test recipient count.

Return:

- Audience definition.
- Known false positives/negatives.
- Test SQL/Data View count.
- Recommended dry run.
- Communication review requirements.

The recurring-giving prompt recipe is a useful pattern but includes a clear warning about external recurring profiles not synced into Rock ([Automate asking Regular Givers to Set up Recurring Giving](https://community.rockrms.com/recipes/122)).

### Recipe: Pledge Progress Analysis

Use when asked to report pledge progress.

Inspect:

- Pledge account.
- Pledge date range.
- Gift date range.
- Pledge amount.
- Transaction details to the pledged account.
- Giving unit/person basis.
- Refund/correction handling.
- Current date vs analysis date.
- v19.1 Pledge Analytics filter naming if installed.

Return:

- Pledged amount.
- Given amount.
- Percent fulfilled.
- Expected percent by elapsed time.
- Meets/behind/ahead status.
- Date/account assumptions.

Community pledge-analysis examples use account filters, analysis date, and tolerance percent, but production reporting should be validated against current Rock pledge analytics and schema ([Pledge Analysis Page](https://community.rockrms.com/recipes/90)).

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

- Approved claims routed to this concept: `108`
- Full generated claim table: `approved-claims.md`

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| rocku-confirmed | operational_guidance | When auditing giving-related guidance, verify the full path from public giving action to Rock financial transaction, account detail, receipts, and reporting definitions. | [source](https://community.rockrms.com/rocku/finance/giving-journey-1) |
| rocku-confirmed | operational_guidance | For AI, automation, and responsible tool use, BI Financial Transaction Report should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/business-intelligence-bi/bi-financial-transaction-report) |
| rocku-confirmed | operational_guidance | The Scheduled Transactions RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/finance/scheduled-transactions) |
| rocku-confirmed | operational_guidance | The Pledges RockU lesson provides training context for reporting, analytics, and measurement; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/finance/pledges) |
| rocku-confirmed | operational_guidance | For ministry process design, Giving Overview should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/finance/giving-overview) |
| rocku-confirmed | operational_guidance | The Giving Analytics RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/finance/giving-analytics) |
| rocku-confirmed | operational_guidance | The Text Giving RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/finance/text-giving) |
| rocku-confirmed | operational_guidance | For AI, automation, and responsible tool use, Businesses should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/finance/businesses) |
| rocku-confirmed | operational_guidance | For reporting, analytics, and measurement, Financial Basics should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/finance/financial-basics) |
| rocku-confirmed | operational_guidance | The Online Giving RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/finance/online-giving) |
| rocku-confirmed | operational_guidance | For AI, automation, and responsible tool use, Pledges should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/finance/pledges) |
| rocku-confirmed | operational_guidance | For reporting, analytics, and measurement, Giving Alerts should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. _(live verification recommended)_ | [source](https://community.rockrms.com/rocku/finance/giving-alerts) |
| More |  | 96 additional approved claims are tracked in `approved-claims.md`. |  |

<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `32`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Accounts Transcript Insight](https://community.rockrms.com/rocku/finance/accounts) | approved_for_public_distillation | 1 | media-insight:94e53106a60b5495 |
| [BI Financial Transaction Report Transcript Insight](https://community.rockrms.com/rocku/business-intelligence-bi/bi-financial-transaction-report) | approved_for_public_distillation | 3 | media-insight:a815728575995f92 |
| [Batches Transcript Insight](https://community.rockrms.com/rocku/finance/batches) | approved_for_public_distillation | 1 | media-insight:90e6f49e96607114 |
| [Benevolence Transcript Insight](https://community.rockrms.com/rocku/finance/benevolence) | approved_for_public_distillation | 3 | media-insight:b69297ac23548d8d |
| [Businesses Transcript Insight](https://community.rockrms.com/rocku/finance/businesses) | approved_for_public_distillation | 3 | media-insight:f84cdc67d1626107 |
| [Check Matching Transcript Insight](https://community.rockrms.com/rocku/finance/check-matching) | approved_for_public_distillation | 2 | media-insight:160da6338d8c8c02 |
| [Contribution Statements Transcript Insight](https://community.rockrms.com/rocku/finance/contribution-statements) | approved_for_public_distillation | 1 | media-insight:20d662d37f9ac44c |
| [Dashboard Design Part 1 Transcript Insight](https://www.triumph.tech/resources/dashboard-design-part-1) | approved_for_public_distillation | 3 | media-insight:22ee135c5240caf2 |
| More |  | 24 additional reviewed media records are tracked in `approved-media.md`. |  |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 19. Source Map And Dependency Notes

Primary official sources:

- [Rock Solid Finances](https://community.rockrms.com/documentation/bookcontent/15): official finance documentation book; use for finance components, transactions, batches, accounts, pledges, payment gateways, statements, security, and version-history context.
- [Rock Core Release Notes](https://www.rockrms.com/releasenotes): use for version-specific behavior and finance/mobile/API fixes.
- [RockU Finance](https://community.rockrms.com/rocku/finance): topic index for finance training: accounts, batches, transactions, scheduled transactions, refunds, businesses, online giving, check matching, pledges, analytics, benevolence, contribution statements, settings, fundraising group, giving journey, giving overview, alerts, and text giving.

Developer and source-code sources:

- [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock): source repository.
- [AnalyticsSourceFinancialTransaction.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsSourceFinancialTransaction/AnalyticsSourceFinancialTransaction.cs): detail-grain analytics source table.
- [AnalyticsFactFinancialTransaction.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsFactFinancialTransaction/AnalyticsFactFinancialTransaction.cs): analytics fact view and giving/family/source fields.
- [AnalyticsBaseFinancialTransaction.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Reporting/AnalyticsBaseFinancialTransaction/AnalyticsBaseFinancialTransaction.cs): shared analytics fields.
- [PaymentPlan.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlan.cs): internal scheduled transaction payment-plan state and gateway-sync caveats.
- [PaymentPlanConfigurationService.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/Finance/FinancialScheduledTransaction/PaymentPlanConfigurationService.cs): payment frequency helpers and payment-plan configuration.
- [FinancialStatementTemplateTransactionSetting.cs](https://github.com/SparkDevNetwork/Rock/blob/develop/Applications/Wpf/StatementGenerator/Client/FinancialStatementTemplateTransactionSetting.cs): statement transaction filtering settings.
- [spFinance_ContributionStatementQuery.sql](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Migrations/Migrations/Version%2012.0/Version%201.12.4/202104291818024_GroupSalutation_spFinance_ContributionStatementQuery.sql): older/obsolete contribution statement recipient query and constants; useful for relationship landmarks but verify current implementation.
- [Financial Batch List](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-list): mobile batch list block settings.
- [Financial Batch Detail](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-detail): mobile batch detail/check scanning settings.

Training and operational coverage:

- [Transactions](https://community.rockrms.com/rocku/finance/transactions)
- [Batches](https://community.rockrms.com/rocku/finance/batches)
- [Accounts](https://community.rockrms.com/rocku/finance/accounts)
- [Scheduled Transactions](https://community.rockrms.com/rocku/finance/scheduled-transactions)
- [Refunds](https://community.rockrms.com/rocku/finance/refunds)
- [Businesses](https://community.rockrms.com/rocku/finance/businesses)
- [Online Giving](https://community.rockrms.com/rocku/finance/online-giving)
- [Check Matching](https://community.rockrms.com/rocku/finance/check-matching)
- [Pledges](https://community.rockrms.com/rocku/finance/pledges)
- [Giving Analytics](https://community.rockrms.com/rocku/finance/giving-analytics)
- [Benevolence](https://community.rockrms.com/rocku/finance/benevolence)
- [Contribution Statements](https://community.rockrms.com/rocku/finance/contribution-statements)
- [Financial Settings](https://community.rockrms.com/rocku/finance/financial-settings)
- [Fundraising Group](https://community.rockrms.com/rocku/finance/fundraising-group)
- [Giving Journey](https://community.rockrms.com/rocku/finance/giving-journey)
- [Giving Overview](https://community.rockrms.com/rocku/finance/giving-overview)
- [Giving Alerts](https://community.rockrms.com/rocku/finance/giving-alerts)
- [Text Giving](https://community.rockrms.com/rocku/finance/text-giving)
- [BI Financial Transaction Report](https://community.rockrms.com/rocku/business-intelligence-bi/bi-financial-transaction-report)

Community examples to use cautiously:

- [Custom Financial Transaction Attributes](https://community.rockrms.com/recipes/254): transaction attributes and Transaction Entry URL parameter pattern.
- [Automate asking Regular Givers to Set up Recurring Giving](https://community.rockrms.com/recipes/122): giving-data automation with explicit warning about externally managed recurring profiles.
- [Syncing Planning Center Giving into Rock RMS](https://community.rockrms.com/recipes/521/syncing-planning-center-giving-into-rock-rms): external giving import workflow pattern using REST keys and fund/account mapping.
- [Giving Receipt System Email Shortcodes](https://community.rockrms.com/recipes/510/giving-receipt-system-email-shortcodes): receipt language customization using account tax deductibility.
- [Pledge Analysis Page](https://community.rockrms.com/recipes/90): pledge analysis report pattern.

Dependencies on other concept areas:

- **People**: Person, PersonAlias, GivingId, businesses, addresses, merges, duplicate records.
- **Groups**: family groups, adult/child roles, giving units, fundraising groups.
- **Workflows**: giving alerts, imports, payment failures, reversal notifications, recurring-giving prompts, benevolence.
- **Security**: finance roles, account security, REST keys, Lava commands, mobile access, reports.
- **Reporting**: Data Views, Dynamic Data, analytics source/fact tables, BI jobs, Model Map, statement generator, giving overview.

Live verification checklist for agents:

- Installed Rock version and mobile version.
- Finance block types and settings.
- Financial account fields and attributes.
- Gateway plugin and sync behavior.
- Defined values for transaction type, source, currency type, and frequency.
- Transaction/detail/payment/batch rows.
- Scheduled transaction and gateway profile state.
- Statement settings and saved filters.
- Analytics refresh status.
- Security permissions and API keys.
- Relevant release notes for the installed version.
