---
concept_id: learning-lms-engagement
task_id: recipe-prepare-a-course-for-launch
title: Recipe: Prepare A Course For Launch
generated: true
---

# Recipe: Prepare A Course For Launch

Prepare a course or class for learners by checking structure, activities, schedules, access, communications, and reporting.

## When To Use

- Use this when the user's task matches this operational symptom or implementation path.
- Verify live Rock records before making changes.

## Live Records To Inspect

- `Learning Program`
- `Learning Course`
- `Learning Class`
- `Learning Semester`
- `Learning Class Activity`
- `Learning Participant`
- `System Communication`

## Entities And Tables

- `LearningProgram`
- `LearningCourse`
- `LearningClass`
- `LearningSemester`
- `LearningClassActivity`
- `LearningParticipant`

## Steps

1. Confirm the course belongs to the intended program and has the expected class structure.
2. Review activities, lesson order, due dates, prerequisites, and learner-facing content.
3. Verify participant access, campus or semester scope, and communication triggers.
4. Check reporting and completion behavior before inviting learners.
5. Run a small test learner through the course and inspect the resulting rows.

## Do Not Assume

- Do not launch from content review alone; verify the data model and learner path.
- Do not ignore version-specific LMS release caveats.

## Source Links

- https://www.rockrms.com/releasenotes
- https://community.rockrms.com/documentation/bookcontent/43/354
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Reporting/DataSelect/Person/HasCompletedCourseSelect.cs
- https://community.rockrms.com/documentation/engagement/learning-management-system/program-administration/courses
- https://community.rockrms.com/ModelMap
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.ViewModels/Blocks/Lms/LearningCourseRequirement/LearningCourseRequirementsBag.cs
- https://www.triumph.tech/resources/github-spotlight-11142025
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/v2/Models/CodeGenerated/LearningCourseRequirementsController.CodeGenerated.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock/Model/CodeGenerated/LearningCourseRequirementService.CodeGenerated.cs
- https://github.com/SparkDevNetwork/Rock/blob/develop/Rock.Rest/Controllers/CodeGenerated/LearningCourseRequirementsController.CodeGenerated.cs
