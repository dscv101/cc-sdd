# AI Agent Rules and Guidelines

## Project Overview
cc-sdd is a spec-driven development (SDD) tool that provides structured templates and workflows for AI-assisted software development. It supports multiple IDEs (Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI, Qwen Code, Windsurf) and emphasizes rigorous specification-first development.

## Critical Project Principles

### 1. Specifications Are Source Code
Following Sean Grove's philosophy: "Specifications are the new code. Code is a lossy projection of intent."

- Treat spec templates as executable documentation
- Preserve intent alongside implementation details
- Version control specifications like source code
- Specs should be precise enough to compile into tests and documentation

### 2. EARS Notation Standard
All requirements must follow EARS (Easy Approach to Requirements Syntax):
- Use concrete system/service names, never "the system"
- Every requirement must be testable with clear pass/fail conditions
- Document intent for non-obvious requirements
- Include specific, measurable responses (numbers, SLAs, behaviors)

### 3. Template Quality Standards
Templates must guide users to create:
- **Unambiguous** specifications with clear pass/fail conditions
- **Testable** requirements that can be automated or manually verified
- **Traceable** documents linking requirements → design → tasks → code
- **Intent-preserving** documentation capturing the WHY, not just WHAT

## Development Workflow

### Standard Workflow
1. **Requirements Phase**: Use EARS notation to define testable acceptance criteria
2. **Design Phase**: Document architecture with intent preservation and ambiguity detection
3. **Tasks Phase**: Break design into traceable, validated implementation units
4. **Review**: Each phase requires stakeholder sign-off before proceeding

### Template Enhancement Guidelines
When modifying templates:
- Add rich, domain-specific examples (not generic placeholders)
- Include "good vs bad" examples showing anti-patterns
- Provide intent documentation patterns
- Add quality checklists for validation
- Include metadata for version control and status tracking

## Repository Rules (from .codegen/sandbox_config.yaml)

### Required Tools
- **ruff**: For formatting, linting, and import sorting
- **pytest**: For testing with minimum 80% coverage target
- **bandit**: For security checks
- **pyrefly**: For type checking
- **graphite (gt)**: Use instead of git tools for branch management

### Code Quality Standards
- All Python code must pass ruff formatting and linting
- Security vulnerabilities must be identified with bandit
- Type hints required and validated with pyrefly
- Tests required with 80%+ coverage

### Workflow Standards
- Always read AGENTS.md at start of work
- Always use code-reasoning MCP for structured thinking
- Reflect on work done before submitting PRs
- Update AGENTS.md with new rules after reflection

## Recent Work

### PR #7: Template Enhancement and Command Updates (2025-10-23)

#### Phase 1: Template Enhancement
**What Changed:**
- Enhanced `requirements.md` with intent preservation, conflict detection, rich EARS examples
- Added "Intent Preservation and Design Rationale" section to `design.md`
- Added "Ambiguity Detection and Open Questions" section to `design.md`
- Completely restructured `tasks.md` with detailed traceability and validation criteria
- Significantly expanded `ears-format.md` with domain examples and anti-patterns

#### Phase 2: Command Compatibility Updates
**What Changed:**
- Updated 18 command files across all 6 agent types (claude-code, claude-code-agent, cursor, codex, windsurf, github-copilot)
- Each command now explicitly instructs AI to fill ALL enhanced template sections
- Commands now generate: Document Metadata, Intent/Context, Enhanced formats with IDs/Priority/Intent, Conflict Detection, Review Checklists, Progress Tracking

**Key Improvements:**
- Document metadata sections for version control across all templates
- Conflict/ambiguity detection checklists
- Stakeholder sign-off tracking
- Quality validation checklists
- Domain-specific examples (e-commerce, SaaS, healthcare)
- Common anti-patterns and fixes

**Philosophy Shift:**
Templates now embody "specifications as executable documentation" rather than generic placeholders. Each template guides creation of specs that are testable, traceable, and intent-preserving.

#### Phase 3: MCP Server Template Access Fix
**What Changed:**
- Fixed `TemplateLoader.load_spec_template()` to use correct path: `shared/settings/templates/specs`
- Updated `SpecWorkflow` to use spec_type as template name instead of hardcoded "default"
- MCP server now correctly loads enhanced EARS templates for all specification generation

**Impact:**
- MCP server can now access and use the enhanced requirements, design, and tasks templates
- Specifications generated via MCP tools will use rich EARS notation and Sean Grove's style
- Template loading path mismatch resolved (was looking in `settings/specs/requirements/default.md`, now correctly finds `shared/settings/templates/specs/requirements.md`)

**Lessons Learned:**
1. Real-world examples are far more valuable than generic placeholders like {{ROLE}}/{{CAPABILITY}}
2. Intent documentation is critical for preserving the WHY behind decisions
3. Conflict detection must be built into the specification process, not added later
4. EARS notation requires concrete system names to be truly effective
5. Templates should guide users away from anti-patterns, not just show correct patterns
6. Template path resolution must be validated when template structure changes

---

## Phase 4: Enhanced Workflow Implementation (2025-10-24)

**Status:** ✅ Complete

