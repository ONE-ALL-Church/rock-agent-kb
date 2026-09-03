---
id: authored-documents-signatures
title: Documents And Signatures
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "131696e179b7feadea7c11ce1ea6b377bbcfaa72da0c430057b54df6e94a0e47"
---

# Documents And Signatures

## Agent Summary

Rock separates document work into three operational systems:

- **Entity Documents** attach stored files to a Rock entity such as a person or group. A document type determines the entity type and file type, while a Documents block provides the management interface. Multiple documents of the same type can be associated with one entity. ([Intro to Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/intro-to-entity-documents))
- **Merge Documents** generate Word or HTML output from grid data. Lava supplies the dynamic content, but the supported Lava surface differs between Word and HTML templates. ([Intro to Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/intro-to-merge-documents))
- **Electronic Signatures** generate an individual signing document from a signature document template, distinguish the document subject from the signer, and normally produce a signed PDF after completion. They can be used from workflows and event registrations. ([Intro to Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures), [Generate PDFs for Electronic Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/generate-pdfs-for-electronic-signature-docume))

For troubleshooting, identify which system owns the problem before changing configuration. A merge-template rendering failure, an entity-document permission failure, and an electronic-signature assignment failure may all involve files, but they have different configuration and security paths.

## Scope And Boundaries

This guide covers:

- Entity document types, file-type relationships, page context, block configuration, document-level security, manual uploads, and workflow-created entity documents.
- Personal and global merge templates, grid-to-document operations, Word and HTML templates, supported Lava patterns, and family-row behavior.
- Signature document templates, signer roles, workflow and registration use, completion PDFs, document administration, and version-sensitive security behavior.
- Bounded evaluation of community resend and workflow patterns.

Related concepts remain responsible for their broader domains:

- Person identity, aliases, matching, adult/child classification, and profile-page administration belong to **People**.
- General action execution, persistence, forms, triggering, and workflow security belong to **Workflows**.
- System Communications, recipient delivery, and email diagnostics belong to **Communications**.
- File-type security, authorization design, and personally identifiable information policy belong to **Security**.
- system settings and server hosting belong to **Platform Configuration**.
- Page placement, contexts, zones, and block administration belong to **CMS**.

This is a draft synthesis, not evidence that any particular Rock installation has the described blocks, permissions, file types, templates, provider state, or PDF endpoint configured. The supplied official documentation is principally scoped to Rock 19.0, with additional release-note evidence for 16.1, 17.0, 17.8, 18.3, and 19.5.

## Mental Model

Treat each document operation as a chain with explicit ownership:

1. **Source or subject** — the entity, grid row, workflow attribute, or registrant supplying context.
2. **Template or document type** — the configuration that defines what may be created.
3. **Rendering or storage path** — Word/HTML merge generation, signature-to-PDF generation, or an associated binary file type.
4. **Security path** — template, document type, file type, block, or individual-document permissions, depending on the operation and Rock version.
5. **Resulting record or file** — an entity document, merge output, signature document, or generated signed PDF.
6. **Delivery or downstream action** — download, completion email, workflow continuation, registration status, reporting, or eligibility reuse.

These systems should not be collapsed into one abstraction:

