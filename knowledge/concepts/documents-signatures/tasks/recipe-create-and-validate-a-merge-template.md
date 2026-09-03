---
concept_id: documents-signatures
task_id: recipe-create-and-validate-a-merge-template
title: Recipe: Create and validate a merge template
generated: true
---

# Recipe: Create and validate a merge template

A global or personal template generates the intended output from a known grid source.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Person`
- `Group`
- `GroupMember`
- `Family`

## Entities And Tables

- `Person`
- `Group`
- `GroupMember`
- `Family`

## Steps

1. Choose personal or global scope.
2. For a global template, configure template security before broad use.
3. Choose Word or HTML based on the required output.
4. Open the target grid’s merge action.
5. inspect the row count, first 15 rows, and available merge fields.
6. Decide whether output should remain one row per person or combine family members.
7. Build the template using only the Lava features supported by that format.
8. For Word, choose whole-document repetition or `{% Next %}` multi-record layout deliberately.
9. Use straight quotation marks in all Lava expressions.
10. Run a small representative test and inspect the generated content before using the full population. (Administrate Merge Templates, Use Merge Documents, Create a Merge Document)
11. Replace curved quotation marks with straight quotation marks.
12. Check whether the template uses unsupported Word features: `if`, `raw`, or `lava` tags, Lava commands, or shortcodes.
13. Inspect the available merge fields for the actual grid source.
14. If the source contains GroupMember rows, use the exposed person row and access membership data through `Row.GroupMember`.
15. Check whether `{% Next %}` is present and whether the desired output is one complete document per row or multiple rows in one layout. (Create a Merge Document, Using Lava with Merge Documents)

## Do Not Assume

- The first 15 rows represent every record.
- General Lava features all work in Word.
- GroupMember rows retain GroupMember as the top-level row type.
- Template visibility implies authorization to generate it.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/administrate-merge-templates
- https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-event-registrati
- https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/create-a-merge-document
- https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/intro-to-electronic-signatures
- https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/use-merge-documents
- https://community.rockrms.com/documentation/core-concepts/documents/electronic-signatures/use-electronic-signatures-in-a-workflow
- https://community.rockrms.com/recipes/482
- https://community.rockrms.com/documentation/core-concepts/documents/merge-documents/using-lava-with-merge-documents
