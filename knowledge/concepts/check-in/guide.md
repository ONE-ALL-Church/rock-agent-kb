---
id: authored-check-in
title: Check-In
generated: true
guide_status: llm_generated_needs_review
authority_level: draft
reviewed_by:
reviewed_at:
synthesis_model: "gpt-5.6-sol"
synthesis_reasoning_effort: "xhigh"
synthesis_prompt_id: "rock-kb-concept-guide-synthesis"
synthesis_prompt_version: "2.0.0"
synthesis_source_pack_hash: "90916be8b3a13a9e895872bdda71652b0a5561f4bee31b716235463a45dc917d"
---

# Check-In

## Agent Summary

Treat Rock check-in as a connected operational path, not as a single kiosk screen:

1. Identify a person or family.
2. Resolve who may be checked in.
3. Evaluate the active check-in configuration, areas, groups, locations, schedules, eligibility rules, room state, and capacity.
4. Record attendance.
5. Generate and route any required labels.
6. Monitor or adjust the active session through Check-In Manager or Device Manager.
7. Verify the resulting attendance and printing state.

Family and individual check-in use similar selection logic, but family check-in can process multiple people in one session and may reuse recent selections. Rock skips selection screens when only one valid option remains. [Individual vs. Family Check-in](https://community.rockrms.com/documentation/church-management/check-in/check-in-fundamentals/individual-vs-family-check-in)

When an issue occurs during a live service, inspect the exact active schedule, group-location relationship, room state, attendance context, label assignment, printer route, and manager-side changes before altering permanent configuration. This operational sequence is supported by the approved Check-In Manager claims (`claim:8c12d5c5828068271f42`, `claim:dfbe7795611e3e0a16c3`, and `claim:ee6db5c07a1abfc6a006`). [Check-In Manager training](https://community.rockrms.com/rocku/check-in/check-in-manager-1)

## Scope And Boundaries

This guide covers the evidence-supported check-in workflows in the supplied pack:

- Check-in configurations, areas, groups, locations, schedules, kiosks, and eligibility.
- Family, individual, relationship-based, serving-group, and assisted new-family check-in.
- Mobile, NFC, proximity, automatic, and attendance self-entry flows.
- Next-Gen labels, label types, printing, QR handoff, and reprinting.
- Check-In Manager, Device Manager, room state, thresholds, and live troubleshooting.
- Rapid Attendance Entry and Attendance Analytics.
- Manual check-out.
- Community-reviewed patterns for preregistration, dashboards, label Lava, and API-driven group placement.

Check-in depends on the owning concepts for people and families, groups, schedules, locations, attendance, labels, mobile applications, workflows, connections, and security. This guide explains how those elements meet at check-in; it does not replace their full administration guides. The official check-in documentation organizes the feature around fundamentals, configuration, kiosks, labels, printing, registration, attendance, Check-In Manager, and Device Manager. [Check-in documentation](https://community.rockrms.com/documentation/church-management/check-in)

Community contributions in this guide are implementation patterns, not guarantees about Rock core behavior. Any pattern marked for live verification must be tested against the target Rock version, installed blocks, permissions, schema, and data before use.

## Mental Model

### Configuration selects the rules

A check-in session runs against one configuration template, one kiosk device definition, a theme, and selected areas. The kiosk device supplies location context; the configuration supplies behavioral rules; the selected areas constrain what the session offers. Rock can expose areas associated with other configurations as secondary areas, but the session still uses one configuration template’s settings. [View the Administration Screen](https://community.rockrms.com/documentation/church-management/check-in/prepare-for-check-in/view-the-administration-screen)

A kiosk record is a reusable device configuration, not necessarily a one-to-one representation of a physical computer or tablet. Multiple physical machines can use the same kiosk definition. Kiosks and printers are managed as device types under `Admin Tools > Check-in > Devices`. [Configure Kiosks](https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-kiosks)

### Eligibility is an intersection

A person appears as a valid option only when the relevant configuration, area, group, location, schedule, room state, capacity, and person eligibility rules agree. Family and known-relationship rules additionally determine who may act for whom. [Individual vs. Family Check-in](https://community.rockrms.com/documentation/church-management/check-in/check-in-fundamentals/individual-vs-family-check-in), [Check-in Relationships](https://community.rockrms.com/documentation/church-management/check-in/check-in-fundamentals/check-in-relationships)

The agent should therefore avoid treating “the group exists,” “the room exists,” or “the schedule exists” as proof that check-in is available. The relevant relationships must also exist and be active for the current session. Locations are tied to check-in groups and enabled through schedules. [Configure Locations for a Kiosk](https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk)

### Attendance is the durable operational result

A successful participant flow produces attendance state. Labels are a downstream product of that state and its check-in context. Check-In Manager and analytics read or operate on attendance after it has been recorded. Rapid Attendance Entry and Attendance Self Entry are alternate ways of producing attendance for appropriate ministry workflows. [Attendance documentation](https://community.rockrms.com/documentation/church-management/check-in/attendance)

### Labels depend on context

A label’s output depends on its type, assigned check-in area, merge data, the attendance records generated by the session, printer selection, and print route. A successful test print does not prove the live check-in path is correct, and a functioning printer does not prove the label definition or active attendance context is correct. This is the operational guidance approved in `claim:44c7dd8911e8b6703262`, `claim:c51dddb61c2874195577`, and `claim:f1f6b9b0447d27d298bd`. [Next-Gen Labels training](https://community.rockrms.com/rocku/check-in/next-gen-labels)

## Core Configuration, Kiosks, Locations, And Schedules

### Check-in type and behavior

The check-in configuration controls whether the flow is individual or family-oriented and exposes settings for inactive people, check-out, registration, grade and age matching, required age or grade data, family auto-selection, and duplicate or concurrent attendance behavior. [Configure Settings for a Check-in Type](https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/configure-settings-for-a-check-in-type)

In a family flow, Rock can preselect family members based on recent attendance and can optionally reuse their area, group, and location choices. When only one valid time, area, group, or location exists, the corresponding screen can be skipped. [Individual vs. Family Check-in](https://community.rockrms.com/documentation/church-management/check-in/check-in-fundamentals/individual-vs-family-check-in)

### Kiosk configuration

A kiosk device definition can include its identifying name, location or geofence, printing behavior, kiosk type, camera capability, family-editing options, and served locations. Browser-based check-in cannot perform client printing. Server printing requires the web server to reach the printer; externally hosted Rock environments need an appropriate cloud-printing path for server printing. [Configure Kiosks](https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-kiosks)

For Next-Gen Check-in, the setup page is `/nextgen-checkin/setup` and the kiosk page is `/nextgen-checkin`. Saved kiosk configurations require Rock v16.7 or later and represent remembered combinations of theme, kiosk, configuration, and areas. [Configure Kiosks](https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-kiosks)

Rock also supports `KioskId`, `CheckinConfigId`, and `GroupTypeIds` URL parameters for loading a known setup. If a configuration is supplied without a kiosk identifier, Rock can attempt kiosk matching by client IP address. Theme can also be overridden through a route parameter. Treat URLs containing identifiers as configuration artifacts: validate them in the target environment and do not copy identifiers between installations. [Use URL Parameters for Check-in](https://community.rockrms.com/documentation/church-management/check-in/kiosks/use-url-parameters-for-check-in)

### Locations, schedules, and room state

Locations represent the buildings or rooms where check-in occurs. They are hierarchical, linked to groups, and enabled for specific schedules. A room can be:

- Absent from the group’s configured locations.
- Present but not linked to the current schedule.
- Scheduled but manually closed.
- Open but unavailable because a threshold was reached.
- Open and scheduled but filtered out by the kiosk’s served locations or the person’s eligibility.

Rock documents a normal threshold, which an attendant may override, and an absolute threshold, which cannot be overridden. Rooms can be opened or closed through Check-In Manager or Device Manager. The Auto Open Locations job can reopen rooms on a configured interval. [Configure Locations for a Kiosk](https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk)

A community-reviewed model pattern adds an important inspection distinction: room-capacity thresholds are properties of the location, while schedule availability is represented through the group-location schedule relationship. Because this contribution requires live verification, confirm the installed schema and reuse of the location before changing either capacity or schedule links. [Model Map](https://community.rockrms.com/ModelMap)

### Eligibility by age, grade, and birthdate

Rock v19 documentation identifies three grade-and-age matching modes:

- **Grade And Age Must Match:** grade must match, and either age or birthdate must match.
- **Age Match Not Required:** a valid grade match can avoid an age check.
- **Prioritize Grade Over Age:** grade-matched groups are favored and groups that fail the grade test are excluded.

Inspect the check-in configuration’s selected behavior as well as each group’s ranges before diagnosing a missing or unexpected option. [Use Grade and Age Matching Behavior](https://community.rockrms.com/documentation/church-management/check-in/advanced-check-in/use-grade-and-age-matching-behavior)

Groups may also be configured with a birthdate range. This can keep a cohort together as it ages, but the documentation notes that group names then require ongoing maintenance as the cohort’s grade changes. [Configure by Birthdate](https://community.rockrms.com/documentation/church-management/check-in/advanced-check-in/configure-by-birthdate)

### Check-in relationships

The `Allow Check-in` known relationship permits someone outside a child’s immediate family to check the child in. Rock can also grant check-in capability to other known-relationship roles, such as a grandparent role, by enabling `Can Check-in` on that role. Because this expands who may act for a child, inspect both the person-level relationship and the role configuration when an unexpected adult can or cannot perform check-in. [Check-in Relationships](https://community.rockrms.com/documentation/church-management/check-in/check-in-fundamentals/check-in-relationships)

## Mobile Check-In

### Preconditions

Before enabling mobile check-in, verify all of the following:

1. The public site is served over HTTPS.
2. The required Google API key is configured for geofencing.
3. The underlying groups, locations, schedules, and check-in configuration already work through normal check-in.
4. The intended kiosk devices, areas, configuration, and theme are selected on the Mobile Check-in Launcher.
5. Each campus boundary and its associated locations are correct.

The first three requirements come from approved claim `claim:3d32a2c3e36e71683eb0`, which still requires target-instance verification. [Mobile Check-in Overview](https://community.rockrms.com/rocku/check-in/mobile-check-in-overview)

### Virtual kiosk model

Treat each mobile check-in device record as a virtual kiosk. Use the Check-in Kiosk device type, configure its campus geofence, associate the relevant campus locations, and create separate device definitions when campuses need different boundaries. Point the Mobile Check-in Launcher at the permitted devices, configuration, theme, and areas. These dependencies are supported by approved claims `claim:0b6f8c45033ed0228a3b`, `claim:72dd1841cd10ed6d5a30`, and `claim:c78fd6f074218814ab14`. [Mobile Check-in Configuration](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration)

The supplied immutable source snapshot shows the launcher’s configuration surface includes device selection, check-in configuration, check-in areas, theme, and an option to bypass device location services in favor of campus selection. This is implementation evidence from the `develop` branch, not proof that those fields exist in the same form on every installed version. [Mobile Check-in Launcher settings at commit 471fd303](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/MobileCheckInLauncher/CustomSettingsBag.cs)

### Participant flow

Mobile check-in can support family or individual check-in. Design the first visit around identity confirmation, such as login or phone lookup. A recognized returning device can begin closer to the selection flow and show a welcome-back experience. Approved claims `claim:0b388b0e4afdabbc9903`, `claim:520ba5f389698ad4894c`, and `claim:c04a3055801d1b1a9fa4` support this structure. [Using Mobile Check-in](https://community.rockrms.com/rocku/check-in/using-mobile-check-in)

The operational flow remains:

1. Identify the person.
2. Select the people being checked in.
3. Select valid check-in opportunities.
4. Complete the attendance transaction.
5. Use the resulting QR code for label-printing handoff when labels are required.

The QR code is a printing bridge, not the attendance transaction itself. Additional completed selections can update the QR payload rather than requiring a separate label handoff. These points are approved but still marked for target-flow verification in `claim:aa549ff122698db9c8a1` and `claim:9f505350705f22d88caf`. [Mobile Check-in Overview](https://community.rockrms.com/rocku/check-in/mobile-check-in-overview), [Using Mobile Check-in](https://community.rockrms.com/rocku/check-in/using-mobile-check-in)

The supplied evidence describes QR handoff from Classic Mobile Check-in to a configured iPad kiosk. Current kiosk documentation also distinguishes that Classic-generated mobile QR scanning remains limited to iPads, while other kiosk QR scenarios have different camera and theme requirements. Verify the exact mobile and kiosk generation in use before promising cross-device scanning. [Configure Kiosks](https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-kiosks)

### Fallback states and copy

The participant-facing flow can show fallback messages when:

- No kiosk matches the participant’s location or selected campus.
- Check-in is outside the active service window.
- No eligible person or opportunity exists.
- Location cannot be determined.
- Location permission is not available.

Approved claim `claim:ff136cde6aa716bfc87c` supports these fallback states. The immutable source snapshot also represents distinct kiosk-resolution, availability, no-service, identity, and message states. [Kiosk resolution at commit 471fd303](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/MobileCheckInLauncher/KioskResolutionBag.cs), [launcher states at commit 471fd303](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.JavaScript.Obsidian.Blocks/src/CheckIn/MobileCheckInLauncher/types.partial.ts)

Launcher copy can be Lava-enabled, but early screens may not have an identified person. Write identity-neutral copy until the flow has actually resolved the individual or family. [Mobile Check-in Configuration](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration)

## Labels And Printing

### Choose the label type by print cardinality

Rock v19 documents five Next-Gen label types:

- **Family:** one label per check-in session.
- **Person:** one label for each checked-in person.
- **Attendance:** one label for every attendance record.
- **Checkout:** one label for each person during check-out.
- **Person Location:** one label for each person-location combination.

Choose the type according to the required number and context of labels. A wrong type can look like duplicate or missing printing even when the printer behaves correctly. [Label Types](https://community.rockrms.com/documentation/church-management/check-in/labels/label-types)

Rock includes sample Child, Note, Parent, and Name Tag labels. The first-visit indicator is based on prior group attendance, not the person’s `First Visit` attribute. [Intro to Labels](https://community.rockrms.com/documentation/church-management/check-in/labels/intro-to-labels)

### Design, link, preview, and print

The Label Designer is available under `Admin Tools > Settings > Check-in > Next-gen Labels`. It supports both visual label construction and ZPL-based formats. The visual designer can place text, images, icons, and security codes and apply conditions to controls. [Use the Label Designer](https://community.rockrms.com/documentation/church-management/check-in/labels/use-the-label-designer)

After designing a label, link it to the intended check-in area under the check-in configuration’s **Next-Gen Check-in Labels** settings. Installations migrating from labels used before v16.7 must recreate corresponding label definitions in the Label Designer. [Link Labels to Check-in](https://community.rockrms.com/documentation/church-management/check-in/labels/link-labels-to-check-in)

Preview with representative data. The designer can preview from an actual attendance identifier and send the result to a configured printer. Test at least one case for every meaningful conditional, long value, missing value, room, schedule, and security-code path. [Use the Label Designer](https://community.rockrms.com/documentation/church-management/check-in/labels/use-the-label-designer)

### Merge data and dynamic text

Available merge fields vary by label type. Person labels include fields such as `Person`, `PersonAttendance`, `AllAttendance`, `Family`, `IsFirstTime`, area, group, role, location and schedule names, and `SecurityCode`. Attendance labels center on a specific attendance detail. Person Location labels add location-scoped attendance context. [Label Types](https://community.rockrms.com/documentation/church-management/check-in/labels/label-types)

A reviewed community contribution distinguishes two designer behaviors:

- Built-in attendee, check-in, and achievement data-source controls should use their provided field selection.
- Custom Text with Dynamic Text enabled evaluates Lava against the merge object made available for the selected label type.

For a Person label, the contribution recommends starting from `PersonAttendance` when the desired value belongs to the checked-in group, room, schedule, or attendance context. Treat this as a community implementation pattern and test it with representative attendance data before publication or production use. [Label Types](https://community.rockrms.com/documentation/church-management/check-in/labels/label-types), [Next-Gen Labels training](https://community.rockrms.com/rocku/check-in/next-gen-labels)

### Reprinting

Labels can be reprinted from the kiosk Device Manager or Check-In Manager when the relevant setting and security permission allow it. Browser restrictions mean Check-In Manager reprinting works only with server printing, while kiosk Device Manager reprinting can work with server or device printing. The documented reprint feature is not available for mobile check-ins. [Reprint a Label](https://community.rockrms.com/documentation/church-management/check-in/printing/reprint-a-label)

On the Check-In Manager person profile, the reprint action can allow selection of label types and printer. The `Reprint Labels` security action on the recent-attendance block provides finer control over who sees the action. [Check-In Manager Person Profile](https://community.rockrms.com/documentation/church-management/check-in/check-in-manager/check-in-manager-person-profile)

## Check-In Manager And Device Manager

Treat Check-In Manager as the operational control surface for an active session. Start diagnosis from the current roster, room, schedule, attendance, label, and manager state rather than from the intended configuration alone. Approved claims `claim:8c12d5c5828068271f42` and `claim:ee6db5c07a1abfc6a006` support this approach. [Check-In Manager training](https://community.rockrms.com/rocku/check-in/check-in-manager-1)

The Check-In Manager person profile can show current and past check-ins, attendance-change history, family members, selected person attributes, badges, and label reprinting when enabled. Attendance history can expose room changes or deletion, which is useful when the live state differs from what volunteers remember. [Check-In Manager Person Profile](https://community.rockrms.com/documentation/church-management/check-in/check-in-manager/check-in-manager-person-profile)

At the kiosk, an authorized operator can enter Device Manager through the gear icon and PIN authentication. Device Manager can open or close rooms assigned to that kiosk. Its override action can check a child into a room without applying the room’s age or grade ranges, so use it as an explicit operational exception rather than as routine eligibility repair. [Intro to the Device Manager](https://community.rockrms.com/documentation/church-management/check-in/device-manager/intro-to-the-device-manager)

Rock v19’s Check-In Manager roster uses real-time updates so attendance changes can appear without manual refresh. If changes lag, inspect browser connectivity, the installed block version, and the local check-in configuration. This behavior is supported by approved v19 claims `claim:7df4b8c20f9419a30a5a`, `claim:9ad17cb08b8955d0d3ec`, and `claim:dc7cb132c34cdde8cb4e`. [New Features and Enhancements Coming to v19](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=262s)

## Attendance Entry And Analysis

### Rapid Attendance Entry

Rapid Attendance Entry is designed for high-volume attendance recording and can also capture communication cards, prayer requests, notes, family updates, and workflow launches when its block settings enable those actions. [Rapid Attendance Entry](https://community.rockrms.com/documentation/church-management/check-in/attendance/rapid-attendance-entry)

The operator begins with a group and attendance date. Location appears when the group has multiple locations, and schedule appears when the selected location has multiple schedules. Campus can be exposed as an optional location filter through block settings. This is supported by approved claim `claim:dae53f2715a5838fd9fc`. [Rapid Attendance Entry](https://community.rockrms.com/documentation/church-management/check-in/attendance/rapid-attendance-entry)

After the context is selected, the operator searches for a person or family. Depending on configuration, the screen can:

- Record attendance.
- Add a family.
- Add or edit related information.
- Capture notes or prayer requests.
- Launch a workflow.
- Link the current attendance count to the attendance list.

When launched, a workflow receives the person as its entity, and appropriately typed workflow attributes can receive the selected group, location, and schedule. [Rapid Attendance Entry](https://community.rockrms.com/documentation/church-management/check-in/attendance/rapid-attendance-entry)

Because the block is configurable at the page level, teams can create focused page variants for different ministries instead of enabling every action on one catch-all page. This is the approved configuration guidance in `claim:a69d0b49451cf59e5ef8`.

### Attendance Analytics

Attendance Analytics is available at `Tools > Reporting > Attendance Analytics` and operates in Chart and Attendees modes. Chart mode returns counts over the chosen criteria; Attendees mode returns matching people. Supported filters include attendance area, date range, schedules, campuses, groups, data views, visits, and attendance patterns. [Use Attendance Analytics](https://community.rockrms.com/documentation/church-management/check-in/attendance/use-attendance-analytics)

The block can be configured for different group types, including serving-team attendance. A group-specific mode can constrain the results to a group supplied to the page, while hiding broader bulk operations. Verify the selected group types and visible filters before concluding that attendance is missing. [Use Attendance Analytics](https://community.rockrms.com/documentation/church-management/check-in/attendance/use-attendance-analytics)

### Attendance Self Entry

Attendance Self Entry lets a participant report who attended an online, in-person, or hybrid service with them. The flow can include family members and configured relationship types, remember prior companions, and record attendance after the participant confirms the selected people. [Attendance Self Entry](https://community.rockrms.com/documentation/church-management/check-in/attendance/attendance-self-entry)

The block uses its selected check-in configuration and current time to identify an appropriate service. If no applicable scheduled opportunity is found, the documented fallback is the first matching group without a location or schedule; if no such group exists, attendance cannot be recorded. The process can create person and family records because a Rock person record is required for attendance. A workflow may optionally launch after submission. [Attendance Self Entry](https://community.rockrms.com/documentation/church-management/check-in/attendance/attendance-self-entry)

## Registration And New Families

A check-in kiosk can support volunteer-assisted registration of new families or guests. The documented kiosk registration experience is intended for a trained volunteer rather than unassisted guest entry. It emphasizes essential fields during arrival, with additional data collected later when appropriate. [Intro to Registration](https://community.rockrms.com/documentation/church-management/check-in/registration/intro-to-registration)

For public family preregistration, the supplied community-reviewed pattern recommends designing the form to reduce first-visit friction while improving person, family, and child data before arrival. The page should explain its value, minimize duplicate or partial records, and connect captured information to a defined workflow or connection process. Before broad launch, test the complete path from the public form through family creation, check-in eligibility, and staff follow-up. These patterns are supported by approved community claims `claim:57b56ebf5bb293682e3d`, `claim:90fecb6ea51cf994ff92`, `claim:b6025804c011523e291d`, and `claim:bd2faf9d63fc7ecc41c1`. [Community preregistration example](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz)

## Additional Check-In Options

### Automatic check-in

Automatic check-in works with family check-in. It can reuse recent people and opportunity selections from a configurable lookback period. If no recent check-in is available, Rock can select the first eligible option based on age, grade, and room availability. Participants can still change the selected location. [Use Auto Check-in](https://community.rockrms.com/documentation/church-management/check-in/additional-check-in-options/use-auto-check-in)

### Serving groups and other group types

Serving groups are preconfigured for check-in, but each group still needs a meeting location and schedule. The kiosk must serve the selected location. [Check-in for Serving Groups](https://community.rockrms.com/documentation/church-management/check-in/advanced-check-in/check-in-for-serving-groups)

For another group type to participate in check-in, Rock v19 documentation directs administrators to allow named locations, include the Meeting Location type, and enable location schedules. Each group still needs its meeting details configured. [Create a New Group Type](https://community.rockrms.com/documentation/church-management/check-in/advanced-check-in/create-a-new-group-type)

### NFC check-in

Rock v19 documents NFC check-in as a Rock Mobile App flow launched by an NFC tag. The setup uses a mobile Check-in block, a deep link, an optional short link, and an NFC tag containing that link. Page parameters can supply location, kiosk, and related check-in context. Test both app opening and web fallback behavior on the supported mobile platforms before rollout. [Use NFC Check-In](https://community.rockrms.com/documentation/church-management/check-in/additional-check-in-options/use-nfc-check-in)

### Proximity attendance

Proximity Attendance requires a provisioned Rock Mobile app, Beacon Monitoring, enabled proximity check-in, and configured beacon hardware. Rock maps campus and location information into beacon identifiers; the named location needs a valid 16-bit beacon identifier. [Use Proximity Attendance](https://community.rockrms.com/documentation/church-management/check-in/additional-check-in-options/use-proximity-attendance)

Avoid overly dense or overlapping beacon coverage. The documentation warns that nearby areas can be confused and that overlapping services can cause automatic schedule selection to favor the service that starts and ends later. Validate the attendance result under real movement and schedule conditions. [Use Proximity Attendance](https://community.rockrms.com/documentation/church-management/check-in/additional-check-in-options/use-proximity-attendance)

### Kiosk ads

Next-Gen Check-in can display Content Channel items as kiosk ads on the welcome screen. Item-level Content Channel security is not enforced for these ads; every item in the assigned channel can appear. Use separate channels and campus filtering when visibility must differ by audience or location. [Run Kiosk Ads](https://community.rockrms.com/documentation/church-management/check-in/kiosks/run-kiosk-ads)

### Manual check-out

Rock normally removes people from the Check-In Manager display after the event end time without marking a manual check-out. Manual check-out can be enabled separately for kiosks and Check-In Manager. A Checkout-type label can be linked to an area when printing at checkout is required. [Administer Check-Out](https://community.rockrms.com/documentation/church-management/check-in/advanced-check-in/administer-check-out)

## Version And Authority Caveats

Most hydrated official documentation in this pack targets Rock v19.0. Some kiosk and Next-Gen label material also identifies v16.7 as the minimum version for saved kiosk configurations and the Next-Gen label migration path. Verify the installed Rock version and consult its corresponding documentation before applying a v19 procedure. [Configure Kiosks](https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-kiosks), [Link Labels to Check-in](https://community.rockrms.com/documentation/church-management/check-in/labels/link-labels-to-check-in)

Specific v19 evidence includes:

- Check-In Manager roster attendance updates can appear in real time without manual refresh. [v19 feature overview](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=262s)
- Recurring iCal occurrences are materialized into `ScheduleDate` rows for date-oriented SQL and Lava access. Agents working on v19 reporting should use those generated dates rather than inventing another recurrence-expansion process. [3 Underrated Features, 06:26](https://www.youtube.com/watch?v=edanHiYSDIM&t=386s)
- Built-in proof-of-work CAPTCHA has organization and block controls with visible, invisible, and disabled modes. For exposed preregistration or self-entry forms, verify the selected mode and test every public form. [3 Underrated Features, 03:15](https://www.youtube.com/watch?v=edanHiYSDIM&t=195s)
- If preregistration follow-up depends on the redesigned v19 Connections experience, show staff the new interface and provide brief training before deployment. [3 Underrated Features, 01:31](https://www.youtube.com/watch?v=edanHiYSDIM&t=91s)

Large-version upgrades and patch releases carry different validation risks. Verify current release notes and retest the full check-in path after both major and patch upgrades; do not rely on an older release discussion as current release status. [Rock Cast episode 33](https://shows.acast.com/rock-cast/episodes/episode-33-rock-73-and-new-rx2018-tracks)

The pack also contains immutable `develop`-branch code and a migration under a Version 20.0 path for the Mobile Check-in Launcher. It shows an implementation with launcher devices, configuration, areas, theme, location-service behavior, identity states, availability messages, and QR configuration. Treat this only as implementation-in-development at commit `471fd303d111b2e46218228dbc1e93dba8856fa3`; it does not establish release availability or the configuration of any installation. [Mobile Check-in Launcher source](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Blocks/CheckIn/MobileCheckInLauncher.cs), [associated migration](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Migrations/Migrations/Version%2020.0/Version%2020.0/202608241752115_PerformAdditionalMobileCheckinLauncherChopSteps.cs)

## Troubleshooting Decision Tree

### A person or family cannot be found

1. Confirm whether the flow expects login, phone lookup, another search method, or an already recognized mobile device.
2. Search thoroughly before creating a new person or family.
3. Verify that the person record and family membership are correct.
4. If someone outside the family should act for a child, inspect the person’s known relationship and the relationship role’s `Can Check-in` setting.
5. If using mobile check-in, confirm that the identity step actually completed before interpreting eligibility results.
6. Stop before creating a duplicate when an existing record might be incomplete or matched under another family. [Check-in Relationships](https://community.rockrms.com/documentation/church-management/check-in/check-in-fundamentals/check-in-relationships), [Rapid Attendance Entry](https://community.rockrms.com/documentation/church-management/check-in/attendance/rapid-attendance-entry)

### A person is found but has no check-in options

1. Identify the exact configuration, kiosk, and enabled areas for the active session.
2. Confirm the current schedule window.
3. Verify that the group is linked to the intended location and schedule.
4. Confirm that the kiosk serves that location.
5. Check whether the room is open and below its applicable thresholds.
6. Compare the person’s age, grade, birthdate, ability level, inactive status, and prior attendance against the selected configuration rules.
7. Inspect duplicate or concurrent check-in prevention.
8. Check for manager-side room closures or attendance edits.
9. Do not use Device Manager override until the failed eligibility rule is understood. [Configure Settings for a Check-in Type](https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/configure-settings-for-a-check-in-type), [Configure Locations for a Kiosk](https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk)

### A room is unavailable only during one service

1. Confirm the current date and service window.
2. Inspect the group-location relationship.
3. Inspect the schedule linked to that group-location pair.
4. Confirm that the room has not been closed in Check-In Manager or Device Manager.
5. Check the normal and absolute thresholds.
6. Compare other services using the same location before changing a location-level threshold.
7. Stop when the evidence only proves the desired schedule exists but not that it is linked to the group-location pair. [Configure Locations for a Kiosk](https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk)

### Mobile check-in reports no campus, no service, or location failure

1. Confirm HTTPS and the required geofencing API configuration.
2. Prove that the same person can use the underlying normal check-in configuration.
3. Verify that the launcher enables the intended virtual kiosk devices, configuration, and areas.
4. Verify each device’s campus geofence and associated locations.
5. Check whether browser location permission was granted.
6. If location services are intentionally disabled, confirm that the intended campus-selection option is available.
7. Verify the current schedule window and room availability.
8. Read the exact fallback message before changing configuration; no kiosk match, no active service, and no eligible person are different failures. [Mobile Check-in Configuration](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration), [Kiosk availability at commit 471fd303](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/MobileCheckInLauncher/KioskAvailabilityBag.cs)

### A mobile QR code does not print labels

1. Verify that check-in completed and attendance exists before diagnosing the QR code.
2. Confirm that QR display is enabled for the mobile flow.
3. Identify whether the QR was generated by Classic Mobile Check-in or another check-in implementation.
4. Confirm that the scanning kiosk type, camera, theme, and platform support that QR path.
5. Verify label assignments, printer route, and active printer.
6. Do not assume scanning the QR creates attendance; the approved workflow treats it as a label-printing handoff. [Configure Kiosks](https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-kiosks), [Using Mobile Check-in](https://community.rockrms.com/rocku/check-in/using-mobile-check-in)

### Symptom: Attendance Saved But Label Did Not Print

1. Confirm that attendance was saved.
2. Identify the expected label type and resulting print count.
3. Verify that the label is linked to the selected check-in area.
4. Preview the label with representative attendance data.
5. Inspect merge data and conditions.
6. Confirm the active kiosk’s print method.
7. Confirm the selected printer and its network path.
8. Check whether the issue affects all labels, one label type, one room, or one person.
9. Treat the printer as the cause only after template, linkage, merge data, routing, and attendance context pass. [Use the Label Designer](https://community.rockrms.com/documentation/church-management/check-in/labels/use-the-label-designer), [Link Labels to Check-in](https://community.rockrms.com/documentation/church-management/check-in/labels/link-labels-to-check-in)

### A label prints with wrong or duplicated data

1. Compare the chosen label type with its documented print cardinality.
2. Inspect the exact attendance records generated by the session.
3. Verify whether the merge field is top-level, person-scoped, attendance-scoped, or location-scoped.
4. For dynamic Lava, inspect the object available to the selected label type.
5. Preview against an attendance case that reproduces the problem.
6. Test multiple services and multiple rooms separately.
7. Do not rewrite the template until the active attendance context is understood. [Label Types](https://community.rockrms.com/documentation/church-management/check-in/labels/label-types)

### A label cannot be reprinted

1. Determine whether reprinting is being attempted from Device Manager, Check-In Manager, or a mobile check-in.
2. Confirm that reprinting is enabled on the relevant block.
3. Confirm that the operator has the `Reprint Labels` security permission.
4. For Check-In Manager, verify server printing.
5. For kiosk Device Manager, verify the configured device or server printing route.
6. Stop if the original transaction was mobile check-in; the documented reprint feature does not support that case. [Reprint a Label](https://community.rockrms.com/documentation/church-management/check-in/printing/reprint-a-label)

### Check-In Manager attendance updates lag

1. Confirm that the installation is running the expected v19 block.
2. Verify browser connectivity.
3. Compare the roster with the underlying attendance state.
4. Confirm that the browser is on the intended page and active configuration.
5. Inspect whether the attendance was edited, moved, checked out, or deleted.
6. Refresh only as a diagnostic step; persistent dependence on refresh indicates the real-time path still needs investigation. [v19 Check-In Manager feature](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=262s), [Check-In Manager Person Profile](https://community.rockrms.com/documentation/church-management/check-in/check-in-manager/check-in-manager-person-profile)

### Rapid Attendance Entry is missing expected actions

1. Confirm which page variant and block instance the operator is using.
2. Verify the selected group and attendance date.
3. Confirm whether location and schedule should appear for that group context.
4. Inspect block settings for attendance, family addition, notes, prayer requests, workflows, and navigation pages.
5. Confirm that the desired workflow and correctly typed group, location, or schedule attributes exist.
6. Do not assume every Rapid Attendance Entry page exposes every supported action. [Rapid Attendance Entry](https://community.rockrms.com/documentation/church-management/check-in/attendance/rapid-attendance-entry)

### Attendance Self Entry does not record attendance

1. Verify the block’s selected check-in configuration.
2. Confirm the current time relative to configured schedules.
3. Verify that the appropriate group is associated with the intended location.
4. If no schedule matches, inspect whether a fallback group without a location or schedule exists.
5. Confirm that valid person records were created or resolved.
6. Inspect any post-submit workflow or redirect separately from attendance creation. [Attendance Self Entry](https://community.rockrms.com/documentation/church-management/check-in/attendance/attendance-self-entry)

### Proximity attendance records the wrong service or area

1. Confirm the person opted in and the mobile app has Beacon Monitoring enabled.
2. Inspect the campus and location beacon identifiers.
3. Check for nearby overlapping beacon coverage.
4. Check for overlapping service windows.
5. Compare the recorded attendance with the documented automatic schedule-selection behavior.
6. Reduce ambiguity in beacon placement or scheduling before changing attendance after the fact. [Use Proximity Attendance](https://community.rockrms.com/documentation/church-management/check-in/additional-check-in-options/use-proximity-attendance)

### A REST integration creates unexpected schedules or links

This is a community-reviewed troubleshooting pattern that requires target-version verification.

1. Stop further mutations.
2. Read back the created `GroupLocation`, schedule records, and group-location schedule relationships.
3. Determine whether the request included partial navigation objects instead of scalar relationship fields.
4. Prove that any unexpected schedule is accidental and unreferenced before considering deletion.
5. Use only a tested, authorized endpoint for cleanup.
6. Read back every relationship after cleanup.
7. Do not treat a successful REST response as proof that the intended relationship was created. [Generated REST controller source](https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/ApiController.cs)

### Attendance appears to save but the page gives no confirmation

A Rock v15 community recipe describes adding a toast around Group Attendance Detail network results because that block’s save behavior could be unclear to users. The recipe is neither reviewed nor endorsed by the Rock core team and intercepts endpoint traffic, so do not apply it as a general v19 fix. First verify whether attendance actually saved and whether the behavior still reproduces on the installed block version. [Community recipe 461](https://community.rockrms.com/recipes/461)

## Agent Task Recipes

### Recipe: Preflight a standard kiosk session

**Outcome:** The intended people can check in to the intended rooms and schedules, and required labels print through the configured route.

1. Record the target campus, service, kiosk definition, check-in configuration, areas, rooms, and label set.
2. Confirm the kiosk’s served locations and print method.
3. Confirm each group-location-schedule relationship.
4. Verify current room state and thresholds.
5. Test one normal returning family.
6. Test one first-time or assisted family flow if enabled.
7. Test one boundary eligibility case.
8. Confirm attendance creation.
9. Confirm every required label type and expected print count.
10. Open Check-In Manager and verify the resulting roster state.

**Inspect:**

- Configuration, kiosk, areas, locations, schedules, room state, thresholds, attendance, labels, and printer route.

**Do not assume:**

- A working setup page proves that the current service is open.
- A test print proves that live check-in merge data and routing are correct.

**Stop when:**

- The exact active relationships cannot be identified or a proposed change would affect another service or campus. [View the Administration Screen](https://community.rockrms.com/documentation/church-management/check-in/prepare-for-check-in/view-the-administration-screen), [Configure Locations for a Kiosk](https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk)

### Recipe: Preflight mobile check-in

**Outcome:** A first-time and returning participant can complete attendance and, where required, hand labels off to a supported kiosk.

1. Prove standard check-in works for the target groups, rooms, and schedules.
2. Verify HTTPS and the target instance’s geofencing API configuration.
3. Inspect the virtual kiosk device for type, campus boundary, and locations.
4. Inspect the launcher’s devices, configuration, theme, and areas.
5. Test identity-neutral early-screen copy.
6. Test first-time identification.
7. Test a recognized returning device.
8. Test outside-geofence, outside-schedule, and no-eligible-person states.
9. Complete attendance and verify it independently.
10. Scan the QR code on the supported kiosk and verify label output.

**Do not assume:**

- A recognized device guarantees current eligibility.
- The QR code performs the attendance transaction.
- One campus device definition is suitable for another campus boundary.

**Stop when:**

- The target platform’s QR support or the installed launcher generation is unclear. [Mobile Check-in Overview](https://community.rockrms.com/rocku/check-in/mobile-check-in-overview), [Mobile Check-in Configuration](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration)

### Recipe: Validate a Next-Gen label end to end

**Outcome:** The correct number of labels prints with accurate data for representative check-in scenarios.

1. Define the desired print event and cardinality.
2. Select the matching Family, Person, Attendance, Checkout, or Person Location type.
3. Build or copy the label in Label Designer.
4. Link the label to the intended area.
5. Preview with representative attendance.
6. Test long, missing, and conditional values.
7. Run a real staged check-in.
8. Compare created attendance records with printed labels.
9. Verify kiosk routing and printer selection.
10. Test reprinting through the supported operational surface if required.

**Inspect:**

- Label type, area linkage, merge object, attendance context, routing, printer, and reprint permissions.

**Do not assume:**

- `First Visit` person data controls the label’s first-time indicator.
- A field available to one label type is available to another. [Intro to Labels](https://community.rockrms.com/documentation/church-management/check-in/labels/intro-to-labels), [Label Types](https://community.rockrms.com/documentation/church-management/check-in/labels/label-types)

### Recipe: Triage a live-service incident

**Outcome:** The immediate cause is isolated without prematurely changing permanent configuration.

1. Capture the exact time, campus, kiosk, person, group, room, schedule, and symptom.
2. Compare another person and another kiosk to bound the impact.
3. Inspect Check-In Manager for current room and attendance state.
4. Inspect the active schedule window.
5. Inspect group-location-schedule relationships.
6. Inspect room open/closed state and thresholds.
7. Inspect label and printer state if printing is involved.
8. Review recent manager-side attendance or room changes.
9. Apply only an authorized, reversible live remedy.
10. Record what was observed separately from what was changed.

**Stop when:**

- The remedy would alter shared location capacity, schedules, eligibility, or production data without knowing the affected scope. [Check-In Manager training](https://community.rockrms.com/rocku/check-in/check-in-manager-1), [Configure Locations for a Kiosk](https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk)

### Recipe: Create a focused Rapid Attendance Entry page

**Outcome:** A ministry receives only the attendance and follow-up actions needed for its workflow.

1. Define the group scope and attendance outcome.
2. Decide whether attendance itself is enabled.
3. Decide whether staff may add families.
4. Select required note, prayer-request, and workflow actions.
5. Configure any group restriction or parent-group boundary.
6. Configure destination pages for family creation and attendance review.
7. If launching workflows, provide correctly typed group, location, and schedule attributes where needed.
8. Test the page with its actual group, location, schedule, and attendance date.
9. Verify attendance and every enabled side action independently.

**Do not assume:**

- Settings on one page instance apply to another page variant.
- A workflow launch proves that attendance saved. [Rapid Attendance Entry](https://community.rockrms.com/documentation/church-management/check-in/attendance/rapid-attendance-entry)

### Recipe: Build an attendance analysis

**Outcome:** The result answers a bounded attendance question with reproducible criteria.

1. State whether the output needs counts or people.
2. Select Chart or Attendees mode.
3. Select the correct attendance area.
4. Set the date range.
5. Apply schedule, campus, group, and data-view filters only when required.
6. Add visit or pattern criteria when the question concerns frequency or absence.
7. Record every selected filter.
8. Compare the result with Check-In Detail when validation is needed.
9. On v19, use materialized `ScheduleDate` occurrences for custom date-oriented SQL or Lava work.

**Stop when:**

- The selected group type, schedule basis, or attendance area is ambiguous. [Use Attendance Analytics](https://community.rockrms.com/documentation/church-management/check-in/attendance/use-attendance-analytics), [v19 ScheduleDate overview](https://www.youtube.com/watch?v=edanHiYSDIM&t=386s)

### Recipe: Prepare a new-family arrival path

**Outcome:** A new family reaches an eligible check-in state without duplicate records and with an assigned follow-up process.

1. Decide whether the entry point is volunteer-assisted kiosk registration or public preregistration.
2. For kiosk registration, station a trained volunteer and collect the essential arrival fields.
3. For public preregistration, explain the benefit and gather only the data needed for reliable family creation and check-in eligibility.
4. Search for existing people before creating records.
5. Verify family membership and child data.
6. Verify check-in eligibility in the intended configuration.
7. Connect the result to the approved workflow or connection process.
8. Test the full path with a non-production test family before broad launch.
9. On v19 public forms, verify CAPTCHA mode and test the complete exposed form.

**Do not assume:**

- Form submission proves family creation, check-in eligibility, or staff follow-up.
- The assisted kiosk registration flow is designed for unassisted guests. [Intro to Registration](https://community.rockrms.com/documentation/church-management/check-in/registration/intro-to-registration), [community preregistration example](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz)

### Recipe: Reprint a damaged label

**Outcome:** An authorized operator reproduces the required label through a supported route.

1. Identify the person and original attendance.
2. Determine whether Device Manager or Check-In Manager is the supported surface.
3. Confirm reprinting is enabled.
4. Confirm the operator has the required security access.
5. Select the required label types.
6. Select the intended printer.
7. Print and verify legibility.
8. Stop if the source was mobile check-in or if the current print route does not support reprinting.

**Inspect:**

- Attendance, reprint setting, security action, label selection, printer, and print method. [Reprint a Label](https://community.rockrms.com/documentation/church-management/check-in/printing/reprint-a-label)

## Known Gaps And Live Verification

No current target installation was reviewed as part of this synthesis. The live-verification notes in the evidence pack confirmed structural surfaces on a bounded read-only instance; they did not prove that another installation’s pages, blocks, devices, geofences, schedules, permissions, labels, or printers are correctly configured.

Verify locally before action:

- Installed Rock version, patch level, and whether the relevant block is legacy, Next-Gen, mobile-shell, or the newer browser Mobile Check-in Launcher.
- HTTPS, Google API key, browser location permission, campus geofences, and physical boundary behavior.
- QR generation and scanning support for the exact mobile and kiosk clients.
- Check-in configuration, areas, devices, locations, schedules, room states, thresholds, and manager-side overrides.
- Printer provider, device versus server printing, cloud-printing requirements, network reachability, and reprint support.
- Block and page permissions, PIN authentication, reprint security, family-editing access, and public-form CAPTCHA mode.
- Public preregistration record matching, duplicate prevention, eligibility, and follow-up behavior.
- Attendance Self Entry’s schedule resolution and fallback group on the target configuration.
- Proximity beacon placement, mobile-shell provisioning, opt-in state, and overlapping-service results.
- Current release notes for major and patch upgrades.

The following community-reviewed patterns require separate target-version and implementation verification:

- Treating location capacity separately from group-location schedule availability.
- Updating group-location schedule links through an available and authorized Obsidian Schedule Builder action.
- Avoiding partial navigation objects in generated REST payloads.
- Reading back a created `GroupMember` before linking it to a `RegistrationRegistrant`.
- Building a read-only operational dashboard from registration, placement, occurrence, and attendance state.
- Using temporary ministry groups when a shadowing state must affect badges, rosters, or check-in visibility.
- Adding UI confirmation around attendance-saving behavior.

The REST-related contributions cite mutable `develop` paths rather than immutable excerpts in this pack. Do not promote them to universal API behavior. Reproduce the behavior safely on the target version, inspect the generated endpoint contract, use read-back verification, and obtain explicit authorization before any corrective mutation.

## Source Map

### Official Rock documentation

- [Check-in](https://community.rockrms.com/documentation/church-management/check-in) — owning documentation map.
- [Individual vs. Family Check-in](https://community.rockrms.com/documentation/church-management/check-in/check-in-fundamentals/individual-vs-family-check-in) — participant flow and skipped selection screens.
- [Check-in Relationships](https://community.rockrms.com/documentation/church-management/check-in/check-in-fundamentals/check-in-relationships) — relationship-based authority.
- [Configure Settings for a Check-in Type](https://community.rockrms.com/documentation/church-management/check-in/configure-check-in/configure-settings-for-a-check-in-type) — configuration behavior and eligibility settings.
- [Configure Kiosks](https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-kiosks) — device definitions, printing, cameras, locations, and Next-Gen setup.
- [Configure Locations for a Kiosk](https://community.rockrms.com/documentation/church-management/check-in/kiosks/configure-locations-for-a-kiosk) — group-location scheduling, room state, and thresholds.
- [Use URL Parameters for Check-in](https://community.rockrms.com/documentation/church-management/check-in/kiosks/use-url-parameters-for-check-in) — kiosk setup parameters and matching.
- [Run Kiosk Ads](https://community.rockrms.com/documentation/church-management/check-in/kiosks/run-kiosk-ads) — Next-Gen ads and security caveat.
- [Intro to Labels](https://community.rockrms.com/documentation/church-management/check-in/labels/intro-to-labels) — standard labels and first-time behavior.
- [Label Types](https://community.rockrms.com/documentation/church-management/check-in/labels/label-types) — label cardinality and merge fields.
- [Use the Label Designer](https://community.rockrms.com/documentation/church-management/check-in/labels/use-the-label-designer) — design and preview.
- [Link Labels to Check-in](https://community.rockrms.com/documentation/church-management/check-in/labels/link-labels-to-check-in) — area assignment and migration.
- [Reprint a Label](https://community.rockrms.com/documentation/church-management/check-in/printing/reprint-a-label) — supported reprint paths and restrictions.
- [Check-In Manager Person Profile](https://community.rockrms.com/documentation/church-management/check-in/check-in-manager/check-in-manager-person-profile) — attendance history, profiles, and reprinting.
- [Intro to the Device Manager](https://community.rockrms.com/documentation/church-management/check-in/device-manager/intro-to-the-device-manager) — PIN access, room management, and override.
- [Rapid Attendance Entry](https://community.rockrms.com/documentation/church-management/check-in/attendance/rapid-attendance-entry) — bulk attendance and ministry actions.
- [Use Attendance Analytics](https://community.rockrms.com/documentation/church-management/check-in/attendance/use-attendance-analytics) — reporting modes and filters.
- [Attendance Self Entry](https://community.rockrms.com/documentation/church-management/check-in/attendance/attendance-self-entry) — participant-submitted attendance.
- [Intro to Registration](https://community.rockrms.com/documentation/church-management/check-in/registration/intro-to-registration) — volunteer-assisted family registration.
- [Administer Check-Out](https://community.rockrms.com/documentation/church-management/check-in/advanced-check-in/administer-check-out) — manual checkout.
- [Check-in for Serving Groups](https://community.rockrms.com/documentation/church-management/check-in/advanced-check-in/check-in-for-serving-groups) — serving-group setup.
- [Use Auto Check-in](https://community.rockrms.com/documentation/church-management/check-in/additional-check-in-options/use-auto-check-in) — reuse of recent family selections.
- [Use NFC Check-In](https://community.rockrms.com/documentation/church-management/check-in/additional-check-in-options/use-nfc-check-in) — mobile deep-link and tag workflow.
- [Use Proximity Attendance](https://community.rockrms.com/documentation/church-management/check-in/additional-check-in-options/use-proximity-attendance) — beacon-based attendance.

### Approved RockU guidance

- [Mobile Check-in Overview](https://community.rockrms.com/rocku/check-in/mobile-check-in-overview)
- [Mobile Check-in Configuration](https://community.rockrms.com/rocku/check-in/mobile-check-in-configuration)
- [Using Mobile Check-in](https://community.rockrms.com/rocku/check-in/using-mobile-check-in)
- [Check-In Manager](https://community.rockrms.com/rocku/check-in/check-in-manager-1)
- [Next-Gen Labels](https://community.rockrms.com/rocku/check-in/next-gen-labels)
- [Rapid Attendance Entry](https://community.rockrms.com/rocku/check-in/rapid-attendance-entry)

### Version-scoped release evidence

- [New Features and Enhancements Coming to v19](https://www.youtube.com/watch?v=c-wycR9HEuQ&t=262s) — real-time Check-In Manager roster.
- [3 Underrated Features Churches Are Overlooking](https://www.youtube.com/watch?v=edanHiYSDIM) — v19 Connections, CAPTCHA, Check-In Manager, and `ScheduleDate` claims.
- [Rock Cast episode 33](https://shows.acast.com/rock-cast/episodes/episode-33-rock-73-and-new-rx2018-tracks) — upgrade-planning caveat.

### Immutable implementation evidence

- [Mobile Check-in Launcher settings](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/MobileCheckInLauncher/CustomSettingsBag.cs)
- [Kiosk availability](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/MobileCheckInLauncher/KioskAvailabilityBag.cs)
- [Kiosk resolution](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.ViewModels/Blocks/CheckIn/MobileCheckInLauncher/KioskResolutionBag.cs)
- [Mobile Check-in Launcher block](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Blocks/CheckIn/MobileCheckInLauncher.cs)
- [Version 20 migration snapshot](https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Rock.Migrations/Migrations/Version%2020.0/Version%2020.0/202608241752115_PerformAdditionalMobileCheckinLauncherChopSteps.cs)

### Community patterns

- [Community preregistration example](https://community.rockrms.com/community-hubs/5QlyA2Ydlq/media/D9PDdgePqz) — end-to-end family preregistration and follow-up pattern.
- [Recipe 461](https://community.rockrms.com/recipes/461) — version-specific attendance confirmation example; not endorsed by Rock core.
- [Model Map](https://community.rockrms.com/ModelMap) — starting point for community entity-inspection patterns.
