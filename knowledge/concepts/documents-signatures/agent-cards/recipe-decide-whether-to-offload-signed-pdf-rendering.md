---
concept_id: documents-signatures
task_id: recipe-decide-whether-to-offload-signed-pdf-rendering
title: Recipe: Decide whether to offload signed-PDF rendering
generated: true
---

# Recipe: Decide whether to offload signed-PDF rendering

The organization has a justified local or external rendering path.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Guide section`

## Entities And Tables

- `See guide`

## Steps

1. Identify whether the host can run Puppeteer or Chrome.
2. If it cannot, plan an external rendering service.
3. If it can, evaluate expected signature volume and concurrent server load.
4. When local rendering poses excessive load, select and review an external service.
5. Configure the **PDF External Render Endpoint** under System Configuration.
6. Test preview, completed signing, PDF storage, and receipt delivery.
7. Load-test only within an approved non-production or otherwise controlled scope.
8. Document provider, privacy, credential, capacity, and failure-handling ownership. (Generate PDFs for Electronic Signature Documents)
9. Separate rendering from communication delivery: first determine whether the signed PDF exists.
10. Inspect the signature template’s file type and completion System Communication.
11. Inspect the **PDF External Render Endpoint** system setting.
12. Determine whether the host can run Puppeteer or Chrome.
13. If local rendering is supported, review whether concurrent volume is exhausting server capacity.
14. If external rendering is required, verify endpoint configuration and reachability without exposing credentials.
15. After PDF generation succeeds, troubleshoot the completion email through the communications system. (Generate PDFs for Electronic Signature Documents, Set Up Electronic Signatures)

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/generate-pdfs-for-electronic-signature-docume
- https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/set-up-electronic-signatures
