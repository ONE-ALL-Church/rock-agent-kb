---
id: concept-documents-signatures
title: Documents And Signatures
generated: true
last_built: 2026-07-18T02:03:48+00:00
guide_status: generated_needs_review
rebuild_policy: source_hash_changed_or_weekly
source_count: 60
depends_on_topics:
  - people
  - workflows
  - communications
  - security
  - platform-configuration
  - cms
---

# Documents And Signatures

Documents, document templates, generated PDFs, electronic signatures, signature requests, storage, and document-related workflow patterns.

> Generated guide. Treat this as a synthesis and source map, not as a substitute for official Rock documentation or local verification.

## Agent Starting Points

- Start with this concept's official or highest-weight records before using community answers.
- Check release records when the task could be version-sensitive.
- Follow citations for operational steps, screenshots, or code before making a change.
- Verify permissions and security inheritance before changing access, APIs, workflows, pages, or groups.
- Use the data model landmarks to orient SQL, Lava entity commands, and API/entity work.
- Treat recipes and Q&A as community guidance; validate against your Rock version and environment.

## How To Think About This Area

- `Documents And Signatures` spans people, workflows, communications, security, platform-configuration, cms. Agents should expect cross-cutting dependencies rather than a single page or table.
- The strongest source families in this build are: rock_documentation, rock_recipes, rock_core_release_notes, rock_rocku, rock_model_map, triumph_resources.
- Related tags found in source records: usage, workflow, training, operations, admin, lava, releases, development.
- Source detail types include: documentation_article, recipe, training, triumph_resources.

## Reviewed Media Insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Electronic Signatures Transcript Insight | Rock operations | 00:00 | The Electronic Signatures RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. | [source](https://community.rockrms.com/rocku/event-registration/electronic-signatures) |
| Electronic Signatures Transcript Insight | release and roadmap awareness | 00:44 | For version, roadmap, and release-caveat awareness, Electronic Signatures should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. | [source](https://community.rockrms.com/rocku/event-registration/electronic-signatures) |
| Electronic Signatures Transcript Insight | Rock operations | 00:00 | The Electronic Signatures RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. | [source](https://community.rockrms.com/rocku/workflows/electronic-signatures-1) |
| Electronic Signatures Transcript Insight | release and roadmap awareness | 00:44 | For version, roadmap, and release-caveat awareness, Electronic Signatures should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. | [source](https://community.rockrms.com/rocku/workflows/electronic-signatures-1) |


## Approved Claims

These are reviewed, source-backed public claims routed to this concept. Community-derived claims are labeled by authority tier and should not be treated as official behavior.

| Authority | Type | Claim | Source |
| --- | --- | --- | --- |
| official | behavior | Rock merge documents support Word and HTML formats, with Lava used to supply templated content in either format. | [source](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/intro-to-merge-documents) |
| official | behavior | For an event registration signature document, Applies To is each registrant; Assigned To is the registrant when the registrant is an adult, but the person completing the registration when the registrant is a child. | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-event-registrati) |
| official | behavior | In Rock electronic signatures, Applies To identifies the subject of the document, Assigned To identifies the expected signer, and Signed By records the person who completed the signature. | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures) |
| official | behavior | When preparing grid data for a merge document, Rock can preview the first 15 source records and display the available merge fields before the merge is run. | [source](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/use-merge-documents) |
| official | behavior | The Entity Document block can manage documents for any Rock entity; the document types available for adding are determined by entity document type configuration and the block's settings. | [source](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/manage-entity-documents) |
| official | behavior | Entity Documents can associate multiple documents of the same document type with a single Rock entity, including a person or group. | [source](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/intro-to-entity-documents) |
| official | behavior | When a merge document receives GroupMember rows, Rock exposes each row as a person and makes the original membership data available through the person's GroupMember property, including group member attributes. | [source](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/using-lava-with-merge-documents) |
| official | behavior | After an electronic signature is completed, Rock normally generates a PDF containing the document content and signature so a copy can be sent to the signer. | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/generate-pdfs-for-electronic-signature-docume) |
| official | configuration | The Entity Document block supports per-document security when that feature is enabled in the block settings, while deleting a listed document is irreversible. | [source](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/manage-entity-documents) |
| official | configuration | Users can manage merge templates intended for their own use from My Settings, and the page can also expose global templates when its block settings are configured accordingly. | [source](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/administrate-merge-templates) |
| official | configuration | Cloudflare Scrape Shield must be disabled for HTML merge documents that need to display email addresses because the feature blocks those addresses in the generated document. | [source](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/create-a-merge-document) |
| official | configuration | A workflow Electronic Signature action can use a fixed document template or resolve a template ID or GUID from a workflow attribute; the fixed template setting takes precedence when both are supplied. | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow) |
| official | configuration | The Entity Document Add workflow action fails when the workflow entity type does not match the entity type configured for the selected document type; the uploaded file must also satisfy any required preferred-file settings of that document type's associated file type. | [source](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-documents-using-workflows) |
| official | configuration | To manage documents for an entity type other than Person, add a Documents block to a page that has that entity in context and configure the block's Entity Type to match; otherwise, the block warns that it lacks a valid context entity. | [source](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-the-block) |
| official | configuration | In Rock 19.0 event registration, electronic signatures require the Obsidian Registration Entry block; using that block with a legacy signature document can break the registration flow. | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-event-registrati) |
| official | configuration | Uploading a document for a person requires Edit permission for both the applicable Person document type and its associated Person Document file type. | [source](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-documents-using-workflows) |
| official | configuration | An entity document type binds stored documents to both a Rock entity type and a file type, and optional qualifier column and value settings can restrict it to a subset such as one Group Type. | [source](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/configure-entity-documents) |
| official | configuration | A Documents block can be limited to selected document types, and enabling its security button allows access security to be managed separately for each document. | [source](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/add-the-block) |
| More |  | 8 additional approved claims are tracked in `claims/approved-claims.jsonl`. |  |

