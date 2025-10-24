---
mode: 'agent'
description: Generate implementation tasks for a specification
---
<meta>
description: Generate implementation tasks for a specification
argument-hint: <feature-name:$1> [-y:$2]
</meta>

# Implementation Tasks Generator

<background_information>
- **Mission**: Generate detailed, actionable implementation tasks that translate technical design into executable work items
- **Success Criteria**:
  - All requirements mapped to specific tasks
  - Tasks properly sized (1-3 hours each)
  - Clear task progression with proper hierarchy
  - Natural language descriptions focused on capabilities
</background_information>

<instructions>
## Core Task
Generate implementation tasks for feature **$1** based on approved requirements and design.

## Execution Steps

### Step 1: Load Context

**Read all necessary context**:
- `{{KIRO_DIR}}/specs/$1/spec.json`, `requirements.md`, `design.md`
- `{{KIRO_DIR}}/specs/$1/tasks.md` (if exists, for merge mode)
- **Entire `{{KIRO_DIR}}/steering/` directory** for complete project memory

**Validate approvals**:
- If `-y` flag provided ($2 == "-y"): Auto-approve requirements and design in spec.json
- Otherwise: Verify both approved (stop if not, see Safety & Fallback)

### Step 2: Generate Implementation Tasks

**Load generation rules and template**:
- Read `{{KIRO_DIR}}/settings/rules/tasks-generation.md` for principles
- Read `{{KIRO_DIR}}/settings/templates/specs/tasks.md` for format

**Generate task list following enhanced format**:

**A. Fill Document Metadata Section**:
- VERSION: Start with 1.0.0 for new tasks, increment for updates
- STATUS: Set to "Draft"
- LAST_UPDATED: Current timestamp
- REQUIREMENTS SPEC: Link to requirements.md with its version
- DESIGN SPEC: Link to design.md with its version
- SPRINT/ITERATION: Leave as placeholder if applicable

**B. Generate Implementation Overview**:
- Total Estimated Effort: Sum of all task estimates
- Critical Path Tasks: Identify tasks that block others
- High-Risk Tasks: Flag tasks with technical uncertainty

**C. Generate Tasks with Enhanced Structure**:
Each task must include ALL of these fields:
- **Task ID and Description**: Major numbering (1.0, 2.0) or sub-task (2.1, 2.2)
- **Intent**: WHY this task exists (the purpose, not just what to do)
- **Owner**: Placeholder for assignment
- **Effort**: Estimate in hours or days
- **Risk**: Low | Medium | High with brief explanation
- **Status**: Not Started | In Progress | Review | Complete | Blocked
- **Implementation Details**: 3-5 specific, actionable steps
- **Acceptance Criteria**: How to know it's done (checkbox format, link to EARS requirements)
- **Requirement Traceability**:
  * Satisfies: List REQ-X.Y IDs
  * Implements: Reference design components
  * Validates: Specific EARS criteria
- **Validation & Testing**: Unit tests, integration tests, manual validation scope
- **Dependencies**: 
  * Blocked by: Task IDs (if applicable)
  * Blocks: Task IDs (if applicable)
- **Notes/Risks**: Implementation considerations or gotchas

**D. Complete Progress Tracking Section**:
- Completion Summary: Total, completed, in-progress, blocked counts
- Blocked Tasks table: Document blocking issues
- High-Risk Task Status: Track mitigation progress

**E. Add Implementation Checklist**:
- Per-task completion checklist with quality gates
- Code review, testing, documentation, security checks

Use language specified in spec.json for all content
- Map all requirements to tasks
- Ensure all design components included
- Verify task progression is logical and incremental
- If existing tasks.md found, merge with new content

### Step 3: Finalize

**Write and update**:
- Create/update `{{KIRO_DIR}}/specs/$1/tasks.md` with all enhanced fields
- Update spec.json metadata:
  - Set `phase: "tasks-generated"`
  - Set `approvals.tasks.generated: true, approved: false`
  - Set `approvals.requirements.approved: true`
  - Set `approvals.design.approved: true`
  - Update `updated_at` timestamp

## Critical Constraints
- **Follow rules strictly**: All principles in tasks-generation.md are mandatory
- **Natural Language**: Describe what to do, not code structure details
- **Complete Coverage**: ALL requirements must map to tasks
- **Maximum 2 Levels**: Major tasks and sub-tasks only (no deeper nesting)
- **Sequential Numbering**: Major tasks increment (1, 2, 3...), never repeat
- **Task Integration**: Every task must connect to the system (no orphaned work)
</instructions>

## Tool Guidance
- **Read first**: Load all context, rules, and templates before generation
- **Write last**: Generate tasks.md only after complete analysis and verification

## Output Description

Provide brief summary in the language specified in spec.json:

1. **Status**: Confirm tasks generated at `{{KIRO_DIR}}/specs/$1/tasks.md`
2. **Task Summary**: 
   - Total: X major tasks, Y sub-tasks
   - All Z requirements covered
   - Average task size: 1-3 hours per sub-task
3. **Quality Validation**:
   - ✅ All requirements mapped to tasks
   - ✅ Task dependencies verified
   - ✅ Testing tasks included
4. **Next Action**: Review tasks and proceed when ready

**Format**: Concise (under 200 words)

## Safety & Fallback

### Error Scenarios

**Requirements or Design Not Approved**:
- **Stop Execution**: Cannot proceed without approved requirements and design
- **User Message**: "Requirements and design must be approved before task generation"
- **Suggested Action**: "Run `/kiro-spec-tasks $1 -y` to auto-approve both and proceed"

**Missing Requirements or Design**:
- **Stop Execution**: Both documents must exist
- **User Message**: "Missing requirements.md or design.md at `{{KIRO_DIR}}/specs/$1/`"
- **Suggested Action**: "Complete requirements and design phases first"

**Incomplete Requirements Coverage**:
- **Warning**: "Not all requirements mapped to tasks. Review coverage."
- **User Action Required**: Confirm intentional gaps or regenerate tasks

**Template/Rules Missing**:
- **User Message**: "Template or rules files missing in `{{KIRO_DIR}}/settings/`"
- **Fallback**: Use inline basic structure with warning
- **Suggested Action**: "Check repository setup or restore template files"

### Next Phase: Implementation

**Before Starting Implementation**:
- **IMPORTANT**: Clear conversation history and free up context before running `/kiro-spec-impl`
- This applies when starting first task OR switching between tasks
- Fresh context ensures clean state and proper task focus

**If Tasks Approved**:
- Execute specific task: `/kiro-spec-impl $1 1.1` (recommended: clear context between each task)
- Execute multiple tasks: `/kiro-spec-impl $1 1.1,1.2` (use cautiously, clear context between tasks)
- Without arguments: `/kiro-spec-impl $1` (executes all pending tasks - NOT recommended due to context bloat)

**If Modifications Needed**:
- Provide feedback and re-run `/kiro-spec-tasks $1`
- Existing tasks used as reference (merge mode)

**Note**: The implementation phase will guide you through executing tasks with appropriate context and validation.
