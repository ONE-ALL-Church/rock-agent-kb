---
concept_id: check-in
task_id: diagnose-labels-not-printing
title: Diagnose Labels Not Printing
generated: true
---

# Diagnose Labels Not Printing

Find whether the failure is configuration, device routing, printer hardware, label definition, mobile/cloud print, or version-specific behavior.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Device`
- `Location`
- `Check-in Configuration`
- `Label`
- `Attendance`

## Entities And Tables

- `Device`
- `Location`
- `Attendance`
- `AttendanceOccurrence`

## Steps

1. Identify whether the flow is legacy, Next-Gen, mobile, or Windows Check-In Application.
2. Inspect whether labels route to the device printer, location printer, or cloud/mobile print route.
3. Verify the device, named location, physical printer, DPI, label dimensions, and label stock.
4. Run a test check-in and confirm whether an Attendance row is created before debugging the printer.
5. Check release caveats for shared printers, mobile self-check-in printing, DPI, and Windows app cut settings.

## Do Not Assume

- Do not assume the label template is broken before confirming printer routing.
- Do not assume mobile check-in prints to the phone.

## Source Links

- https://community.rockrms.com/documentation/church-management/check-in/labels/label-types
- https://community.rockrms.com/documentation/church-management/check-in/printing/reprint-a-label
- https://community.rockrms.com/documentation/church-management/check-in/labels/use-the-label-designer
- https://community.rockrms.com/documentation/church-management/check-in/labels/intro-to-labels
- https://community.rockrms.com/documentation/church-management/check-in/labels/link-labels-to-check-in
- https://community.rockrms.com/rocku/check-in/next-gen-labels
- https://community.rockrms.com/documentation/church-management/check-in/check-in-manager/check-in-manager-person-profile
- https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-kiosks
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/Manager/PersonRight/PersonRightPrintNextGenLabelsRequestBag.cs
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian/Framework/ViewModels/Blocks/CheckIn/Manager/PersonRight/personRightPrintNextGenLabelsRequestBag.d.ts
- https://community.rockrms.com/rocku/check-in/using-mobile-check-in
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/CheckIn/v2/Labels/PrintLabelRequest.cs
