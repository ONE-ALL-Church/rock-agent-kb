---
concept_id: platform-configuration
task_id: recipe-stage-a-campus
title: Recipe: Stage a campus
generated: true
---

# Recipe: Stage a campus

A campus is configured without prematurely exposing it as active.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Location`
- `Schedule`
- `Campus`
- `Block`
- `Attribute`

## Entities And Tables

- `Location`
- `Schedule`
- `Campus`
- `Block`
- `Attribute`

## Steps

1. Create the required named location with Location Type `Campus`.
2. Create the campus as inactive.
3. Assign its name, code, status, type, dates, leader, location, contact details, and URL as applicable.
4. Associate the intended campus schedules.
5. Configure topics and campus attributes only where required.
6. Avoid building new dependencies on legacy Service Times.
7. Test downstream blocks and reports with the campus inactive.
8. Prepare staff and public communication.
9. Activate only after the dependent surfaces have been verified.

## Do Not Assume

- Avoid building new dependencies on legacy Service Times.

## Source Links

- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses/manage-campuses
- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/campuses/add-attributes-to-campuses
- https://community.rockrms.com/documentation/church-management/people/person-attributes/display-person-attributes
- https://community.rockrms.com/documentation/church-management/people/person-profile-page/extended-attributes-tab
- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values
- https://community.rockrms.com/ModelMap
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/Archive/View_DefinedValuesAttributeValues.sql
- https://community.rockrms.com/documentation/core-concepts/rock-fundamentals/attributes
- https://community.rockrms.com/developer/303---blast-off/attributes
- https://github.com/SparkDevNetwork/Rock/blob/471fd303d111b2e46218228dbc1e93dba8856fa3/Dev%20Tools/Sql/Archive/View_DefinedTypeAttributes.sql
- https://community.rockrms.com/rocku/check-in/check-in-manager-1
