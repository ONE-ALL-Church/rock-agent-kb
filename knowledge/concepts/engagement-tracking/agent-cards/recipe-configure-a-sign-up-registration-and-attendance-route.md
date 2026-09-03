---
concept_id: engagement-tracking
task_id: recipe-configure-a-sign-up-registration-and-attendance-route
title: Recipe: Configure a Sign-Up registration and attendance route
generated: true
---

# Recipe: Configure a Sign-Up registration and attendance route

Guests or an existing group can register, and authorized operators can record attendance.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Attendance`
- `Group`
- `Location`
- `Schedule`
- `Page`

## Entities And Tables

- `Attendance`
- `Group`
- `Location`
- `Schedule`
- `Page`

## Steps

1. Confirm the project’s underlying group and opportunity structure.
2. For a custom project type, verify inheritance, child-type allowance, schedule option, location mode and Finder inclusion.
3. Configure the external Finder for guest self-registration, or configure Sign-Up Register in Group mode for an existing group.
4. Pass the required project, location, schedule and group IdKeys.
5. Configure the attendance page with the required IdKeys and a `yyyy-MM-dd` occurrence date.
6. Configure the Group Attendance Reminder communication when reminder links are needed.
7. Verify the organization phone number on SMS-enabled registration and reminder communications.
8. Test with an account holding the intended project or group-type permissions.
9. For registration or reminder communication errors, confirm that an organization phone number is configured for the SMS-enabled system communication.
10. For a registration route, verify project, location, schedule and, when applicable, group IdKeys.
11. Remember that the project parameter represents the Sign-Up group.
12. For attendance, confirm the occurrence date uses `yyyy-MM-dd`.
13. Inspect project or group-type permissions before changing attendee records. (Configure Sign-Ups, Group Registration and Attendance for Sign-Ups, Configure Sign-Up Permissions)

## Do Not Assume

- Do not treat generated guidance as live-instance proof.

## Source Links

- https://community.rockrms.com/documentation/engagement/additional-engagement-tools
