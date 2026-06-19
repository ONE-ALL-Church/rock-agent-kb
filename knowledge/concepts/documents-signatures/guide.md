---
id: authored-documents-signatures
title: Documents And Signatures
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
---

# Documents And Signatures

<!-- BEGIN GENERATED MODEL MAP POINTERS -->
## Generated Model Map Pointers

Agents starting from this long-form guide should inspect the stable generated model-map artifacts first, then use the pre-alpha diff only for upcoming-version callouts:

- Concept data-model landmarks: [Documents And Signatures index](index.md#data-model-landmarks)
- Global model-map index: [Rock Model Map](../../model-map/index.md)
- Stable model rows: `../../model-map/stable-models.jsonl`
- Stable property rows: `../../model-map/stable-properties.jsonl`
- Pre-alpha/upcoming model rows: `../../model-map/latest-models.jsonl`
- Stable-to-pre-alpha model-map diff: `../../model-map/version-diff.jsonl`

<!-- END GENERATED MODEL MAP POINTERS -->

## 1. Executive Summary For Agents

Documents in Rock RMS are not one feature. They are a family of related patterns for storing files against records, generating mail-merge-style documents from grids, collecting electronic signatures, producing signed PDF artifacts, and connecting all of that to people, workflows, event registrations, security, communications, and CMS pages. The official Rock documentation groups this area under Entity Documents, Merge Documents, and Electronic Signatures in the [Documents](https://community.rockrms.com/documentation/core-concepts/documents) guide.

For agent work, treat "documents and signatures" as four distinct operational surfaces:

1. **Entity Documents** attach uploaded files to Rock entities such as people, groups, or other supported records. The document type defines which entity the document belongs to and which File Type controls the uploaded binary file. Rock documents this flow in [Intro to Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/intro-to-entity-documents), [Configure Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/configure-entity-documents), [Add the Block](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-the-block), [Manage Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/manage-entity-documents), and [Add Documents Using Workflows](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-documents-using-workflows).

2. **Merge Documents** are templates used to generate output from grid data. They use Lava and can be HTML or Word based. The official docs cover usage, administration, creation, and Lava behavior in [Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents), [Use Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/use-merge-documents), [Administrate Merge Templates](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/administrate-merge-templates), [Creating a Merge Document](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/creating-a-merge-document), and [Using Lava with Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/using-lava-with-merge-documents).

3. **Electronic Signatures** create a `SignatureDocument` instance from a `SignatureDocumentTemplate`, route it to an assigned signer, collect signature evidence, and optionally make a signed document valid for future use. Rock documents the feature in [Intro to Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures), [Set Up Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures), [Use Electronic Signatures in a Workflow](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow), [Use Electronic Signatures in Event Registrations](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-event-registrati), and [Manage Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/manage-signature-documents).

4. **Generated PDFs** are signed-document artifacts produced after signing. Rock can generate these itself, but the official PDF guidance warns that server-side generation can be expensive during high-volume events and may be offloaded to an external rendering service such as browserless.io, as described in [Generate PDFs for Electronic Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/generate-pdfs-for-electronic-signature-docume).

The highest-risk parts of this domain are not template syntax. They are **security**, **legal/PII handling**, **version-specific behavior**, **person matching**, **registration relationships**, and **PDF generation load**. Before making changes in a live instance, inspect the exact Rock version, block generation, template configuration, File Type and Document Type security, system communications, and entity relationships.

Agent rule of thumb: when asked to "fix a document issue," first classify the issue as Entity Document, Merge Document, Electronic Signature, or generated PDF. Then inspect the relevant template or document record, not just the page where the failure was observed.

## 2. Scope And Terminology

This guide covers:

- Entity documents attached to Rock records.
- Document Types and their connection to File Types.
- Documents blocks used on entity detail pages.
- Workflow-driven document upload using the Entity Document Add action.
- Merge templates and merge documents generated from grid data.
- HTML and Word merge document patterns.
- Lava behavior in merge documents.
- Signature document templates.
- Signature document instances.
- Signature requests and completion emails.
- Typed and drawn signatures.
- Generated signed PDFs.
- Registration and workflow signature collection.
- Model relationships and source-code landmarks.
- Reporting and operational checks.

This guide does not provide legal advice. Electronic signatures can have legal significance, but an agent should not decide whether a particular waiver, consent, release, or storage practice satisfies a jurisdiction-specific legal requirement. Instead, verify the Rock configuration and route legal content, retention rules, and signature evidence requirements to the organization’s legal or compliance owner.

Important terms:

- **Document**: A generic word that may mean an uploaded entity document, a merge output, a signature template, a signature request, or a signed PDF. Always disambiguate.
- **Entity Document**: A file entry attached to a Rock entity through a configured Document Type.
- **Document Type**: Configuration under `Admin Tools > Settings > Document Types` that defines what kind of document can be attached to which entity and which File Type stores the binary content, according to [Configure Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/configure-entity-documents).
- **File Type**: Rock’s binary file configuration surface. Entity Document behavior depends on File Type storage and security, but recent versions also enforce Document Type security for document access, as noted in the v17.8 release notes on [Rock Core Release Notes](https://www.rockrms.com/releasenotes).
- **Merge Template**: A reusable template available globally or personally for generating merge output, described in [Administrate Merge Templates](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/administrate-merge-templates).
- **Merge Document**: Output generated by merging grid rows into a selected merge template, described in [Use Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/use-merge-documents).
- **Signature Document Template**: A model in Rock’s Core category according to the [Model Map](https://community.rockrms.com/ModelMap), configured at `Admin Tools > Settings > Signature Documents`.
- **Signature Document**: A persisted signing instance generated from a template. In source code, `SignatureDocument` represents a persisted signature execution or instance in Rock.
- **Applies To Person**: The person the signed document applies to. This can differ from the signer, such as when a parent signs for a minor.
- **Assigned To Person**: The person asked to sign.
- **Signed By Person**: The person alias recorded as having signed.
- **Signed Document Text**: The rendered document text that was shown before signing. Source-code snippets indicate it does not include signature data.
- **Signature Verification Hash**: A computed integrity hash for signature-related data. Source snippets show Rock calculates it from signed document text, client IP, user agent, signed date/time, signed-by person alias, signature data, and signed name, and a save hook prevents changing it after set.
- **Generated PDF**: The PDF artifact generated after signing, containing the document content and signature evidence, described in [Generate PDFs for Electronic Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/generate-pdfs-for-electronic-signature-docume).

## 3. Documents And Signatures Mental Model

The simplest mental model is: **configuration creates allowed document shapes; operational flows create document instances; security determines who can see files and templates; workflows and registrations connect document events to ministry processes.**

### Entity Documents

Entity Documents start with configuration. An administrator defines a Document Type. That Document Type is associated with an entity type and a File Type. If a Document Type is configured for `Person`, it should be used against people. If it is configured for `Group`, it should be used against groups. The workflow documentation explicitly warns that workflow-added documents must match both the target entity and the file constraints or the action can fail, as described in [Add Documents Using Workflows](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-documents-using-workflows).

The lifecycle is:

1. Create or verify a Document Type.
2. Verify the Document Type’s entity and File Type.
3. Place a Documents block where staff should manage the documents, unless the entity already has a built-in surface such as the Person Profile documents tab.
4. Upload one or more files for a target record.
5. Use Document Type and File Type security to control visibility.
6. Report on document presence, absence, age, or type.

### Merge Documents

Merge Documents start from a grid. Rock exposes merge actions at the bottom of many grids. The merge interface shows row count, a sample of data rows, merge fields, and a selected merge template, according to [Use Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/use-merge-documents). The output is not a long-lived signature record by default; it is generated output from selected data.

The lifecycle is:

1. Start from a grid.
2. Review the row count and sample rows.
3. Inspect available merge fields.
4. Select a global or personal merge template.
5. Optionally combine family members when merging people data.
6. Generate the merged document.

Merge templates can be global, managed under `Admin Tools > Settings > Merge Templates`, or personal, managed from the user’s settings page. Global templates can be secured, and Rock enforces that security during document creation, according to [Administrate Merge Templates](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/administrate-merge-templates).

### Electronic Signatures

Electronic Signatures start from a Signature Document Template. The template controls the content, signature type, file type, communication templates, active state, validity settings, and provider behavior. A signing flow then creates a Signature Document instance from that template.

The lifecycle is:

1. Create or select a Signature Document Template under `Admin Tools > Settings > Signature Documents`, as described in [Set Up Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures).
2. Place the signature requirement in a workflow action, registration template, registration instance, or related process.
3. Rock creates a Signature Document instance with an applies-to person, assigned-to person, document name, and optional relationship to a source entity such as registration.
4. The assigned signer signs.
5. Rock captures evidence such as signed name, signed date/time, client IP, user agent, signed text, signer identity, and signature data where applicable.
6. Rock computes a verification hash and blocks later modification of that hash after it has been set.
7. Rock generates or stores a signed PDF.
8. Rock sends or can resend completion communications, depending on configuration and management actions.

The official introduction emphasizes that signatures can be used in registrations and workflows and that each electronic signature produces a signed document based on a template, as described in [Intro to Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures).

### Generated PDFs

PDF generation is a post-signature artifact step. The signed PDF is useful because the signer can receive a copy and the organization has a portable artifact. The official PDF guide warns that PDF rendering on the Rock server is resource-intensive, especially when many registrations and signatures occur at once, and recommends offloading to an external service when needed, as documented in [Generate PDFs for Electronic Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/generate-pdfs-for-electronic-signature-docume).

For agents, PDF issues usually fall into one of these branches:

- The signature was never completed.
- The signed document exists but no PDF exists.
- The Binary File Type or storage provider is misconfigured.
- External rendering is misconfigured or unavailable.
- Server load caused delayed or failed generation.
- The PDF preview in the template detail block does not match the final signed document.
- The template contains Lava, CSS, image, or external asset issues that render poorly in PDF context.

## 4. Source Authority And How To Use This Guide

Use source authority in this order:

1. **Rock official documentation** for administrative behavior and supported usage. Primary official sources in this pack include [Documents](https://community.rockrms.com/documentation/core-concepts/documents), [Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents), [Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents), and [Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures).
2. **Rock source code and model snippets** for fields, relationships, enums, block behavior, API exposure, and implementation caveats. Source-code records in this pack point to `SignatureDocumentTemplate`, `SignatureDocument`, Obsidian blocks, view model bags, status enums, and PDF preview request models in the [SparkDevNetwork/Rock](https://github.com/SparkDevNetwork/Rock) repository.
3. **Release notes** for version caveats. This pack includes release notes for signature placement, inactive-template filtering, registration document relationships, and Document Type security on [Rock Core Release Notes](https://www.rockrms.com/releasenotes).
4. **RockU training** for practical workflow and event-registration context, including electronic signatures in [RockU Event Registration](https://community.rockrms.com/rocku/event-registration/electronic-signatures), electronic signatures in [RockU Workflows](https://community.rockrms.com/rocku/workflows/electronic-signatures-1), entity documents in [RockU CMS](https://community.rockrms.com/rocku/cms/entity-documents), and merge documents in [RockU Individuals in Rock](https://community.rockrms.com/rocku/individuals-in-rock/merge-documents).
5. **Community recipes** only as examples of local patterns, not as authoritative product behavior. The source pack includes a resend-signature recipe at [Recipe 434](https://community.rockrms.com/recipes/434) and a group requirement resend helper at [Recipe 482](https://community.rockrms.com/recipes/482). Both are useful for understanding real-world pain points, but community recipes are not core-team-reviewed product documentation.

When a fact must be verified live, this guide states what to inspect. Do not infer instance-specific IDs, security rules, page routes, or configured communications from documentation alone.

## 5. Core Configuration And Data Model

### Entity Document Configuration

Entity Documents are configured through `Admin Tools > Settings > Document Types`, according to [Configure Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/configure-entity-documents). The source pack identifies these operational fields:

- **Name**: A descriptive label for the document type.
- **File Type**: The File Type used for uploaded files.
- **Entity Type**: The Rock entity the document can attach to.
- **Default document name**: The management UI may pre-populate a document name if configured for the type, according to [Manage Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/manage-entity-documents).
- **Description**: Optional explanatory metadata supplied per document entry.
- **Attached document file**: The actual uploaded file or files associated with the entity document entry.

The most important operational invariant is that the Document Type’s entity must match the entity being documented. [Add Documents Using Workflows](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-documents-using-workflows) explicitly calls out that a Group Document Type cannot be used to add a document for a Person, and a workflow can fail when the entity or file type does not match.

For live inspection:

- Check `Admin Tools > Settings > Document Types`.
- Open the Document Type detail.
- Confirm the entity type.
- Confirm the File Type.
- Confirm security on the Document Type.
- Confirm the File Type storage provider and file extension rules.
- Confirm whether the target page has a Documents block and whether block settings restrict which document types appear.

### Merge Template Configuration

Global merge templates are configured under `Admin Tools > Settings > Merge Templates`, according to [Administrate Merge Templates](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/administrate-merge-templates). Personal merge templates are configured from the user’s settings page.

A merge template should be checked for:

- Global versus personal scope.
- Template file format: HTML or Word.
- Security settings on global templates.
- Lava syntax.
- Expected row shape.
- Whether it assumes person rows, group member rows, or another entity type.
- Whether it uses straight quotes rather than stylized quotes, a documented Lava caveat in [Using Lava with Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/using-lava-with-merge-documents).
- Whether it relies on `Row.GroupMember` when group member data is needed, as described in [Using Lava with Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/using-lava-with-merge-documents).

### Signature Document Template Configuration

Signature templates are managed under `Admin Tools > Settings > Signature Documents`, according to [Set Up Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures). Source-code snippets identify the `SignatureDocumentTemplate` as a Core model exposed for REST code generation and reporting, with a table named `SignatureDocumentTemplate`.

Fields and properties surfaced by model and view-model snippets include:

- **Name**: Required friendly name, max length 100 in source snippets.
- **Description**: User-defined description or summary.
- **ProviderEntityTypeId**: Legacy provider entity type. Source snippets identify templates with provider entity type values as legacy providers.
- **ProviderTemplateKey**: Legacy provider template key.
- **BinaryFileTypeId / BinaryFileType**: Binary File Type used for generated signed document files.
- **InviteSystemCommunicationId**: Communication used for signature invitations.
- **CompletionSystemCommunication**: System Communication used for completion emails.
- **LavaTemplate**: Template used to build the signature document.
- **IsActive**: Active flag. Release notes show inactive-template filtering has had version-specific fixes.
- **DocumentTerm**: A plain-language term for the document, such as waiver or release form.
- **SignatureType**: The kind of signature collected, such as typed or drawn.
- **SignatureInputTypes**: Available signature input types surfaced to the template detail view model.
- **PdfUrl**: PDF URL surfaced by the template detail view model.
- **CanAdministrate**: Whether current user can administer the template in the Obsidian block.
- **IsValidInFuture**: Whether signed documents generated by this template may remain valid for future use.
- **ValidityDurationInDays**: Number of days a signature remains valid, honored only when `IsValidInFuture` is enabled.

The Obsidian Signature Document Template Detail block has a **Default File Type** block setting whose default Binary File Type GUID is Rock’s signed document file type, according to the source-code snippet for `SignatureDocumentTemplateDetail.cs`. That block also has a **Show Legacy Signature Providers** setting; its description warns that legacy provider support is on a removal path. The `SignatureDocumentTemplateService` source snippets mark legacy provider send and cancel methods obsolete and state that legacy signature providers are no longer supported in Rock as of the RockObsolete 19.0 marker.

### Signature Document Instance Data

The `SignatureDocument` model represents a persisted signing instance. Source snippets identify fields and view-model properties including:

- **SignatureDocumentTemplateId**: Template used to create the signing instance.
- **Name**: Document name.
- **DocumentKey**: A key used to locate the document for signing or lookup.
- **RequestDate**: Request timestamp.
- **Status**: Signature document status.
- **LastStatusDate**: Last time status changed.
- **AppliesToPersonAliasId**: Person alias the document applies to.
- **AssignedToPersonAliasId**: Person alias assigned to sign.
- **SignedByPersonAliasId**: Person alias that signed.
- **SignedDocumentText**: Rendered document text shown before signing, without signature data.
- **SignedName**: Name entered or recorded at signing.
- **SignedClientIp**: Observed client IP.
- **SignedClientUserAgent**: Observed user agent.
- **SignedDateTime**: Date and time signed.
- **SignedByEmail**: Email address used for completion receipt.
- **SignatureDataEncrypted**: Encrypted signature data for drawn signatures.
- **SignatureVerificationHash**: Hash used to prove the signature document has not changed after signing.
- **BinaryFileId / BinaryFile**: Generated signed file artifact.
- **CompletionEmailSentDateTime**: When the completion email was sent.
- **InviteCount**: Number of invites.
- **LastInviteDate**: Last invite timestamp.
- **EntityTypeId / EntityType**: Related entity type, such as registration.
- **EntityId**: Related entity ID.
- **IsLegacyDocument**: View-model flag for legacy documents.

Status values are defined in the `SignatureDocumentStatus` enum:

- `None = 0`: Document has not yet been sent.
- `Sent = 1`: Document has been sent but not signed.
- `Signed = 2`: Document has been signed.
- `Cancelled = 3`: Document was cancelled.
- `Expired = 4`: Invite expired.

## 6. Primary Entities And Relationships

### Entity Document Relationships

The source pack gives less source-code detail for Entity Documents than for signatures, so agents should verify exact table and property names in the live model map, REST API, or database before writing reports or automation. Operationally, the relationships are clear from official docs:

- A **Document Type** is associated with one **Entity Type**.
- A **Document Type** is associated with one **File Type**.
- An **Entity Document** attaches a file entry to a specific entity instance.
- A **Documents block** displays and manages documents for the current entity context.
- A **Person** can use a built-in person profile document surface.
- Other entities, such as **Group**, need an appropriate Documents block placed on a page, as described in [Add the Block](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-the-block).

Live verification steps:

- Inspect the Document Type detail to confirm the target entity.
- Inspect the block type and settings on the page where documents are managed.
- Confirm the block’s entity context or entity ID source.
- Confirm File Type storage and security.
- Confirm Document Type security, especially on Rock versions with Document Type View Permissions changes.

### Merge Document Relationships

Merge documents are less about persisted entity relationships and more about a grid-to-template contract:

- A grid provides rows.
- The merge screen shows the available merge fields.
- The merge template references row data using Lava.
- The selected template generates output for the selected row shape.
- Global templates are shared and can be secured.
- Personal templates belong to the current user.

The official docs note that merge templates can be used with any entity type, but are commonly used with people. They also state that group member entities are converted to people for broader template compatibility, with group member data available through the `GroupMember` property, as described in [Using Lava with Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/using-lava-with-merge-documents).

### Signature Document Relationships

The signature model has richer relationships:

- `SignatureDocumentTemplate` defines the reusable template.
- `SignatureDocument` is the created signing instance.
- `SignatureDocument.SignatureDocumentTemplateId` points back to the template.
- `SignatureDocument.AppliesToPersonAliasId` identifies whom the document applies to.
- `SignatureDocument.AssignedToPersonAliasId` identifies whom the request is assigned to.
- `SignatureDocument.SignedByPersonAliasId` identifies who actually signed.
- `SignatureDocument.BinaryFileId` points to the signed PDF file artifact when generated.
- `SignatureDocument.EntityTypeId` and `EntityId` relate the signature document to a source entity such as registration.
- Event registration records may have a `SignatureDocumentId` relationship in versions addressed by the v18.3 release note on registration blocks, documented in [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

The distinction between applies-to, assigned-to, and signed-by is central. In child event registrations, the document may apply to a child while a parent or guardian is assigned to sign. Community resend workflows exist because a request can be routed to the wrong person or need to be resent to a registrar; see [Recipe 434](https://community.rockrms.com/recipes/434) as a non-authoritative example of this operational problem.

## 7. Common Documents And Signatures Workflows

### Add A Document To A Person

Use this when staff need to store a static document such as a form, certificate, permission letter, or scanned artifact on a person record.

Process:

1. Confirm the Document Type exists for the `Person` entity.
2. Confirm the Document Type’s File Type allows the expected file extension and storage location.
3. Confirm Document Type and File Type security.
4. Open the person’s profile document surface.
5. Add the document.
6. Set document name and optional description.
7. Upload the file.
8. Save.
9. Verify that the correct staff roles can view the document and that unauthorized roles cannot.

If the file cannot be selected or saved, inspect the File Type first. If the type is not available in the picker, inspect the Document Type’s entity and the page/block settings.

### Add Documents To Groups Or Other Entities

Use this when documents belong to a group, event, organization-specific custom entity, or another non-person record.

Process:

1. Create a Document Type for the target entity, such as Group.
2. Add or verify a page where that entity is displayed.
3. Add the Documents block if the page does not already include one.
4. Configure the block for the entity context.
5. Add the document from the block.
6. Verify security.

[Add the Block](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-the-block) describes why non-person entities require this extra block placement step.

### Add Entity Documents From Workflows

Use the Entity Document Add workflow action when an uploaded file or generated file should become an entity document.

Process:

1. Confirm the workflow has the target entity available.
2. Confirm the Document Type entity matches the target entity.
3. Confirm the uploaded file conforms to the File Type.
4. Add the Entity Document Add action.
5. Test with a known entity and a known valid file.
6. Verify that the saved file is linked to the parent document record.

Version caveat: Rock v17.8 fixed a high-severity issue where files uploaded through Entity Document Add were not properly linked to their parent Document, causing access checks to fall back to File Type security instead of Document Type security. The release notes say files are now linked so Document Type security applies as intended; they also describe default security copying and public-viewable warning labels on Document Types, in [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

### Generate A Merge Document From A Grid

Use this for letters, labels, reports, personal ministry communication, printable lists, or Word/HTML output from selected records.

Process:

1. Navigate to the grid.
2. Apply filters so the grid contains the intended records.
3. Open the merge action.
4. Review the count.
5. Review sample data rows.
6. Review available merge fields.
7. Decide whether to combine family members.
8. Select the merge template.
9. Generate the document.
10. Verify output before using it externally.

The merge interface details come from [Use Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/use-merge-documents).

### Collect A Signature In A Workflow

Use this when a business process must pause for a signature, such as volunteer consent, facility use, ministry onboarding, or a custom approval flow.

Process:

1. Create a Signature Document Template.
2. Create workflow attributes for the applies-to person, assigned-to person, and optional selected template.
3. Add the Electronic Signature workflow action.
4. Configure either a specific Signature Document Template or a dynamic selected template field.
5. Configure applies-to person and assigned-to person.
6. Configure document name.
7. Configure any invite content or email behavior needed by the workflow.
8. Persist the workflow before sending if the signing page must return to workflow context.
9. Test as the assigned signer.
10. Verify the `SignatureDocument` status, signed text, signer, PDF, and completion email.

The workflow action is described in [Use Electronic Signatures in a Workflow](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow). The official docs state that if a template is selected directly in the action, a later dynamic selected-document field is ignored; this matters when troubleshooting why a workflow is not using the expected template.

### Collect A Signature In Event Registration

Use this for waivers and release forms during event registration. Rock’s docs state that if the person being registered already has a valid signed document for the required form, Rock should not require the same signature again, relying on standard person matching logic. The same article warns that electronic signatures for event registrations require the Obsidian version of the external Registration Entry block, and that block generation must match the signature document generation being used, as described in [Use Electronic Signatures in Event Registrations](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-event-registrati).

Process:

1. Create or verify the Signature Document Template.
2. Configure validity if the signature can be reused.
3. Attach the required signature template to the registration template or relevant event-registration configuration.
4. Verify the external site uses the Obsidian Registration Entry block.
5. Run a test registration for a new person.
6. Run a second test where the person already has a valid signed document.
7. Verify whether Rock skips or requires signing as expected.
8. Inspect the registrant record and related Signature Document ID.
9. Verify completion email and generated PDF.

Version caveat: v18.3 fixed an internal Event Registration block issue where a signature document could be shown for a registrant without a valid `SignatureDocumentId`, because matching used person instead of the registrant relationship. The release notes say blocks were updated to use the registrant’s SignatureDocument relationship and that a data migration backfilled missing values when a valid matching document existed, excluding legacy templates, in [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

## 8. Document Templates Deep Dive

"Document template" can mean two different things in Rock conversations:

- A **Merge Template** used for merge documents.
- A **Signature Document Template** used for electronic signatures.

Agents must clarify which kind is involved before changing anything.

### Merge Templates

A merge template is selected from a grid merge action. Rock supports HTML and Word formats, according to [Creating a Merge Document](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/creating-a-merge-document). HTML templates are plain HTML files with Lava. Word templates allow Lava content inside a Word document, but agents should test output carefully because word-processing layout, table repetition, image placement, and syntax quoting can be fragile.

Operational template rules:

- Keep global templates generic and secured.
- Put one-off personal templates in user settings.
- Use the merge screen’s "Show Merge Fields" data to design the template.
- Avoid assuming fields exist across grids.
- For person-oriented templates, use fields that are likely to appear across person grids.
- For group member data, use the documented `Row.GroupMember` access pattern if group member attributes are needed, as described in [Using Lava with Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/using-lava-with-merge-documents).
- Avoid smart quotes in Lava.
- Test with sample rows before sending or printing broadly.

### Signature Document Templates

A signature document template has more lifecycle consequences than a merge template because it produces signed records. According to [Set Up Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures), templates are managed under `Admin Tools > Settings > Signature Documents`, and Rock ships example templates such as Photo Release and Field Trip Release for reference.

Template fields and operational implications:

- **Name**: Use a clear name. Workflows and registration templates often present this name to admins. Ambiguous names cause incorrect template selection.
- **Description**: Use this for admin-facing explanation, not the full legal document.
- **Document Term**: Use a human-friendly term such as waiver, release, consent, agreement, or permission form.
- **Lava Template**: The legal/body content rendered for the signer.
- **Signature Type**: Determines typed versus drawn behavior.
- **Binary File Type**: Determines where generated signed PDFs are stored.
- **Invite Communication**: Controls request email behavior.
- **Completion Communication**: Controls completion receipt behavior.
- **Is Active**: Controls whether template should be selectable. Because inactive filtering has had fixes in earlier versions, verify version behavior when a disabled template still appears.
- **Valid In Future**: Determines whether a signed document can satisfy future signing requirements.
- **Validity Duration In Days**: Limits future validity when future validity is enabled.
- **Legacy Provider Fields**: Provider entity type and provider template key indicate legacy provider behavior; source snippets mark legacy provider methods obsolete and no longer supported in Rock 19 context.

Template design guidance:

- Use legal language supplied by the organization.
- Keep signer instructions plain.
- Use Lava only for values that should be rendered at signing time.
- Do not include private operational notes in the template body.
- Test template preview and live signing output.
- Verify PDF output, not just browser output.
- Use typed signatures unless there is a strong reason for drawn signatures. The official setup article strongly recommends typed signatures and notes drawn signatures are PII, in [Set Up Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures).
- If using Rock v17.0 or later behavior, evaluate the optional `<!--[[ SignatureDetails ]]-->` placement keyword added for inserting the signer’s final signature at a specific place in the template, documented in [Rock Core Release Notes](https://www.rockrms.com/releasenotes) and summarized by [Triumph Tech GitHub Spotlight 1/8/2025](https://www.triumph.tech/resources/github-spotlight-182025).

### Signature Placement

Historically, signature details were commonly appended or placed in a standard location. The v17.0 release note says Electronic Signatures were updated to allow inserting the signature at specific places using the optional `<!--[[ SignatureDetails ]]-->` keyword, on [Rock Core Release Notes](https://www.rockrms.com/releasenotes). Agents should verify the Rock version and template body before assuming this keyword is supported.

If a signature appears in the wrong place:

1. Confirm Rock version.
2. Open the Signature Document Template.
3. Search for `<!--[[ SignatureDetails ]]-->`.
4. Verify whether the template is legacy or Rock-native.
5. Preview the PDF.
6. Complete a test signature and inspect the actual signed PDF.
7. Check release notes for version-specific behavior.

## 9. Electronic Signatures Deep Dive

### Anatomy Of A Rock Electronic Signature

A Rock electronic signature is a generated signature document instance based on a template. The official introduction describes a signing document based on a template and notes that each signature produces a signed document, in [Intro to Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures).

A robust agent mental model includes:

- **Template**: What is being signed.
- **Applies-to person**: Whose participation, record, or responsibility the document concerns.
- **Assigned-to person**: Who is asked to sign.
- **Signer**: Who actually signs.
- **Source**: What process generated the request, such as workflow or registration.
- **Evidence**: Signed text, signed date/time, signed name, client IP, user agent, signer identity, signature data if drawn, and verification hash.
- **Artifact**: Generated signed PDF stored as a binary file.
- **Validity**: Whether this signature can satisfy future requirements.

### Typed Versus Drawn Signatures

The official setup docs strongly recommend typed signatures over drawn signatures and note that drawn signatures are PII, in [Set Up Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures). Source snippets reinforce why: drawn signature data is stored as encrypted image data in `SignatureDataEncrypted`, with the unencrypted `SignatureData` property hidden from reporting and Lava.

Agent guidance:

- Prefer typed signatures for new templates unless the organization has a documented requirement for drawn signature capture.
- If drawn signatures are already used, audit who can view or export signature data.
- Do not expose drawn signature data in reports, Lava, API responses, or public pages.
- Verify storage encryption behavior in the current Rock version before making compliance claims.
- Treat signed PDFs containing drawn signatures as sensitive files.

### Validity And Reuse

Signature templates can be configured so documents may remain valid for future use. Source snippets expose `IsValidInFuture` and `ValidityDurationInDays`. The event registration docs give a practical example: if a person already has a valid signed document for the required release, Rock should not require the same form again, as described in [Use Electronic Signatures in Event Registrations](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-event-registrati).

When troubleshooting reuse:

1. Confirm the template has future validity enabled.
2. Confirm validity duration.
3. Confirm the existing signature is for the same template.
4. Confirm the applies-to person matches the registrant/person.
5. Confirm person matching found the correct person.
6. Confirm the existing signature status is signed.
7. Confirm the signed date is within the validity window.
8. Confirm the registration flow is using the supported Obsidian block.
9. Inspect version-specific registration fixes around `SignatureDocumentId`.

### Workflows

The Electronic Signature workflow action presents a signing step within a workflow, similar to a workflow form, according to [Use Electronic Signatures in a Workflow](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow).

Important workflow action configuration concepts from the source pack:

- **Signature Document Template**: Direct selected template.
- **Select Signature Document**: Dynamic template ID or GUID, often through a workflow attribute.
- **Applies To Person**: Person the document applies to.
- **Assigned To Person**: Person asked to sign.
- **Document Name**: Name of the generated document.

The official workflow article notes that if the direct template field is populated, the dynamic selection field is ignored. When a workflow is using the wrong template, this is one of the first settings to inspect.

Workflow implementation cautions:

- Persist the workflow before sending links that need workflow context.
- Do not rely on an unpersisted workflow if the user will leave and return.
- Store selected template, applies-to person, assigned-to person, and generated document identifiers in workflow attributes when needed for later troubleshooting.
- Avoid SQL delete or direct mutation patterns unless reviewed by a senior Rock developer. Community recipes may use SQL deletion for local needs, but those are not core authoritative patterns.

### Event Registrations

Electronic signatures in event registrations are highly sensitive because they combine external CMS forms, person matching, payment flows, registrant records, family/minor relationships, email delivery, and signed artifacts.

Key requirements:

- Use the Obsidian Registration Entry block for current electronic signatures, per [Use Electronic Signatures in Event Registrations](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-event-registrati).
- Do not mix block generations and legacy signature documents without verifying compatibility.
- Test parent-signs-for-child scenarios.
- Test existing-valid-signature scenarios.
- Inspect `SignatureDocumentId` relationships on registrants in versions affected by v18.3 fixes.
- Confirm completion email delivery.
- Confirm signed PDF generation.

### Managing Signed Documents

Administrators can view signature documents by navigating to `Admin Tools > Settings > Signature Documents`, selecting a template, and reviewing documents for that template, according to [Manage Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/manage-signature-documents). The documentation notes that document names combine the source and the person’s name in the documented example, and that selecting a signed document shows detail and allows resending the completion email.

When inspecting a signed document:

- Verify template.
- Verify document name.
- Verify applies-to person.
- Verify assigned-to person.
- Verify signed-by person.
- Verify status.
- Verify signed date/time.
- Verify generated PDF.
- Verify completion email sent timestamp.
- Verify related registration or workflow source.
- Verify that the document is not legacy unless expected.

## 10. Generated PDFs Deep Dive

### What The PDF Represents

After signing, Rock generates a PDF containing the signed content and signature information so the signer can receive a copy, according to [Generate PDFs for Electronic Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/generate-pdfs-for-electronic-signature-docume). This PDF is not just a visual convenience; it is an operational artifact tied to communications, storage, and later review.

Source snippets show `SignatureDocument` has `BinaryFileId` and view-model `binaryFile` properties, while the template references a Binary File Type. A dev SQL script in the source pack identifies the well-known Binary File Type GUID for Digitally Signed Documents as `40871411-4E2D-45C2-9E21-D9FCBA5FC340`. Agents should verify that GUID in the live instance before relying on it, especially in customized or upgraded systems.

### PDF Preview Versus Signed PDF

The Obsidian Signature Document Template Detail source includes request bags for getting a PDF preview URL from:

- Lava template.
- Binary file type.
- Signature type.

This implies admins can preview signature template PDF rendering before actual signing. Preview is useful but not sufficient. A real signed document includes signer-specific evidence and may run in a different context than the preview. Always test a real signing flow before treating a template as production-ready.

### Performance And Offloading

The official PDF guide warns that generating PDFs on the Rock server can be resource-intensive, especially during high-traffic registration events, and recommends offloading to a third-party service such as browserless.io when needed, in [Generate PDFs for Electronic Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/generate-pdfs-for-electronic-signature-docume).

Operational checks before a high-volume event:

- Estimate expected registrations per hour.
- Estimate signatures per registration.
- Confirm whether PDF generation is local or offloaded.
- Confirm external rendering credentials and endpoint.
- Test PDF generation under load if possible.
- Monitor web server CPU, memory, queue length, and exception logs.
- Confirm completion emails are not delayed by PDF generation.
- Confirm generated Binary Files are being stored in the expected provider.
- Have a fallback plan if PDF generation lags but signatures are captured.

### PDF Troubleshooting

If signed documents exist but PDFs are missing:

1. Confirm `SignatureDocument.Status = Signed`.
2. Confirm `SignedDateTime` is set.
3. Confirm `BinaryFileId` is null or invalid.
4. Inspect exception logs around signing time.
5. Inspect PDF generation configuration.
6. Inspect Binary File Type storage provider.
7. Inspect permissions for the storage location.
8. If offloaded, inspect external service logs and credentials.
9. Retry PDF generation only through supported UI or API paths.
10. Do not directly insert fake BinaryFile records in production.

If PDFs render incorrectly:

1. Compare browser signing view to PDF output.
2. Inspect template HTML and CSS.
3. Remove external assets or ensure they are accessible to the renderer.
4. Verify images are HTTPS-accessible if external rendering is used.
5. Test simple template content.
6. Verify `<!--[[ SignatureDetails ]]-->` placement if used.
7. Test typed and drawn signature variants if both are available.
8. Inspect PDF preview request behavior in the template detail block.

## 11. Related Rock Areas: People, Workflows, Communications, Security, Platform Configuration, Cms

### People

People are central to signature behavior. Applies-to, assigned-to, and signed-by are all person-alias-based relationships in source snippets. Event registration reuse also depends on matching the registrant to a person who already has a valid signature, according to [Use Electronic Signatures in Event Registrations](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-event-registrati).

Agent checks:

- Confirm the person record.
- Confirm person aliases.
- Confirm family relationships when a parent signs for a child.
- Confirm duplicate records are not causing person matching failures.
- Confirm whether the signed document applies to the participant or the signer.

### Workflows

Workflows can request signatures and add entity documents. RockU lists electronic signatures within workflow training in [RockU Workflows](https://community.rockrms.com/rocku/workflows/electronic-signatures-1), and official documentation covers the workflow signature action in [Use Electronic Signatures in a Workflow](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow).

Agent checks:

- Workflow type security.
- Workflow persistence.
- Workflow entry page.
- Signature action configuration.
- Dynamic template selection.
- Person attributes.
- Email actions.
- Completion path.
- Retry behavior.

### Communications

Signature templates can have invite and completion communications. Source snippets expose `InviteSystemCommunicationId` and `CompletionSystemCommunication`. The management doc notes that signed document detail can resend a completion email, in [Manage Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/manage-signature-documents).

Agent checks:

- Invite system communication.
- Completion system communication.
- From address and reply-to.
- Lava merge fields in communication.
- Whether the assigned signer has a valid email.
- Communication history.
- Email transport errors.
- Whether completion emails require a generated PDF before sending.

### Security

Security is the most important cross-cutting concern. Entity Documents depend on Document Type and File Type security. Merge templates can be secured. Signature documents and signed PDFs can contain sensitive personal and legal information. Drawn signatures are PII per [Set Up Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures).

Release-note caveat: v17.8 changed Document Type security behavior for workflow-added entity documents and surfaced public-viewable warnings on Document Types, in [Rock Core Release Notes](https://www.rockrms.com/releasenotes). Before assuming access behavior, inspect the Rock version and the current Document Type security.

Agent checks:

- Who can view the Document Type.
- Who can view the File Type.
- Whether the Document Type is publicly viewable.
- Whether signed PDFs are exposed through public links.
- Whether external site pages require authentication.
- Whether workflow types have appropriate view permissions.
- Whether reports expose signed document data.
- Whether API keys can read signature documents.

### Platform Configuration

Platform configuration includes Binary File Types, storage providers, system communications, background jobs, external PDF services, and block settings.

Agent checks:

- Binary File Type for signed documents.
- Storage provider and container/path settings.
- File extension and size limits.
- PDF generation configuration.
- External rendering endpoint.
- System communications.
- Exception logs.
- Rock version and release notes.

### CMS

CMS matters because signatures and document blocks may appear on internal and external pages. Event registration signatures require the appropriate external Registration Entry block generation, according to [Use Electronic Signatures in Event Registrations](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-event-registrati). Entity Documents for non-person entities may require adding a Documents block to a CMS page, per [Add the Block](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-the-block). RockU also places Entity Documents in CMS training context at [RockU CMS Entity Documents](https://community.rockrms.com/rocku/cms/entity-documents).

Agent checks:

- Page route.
- Block type generation: WebForms versus Obsidian.
- Block settings.
- Page security.
- Site type.
- Context entity.
- External user experience.
- Return URL after signing.

## 12. Administration And Operational Guardrails

### Before Creating A New Document Type

Use this checklist:

- What entity is this document for?
- Should the document be stored on Person, Group, Registration, or another entity?
- Does a Document Type already exist?
- Which File Type should store the file?
- Does the File Type allow the expected file extension?
- Who should view the document?
- Who should upload or edit it?
- Should the document be reportable?
- Is the content sensitive?
- Does retention policy apply?

Do not create a new Document Type for every minor variation if one governed type with a document name or description is sufficient. But do not reuse a broad Document Type for sensitive documents if it weakens security.

### Before Creating A New Signature Template

Use this checklist:

- Has legal/content owner approved the body text?
- Is the template for one document type or multiple?
- Should a signature remain valid for future use?
- If valid in future, for how many days?
- Should the document apply to the participant, signer, or another person?
- Should a parent/guardian sign for a child?
- Should the signature be typed?
- Which Binary File Type stores the signed PDF?
- Which invite email is used?
- Which completion email is used?
- Should signature placement use `<!--[[ SignatureDetails ]]-->`?
- Has the template been tested in browser view and PDF output?
- Has the workflow or registration path been tested end to end?

### Naming Standards

Suggested naming patterns:

- Signature templates: `Ministry - Document Purpose - Version/Year`, for example `Kids - Field Trip Release - 2026`.
- Document Types: `Entity - Document Category`, for example `Person - Background Check Consent`.
- Merge templates: `Audience - Output Purpose`, for example `Family - Camp Scholarship Letter`.
- Workflow attributes: `AppliesToPerson`, `AssignedToPerson`, `SignatureDocumentTemplate`, `SignatureDocument`, `SignedDocument`.

### Security Guardrails

For any public or external flow:

- Never assume a signed document URL is safe because it is hard to guess.
- Confirm page security.
- Confirm file access checks.
- Confirm Document Type and File Type security.
- Confirm workflow type view permissions.
- Confirm template detail and document list pages are staff-only.
- Confirm public registration pages expose only the required signing step.
- Confirm generated PDFs are not indexed or linked publicly.

### Data Integrity Guardrails

Do not directly update or delete signature records in production unless there is an approved remediation plan. Source snippets show Rock uses a verification hash and save hook to protect signed document integrity. Direct SQL changes can damage legal evidence, break related registrant records, or invalidate audits.

If a signature request was sent to the wrong person, prefer supported resend, cancel, or reissue behavior. Community recipes such as [Recipe 434](https://community.rockrms.com/recipes/434) illustrate why organizations build helper workflows, but those recipes include direct deletion patterns and should not be treated as product-approved data correction procedures.

## 13. Developer, API, Lava, And Source-Code Landmarks

### Source-Code Landmarks

The source pack includes these important Rock source-code locations:

- `Rock/Model/Core/SignatureDocumentTemplate/SignatureDocumentTemplate.cs`: Core model for signature templates, table `SignatureDocumentTemplate`, REST code generation, active flag, reporting include attributes, and fields such as name, description, provider data, binary file type, invite communication, Lava template, active state, document term, and signature type.
- `Rock/Model/Core/SignatureDocumentTemplate/SignatureDocumentTemplate.Logic.cs`: Defines the default Lava template placeholder.
- `Rock/Model/Core/SignatureDocumentTemplate/SignatureDocumentTemplateExtensionMethods.cs`: Identifies legacy provider templates by provider entity type.
- `Rock/Model/Core/SignatureDocumentTemplate/SignatureDocumentTemplateService.cs`: Marks legacy provider send/cancel methods obsolete and no longer supported.
- `Rock.Blocks/Core/SignatureDocumentTemplateDetail.cs`: Obsidian detail block for signature document templates, with default file type and legacy provider display settings.
- `Rock.Blocks/Core/SignatureDocumentTemplateList.cs`: Obsidian list block that counts signature documents per template and links to detail pages.
- `Rock/Model/Core/SignatureDocument/SignatureDocument.cs`: Core model for persisted signature document instances.
- `Rock/Model/Core/SignatureDocument/SignatureDocument.Logic.cs`: Formatted user agent and encrypted drawn signature data behavior.
- `Rock/Model/Core/SignatureDocument/SignatureDocument.SaveHook.cs`: Protects `SignatureVerificationHash` from modification after set.
- `Rock/Model/Core/SignatureDocument/SignatureDocumentService.cs`: Lookup by document key and deterministic signature verification hash calculation.
- `Rock.Enums/Core/SignatureDocumentStatus.cs`: Status enum values.
- `Rock.JavaScript.Obsidian/Framework/Enums/Core/signatureDocumentStatus.ts`: Obsidian enum mirror.
- `Rock.ViewModels/Blocks/Core/SignatureDocumentTemplateDetail/SignatureDocumentTemplateBag.cs`: Template detail view model fields.
- `Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/SignatureDocumentTemplateDetail/signatureDocumentTemplateBag.d.ts`: TypeScript view model mirror.
- `Rock.ViewModels/Blocks/Core/SignatureDocumentTemplateDetail/GetPdfPreviewUrlRequestBag.cs`: PDF preview request input fields.
- `Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/Core/SignatureDocumentDetail/signatureDocumentBag.d.ts`: Signature document detail view model fields.

### API Considerations

Because snippets show `[CodeGenerateRest]` on `SignatureDocumentTemplate` and `SignatureDocument`, API surfaces may exist for these models. Agents should not assume every field is safe or writable through REST. Verify:

- Endpoint availability in the current version.
- API key permissions.
- Field-level behavior.
- Whether signed fields are read-only after signing.
- Whether save hooks execute through the API.
- Whether binary files require separate upload APIs.
- Whether current Rock security checks are enforced.

### Lava In Merge Documents

Rock’s merge document docs state that most Lava skills work with Merge Templates, but with specific caveats, in [Using Lava with Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/using-lava-with-merge-documents):

- Use straight quotes.
- Group member entities may be converted to people.
- Access group member data through `Row.GroupMember` when needed.
- Use the merge screen’s field list rather than guessing field names.

### Lava In Signature Templates

Signature templates use a Lava template to build the document body. Source snippets identify `LavaTemplate` as the field used to build the signature document. Because the signed document text is stored at signing time, changes to the template after signing should not be assumed to modify existing signed document text.

Agent guidance:

- Test Lava with realistic data.
- Avoid expensive Lava operations in high-volume registration flows.
- Do not embed private implementation notes.
- Do not expose internal IDs unless required.
- Verify whether the signing context provides the objects your Lava expects.
- If using external images, verify PDF renderer access.

## 14. Reporting, Analytics, And Model Map

### Model Map

The source pack includes a [Model Map](https://community.rockrms.com/ModelMap) record identifying `Signature Document Template` as a Core model. Use Model Map to confirm model names, categories, and reporting availability. For exact field lists, verify current source code or the live Rock schema.

### Signature Reporting

Useful signature reports include:

- Count of signature documents by template.
- Count by status.
- Pending signatures by assigned person.
- Signed signatures by date.
- Expired invites.
- Missing PDFs.
- Signature documents without completion email timestamp.
- Registrants missing `SignatureDocumentId` when a required template exists.
- Signatures expiring soon based on validity duration.
- Templates with inactive status but active usage.
- Legacy provider templates still present.
- Signed documents with drawn signatures.

When reporting, avoid exposing sensitive data. Do not include raw signature data. Treat signed document text as potentially sensitive.

### Entity Document Reporting

Useful entity document reports include:

- People missing a required document.
- Groups missing a required document.
- Documents uploaded in a date range.
- Documents by Document Type.
- Document Types with public view access.
- Files whose File Type security differs from Document Type security.
- Workflow-uploaded documents created before the v17.8 security fix.
- Documents with missing binary files.

Because the source pack is thin on exact entity document model fields, verify table and model names in the live instance before writing SQL.

### Merge Document Analytics

Merge documents are usually generated on demand and may not have a persistent audit trail equivalent to signature documents. To answer "who generated a merge document," inspect:

- Rock audit logs if enabled.
- Communication history if the output was sent.
- File storage if the merge output was saved.
- Browser downloads cannot usually be reconstructed from Rock alone unless the action created a persisted artifact.

## 15. Version And Release Caveats

### Inactive Signature Templates

Rock v15.2 fixed inactive signature document templates being selectable in event registration, according to [Rock Core Release Notes](https://www.rockrms.com/releasenotes). Rock v16.1 fixed inactive signature document templates showing in workflow actions, also in [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

Agent implication: If an inactive template appears selectable, inspect the Rock version and block/action generation before assuming current behavior.

### Signature Placement Keyword

Rock v17.0 added support for placing signature details at specific places in a document template using `<!--[[ SignatureDetails ]]-->`, according to [Rock Core Release Notes](https://www.rockrms.com/releasenotes). [Triumph Tech GitHub Spotlight 1/8/2025](https://www.triumph.tech/resources/github-spotlight-182025) also summarized this as a v16.10 highlight in pre-alpha context. Treat the official release notes as higher authority for released behavior.

Agent implication: Verify version before using the keyword.

### Signature Template Detail PDF Viewer

A Triumph Tech GitHub Spotlight notes that PDFViewer was added to the Obsidian Signature Document Template Detail block in a v16.7/v17 pre-alpha context, at [GitHub Spotlight 10/4/2024](https://www.triumph.tech/resources/github-spotlight-1042024). Treat this as implementation context, not a substitute for current official docs.

Agent implication: If preview behavior is absent, inspect Rock version and whether the page is using the Obsidian block.

### Registration Signature Relationship Fix

Rock v18.3 fixed internal Event Registration blocks so they use the registrant’s `SignatureDocument` relationship instead of matching by person when showing signature documents. The release note also mentions a data migration to backfill missing `SignatureDocumentId` values when a valid match exists, excluding legacy templates, in [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

Agent implication: For signature display mismatches in registration detail pages, check Rock version, `RegistrationRegistrant.SignatureDocumentId`, the required template, and whether documents are legacy.

### Document Type Security Fix

Rock v17.8 fixed a high-severity workflow issue where Entity Document Add uploads were not linked to parent Document records, causing access to fall back to File Type security. The release notes state that files are now linked correctly and Document Type security applies; they also note default security copying for General Person Document and Giving Statement if no Document Type security existed, plus warning labels for public-viewable Document Types, in [Rock Core Release Notes](https://www.rockrms.com/releasenotes).

Agent implication: Audit workflow-uploaded entity documents and public-viewable Document Types, especially after upgrades.

### Legacy Signature Providers

Source snippets mark legacy provider methods obsolete and state legacy signature providers are no longer supported in Rock, with a RockObsolete marker for 19.0. The template detail block still has an option to show legacy providers, but its description warns support is on a removal path.

Agent implication: Do not build new workflows around legacy provider templates. For existing templates, plan migration to Rock-native electronic signatures.

## 16. Implementation Playbooks

### Playbook: Build A New Event Waiver

1. Confirm legal text with the ministry/legal owner.
2. Create a Signature Document Template under `Admin Tools > Settings > Signature Documents`.
3. Name it clearly, such as `Students - Camp Waiver - 2026`.
4. Set Document Term to `Waiver` or the organization’s preferred term.
5. Use typed signature unless there is a documented reason for drawn.
6. Configure Lava template body.
7. Configure Binary File Type for signed documents.
8. Configure invite and completion communications.
9. Enable future validity if the waiver can be reused.
10. Set validity duration if reuse expires.
11. Use `<!--[[ SignatureDetails ]]-->` only if the current Rock version supports it.
12. Preview PDF.
13. Attach template to the registration configuration.
14. Confirm external site uses Obsidian Registration Entry.
15. Test a new registrant.
16. Test parent signing for child.
17. Test existing valid signature reuse.
18. Confirm signed document status.
19. Confirm generated PDF.
20. Confirm completion email.
21. Confirm staff can view and public users cannot view admin document pages.

### Playbook: Add Documents To A Group Page

1. Create Document Type for Group.
2. Select appropriate File Type.
3. Configure security.
4. Open the Group detail page where documents should appear.
5. Add Documents block.
6. Configure block context and allowed document types.
7. Add a test document.
8. Verify upload, display, edit, delete, and security behavior.
9. Train staff on naming and description standards.

### Playbook: Build A Merge Letter Template

1. Identify the grid users will start from.
2. Generate a sample merge and inspect available fields.
3. Decide HTML or Word format.
4. Create a template using `Row` fields.
5. If group member data is needed, use the documented `Row.GroupMember` path.
6. Avoid smart quotes.
7. Test with one row.
8. Test with many rows.
9. Test family combine behavior if people are involved.
10. Save as personal or global template.
11. Apply security if global.
12. Document expected source grid for staff.

### Playbook: Move From Legacy Signature Provider To Rock-Native Signatures

1. Inventory templates with `ProviderEntityTypeId` or provider template keys.
2. Identify workflows and registration templates using those templates.
3. Create Rock-native Signature Document Templates.
4. Recreate legal body content as Lava templates.
5. Configure typed signatures.
6. Configure signed document Binary File Type.
7. Configure communications.
8. Replace workflow action template references.
9. Replace registration required template references.
10. Test signing flows.
11. Confirm old templates are inactive.
12. Preserve historical documents according to retention policy.
13. Do not delete legacy records until legal and reporting owners approve.

### Playbook: Audit Document Security After Upgrade

1. Review Rock version and release notes.
2. List Document Types.
3. Identify public-viewable Document Types.
4. Compare Document Type security with paired File Type security.
5. Identify workflow-uploaded entity documents.
6. Confirm files are linked to parent document records.
7. Test access as staff and non-staff.
8. Review signed document Binary File Type security.
9. Review merge template security.
10. Review workflow type view security.
11. Remediate Document Type security first.
12. Retest access paths.

## 17. Troubleshooting Decision Tree

### Start Here: What Kind Of Document Is Broken?

If the issue is an uploaded file attached to a person, group, or entity, go to Entity Documents.

If the issue is a Word or HTML output from a grid, go to Merge Documents.

If the issue is a waiver, release, signature request, signer email, signed record, or signed PDF, go to Electronic Signatures.

If the issue is only the PDF artifact after signing, go to Generated PDFs.

### Entity Documents

Problem: Document type is not available.

- Check the Document Type’s entity.
- Check block settings.
- Check whether the current page has entity context.
- Check user security.
- Check whether the document type is active if applicable in the current version.

Problem: Upload fails.

- Check File Type extension rules.
- Check File Type storage provider.
- Check file size.
- Check exception logs.
- Check workflow action target entity if upload came from workflow.

Problem: Wrong users can view the document.

- Check Document Type security.
- Check File Type security.
- Check Rock version relative to v17.8 Document Type security changes.
- Check whether the file is linked to the parent Document.
- Check public page routes and direct file URLs.

### Merge Documents

Problem: Merge fields are blank.

- Check the source grid’s available fields.
- Use the merge screen’s field list.
- Confirm template expects `Row` fields.
- Confirm group member data is accessed through `Row.GroupMember` when needed.
- Confirm the grid contains the expected entity type.

Problem: Lava error.

- Check straight quotes.
- Check filter syntax.
- Test with a simple template.
- Remove complex conditionals.
- Confirm fields exist.
- Confirm Word did not transform characters.

Problem: Wrong records merged.

- Check grid filters.
- Check selected rows.
- Check family combine option.
- Check whether the grid is person-based or group-member-based.

### Electronic Signatures

Problem: Template does not show in workflow action.

- Check template `IsActive`.
- Check Rock version relative to v16.1 inactive-template filtering.
- Check whether the action is configured to show Rock-native or legacy templates.
- Check security.

Problem: Template does not show in registration.

- Check template `IsActive`.
- Check Rock version relative to v15.2 inactive-template filtering.
- Check registration block generation.
- Check required signature template configuration.

Problem: Wrong template is used in workflow.

- Check whether the direct Signature Document Template field is set.
- If it is set, the dynamic selected-template field may be ignored, per [Use Electronic Signatures in a Workflow](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow).
- Check workflow attributes and Lava that compute template ID or GUID.

Problem: Parent cannot sign for child.

- Check applies-to person.
- Check assigned-to person.
- Check signer email.
- Check registration person matching.
- Check document name and source entity.
- Test with a known family.

Problem: Registration shows wrong signed document.

- Check Rock version relative to v18.3 registration fix.
- Inspect registrant `SignatureDocumentId`.
- Confirm document template matches required template.
- Confirm document applies to the correct person.
- Confirm it is not a legacy template unless expected.

Problem: Completion email did not send.

- Check completion communication on template.
- Check signer email.
- Check `CompletionEmailSentDateTime`.
- Check communication logs.
- Check whether PDF generation failed before email send.

### Generated PDFs

Problem: No PDF.

- Check status is signed.
- Check `BinaryFileId`.
- Check signed date/time.
- Check PDF generation configuration.
- Check exception logs.
- Check external rendering service if used.
- Check Binary File Type storage.

Problem: PDF looks wrong.

- Check template HTML.
- Check CSS support.
- Check image URLs.
- Check signature placement keyword.
- Check typed versus drawn rendering.
- Compare preview and live signed output.

Problem: Server slows during registration launch.

- Check PDF generation load.
- Offload rendering if needed, per [Generate PDFs for Electronic Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/generate-pdfs-for-electronic-signature-docume).
- Monitor CPU, memory, logs, and queueing.
- Consider staging communications or testing high-volume signing ahead of launch.

## 18. Agent Task Recipes

### Recipe: Find All Pending Signature Requests For A Template

Inspect:

- `SignatureDocumentTemplate` by name or ID.
- Related `SignatureDocument` records where status is `Sent`.
- Assigned-to person alias.
- Last invite date.
- Invite count.
- Related entity type and ID.

Report:

- Template name.
- Count pending.
- Oldest pending request.
- Requests with no assigned person.
- Requests with missing email.
- Requests tied to registration or workflow.

### Recipe: Verify A Person Has A Valid Signed Waiver

Inspect:

- The person and aliases.
- Signature template ID.
- `SignatureDocument` records for applies-to person alias.
- Status `Signed`.
- Signed date/time.
- Template validity settings.
- Validity duration.
- Binary file presence.
- Whether document is legacy.

Report:

- Found or not found.
- Signed date.
- Expiration date if duration applies.
- Signed by person.
- PDF present or missing.
- Any ambiguity due to duplicates or multiple aliases.

### Recipe: Diagnose A Failed Registration Signature

Inspect:

- Registration instance.
- Registration template required signature template.
- External Registration Entry block generation.
- Registrant person alias.
- Registrant `SignatureDocumentId`.
- Existing valid signatures for that person and template.
- Signature document status.
- Exception logs.

Report:

- Whether the signature was required.
- Whether it was skipped because a valid signature already existed.
- Whether a Signature Document was created.
- Whether the registrant is linked to it.
- Whether the signer completed it.
- Whether the PDF and completion email exist.

### Recipe: Audit Public Exposure Risk

Inspect:

- Document Types with public view.
- File Types used by documents and signed PDFs.
- Signature Documents admin pages.
- Merge Template security.
- Workflow type view security.
- External signing page routes.
- Direct file URL behavior.
- API keys and roles.

Report:

- Publicly viewable Document Types.
- Sensitive File Types.
- Signed document exposure paths.
- Misaligned Document Type/File Type security.
- Recommended remediation order.

### Recipe: Build A Staff Resend Process

Prefer supported UI actions first. [Manage Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/manage-signature-documents) notes that signed document detail can resend completion email. For invite resends or reissue scenarios, inspect current Rock-supported actions before using custom workflows.

If a custom workflow is required:

- Do not delete signed records by default.
- Capture applies-to person, assigned-to person, template, and source entity.
- Create a new signature request if legally appropriate.
- Preserve the old request for audit unless approved.
- Log who initiated resend and why.
- Test parent/guardian and registrar scenarios.

Community examples such as [Recipe 434](https://community.rockrms.com/recipes/434) and [Recipe 482](https://community.rockrms.com/recipes/482) show real-world resend needs, but their implementation details should be reviewed before use.

<!-- BEGIN GENERATED APPROVED CLAIM COVERAGE -->
## Approved Claim Coverage

This generated summary links the long-form guide to the approved public claim graph. Claims remain governed by `claims/approved-claims.jsonl`; community-derived rows are labeled by authority tier and should not be treated as official Rock behavior.

No approved claims are currently routed to this concept.
<!-- END GENERATED APPROVED CLAIM COVERAGE -->

<!-- BEGIN GENERATED APPROVED MEDIA COVERAGE -->
## Approved Media Coverage

This generated summary links the long-form guide to reviewed media distillations. Full media coverage is tracked in `approved-media.md`; raw transcripts and media URLs remain private.

- Approved media records routed to this concept: `2`
- Full generated media table: `approved-media.md`

| Source | Review Status | Insights | Citation |
| --- | --- | --- | --- |
| [Electronic Signatures Transcript Insight](https://community.rockrms.com/rocku/event-registration/electronic-signatures) | approved_for_public_distillation | 2 | media-insight:7ededa8a19f050ad |
| [Electronic Signatures Transcript Insight](https://community.rockrms.com/rocku/workflows/electronic-signatures-1) | approved_for_public_distillation | 2 | media-insight:ddfbf4b112e0b7a8 |

<!-- END GENERATED APPROVED MEDIA COVERAGE -->

## 19. Source Map And Dependency Notes

Primary official documentation:

- [Documents](https://community.rockrms.com/documentation/core-concepts/documents): Top-level guide grouping Entity Documents, Merge Documents, and Electronic Signatures.
- [Intro to Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/intro-to-entity-documents): Entity documents concept.
- [Configure Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/configure-entity-documents): Document Types and File Types.
- [Add the Block](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-the-block): Non-person entity document block setup.
- [Manage Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/manage-entity-documents): Staff upload/manage behavior.
- [Add Documents Using Workflows](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-documents-using-workflows): Workflow document add behavior and entity/file-type matching.
- [Intro to Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/intro-to-merge-documents): Merge document concept.
- [Use Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/use-merge-documents): Grid merge UI.
- [Administrate Merge Templates](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/administrate-merge-templates): Global and personal merge templates.
- [Creating a Merge Document](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/creating-a-merge-document): HTML and Word formats.
- [Using Lava with Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/using-lava-with-merge-documents): Lava caveats.
- [Intro to Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures): Signature concept and anatomy.
- [Set Up Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures): Template setup and typed/drawn recommendation.
- [Use Electronic Signatures in a Workflow](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow): Workflow action configuration.
- [Use Electronic Signatures in Event Registrations](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-event-registrati): Registration signature behavior and Obsidian block requirement.
- [Generate PDFs for Electronic Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/generate-pdfs-for-electronic-signature-docume): PDF generation and offloading.
- [Manage Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/manage-signature-documents): Admin viewing and completion email resend.

Training and context:

- [RockU Event Registration Electronic Signatures](https://community.rockrms.com/rocku/event-registration/electronic-signatures): Training context for registration signatures.
- [RockU Workflow Electronic Signatures](https://community.rockrms.com/rocku/workflows/electronic-signatures-1): Training context for workflow signatures.
- [RockU CMS Entity Documents](https://community.rockrms.com/rocku/cms/entity-documents): Training context for entity documents.
- [RockU Individuals Merge Documents](https://community.rockrms.com/rocku/individuals-in-rock/merge-documents): Training context for merge documents.

Release and implementation notes:

- [Rock Core Release Notes](https://www.rockrms.com/releasenotes): Version caveats for inactive templates, signature placement, registration signature relationships, and Document Type security.
- [Triumph Tech GitHub Spotlight 1/8/2025](https://www.triumph.tech/resources/github-spotlight-182025): Secondary implementation context for signature details placement.
- [Triumph Tech GitHub Spotlight 10/4/2024](https://www.triumph.tech/resources/github-spotlight-1042024): Secondary implementation context for PDFViewer in Obsidian template detail.
- [Triumph Tech GitHub Spotlight 9/30/2025](https://www.triumph.tech/resources/github-spotlight-9302025): Secondary implementation context for Obsidian signature template list behavior.

Model and source-code dependency notes:

- Use the [Model Map](https://community.rockrms.com/ModelMap) to confirm model category and current naming.
- Use SparkDevNetwork/Rock source files for exact current fields and behavior when writing code, reports, or API integrations.
- Verify exact schema in the live instance before writing SQL, especially for Entity Documents where this source pack contains less direct model detail.
- Treat community recipes [434](https://community.rockrms.com/recipes/434) and [482](https://community.rockrms.com/recipes/482) as operational examples only, not product authority.

Live-verification dependencies:

- Rock version.
- Block generation and block settings.
- Template active state.
- Document Type and File Type security.
- Binary File Type storage.
- System communications.
- Workflow persistence.
- Registration template and registrant relationships.
- Whether legacy provider templates remain.
- Exception logs and PDF rendering service configuration.