- A **merge template** formats rows into generated Word or HTML output.
- An **entity document type** controls which stored documents can attach to an entity and which file type stores them.
- A **signature document template** defines the content and settings used to create individual signing documents.
- A **signature document** represents the individual document associated with the people identified as Applies To, Assigned To, and Signed By. ([Documents](https://community.rockrms.com/documentation/core-concepts/documents), [Intro to Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures))

When diagnosing access, inspect the precise object and Rock version rather than assuming that security configured on one layer governs every related file.

## Entity Documents

### Document types and storage

An entity document type binds documents to both a Rock entity type and a file type. Configuration is managed under `Admin Tools > Settings > Document Types`. Supported settings in the supplied Rock 19.0 documentation include:

- A descriptive name.
- The associated file type.
- The Rock entity type.
- Whether the document represents an image.
- Whether users may add it manually.
- A maximum number of documents per entity.
- An optional default document-name template.
- Optional entity qualifier column and value settings.

The qualifier settings narrow a document type to a subset of the selected entity type. For example, a document type associated with Group can be restricted by `GroupTypeId` and a particular Group Type value. These values are installation-specific and must be inspected rather than guessed. ([Configure Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/configure-entity-documents))

Rock can associate multiple documents of the same document type with one entity, including a person or group, subject to any configured maximum. ([Intro to Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/intro-to-entity-documents), [Configure Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/configure-entity-documents))

### Page context and Documents block

Person documents have a dedicated management surface on the Person Profile page in the documented Rock configuration. For another entity type, place a Documents block on a page that supplies the relevant entity in context and configure the block’s Entity Type to match. A block without a valid matching context displays a warning that it needs a valid context entity. ([Add the Block](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-the-block))

The Documents block can be restricted to selected document types. Its **Show Security Button** setting determines whether users can manage security separately for each listed document. The document types offered when adding a document are controlled jointly by the entity document type configuration and the block settings. ([Add the Block](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-the-block), [Manage Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/manage-entity-documents))

From the block, users can review document information, download a file, apply per-document security when that control is enabled, and delete a document. Deletion is irreversible. An agent should therefore treat deletion as a destructive operation requiring an exact record selection and explicit authorization. ([Manage Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/manage-entity-documents))

### Adding entity documents through workflows

The **Entity Document Add** workflow action can add a document to an entity, but two alignments are required:

1. The workflow entity type must match the entity type configured on the selected document type.
2. The uploaded file must satisfy applicable required preferred-file settings on the file type associated with that document type.

For example, a workflow operating on Person cannot add a document through a document type configured for Group. ([Add Documents Using Workflows](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-documents-using-workflows))

Uploading a person document requires Edit permission on both the applicable Person document type and the associated Person Document file type. Do not stop after proving access to only one of those layers. ([Add Documents Using Workflows](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-documents-using-workflows))

Security for workflow-created entity documents is version-sensitive. Rock 17.8 fixed a defect in which files created by the Entity Document Add action were not linked correctly to their parent Document, causing access to fall back to file-type security instead of the intended document-type security. The release also added a warning for publicly viewable document types and conditionally copied security from two paired default file types when no document-type security was already configured. Confirm the installed patch level before interpreting older records or unexpected access. ([Rock Core Release Notes](https://www.rockrms.com/releasenotes))

## Document Templates And Merge Documents

### Global and personal templates

Global merge templates are managed under `Admin Tools > Settings > Merge Templates`. They are database-wide in scope, but individual templates can be restricted through security on the Merge Template Detail block. Rock enforces those template security settings whenever a merge document is created. ([Administrate Merge Templates](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/administrate-merge-templates))

Users can manage templates intended for their own use from **My Settings**. That page normally exposes their personal templates and can also expose global templates when its block settings are configured to do so. Personal ownership, global visibility, and authorization to run a template are separate questions. ([Administrate Merge Templates](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/administrate-merge-templates))

### Preparing and inspecting merge data

The merge action available from supported grids passes the grid’s rows into a selected merge template. Before running the merge, Rock can show:

- The number of records.
- The first 15 source rows.
- The merge fields available for that data.
- The selected merge template.
- An option to combine family members.

Use the row preview to validate the source population and use the merge-field display to validate field availability. Neither proves that every later record has the same values as the first 15. ([Use Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/use-merge-documents))

When **Combine Family Members** is enabled, Rock produces one row per family instead of one row per person and combines member values such as nicknames within that row. Templates that depend on one-person-per-row semantics should not enable this option without a deliberate template review. ([Use Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/use-merge-documents))

### Word templates

Word merge templates use Lava for dynamic content. The documented Word implementation supports variables, filters, and most tags, but does not support the `if`, `raw`, or `lava` tags, Lava commands, or Lava shortcodes. A template that works in a general Lava block is therefore not guaranteed to work unchanged in Word merge generation. ([Create a Merge Document](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/create-a-merge-document))

Word templates have two documented record-layout patterns:

- Without a `{% Next %}` tag, Rock repeats the entire document for each source record.
- With `{% Next %}`, the template can advance through records inside a shared layout, such as a page of mailing labels.

Rock determines the strategy from the template. Inspect the template itself before diagnosing repeated pages as a data problem. ([Create a Merge Document](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/create-a-merge-document))

### HTML templates

HTML merge templates also use Lava and are suited to browser-viewed or printed output, including layouts containing images. If an HTML merge document must display email addresses and the site is behind Cloudflare, Cloudflare Scrape Shield must be disabled because it blocks those addresses in the generated document. Verify the actual Cloudflare zone and feature state before changing it; the documentation establishes the dependency, not an installation’s current configuration. ([Create a Merge Document](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/create-a-merge-document))

### Lava row behavior

When the merge source contains `GroupMember` rows, Rock exposes each row as a person for template portability. The original membership data remains available through the person’s `GroupMember` property, including group member attributes. A documented access pattern is:

```liquid
{{ Row.GroupMember | Attribute:'attributekey' }}
```

Attribute keys are configuration-specific and must be verified in the target installation. ([Using Lava with Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/using-lava-with-merge-documents))

Use straight quotation marks in Lava expressions. Curved or stylized quotation marks introduced by rich-text editors can cause parsing errors. ([Using Lava with Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/using-lava-with-merge-documents))

## Electronic Signatures

### Signature roles

Rock distinguishes three people associated with a signature document:

- **Applies To** is the subject of the document.
- **Assigned To** is the person expected to sign.
- **Signed By** records the person who actually completed the signature.

For an adult signing their own form, these may identify the same person. For a minor’s waiver, the document can apply to the child while being assigned to and signed by a parent or other responsible person. ([Intro to Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures))

Do not use “signer” ambiguously in automation or diagnostics. Establish whether a condition refers to the subject, intended signer, or actual signer.

### Signature document templates

In the documented Rock 19.0 interface, signature templates are created under `Admin Tools > Settings > Signature Documents`. Evidence-supported template settings include:

- Name and description.
- A document term used in signing prompts and the standard receipt communication.
- Typed or drawn signature input.
- The binary file type used to store the signed document.
- A completion System Communication.
- Whether completed documents can remain valid for future use.
- Lava template content and the attribute keys expected from a workflow or registration context.

The template creates individual documents; it is not itself proof that a particular person signed one. ([Set Up Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures))

Rock recommends typed signatures. The official documentation states that a drawn signature is personally identifiable information and may create additional legal obligations when stored in Rock. The supplied immutable source snapshot also shows that drawn signature image data is stored through an encrypted signature-data field, but that implementation observation does not replace an organization’s legal, retention, or access-control review. ([Set Up Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures), [source at commit `471fd303`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Core/SignatureDocument/SignatureDocument.Logic.cs))

By default, the signature is placed at the bottom of the generated PDF. Rock 17.0 added an optional signature-details marker that can place the signature at specific locations, including multiple locations. The Rock 19.0 documentation shows the marker as:

```html
<!-- [[ SignatureDetails ]] -->
```

Each occurrence is replaced with the signature. ([Set Up Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures), [Rock Core Release Notes](https://www.rockrms.com/releasenotes))

### Electronic signatures in workflows

The **Electronic Signature** workflow action can select a fixed signature document template or resolve a template ID or GUID, including from a workflow attribute. If both methods are configured, the fixed **Signature Document Template** setting takes precedence and the dynamic selection is ignored. ([Use Electronic Signatures in a Workflow](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow))

The action can map workflow Person attributes to Applies To, Assigned To, and Signed By. It can also place the resulting document in a Binary File workflow attribute; the official example uses the **Digitally Signed Documents** file type. The document name is Lava-enabled. If the signer is logged in, the documented workflow behavior assigns that person as Signed By regardless of the mapped Signed By attribute. ([Use Electronic Signatures in a Workflow](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow))

A reviewed community pattern addresses workflows launched both from a connection request and from a bulk audience. It recommends keeping signature, communication, and document actions independent of connection updates, then conditionally running connection mutations only when a ConnectionRequest context actually exists. This is a community operational pattern, not documented universal Rock behavior, and requires live validation against the workflow’s launch paths and conditions. ([RockU Workflows](https://community.rockrms.com/rocku/workflows))

### Electronic signatures in event registration

In Rock 19.0, event-registration signatures require the Obsidian Registration Entry block. Using that block with a legacy signature document can break the registration flow. The required signature template is selected on the registration template under `Tools > Event Registration`. ([Use Electronic Signatures in Event Registrations](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-event-registrati))

For each registration signature document:

- Applies To is the individual registrant.
- Assigned To is the registrant when the registrant is an adult.
- Assigned To is the person completing the registration when the registrant is a child.

Because this behavior distinguishes adults from children, the official documentation suggests requiring birthdate in the registration form when that classification must be reliable. ([Use Electronic Signatures in Event Registrations](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-event-registrati))

The documented registration flow can recognize an existing valid signed document for a matched person and avoid requiring another signature. That behavior depends on person matching, the required template, and document validity. It should not be generalized to unmatched, duplicate, expired, or differently scoped records without live inspection. ([Use Electronic Signatures in Event Registrations](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-event-registrati))

Rock 18.3 fixed internal event-registration blocks that could show a person-matched signature document for a registrant without a valid `SignatureDocumentId`. The fix changed those blocks to use the registrant’s SignatureDocument relationship and included a migration to backfill qualifying missing relationships. Verify the installed version when investigating historical or mismatched registration signature displays. ([Rock Core Release Notes](https://www.rockrms.com/releasenotes))

## Generated PDFs And Completion Delivery

After an electronic signature is completed, Rock normally generates a PDF containing the document content and signature so a copy can be sent to the signer. The configured completion System Communication controls the receipt communication associated with the signature template. ([Generate PDFs for Electronic Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/generate-pdfs-for-electronic-signature-docume), [Set Up Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures))

Local PDF rendering can be resource-intensive during high-volume activity. Organizations should configure a third-party rendering service through the **PDF External Render Endpoint** system setting when local rendering would impose excessive server load. An external service is required when the Rock environment cannot run Puppeteer or Chrome, including applicable Azure web-service deployments. The documented setting is under `Admin Tools > Settings > System Configuration`. Provider selection, endpoint credentials, capacity, privacy terms, and network reachability require installation-specific review. ([Generate PDFs for Electronic Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/generate-pdfs-for-electronic-signature-docume))

The immutable source snapshot includes a PDF-preview request model carrying Lava template content, a binary file type, and a signature type. This confirms an implementation path for template preview at that commit, but it does not prove that preview succeeded, that production rendering is configured, or that the same contract exists in another version. ([source at commit `471fd303`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Core/SignatureDocumentTemplateDetail/GetPdfPreviewUrlRequestBag.cs))

## Managing Completed Signature Documents

In Rock 19.0, administrators can navigate to `Admin Tools > Settings > Signature Documents`, select a signature template, review its document list, and open an individual record. The detail view can display the signed file and resend the completion email. ([Manage Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/manage-signature-documents))

The security authority for viewing completed documents changed across the supplied evidence:

- Rock 19.0 documentation states that view access is based on the associated binary file type rather than the signature document template.
- Rock 19.5 release notes report a fix so direct signed-document downloads honor Signature Document Template security and say existing records are corrected automatically.

Treat the 19.0 rule as version-scoped, and verify the exact installed patch before diagnosing or changing access. ([Manage Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/manage-signature-documents), [Rock Core Release Notes](https://www.rockrms.com/releasenotes))

A reviewed community contribution recommends using actual SignatureDocument records, scoped to the intended template and linked through the Applies To person alias, when evaluating completion for reports or reminder suppression. It warns that a separate person attribute such as a signed date may drift from the document record. This is a community reporting pattern requiring schema and data verification, not an approved universal query or authorization to run SQL. ([Rock Model Map](https://community.rockrms.com/ModelMap), [Rock Core Release Notes](https://www.rockrms.com/releasenotes))

## Version And Authority Caveats

- Most official documentation excerpts in this evidence pack identify Rock 19.0 as their current version. Claims without a processed version scope should be checked against the installed version before implementation.
- Rock 16.1 fixed workflow template filtering so inactive signature document templates would not appear in workflow actions. Older behavior should not be projected onto later installations. ([Rock Core Release Notes](https://www.rockrms.com/releasenotes))
- Rock 17.0 introduced the optional signature-placement marker. ([Rock Core Release Notes](https://www.rockrms.com/releasenotes))
- Rock 17.8 corrected parent-document linkage and security evaluation for files uploaded through Entity Document Add workflows. ([Rock Core Release Notes](https://www.rockrms.com/releasenotes))
- Rock 18.3 corrected registrant-to-signature-document relationships in internal event-registration displays. ([Rock Core Release Notes](https://www.rockrms.com/releasenotes))
- Rock 19.0 documentation says third-party signature providers are no longer supported. The supplied source snapshot likewise marks legacy-provider send methods obsolete in 19.0. This does not prove that an upgraded installation has no legacy records or configuration remnants. ([Set Up Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures), [source at commit `471fd303`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Core/SignatureDocumentTemplate/SignatureDocumentTemplateService.cs))
- Rock 19.5 changed or corrected direct-download security for signed documents so that template security is honored. ([Rock Core Release Notes](https://www.rockrms.com/releasenotes))
- The supplied release page identifies Rock 20.0 as alpha. No pack evidence establishes changed document behavior for a production-ready Rock 20 release; do not infer it from the branch or version title.
- GitHub excerpts in this guide come from immutable commit `471fd303d111b2e46218228dbc1e93dba8856fa3`. They describe implementation at that commit, not an installation’s deployed version or configuration.
- Rock community recipes are explicitly community-contributed and not reviewed or endorsed by the Rock core team. Recipes that delete records, clear relationships, or execute command SQL require independent security, data-integrity, version, backup, and rollback review. ([Re-Send Signature Documents from Registrant](https://community.rockrms.com/recipes/434), [Resend a Group Requirement Helper Workflow](https://community.rockrms.com/recipes/482))

## Troubleshooting Decision Tree

### A document type is missing from the Documents block

1. Confirm that the page supplies the intended entity in context.
2. Confirm that the Documents block’s Entity Type matches that context.
3. Inspect the block’s selected Document Types.
4. Inspect the document type’s Entity Type and any qualifier column and value.
5. Confirm that the document type is manually selectable if a user is trying to add it manually.
6. Confirm that any maximum-documents limit has not been reached. ([Configure Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/configure-entity-documents), [Add the Block](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-the-block))

### An Entity Document Add workflow fails

1. Identify the workflow entity type.
2. Identify the selected document type’s configured entity type.
3. Stop if they do not match.
4. Inspect the document type’s associated file type.
5. Check whether required preferred-file settings reject the uploaded file.
6. For a person document, verify Edit permission on both the document type and the Person Document file type.
7. If the problem concerns access after upload, determine whether the installation predates the Rock 17.8 linkage fix. ([Add Documents Using Workflows](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-documents-using-workflows), [Rock Core Release Notes](https://www.rockrms.com/releasenotes))

### A user cannot view or download a document

1. Identify whether this is an entity document, merge template, unsigned signature request, or completed signature document.
2. For an entity document, inspect document-type, associated file-type, block, and any per-document security relevant to the installed version.
3. For a completed signature document on Rock 19.0, inspect associated binary file-type permissions.
4. For direct signed-document downloads on Rock 19.5 or later, inspect signature-template security and confirm the relevant fix is installed.
5. Do not broaden permissions until the precise failing layer and version are established. ([Manage Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/manage-entity-documents), [Manage Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/manage-signature-documents), [Rock Core Release Notes](https://www.rockrms.com/releasenotes))

### Lava fails in a Word merge template

1. Replace curved quotation marks with straight quotation marks.
2. Check whether the template uses unsupported Word features: `if`, `raw`, or `lava` tags, Lava commands, or shortcodes.
3. Inspect the available merge fields for the actual grid source.
4. If the source contains GroupMember rows, use the exposed person row and access membership data through `Row.GroupMember`.
5. Check whether `{% Next %}` is present and whether the desired output is one complete document per row or multiple rows in one layout. ([Create a Merge Document](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/create-a-merge-document), [Using Lava with Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/using-lava-with-merge-documents))

### Email addresses are missing from an HTML merge document

1. Confirm the source row and merge field contain the email value.
2. Confirm the problem occurs in HTML merge output rather than in the underlying grid.
3. If Cloudflare is in the request path, inspect whether Scrape Shield is enabled.
4. If enabled, evaluate disabling Scrape Shield for the relevant zone because the official documentation identifies it as blocking email addresses in HTML merge documents.
5. Regenerate a bounded test document and verify the output. ([Create a Merge Document](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/create-a-merge-document))

### A workflow uses the wrong signature template

1. Inspect the fixed **Signature Document Template** action setting.
2. Inspect the dynamic template ID, GUID, or workflow attribute.
3. If both are populated, treat the fixed template as authoritative because it takes precedence.
4. Confirm that the selected template is active; Rock 16.1 fixed inactive-template filtering in workflow actions.
5. Confirm that attribute values contain the expected ID or GUID representation. ([Use Electronic Signatures in a Workflow](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow), [Rock Core Release Notes](https://www.rockrms.com/releasenotes))

### The wrong person is expected to sign

1. Identify the document’s Applies To person.
2. Identify its Assigned To person.
3. Identify the recorded Signed By person.
4. For workflows, inspect the mapped Person attributes and whether the signer was logged in.
5. For event registration, confirm whether the registrant is classified as an adult or child.
6. Confirm the person completing the registration when a child is the registrant.
7. Check whether missing birthdate data makes the adult/child classification unreliable. ([Intro to Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures), [Use Electronic Signatures in a Workflow](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow), [Use Electronic Signatures in Event Registrations](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-event-registrati))

### Event registration signatures break or display the wrong document

1. Confirm the external registration page uses the Obsidian Registration Entry block.
2. Confirm the required template is a current built-in electronic-signature template rather than a legacy-provider document.
3. Inspect the registration template’s Required Signature Document selection.
4. Confirm the registrant’s person match, signature-document relationship, required template, and validity.
5. Determine whether the installation includes the Rock 18.3 registrant relationship fix and migration. ([Use Electronic Signatures in Event Registrations](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-event-registrati), [Rock Core Release Notes](https://www.rockrms.com/releasenotes))

### A signed PDF is not generated or delivery stalls

1. Separate rendering from communication delivery: first determine whether the signed PDF exists.
2. Inspect the signature template’s file type and completion System Communication.
3. Inspect the **PDF External Render Endpoint** system setting.
4. Determine whether the host can run Puppeteer or Chrome.
5. If local rendering is supported, review whether concurrent volume is exhausting server capacity.
6. If external rendering is required, verify endpoint configuration and reachability without exposing credentials.
7. After PDF generation succeeds, troubleshoot the completion email through the communications system. ([Generate PDFs for Electronic Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/generate-pdfs-for-electronic-signature-docume), [Set Up Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures))

## Agent Task Recipes

### Recipe: Configure an entity document type and management surface

**Outcome:** Users can manage an approved document category for the intended entity type.

1. Identify the target entity type and whether qualifiers should restrict the type to a subset.
2. Select the associated file type and review its security and required preferred-file settings.
3. Create or review the entity document type under `Admin Tools > Settings > Document Types`.
4. Configure manual selection, maximum documents, qualifiers, and default naming as needed.
5. For Person, inspect the existing Person Profile document surface.
6. For another entity, place a Documents block on a page with that entity in context.
7. Configure the block’s Entity Type, allowed Document Types, and security-button visibility.
8. Test with a non-sensitive file and an authorized test role.
9. Verify add, list, download, and security behavior separately. ([Configure Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/configure-entity-documents), [Add the Block](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-the-block))

**Inspect:**

- Entity and qualifier match.
- Document-type and file-type permissions.
- Block context and filters.
- Installed Rock version.

**Stop when:**

- The requested qualifier value is unknown.
- Testing would require uploading private data.
- A permission change has not been authorized.

### Recipe: Create and validate a merge template

**Outcome:** A global or personal template generates the intended output from a known grid source.

1. Choose personal or global scope.
2. For a global template, configure template security before broad use.
3. Choose Word or HTML based on the required output.
4. Open the target grid’s merge action.
5. inspect the row count, first 15 rows, and available merge fields.
6. Decide whether output should remain one row per person or combine family members.
7. Build the template using only the Lava features supported by that format.
8. For Word, choose whole-document repetition or `{% Next %}` multi-record layout deliberately.
9. Use straight quotation marks in all Lava expressions.
10. Run a small representative test and inspect the generated content before using the full population. ([Administrate Merge Templates](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/administrate-merge-templates), [Use Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/use-merge-documents), [Create a Merge Document](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/create-a-merge-document))

**Do not assume:**

- The first 15 rows represent every record.
- General Lava features all work in Word.
- GroupMember rows retain GroupMember as the top-level row type.
- Template visibility implies authorization to generate it.

### Recipe: Configure a signature template

**Outcome:** A reviewed signature template can generate and store signed documents using the intended signer experience.

1. Open `Admin Tools > Settings > Signature Documents`.
2. Define a clear name, description, and document term.
3. Select typed or drawn input; prefer typed unless an approved requirement justifies storing drawn-signature PII.
4. Select the signed-document file type.
5. Select the completion System Communication.
6. Decide whether completed documents can remain valid for future use.
7. Author the Lava body and verify that its attribute keys match the intended workflow or registration inputs.
8. Add `<!-- [[ SignatureDetails ]] -->` wherever explicit or repeated signature placement is required.
9. Preview or test with non-sensitive representative data.
10. Verify the stored document and completion email as separate outcomes. ([Set Up Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures))

**Stop when:**

- Legal language is unapproved.
- Retention or PII requirements are unresolved.
- The storage file type or its security has not been reviewed.

### Recipe: Add an electronic signature to a workflow

**Outcome:** The workflow presents the correct document to the correct signer and retains the resulting signed file.

1. Decide whether the action uses one fixed template or a dynamic template ID/GUID.
2. Do not populate the fixed field if dynamic selection is intended.
3. Map Applies To, Assigned To, and Signed By to explicit Person attributes.
4. Add a Binary File workflow attribute for the resulting signature document and select the intended signed-document file type.
5. Define a Lava-enabled document name.
6. Test logged-in and applicable non-logged-in behavior because login affects Signed By handling.
7. Verify the template selected, subject, assigned signer, actual signer, stored PDF, and receipt delivery.
8. If the workflow has multiple launch contexts, condition any unrelated entity mutations on the presence of their required context. ([Use Electronic Signatures in a Workflow](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow), [RockU Workflows](https://community.rockrms.com/rocku/workflows))

**Do not assume:**

- Assigned To and Applies To are interchangeable.
- A dynamic template value overrides a fixed template.
- A bulk launch contains a ConnectionRequest or another pipeline entity.

### Recipe: Configure an event-registration signature requirement

**Outcome:** Each registrant receives the correct signature requirement through the supported registration flow.

1. Confirm the external page uses the Obsidian Registration Entry block.
2. Confirm the signature template uses Rock’s built-in electronic-signature system.
3. Edit the registration template under `Tools > Event Registration`.
4. Select the required signature document.
5. Review whether birthdate should be required so adult/child assignment is reliable.
6. Test an adult registering themselves.
7. Test an adult registering a child.
8. Test a matched person with an existing valid document for the same required template.
9. Verify the registrant relationship and displayed completion state from the registration instance.
10. Confirm receipt PDF generation and delivery separately. ([Use Electronic Signatures in Event Registrations](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-event-registrati))

### Recipe: Review a completed signature document and resend its receipt

**Outcome:** An authorized administrator verifies the signed record and resends the existing completion email when appropriate.

1. Confirm the installed Rock version and applicable security authority.
2. Navigate to `Admin Tools > Settings > Signature Documents`.
3. Select the exact signature document template.
4. Locate the intended document record.
5. Open its details and inspect the signed file.
6. Confirm the intended recipient before resending.
7. Use the documented resend-completion-email action.
8. Verify communication delivery through the communications system rather than treating the button click as delivery proof. ([Manage Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/manage-signature-documents))

### Recipe: Decide whether to offload signed-PDF rendering

**Outcome:** The organization has a justified local or external rendering path.

1. Identify whether the host can run Puppeteer or Chrome.
2. If it cannot, plan an external rendering service.
3. If it can, evaluate expected signature volume and concurrent server load.
4. When local rendering poses excessive load, select and review an external service.
5. Configure the **PDF External Render Endpoint** under System Configuration.
6. Test preview, completed signing, PDF storage, and receipt delivery.
7. Load-test only within an approved non-production or otherwise controlled scope.
8. Document provider, privacy, credential, capacity, and failure-handling ownership. ([Generate PDFs for Electronic Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/generate-pdfs-for-electronic-signature-docume))

### Recipe: Evaluate a community resend or reset workaround

**Outcome:** A maintainer determines whether a community recipe is safe and still necessary without executing destructive steps by default.

1. First test the official completed-document resend action to determine whether it satisfies the need.
2. Define whether the desired outcome is receipt redelivery, a new signature request, clearing a group requirement, or replacing an invalid registrant signature.
3. Review the installed Rock version and relevant fixes.
4. Read the community recipe as a design example, not as approved core behavior.
5. Identify every delete, relationship reset, command SQL, security-disabled entity access, and bulk-action path.
6. Confirm backups, rollback, authorization, schema compatibility, record scope, and a non-production test plan.
7. Prefer supported workflow actions and current core behavior where they meet the requirement.
8. Stop before executing SQL, deleting signature documents, clearing registrant relationships, or deleting workflows unless those exact mutations are separately reviewed and authorized. ([Re-Send Signature Documents from Registrant](https://community.rockrms.com/recipes/434), [Resend a Group Requirement Helper Workflow](https://community.rockrms.com/recipes/482))

## Known Gaps And Live Verification

No live Rock instance was reviewed for this guide. Before applying it, verify:

- The exact Rock version and patch level.
- Whether the relevant pages use legacy or Obsidian blocks.
- Which entity document types, qualifiers, file types, and preferred-file settings are installed.
- Document-type, file-type, block, template, and individual-document security.
- Whether historical workflow-created files were affected by the pre-17.8 parent-link defect.
- Whether registration signature relationships were affected by the issue fixed in 18.3.
- Whether direct signed-document downloads follow the Rock 19.0 file-type rule or the Rock 19.5 template-security fix.
- Whether legacy signature templates or provider-linked records remain after an upgrade to Rock 19.
- Whether signature templates are active and whether workflow attributes resolve the intended ID or GUID.
- Whether adult/child classification and person matching support the intended registration assignment.
- Whether existing signature documents are still valid for the intended template and policy.
- Whether the host can run Puppeteer or Chrome and whether the PDF External Render Endpoint is configured.
- Whether generated PDFs, stored files, and completion emails succeed under expected load.
- Whether Cloudflare Scrape Shield is enabled on the relevant zone when HTML merge documents need email addresses.
- Whether reports and reminders use verified SignatureDocument relationships rather than a potentially stale convenience attribute.
- Whether workflows launched through multiple routes properly guard context-specific mutations.
- Whether any proposed community resend workflow remains compatible with the installed schema and can avoid direct SQL or destructive record deletion.

Evidence gaps in the supplied pack include:

- No reviewed live configuration, file counts, permission results, or issue reproduction.
- No approved universal SQL query for signature completion, resending, or cleanup.
- No evidence establishing provider-specific external PDF configuration beyond the documented endpoint pattern.
- No evidence that a completion email was delivered merely because Rock generated a PDF or invoked a resend action.
- No production-ready Rock 20 document behavior beyond the release page identifying Rock 20.0 as alpha.
- No legal determination that typed or drawn signatures satisfy a particular jurisdiction, agreement, retention policy, or organizational requirement.

## Source Map

### Official documentation

- [Documents](https://community.rockrms.com/documentation/core-concepts/documents) — official navigation and conceptual grouping.
- [Intro to Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/intro-to-entity-documents) — entity-document purpose and multiplicity.
- [Configure Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/configure-entity-documents) — document types, entity/file binding, qualifiers, limits, and defaults.
- [Add the Block](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-the-block) — entity context and Documents block configuration.
- [Manage Entity Documents](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/manage-entity-documents) — block operations, per-document security, and irreversible deletion.
- [Add Documents Using Workflows](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-documents-using-workflows) — workflow entity matching, file settings, and upload permissions.
- [Intro to Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/intro-to-merge-documents) — Word and HTML merge formats.
- [Administrate Merge Templates](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/administrate-merge-templates) — global and personal templates and template security.
- [Use Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/use-merge-documents) — grid preview, merge fields, and combined-family rows.
- [Create a Merge Document](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/create-a-merge-document) — Word/HTML construction, Word Lava limits, `{% Next %}`, and Cloudflare caveat.
- [Using Lava with Merge Documents](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/using-lava-with-merge-documents) — GroupMember normalization and quotation-mark guidance.
- [Intro to Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures) — signing-document anatomy and person roles.
- [Set Up Electronic Signatures](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures) — template configuration, typed-signature recommendation, signature placement, and legacy-provider warning.
- [Use Electronic Signatures in a Workflow](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow) — workflow action mappings and template precedence.
- [Use Electronic Signatures in Event Registrations](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-event-registrati) — Obsidian requirement, assignment logic, reuse, and registration monitoring.
- [Generate PDFs for Electronic Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/generate-pdfs-for-electronic-signature-docume) — PDF generation and external rendering.
- [Manage Signature Documents](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/manage-signature-documents) — completed-document administration and Rock 19.0 access behavior.

### Release and implementation evidence

- [Rock Core Release Notes](https://www.rockrms.com/releasenotes) — version-specific signature placement and fixes for inactive templates, entity-document linkage, registrant relationships, and direct-download security.
- [SignatureDocument source at commit `471fd303`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Core/SignatureDocument/SignatureDocument.Logic.cs) — implementation evidence for encrypted drawn-signature data.
- [SignatureDocumentTemplateService at commit `471fd303`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock/Model/Core/SignatureDocumentTemplate/SignatureDocumentTemplateService.cs) — implementation evidence marking legacy-provider methods obsolete in Rock 19.0.
- [PDF preview request at commit `471fd303`](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/Core/SignatureDocumentTemplateDetail/GetPdfPreviewUrlRequestBag.cs) — implementation evidence for preview inputs.
- [Rock Model Map](https://community.rockrms.com/ModelMap) — structured model metadata and a routing aid, not independent proof of an installation’s schema or data.

### Training and community examples

- [RockU Documents](https://community.rockrms.com/rocku/documents) — official training index for merge and entity documents.
- [RockU Electronic Signatures](https://community.rockrms.com/rocku/workflows/electronic-signatures-1) — official training route for workflow-oriented signature instruction.
- [Re-Send Signature Documents from Registrant](https://community.rockrms.com/recipes/434) — community recipe containing destructive and SQL-based operations; example only.
- [Resend a Group Requirement Helper Workflow](https://community.rockrms.com/recipes/482) — community recipe for clearing a requirement workflow; example only.
- [RockU Workflows](https://community.rockrms.com/rocku/workflows) — source route associated with the reviewed community pattern for guarding context-specific workflow mutations.