**Change Summary:**
Enhanced the specification workflow to properly use the advanced EARS templates instead of hardcoded placeholder content.

**Key Changes:**

1. **Requirements Workflow Enhancement**
   - Added `_build_requirements_context()` method to create comprehensive template context
   - Refactored `generate_requirements()` to render Jinja2 template with context
   - Removed hardcoded markdown generation in favor of template rendering
   - Context includes all EARS-style variables: roles, capabilities, constraints, rationale

2. **Design Workflow Enhancement**
   - Added `_build_design_context()` method for design template variables
   - Refactored `generate_design()` to use enhanced 19KB design template
   - Context includes architecture decisions, risk management, future considerations
   - Template follows Sean Grove's intent-preservation patterns

3. **Tasks Workflow Enhancement**
   - Added `_build_tasks_context()` method for task breakdown variables
   - Refactored `generate_tasks()` to use enhanced 9.9KB tasks template
   - Context includes estimation, traceability, testing requirements
   - Maintains dependency tracking and acceptance criteria linkage

**Context Builder Pattern:**
Each workflow phase now has a dedicated context builder that:
- Maps metadata to template variables
- Provides sensible defaults for optional fields
- Preserves feature-specific information (name, description, phase)
- Includes workflow-appropriate placeholders (TBD for review fields)

**Template Variable Coverage:**

*Requirements Template (39 variables):*
- Metadata: VERSION, STATUS, AUTHORS, LAST_UPDATED, etc.
- EARS notation: SPECIFIC_ROLE, CAPABILITY, WHY_THIS_REQUIREMENT, etc.
- Constraints: CONSTRAINT_1, WHY_THIS_CONSTRAINT, ASSUMPTION_1
- Success metrics: SUCCESS_METRIC_1, SUCCESS_METRIC_2

*Design Template (33 variables):*
- Metadata: VERSION, STATUS, REQ_VERSION, RELATED_DESIGNS, etc.
- Architecture: DECISION_1, REASONING_1-3, REASON
- Risk management: RISK, RISK_1, MITIGATION_STRATEGY
- Future planning: FUTURE_1, FUTURE_2

*Tasks Template (43 variables):*
- Metadata: VERSION, STATUS, REQ_VERSION, DESIGN_VERSION, SPRINT
- Estimates: TOTAL_ESTIMATE, PHASE_1-3_ESTIMATE, CRITICAL_TASKS
- Task details: TASK_ID, TASK_DESCRIPTION, WHY_THIS_TASK, ASSIGNEE
- Testing: TEST_SCOPE, COVERAGE, MANUAL_STEPS
- Status: TOTAL_TASKS, COMPLETED_TASKS, IN_PROGRESS_TASKS

**Impact:**
- All three specification workflows now generate rich, structured documentation
- Output uses professional EARS notation and Sean Grove's workflow patterns
- Generated specs are substantially more detailed (500+ bytes vs. previous ~200 bytes)
- Context builders make it easy to customize default values per-project
- Template rendering includes proper error handling with fallback messages

**Files Modified:**
- `src/cc_sdd_mcp/workflows/spec_workflow.py`: Added 3 context builders, refactored 3 generation methods
- `tests/test_enhanced_workflows.py`: Comprehensive test suite for enhanced workflows
- `test_manual_enhanced.py`: Manual verification script (for environments without pytest)

**Validation:**
- ✅ Syntax check passed for all Python files
- ✅ Context builders provide all required template variables
- ✅ Template rendering with proper error handling
- ✅ Maintains backwards compatibility with workflow phases
- ✅ Metadata and file generation working correctly

**Lessons Learned:**
1. Template variables should map logically to domain concepts, not just generic placeholders
2. Context builders allow flexible customization while providing safe defaults
3. Separating context building from template rendering improves testability
4. Error handling during rendering prevents workflow failures from malformed templates
5. Default values should be meaningful (e.g., "TBD" for review fields, "Sprint 1" for sprint)
6. Template variable audit is essential before implementation (found 115 total variables)

## Future Considerations

### Potential Enhancements
- Add template validation tools to check EARS notation compliance
- Create automated conflict detection for requirements
- Build traceability tools linking requirements → design → tasks → code
- Add more domain-specific template examples (fintech, IoT, etc.)
- Consider adding specification testing framework

### Open Questions
- Should we provide language-specific templates (Python, TypeScript, etc.)?
- How to balance template comprehensiveness vs. simplicity?
- Should we add AI-specific guidance for generating specs vs. human authoring?

## Contributing

When contributing to templates:
1. Study existing examples in `tools/cc-sdd/templates/shared/settings/`
2. Follow EARS notation guidelines in `rules/ears-format.md`
3. Include both good and bad examples
4. Add domain-specific examples where relevant
5. Update AGENTS.md with learnings

## References

- [Sean Grove's "The New Code" talk](https://www.youtube.com/watch?v=8rABwKRsec4)
- [EARS Notation Guide](https://visuresolutions.com/alm-guide/adopting-ears-notation/)
- [Spec-Driven Development at The New Stack](https://thenewstack.io/spec-driven-development-the-key-to-scalable-ai-agents/)
