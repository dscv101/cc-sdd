---
description: Generate comprehensive requirements for a specification
allowed-tools: Bash, Glob, Grep, LS, Read, Write, Edit, MultiEdit, Update, WebSearch, WebFetch
argument-hint: <feature-name>
---

# Requirements Generation

<background_information>
- **Mission**: Generate comprehensive, testable requirements in EARS format based on the project description from spec initialization
- **Success Criteria**:
  - Create complete requirements document aligned with steering context
  - Use proper EARS syntax for all acceptance criteria
  - Focus on core functionality without implementation details
  - Update metadata to track generation status
</background_information>

<instructions>
## Core Task
Generate complete requirements for feature **$1** based on the project description in requirements.md.

## Execution Steps

1. **Load Context**:
   - Read `{{KIRO_DIR}}/specs/$1/spec.json` for language and metadata
   - Read `{{KIRO_DIR}}/specs/$1/requirements.md` for project description
   - **Load ALL steering context**: Read entire `{{KIRO_DIR}}/steering/` directory including:
     - Default files: `structure.md`, `tech.md`, `product.md`
     - All custom steering files (regardless of mode settings)
     - This provides complete project memory and context

2. **Read Guidelines**:
   - Read `{{KIRO_DIR}}/settings/rules/ears-format.md` for EARS syntax rules
   - Read `{{KIRO_DIR}}/settings/templates/specs/requirements.md` for document structure

3. **Generate Requirements Document**:
   
   **A. Fill Document Metadata Section**:
   - VERSION: Start with 1.0.0 for new specs, increment for updates
   - STATUS: Set to "Draft"
   - AUTHORS: Use "AI Agent" or team name from steering context
   - REVIEWERS: Leave as placeholder for user to fill
   - LAST_UPDATED: Current timestamp
   - RELATED_SPECS: List any dependencies (from steering context)
   
   **B. Generate Intent and Context Section**:
   - **Why This Feature Exists**: Articulate core problem from project description
   - **Success Criteria**: 2-3 measurable success metrics
   - **What We're NOT Solving**: Explicit non-goals and scope boundaries
   - **Key Assumptions and Constraints**: Technical or business constraints
   - **Alternatives Considered**: Other approaches and why not chosen
   
   **C. Generate Requirements with Enhanced Format**:
   - Use REQ-X.Y numbering (e.g., REQ-1.0, REQ-1.1, REQ-2.0)
   - For each requirement include:
     * **ID**: REQ-X.Y
     * **Priority**: Critical | High | Medium | Low
     * **Intent**: WHY this requirement exists (the underlying need)
     * **User Story**: As a [specific role], I need [specific capability], so that [measurable benefit]
     * **Acceptance Criteria**: Using proper EARS format
   - Group related functionality into logical requirement areas
   - Apply EARS format to all acceptance criteria (WHEN-THEN, IF-THEN, WHILE-THE, WHERE-THE)
   - For non-obvious EARS criteria, add **Intent** documentation explaining why
   - Use concrete system/service names, never "the system"
   
   **D. Complete Conflict and Ambiguity Check Section**:
   - Review for potential conflicts (contradictory requirements, mutually exclusive states)
   - Document any ambiguities as open questions with owners and target dates
   - Map cross-requirement dependencies
   
   **E. Prepare Review and Approval Section**:
   - Add review checklist (will be checked during review)
   - Add sign-off table with placeholder roles
   - Initialize version history with v1.0.0 entry
   
   Use language specified in spec.json for all content

4. **Update Metadata** in spec.json:
   - Set `phase: "requirements-generated"`
   - Set `approvals.requirements.generated: true`
   - Update `updated_at` timestamp

## Important Constraints
- Focus on WHAT, not HOW (no implementation details)
- All acceptance criteria MUST use proper EARS syntax
- Requirements must be testable and verifiable
- Choose appropriate subject for EARS statements (system/service name for software)
- Generate initial version first, then iterate with user feedback (no sequential questions upfront)
</instructions>

## Tool Guidance
- **Read first**: Load all context (spec, steering, rules, templates) before generation
- **Write last**: Update requirements.md only after complete generation
- Use **WebSearch/WebFetch** only if external domain knowledge needed

## Output Description
Provide output in the language specified in spec.json with:

1. **Generated Requirements Summary**: Brief overview of major requirement areas (3-5 bullets)
2. **Document Status**: Confirm requirements.md updated and spec.json metadata updated
3. **Next Steps**: Guide user on how to proceed (approve and continue, or modify)

**Format Requirements**:
- Use Markdown headings for clarity
- Include file paths in code blocks
- Keep summary concise (under 300 words)

## Safety & Fallback

### Error Scenarios
- **Missing Project Description**: If requirements.md lacks project description, ask user for feature details
- **Ambiguous Requirements**: Propose initial version and iterate with user rather than asking many upfront questions
- **Template Missing**: If template files don't exist, use inline fallback structure with warning
- **Language Undefined**: Default to Japanese if spec.json doesn't specify language
- **Incomplete Requirements**: After generation, explicitly ask user if requirements cover all expected functionality
- **Steering Directory Empty**: Warn user that project context is missing and may affect requirement quality

### Next Phase: Design Generation

**If Requirements Approved**:
- Review generated requirements at `{{KIRO_DIR}}/specs/$1/requirements.md`
- **Optional Gap Analysis** (for existing codebases):
  - Run `/kiro:validate-gap $1` to analyze implementation gap with current code
  - Identifies existing components, integration points, and implementation strategy
  - Recommended for brownfield projects; skip for greenfield
- Then `/kiro:spec-design $1 -y` to proceed to design phase

**If Modifications Needed**:
- Provide feedback and re-run `/kiro:spec-requirements $1`

**Note**: Approval is mandatory before proceeding to design phase.

think