## Source Coverage

- `rock_core_release_notes`: 4
- `rock_documentation`: 20
- `rock_model_map`: 12
- `rock_recipes`: 2
- `rock_rocku`: 32
- `triumph_resources`: 1

## Highest Signal Sources

| Title | Source | Why It Matters | Citation |
| --- | --- | --- | --- |
| Manage Signature Documents | rock_documentation | OK, so now we've seen how to create electronic signature templates and how to use them in workflows and event registrations to gather signatures. Let's wrap it up by looking at how you can view these documents. To view signed documents, navigate to `Admin Tools > Settings > Signature Documents` and select the document template you wish to view. 1. **Document Template Detail** - From here you can edit the template... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/manage-signature-documents) |
| Documents | rock_documentation | SECTIONS [Entity Documents](?Version=v19.0#entity-documents) [Merge Documents](?Version=v19.0#merge-documents) [Electronic Signatures](?Version=v19.0#electronic-signatures) ### Entity Documents Articles [Intro to Entity Documents](/documentation/core-concepts/documents/entity-documents/intro-to-entity-documents?Version=v19.0) [Configure Entity... | [source](https://community.rockrms.com/documentation/core-concepts/documents) |
| Electronic Signatures | rock_documentation | [Intro to Electronic Signatures](/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures?Version=v19.0) [Use Electronic Signatures in a Workflow](/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow?Version=v19.0) [Use Electronic Signatures in Event... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures) |
| Generate PDFs for Electronic Signature Documents | rock_documentation | After a document is signed, a PDF is generated containing both the document's content and the person’s signature. This is done so the person can be sent a PDF copy of the signed document. In most cases, Rock handles this process automatically. However, some organizations may require an external service for PDF generation. Generating a PDF on the Rock server is resource-intensive, especially during high-traffic... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/generate-pdfs-for-electronic-signature-docume) |
| Use Electronic Signatures in a Workflow | rock_documentation | Often, you'll want to have someone electronically sign a document as part of a workflow. This is super easy because there's a Workflow Action Type designed just for that. The *Electronic Signature* action type will present the person with a document to sign from within the workflow, similar to a workflow form. 1. **Signature Document Template** - Select the template for the document the person will be asked to sign.... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow) |
| Set Up Electronic Signatures | rock_documentation | Now that you've seen what electronic signatures can do, let's look at how to set them up. Your first step in gathering electronic signatures will be to create a *Document Template* by navigating to `Admin Tools > Settings > Signature Documents`. The template will be used to generate the individual documents a person will sign. Out of the box, Rock ships with an example *Photo Release* template and a *Field Trip... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures) |
| Intro to Electronic Signatures | rock_documentation | Many events and activities require waivers and releases to be signed by participants. Rock allows you to easily gather these signatures electronically without the need for a third party service. The requirement of a signed document can be added to a registration or a workflow. We'll cover how to configure these, and then we'll walk you through the configuration of the electronic signatures environment. # Anatomy of... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures) |
| Manage Entity Documents | rock_documentation | With the new Entity Document block added, we can start adding documents to our groups. Start by clicking the icon in the Documents block to add your first document as shown below. 1. **Document Type** - Select the type of document that you want to add. The available items are controlled by the document type’s configuration and by block settings. 2. **Document Name** - If configured for the document type, a default... | [source](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/manage-entity-documents) |
| Merge Documents | rock_documentation | [Intro to Merge Documents](/documentation/core-concepts/documents/merge-documents/intro-to-merge-documents?Version=v19.0) [Use Merge Documents](/documentation/core-concepts/documents/merge-documents/use-merge-documents?Version=v19.0) [Administrate Merge Templates](/documentation/core-concepts/documents/merge-documents/administrate-merge-templates?Version=v19.0) [Create a Merge... | [source](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents) |
| Entity Documents | rock_documentation | [Intro to Entity Documents](/documentation/core-concepts/documents/entity-documents/intro-to-entity-documents?Version=v19.0) [Configure Entity Documents](/documentation/core-concepts/documents/entity-documents/configure-entity-documents?Version=v19.0) [Add the Block](/documentation/core-concepts/documents/entity-documents/add-the-block?Version=v19.0) [Manage Entity... | [source](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents) |
| Configure Entity Documents | rock_documentation | The first step is to define what types of documents you can add to entities. Navigate to `Admin Tools > Settings > Document Types` to manage the types of documents that can be stored for each entity. Pictured below, you can see we've already configured three types of documents, all for people. You might be wondering why we didn't mix it up a little and show you some example document types for other entities besides... | [source](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/configure-entity-documents) |
| Intro to Entity Documents | rock_documentation | Want to track documents for a person or group? The *Entity Documents* feature lets you add documents just about anywhere in Rock. You can even add multiple documents of the same type to the same entity, quickly and easily. If you want to cut to the chase and see what adding a document for a person looks like, we have an example in our [Person Profile Documents... | [source](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/intro-to-entity-documents) |

## Data Model Landmarks

| Model | Category | Stable Rock | Properties | DB Props | Lava Props | Lava Non-DB Props | Pre-alpha Changes | Citation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Signature Document Template](../../model-map/models/signature-document-template.md) | Core | 19.2.0 | 55 | 22 | 38 | 16 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Signature Document](../../model-map/models/signature-document.md) | Core | 19.2.0 | 65 | 31 | 49 | 18 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Benevolence Request Document](../../model-map/models/benevolence-request-document.md) | Finance | 19.2.0 | 41 | 12 | 26 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Document](../../model-map/models/document.md) | Core | 19.2.0 | 45 | 15 | 28 | 14 | 1 | [source](https://community.rockrms.com/ModelMap) |
| [Document Type](../../model-map/models/document-type.md) | Core | 19.2.0 | 50 | 21 | 35 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message](../../model-map/models/adaptive-message.md) | CMS | 19.2.0 | 44 | 15 | 29 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message Adaptation](../../model-map/models/adaptive-message-adaptation.md) | CMS | 19.2.0 | 47 | 18 | 32 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message Adaptation Segment](../../model-map/models/adaptive-message-adaptation-segment.md) | CMS | 19.2.0 | 40 | 11 | 25 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Block](../../model-map/models/block.md) | CMS | 19.2.0 | 55 | 23 | 40 | 17 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Block Type](../../model-map/models/block-type.md) | CMS | 19.2.0 | 47 | 18 | 27 | 12 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel](../../model-map/models/content-channel.md) | CMS | 19.2.0 | 65 | 29 | 47 | 18 | 1 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item](../../model-map/models/content-channel-item.md) | CMS | 19.2.0 | 71 | 31 | 52 | 21 | 0 | [source](https://community.rockrms.com/ModelMap) |

Lava fields that the stable generated Model Map marks as non-database are tracked in `knowledge/model-map/stable-properties.jsonl`. Examples for this concept:

- `Adaptive Message.AdaptiveMessageAdaptations` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.AdaptiveMessageCategories` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.AttributeValues` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.Attributes` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.CreatedByPersonId` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.CreatedByPersonName` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.EntityStringValue` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.IdKey` is Lava-marked but not database-marked in the generated Model Map (Rock 19.2.0; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).

## Version And Release Watch

| Version | Module | Change | Citation |
| --- | --- | --- | --- |
| 17.0 | CRM | Updated Electronic Signatures to allow for inserting the signature at specific places in the document template using a new optional "<!--[[ SignatureDetails ]]-->" keyword. | [source](https://www.rockrms.com/releasenotes) |
| 17.8 | Workflow | Fixed an issue where files uploaded through the Entity Document Add workflow action weren't properly linked to their parent Document. Because of that missing link, Rock couldn't check the Document Type's security rules when someone tried to access the file — it fell back to the File Type's security instead. Files are now linked correctly, so access is... | [source](https://www.rockrms.com/releasenotes) |
| 18.3 | Event | Fixed an issue with internal Event Registration blocks (Registration Instance - Registration List, Registration Details, and Registrant Details) where a Signature Document could be incorrectly shown for a registrant without a valid SignatureDocumentId, due to documents being matched by person instead of the registrant's record. Updated these blocks to use... | [source](https://www.rockrms.com/releasenotes) |
| 16.1 | Workflow | Fixed Signature Document Templates filtering to not show inactive templates in Workflow Actions. Fixes: #5511 | [source](https://www.rockrms.com/releasenotes) |

## Subguides

### Document Templates

Keywords: `document template, template, merge field, generated document`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Manage Signature Documents | rock_documentation | OK, so now we've seen how to create electronic signature templates and how to use them in workflows and event registrations to gather signatures. Let's wrap it up by looking at how you can view these documents. To view signed documents, navigate to `Admin Tools > Settings > Signature Documents` and select the document template you wish to view. 1. **Document Template Detail** - From here you can edit the template... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/manage-signature-documents) |
| Documents | rock_documentation | SECTIONS [Entity Documents](?Version=v19.0#entity-documents) [Merge Documents](?Version=v19.0#merge-documents) [Electronic Signatures](?Version=v19.0#electronic-signatures) ### Entity Documents Articles [Intro to Entity Documents](/documentation/core-concepts/documents/entity-documents/intro-to-entity-documents?Version=v19.0) [Configure Entity... | [source](https://community.rockrms.com/documentation/core-concepts/documents) |
| Electronic Signatures | rock_documentation | [Intro to Electronic Signatures](/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures?Version=v19.0) [Use Electronic Signatures in a Workflow](/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow?Version=v19.0) [Use Electronic Signatures in Event... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures) |
| Generate PDFs for Electronic Signature Documents | rock_documentation | After a document is signed, a PDF is generated containing both the document's content and the person’s signature. This is done so the person can be sent a PDF copy of the signed document. In most cases, Rock handles this process automatically. However, some organizations may require an external service for PDF generation. Generating a PDF on the Rock server is resource-intensive, especially during high-traffic... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/generate-pdfs-for-electronic-signature-docume) |
| Use Electronic Signatures in a Workflow | rock_documentation | Often, you'll want to have someone electronically sign a document as part of a workflow. This is super easy because there's a Workflow Action Type designed just for that. The *Electronic Signature* action type will present the person with a document to sign from within the workflow, similar to a workflow form. 1. **Signature Document Template** - Select the template for the document the person will be asked to sign.... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow) |
| Set Up Electronic Signatures | rock_documentation | Now that you've seen what electronic signatures can do, let's look at how to set them up. Your first step in gathering electronic signatures will be to create a *Document Template* by navigating to `Admin Tools > Settings > Signature Documents`. The template will be used to generate the individual documents a person will sign. Out of the box, Rock ships with an example *Photo Release* template and a *Field Trip... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures) |
| Intro to Electronic Signatures | rock_documentation | Many events and activities require waivers and releases to be signed by participants. Rock allows you to easily gather these signatures electronically without the need for a third party service. The requirement of a signed document can be added to a registration or a workflow. We'll cover how to configure these, and then we'll walk you through the configuration of the electronic signatures environment. # Anatomy of... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures) |
| Manage Entity Documents | rock_documentation | With the new Entity Document block added, we can start adding documents to our groups. Start by clicking the icon in the Documents block to add your first document as shown below. 1. **Document Type** - Select the type of document that you want to add. The available items are controlled by the document type’s configuration and by block settings. 2. **Document Name** - If configured for the document type, a default... | [source](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/manage-entity-documents) |
| Merge Documents | rock_documentation | [Intro to Merge Documents](/documentation/core-concepts/documents/merge-documents/intro-to-merge-documents?Version=v19.0) [Use Merge Documents](/documentation/core-concepts/documents/merge-documents/use-merge-documents?Version=v19.0) [Administrate Merge Templates](/documentation/core-concepts/documents/merge-documents/administrate-merge-templates?Version=v19.0) [Create a Merge... | [source](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents) |
| Entity Documents | rock_documentation | [Intro to Entity Documents](/documentation/core-concepts/documents/entity-documents/intro-to-entity-documents?Version=v19.0) [Configure Entity Documents](/documentation/core-concepts/documents/entity-documents/configure-entity-documents?Version=v19.0) [Add the Block](/documentation/core-concepts/documents/entity-documents/add-the-block?Version=v19.0) [Manage Entity... | [source](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents) |

### Electronic Signatures

Keywords: `electronic signature, e-signature, signature request, signed document`


#### Reviewed distilled media insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Electronic Signatures Transcript Insight | Rock operations | 00:00 | The Electronic Signatures RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. | [source](https://community.rockrms.com/rocku/event-registration/electronic-signatures) |
| Electronic Signatures Transcript Insight | release and roadmap awareness | 00:44 | For version, roadmap, and release-caveat awareness, Electronic Signatures should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. | [source](https://community.rockrms.com/rocku/event-registration/electronic-signatures) |
| Electronic Signatures Transcript Insight | Rock operations | 00:00 | The Electronic Signatures RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. | [source](https://community.rockrms.com/rocku/workflows/electronic-signatures-1) |
| Electronic Signatures Transcript Insight | release and roadmap awareness | 00:44 | For version, roadmap, and release-caveat awareness, Electronic Signatures should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. | [source](https://community.rockrms.com/rocku/workflows/electronic-signatures-1) |

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Manage Signature Documents | rock_documentation | OK, so now we've seen how to create electronic signature templates and how to use them in workflows and event registrations to gather signatures. Let's wrap it up by looking at how you can view these documents. To view signed documents, navigate to `Admin Tools > Settings > Signature Documents` and select the document template you wish to view. 1. **Document Template Detail** - From here you can edit the template... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/manage-signature-documents) |
| Electronic Signatures | rock_documentation | [Intro to Electronic Signatures](/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures?Version=v19.0) [Use Electronic Signatures in a Workflow](/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow?Version=v19.0) [Use Electronic Signatures in Event... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures) |
| Generate PDFs for Electronic Signature Documents | rock_documentation | After a document is signed, a PDF is generated containing both the document's content and the person’s signature. This is done so the person can be sent a PDF copy of the signed document. In most cases, Rock handles this process automatically. However, some organizations may require an external service for PDF generation. Generating a PDF on the Rock server is resource-intensive, especially during high-traffic... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/generate-pdfs-for-electronic-signature-docume) |
| Use Electronic Signatures in a Workflow | rock_documentation | Often, you'll want to have someone electronically sign a document as part of a workflow. This is super easy because there's a Workflow Action Type designed just for that. The *Electronic Signature* action type will present the person with a document to sign from within the workflow, similar to a workflow form. 1. **Signature Document Template** - Select the template for the document the person will be asked to sign.... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow) |
| Set Up Electronic Signatures | rock_documentation | Now that you've seen what electronic signatures can do, let's look at how to set them up. Your first step in gathering electronic signatures will be to create a *Document Template* by navigating to `Admin Tools > Settings > Signature Documents`. The template will be used to generate the individual documents a person will sign. Out of the box, Rock ships with an example *Photo Release* template and a *Field Trip... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures) |
| Intro to Electronic Signatures | rock_documentation | Many events and activities require waivers and releases to be signed by participants. Rock allows you to easily gather these signatures electronically without the need for a third party service. The requirement of a signed document can be added to a registration or a workflow. We'll cover how to configure these, and then we'll walk you through the configuration of the electronic signatures environment. # Anatomy of... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures) |
| Use Electronic Signatures in Event Registrations | rock_documentation | Electronic signatures often come in handy for event registrations. When someone signs up for an event, they can easily sign the form or waiver electronically. The neat thing? If, say, Cindy Decker is registering Noah Decker for an activity that requires "Release Form A," and Noah already has a valid signed "Release Form A," we won't make them sign it again. Rock's standard person matching logic helps us figure out... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-event-registrati) |

### Generated PDFs

Keywords: `pdf, generated pdf, document pdf`

| Title | Source | Summary | Citation |
| --- | --- | --- | --- |
| Manage Signature Documents | rock_documentation | OK, so now we've seen how to create electronic signature templates and how to use them in workflows and event registrations to gather signatures. Let's wrap it up by looking at how you can view these documents. To view signed documents, navigate to `Admin Tools > Settings > Signature Documents` and select the document template you wish to view. 1. **Document Template Detail** - From here you can edit the template... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/manage-signature-documents) |
| Documents | rock_documentation | SECTIONS [Entity Documents](?Version=v19.0#entity-documents) [Merge Documents](?Version=v19.0#merge-documents) [Electronic Signatures](?Version=v19.0#electronic-signatures) ### Entity Documents Articles [Intro to Entity Documents](/documentation/core-concepts/documents/entity-documents/intro-to-entity-documents?Version=v19.0) [Configure Entity... | [source](https://community.rockrms.com/documentation/core-concepts/documents) |
| Electronic Signatures | rock_documentation | [Intro to Electronic Signatures](/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures?Version=v19.0) [Use Electronic Signatures in a Workflow](/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow?Version=v19.0) [Use Electronic Signatures in Event... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures) |
| Generate PDFs for Electronic Signature Documents | rock_documentation | After a document is signed, a PDF is generated containing both the document's content and the person’s signature. This is done so the person can be sent a PDF copy of the signed document. In most cases, Rock handles this process automatically. However, some organizations may require an external service for PDF generation. Generating a PDF on the Rock server is resource-intensive, especially during high-traffic... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/generate-pdfs-for-electronic-signature-docume) |
| Use Electronic Signatures in a Workflow | rock_documentation | Often, you'll want to have someone electronically sign a document as part of a workflow. This is super easy because there's a Workflow Action Type designed just for that. The *Electronic Signature* action type will present the person with a document to sign from within the workflow, similar to a workflow form. 1. **Signature Document Template** - Select the template for the document the person will be asked to sign.... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow) |
| Set Up Electronic Signatures | rock_documentation | Now that you've seen what electronic signatures can do, let's look at how to set them up. Your first step in gathering electronic signatures will be to create a *Document Template* by navigating to `Admin Tools > Settings > Signature Documents`. The template will be used to generate the individual documents a person will sign. Out of the box, Rock ships with an example *Photo Release* template and a *Field Trip... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures) |
| Intro to Electronic Signatures | rock_documentation | Many events and activities require waivers and releases to be signed by participants. Rock allows you to easily gather these signatures electronically without the need for a third party service. The requirement of a signed document can be added to a registration or a workflow. We'll cover how to configure these, and then we'll walk you through the configuration of the electronic signatures environment. # Anatomy of... | [source](https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures) |
| Manage Entity Documents | rock_documentation | With the new Entity Document block added, we can start adding documents to our groups. Start by clicking the icon in the Documents block to add your first document as shown below. 1. **Document Type** - Select the type of document that you want to add. The available items are controlled by the document type’s configuration and by block settings. 2. **Document Name** - If configured for the document type, a default... | [source](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/manage-entity-documents) |
| Merge Documents | rock_documentation | [Intro to Merge Documents](/documentation/core-concepts/documents/merge-documents/intro-to-merge-documents?Version=v19.0) [Use Merge Documents](/documentation/core-concepts/documents/merge-documents/use-merge-documents?Version=v19.0) [Administrate Merge Templates](/documentation/core-concepts/documents/merge-documents/administrate-merge-templates?Version=v19.0) [Create a Merge... | [source](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents) |
| Entity Documents | rock_documentation | [Intro to Entity Documents](/documentation/core-concepts/documents/entity-documents/intro-to-entity-documents?Version=v19.0) [Configure Entity Documents](/documentation/core-concepts/documents/entity-documents/configure-entity-documents?Version=v19.0) [Add the Block](/documentation/core-concepts/documents/entity-documents/add-the-block?Version=v19.0) [Manage Entity... | [source](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents) |


## Rebuild Dependencies

- Source records: `71`
- Approved claims: `26`
- Dependency file: `agent/concept-dependencies.jsonl`

When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.
