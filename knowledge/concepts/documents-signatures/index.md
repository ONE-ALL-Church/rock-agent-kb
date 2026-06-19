---
id: concept-documents-signatures
title: Documents And Signatures
generated: true
last_built: 2026-06-19T07:39:26+00:00
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
- The strongest source families in this build are: rock_documentation, rock_recipes, triumph_resources, rock_core_release_notes, rock_rocku, rock_model_map.
- Related tags found in source records: usage, workflow, training, operations, admin, lava, releases, development.
- Source detail types include: documentation_article, recipe, training, triumph_resources.

## Reviewed Media Insights

| Source | Topic | Timestamp | Distilled Claim | Citation |
| --- | --- | --- | --- | --- |
| Electronic Signatures Transcript Insight | Rock operations | 00:00 | The Electronic Signatures RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. | [source](https://community.rockrms.com/rocku/event-registration/electronic-signatures) |
| Electronic Signatures Transcript Insight | release and roadmap awareness | 00:44 | For version, roadmap, and release-caveat awareness, Electronic Signatures should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. | [source](https://community.rockrms.com/rocku/event-registration/electronic-signatures) |
| Electronic Signatures Transcript Insight | Rock operations | 00:00 | The Electronic Signatures RockU lesson provides training context for Rock operations and administration; use the canonical lesson page as the citation and verify local configuration before implementation. | [source](https://community.rockrms.com/rocku/workflows/electronic-signatures-1) |
| Electronic Signatures Transcript Insight | release and roadmap awareness | 00:44 | For version, roadmap, and release-caveat awareness, Electronic Signatures should be treated as a training reference that helps route agents to the right Rock area, not as a substitute for official documentation or live checks. | [source](https://community.rockrms.com/rocku/workflows/electronic-signatures-1) |


## Source Coverage

- `rock_core_release_notes`: 5
- `rock_documentation`: 20
- `rock_model_map`: 12
- `rock_recipes`: 2
- `rock_rocku`: 29
- `triumph_resources`: 3

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
| Merge Documents | rock_documentation | [Intro to Merge Documents](/documentation/core-concepts/documents/merge-documents/intro-to-merge-documents?Version=v19.0) [Use Merge Documents](/documentation/core-concepts/documents/merge-documents/use-merge-documents?Version=v19.0) [Administrate Merge Templates](/documentation/core-concepts/documents/merge-documents/administrate-merge-templates?Version=v19.0) [Creating a Merge... | [source](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents) |
| Entity Documents | rock_documentation | [Intro to Entity Documents](/documentation/core-concepts/documents/entity-documents/intro-to-entity-documents?Version=v19.0) [Configure Entity Documents](/documentation/core-concepts/documents/entity-documents/configure-entity-documents?Version=v19.0) [Add the Block](/documentation/core-concepts/documents/entity-documents/add-the-block?Version=v19.0) [Manage Entity... | [source](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents) |
| Configure Entity Documents | rock_documentation | The first step is to define what types of documents you can add to entities. Navigate to `Admin Tools > Settings > Document Types` to manage the types of documents that can be stored for each entity. Pictured below, you can see we've already configured three types of documents, all for people. You might be wondering why we didn't mix it up a little and show you some example document types for other entities besides... | [source](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents/configure-entity-documents) |
| Creating a Merge Document | rock_documentation | As mentioned previously, Rock currently supports two different merge document formats: HTML and Word. Below we cover how to create a merge document for each format. ## Word The most common document format is Word. Creating these documents is actually pretty simple. Before we jump in it's important to talk about the two strategies for merging using Word. The first strategy is to create a Word document where the whole... | [source](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/creating-a-merge-document) |

## Data Model Landmarks

| Model | Category | Stable Rock | Properties | DB Props | Lava Props | Lava Non-DB Props | Pre-alpha Changes | Citation |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Signature Document Template](../../model-map/models/signature-document-template.md) | Core | 19.1.8 | 55 | 22 | 38 | 16 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Signature Document](../../model-map/models/signature-document.md) | Core | 19.1.8 | 65 | 31 | 49 | 18 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Benevolence Request Document](../../model-map/models/benevolence-request-document.md) | Finance | 19.1.8 | 41 | 12 | 26 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Document](../../model-map/models/document.md) | Core | 19.1.8 | 45 | 15 | 28 | 14 | 1 | [source](https://community.rockrms.com/ModelMap) |
| [Document Type](../../model-map/models/document-type.md) | Core | 19.1.8 | 50 | 21 | 35 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message](../../model-map/models/adaptive-message.md) | CMS | 19.1.8 | 44 | 15 | 29 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message Adaptation](../../model-map/models/adaptive-message-adaptation.md) | CMS | 19.1.8 | 47 | 18 | 32 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Adaptive Message Adaptation Segment](../../model-map/models/adaptive-message-adaptation-segment.md) | CMS | 19.1.8 | 40 | 11 | 25 | 14 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Block](../../model-map/models/block.md) | CMS | 19.1.8 | 55 | 23 | 40 | 17 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Block Type](../../model-map/models/block-type.md) | CMS | 19.1.8 | 47 | 18 | 27 | 12 | 0 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel](../../model-map/models/content-channel.md) | CMS | 19.1.8 | 65 | 29 | 47 | 18 | 1 | [source](https://community.rockrms.com/ModelMap) |
| [Content Channel Item](../../model-map/models/content-channel-item.md) | CMS | 19.1.8 | 71 | 31 | 52 | 21 | 0 | [source](https://community.rockrms.com/ModelMap) |

Lava fields that the stable generated Model Map marks as non-database are tracked in `knowledge/model-map/stable-properties.jsonl`. Examples for this concept:

- `Adaptive Message.AdaptiveMessageAdaptations` is Lava-marked but not database-marked in the generated Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.AdaptiveMessageCategories` is Lava-marked but not database-marked in the generated Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.AttributeValues` is Lava-marked but not database-marked in the generated Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.Attributes` is Lava-marked but not database-marked in the generated Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.CreatedByPersonId` is Lava-marked but not database-marked in the generated Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.CreatedByPersonName` is Lava-marked but not database-marked in the generated Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.EntityStringValue` is Lava-marked but not database-marked in the generated Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).
- `Adaptive Message.IdKey` is Lava-marked but not database-marked in the generated Model Map (Rock 19.1.8; source https://rocksolidchurchdemo.com/admin/power-tools/model-map).

## Version And Release Watch

| Version | Module | Change | Citation |
| --- | --- | --- | --- |
| 17.0 | CRM | Updated Electronic Signatures to allow for inserting the signature at specific places in the document template using a new optional "<!--[[ SignatureDetails ]]-->" keyword. | [source](https://www.rockrms.com/releasenotes) |
| 17.8 | Workflow | Fixed an issue where files uploaded through the Entity Document Add workflow action weren't properly linked to their parent Document. Because of that missing link, Rock couldn't check the Document Type's security rules when someone tried to access the file — it fell back to the File Type's security instead. Files are now linked correctly, so access is... | [source](https://www.rockrms.com/releasenotes) |
| 18.3 | Event | Fixed an issue with internal Event Registration blocks (Registration Instance - Registration List, Registration Details, and Registrant Details) where a Signature Document could be incorrectly shown for a registrant without a valid SignatureDocumentId, due to documents being matched by person instead of the registrant's record. Updated these blocks to use... | [source](https://www.rockrms.com/releasenotes) |
| 16.1 | Workflow | Fixed Signature Document Templates filtering to not show inactive templates in Workflow Actions. Fixes: #5511 | [source](https://www.rockrms.com/releasenotes) |
| 15.2 | Event | Fixed inactive signature document template from being selected in event registration. Fixes: #5510 | [source](https://www.rockrms.com/releasenotes) |

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
| Merge Documents | rock_documentation | [Intro to Merge Documents](/documentation/core-concepts/documents/merge-documents/intro-to-merge-documents?Version=v19.0) [Use Merge Documents](/documentation/core-concepts/documents/merge-documents/use-merge-documents?Version=v19.0) [Administrate Merge Templates](/documentation/core-concepts/documents/merge-documents/administrate-merge-templates?Version=v19.0) [Creating a Merge... | [source](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents) |
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
| Merge Documents | rock_documentation | [Intro to Merge Documents](/documentation/core-concepts/documents/merge-documents/intro-to-merge-documents?Version=v19.0) [Use Merge Documents](/documentation/core-concepts/documents/merge-documents/use-merge-documents?Version=v19.0) [Administrate Merge Templates](/documentation/core-concepts/documents/merge-documents/administrate-merge-templates?Version=v19.0) [Creating a Merge... | [source](https://community.rockrms.com/documentation/core-concepts/documents/merge-documents) |
| Entity Documents | rock_documentation | [Intro to Entity Documents](/documentation/core-concepts/documents/entity-documents/intro-to-entity-documents?Version=v19.0) [Configure Entity Documents](/documentation/core-concepts/documents/entity-documents/configure-entity-documents?Version=v19.0) [Add the Block](/documentation/core-concepts/documents/entity-documents/add-the-block?Version=v19.0) [Manage Entity... | [source](https://community.rockrms.com/documentation/core-concepts/documents/entity-documents) |


## Rebuild Dependencies

- Source records: `71`
- Approved claims: `0`
- Dependency file: `agent/concept-dependencies.jsonl`

When any listed source record or approved claim hash changes, rebuild this guide and review the diff before treating it as current.
