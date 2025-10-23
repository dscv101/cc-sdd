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

### PR #7: Template Enhancement (2025-10-23)
**What Changed:**
- Enhanced `requirements.md` with intent preservation, conflict detection, rich EARS examples
- Added "Intent Preservation and Design Rationale" section to `design.md`
- Added "Ambiguity Detection and Open Questions" section to `design.md`
- Completely restructured `tasks.md` with detailed traceability and validation criteria
- Significantly expanded `ears-format.md` with domain examples and anti-patterns

**Key Improvements:**
- Document metadata sections for version control across all templates
- Conflict/ambiguity detection checklists
- Stakeholder sign-off tracking
- Quality validation checklists
- Domain-specific examples (e-commerce, SaaS, healthcare)
- Common anti-patterns and fixes

**Philosophy Shift:**
Templates now embody "specifications as executable documentation" rather than generic placeholders. Each template guides creation of specs that are testable, traceable, and intent-preserving.

**Lessons Learned:**
1. Real-world examples are far more valuable than generic placeholders like {{ROLE}}/{{CAPABILITY}}
2. Intent documentation is critical for preserving the WHY behind decisions
3. Conflict detection must be built into the specification process, not added later
4. EARS notation requires concrete system names to be truly effective
5. Templates should guide users away from anti-patterns, not just show correct patterns

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

