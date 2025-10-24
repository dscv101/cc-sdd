# EARS Format Guidelines

> **"Requirements must be precise enough to compile into tests, documentation, and evaluations."** - Inspired by Sean Grove's spec-driven development philosophy

## Overview
EARS (Easy Approach to Requirements Syntax) is the standard format for acceptance criteria in spec-driven development. It creates **executable specifications** that are:
- **Unambiguous**: Clear pass/fail conditions
- **Testable**: Can be automated or manually verified
- **Traceable**: Links to design and implementation
- **Intent-Preserving**: Documents the WHY alongside the WHAT

## Primary EARS Patterns

### 1. Event-Driven Requirements (WHEN-THEN)
**Pattern**: WHEN [specific event/action] THEN [concrete system name] SHALL [measurable response]

**Use Case**: Responses to specific user actions, system events, or triggers

**Good Examples:**
- WHEN user submits payment form THEN Payment Service SHALL validate all fields within 200ms and return field-specific error messages for any invalid inputs
- WHEN API request exceeds 5MB THEN API Gateway SHALL reject request with 413 status code and log attempt
- WHEN user uploads avatar THEN Media Service SHALL resize image to 512x512px and store in CDN within 3 seconds

**Bad Examples (and why):**
- ❌ WHEN user submits form THEN the system SHALL validate it
  - Too vague: Which form? What validation? What's "the system"?
- ❌ WHEN payment happens THEN process it quickly
  - Not testable: What's "quickly"? What does "process" mean?

**Intent Documentation:**
Always add why this behavior exists for non-obvious requirements:
```markdown
- WHEN user submits payment form THEN Payment Service SHALL validate all fields within 200ms
  **Intent:** 200ms SLA ensures responsive UX (users abandon after 3s). Field-specific errors enable inline validation UX.
```

### 2. State-Based Requirements (IF-THEN)
**Pattern**: IF [specific state/precondition] THEN [system] SHALL [response]

**Use Case**: Behavior dependent on system state, preconditions, or business rules

**Good Examples:**
- IF user balance is insufficient THEN Payment Service SHALL reject transaction and suggest minimum top-up amount required
- IF feature flag "new-checkout" is disabled THEN Router Service SHALL redirect users to legacy checkout flow
- IF user has not verified email THEN Profile Service SHALL display verification banner and restrict access to premium features

**Bad Examples:**
- ❌ IF there's a problem THEN show an error
  - Vague: What problem? What error?
- ❌ IF user is premium THEN give them access
  - Missing: Access to what specifically?

**Negative Requirements (SHALL NOT):**
Use for explicit constraints and security requirements:
- IF user is not authenticated THEN API Gateway SHALL NOT return any user data and SHALL respond with 401 status
- IF credit card number is stored THEN Database Layer SHALL NOT log the full number in any log files

### 3. Continuous Behavior (WHILE-THE)
**Pattern**: WHILE [ongoing condition] THE [system] SHALL [continuous behavior]

**Use Case**: Ongoing behaviors that persist during a condition, real-time updates, monitoring

**Good Examples:**
- WHILE file upload is in progress THE Upload Service SHALL broadcast progress updates via WebSocket every 500ms
- WHILE user session is active THE Auth Service SHALL refresh access token 5 minutes before expiration
- WHILE background job is running THE Worker Service SHALL update job status in database every 10 seconds

**Bad Examples:**
- ❌ WHILE processing THEN show status
  - Not a continuous behavior pattern; use WHEN instead
- ❌ WHILE system is on THE system SHALL work
  - Too vague to be useful

### 4. Contextual Requirements (WHERE-THE)
**Pattern**: WHERE [location/context/mode] THE [system] SHALL [contextual behavior]

**Use Case**: Location-specific requirements, context-dependent behavior, mode-specific rules

**Good Examples:**
- WHERE user is on checkout page THE Payment Service SHALL encrypt all form data using TLS 1.3 before transmission
- WHERE request originates from EU region THE Data Service SHALL store data in EU-West datacenter per GDPR requirements
- WHERE system is in maintenance mode THE API Gateway SHALL return 503 status with estimated recovery time

**Bad Examples:**
- ❌ WHERE user is logged in THE system SHALL work
  - Not contextual; use IF for state-based requirements
- ❌ WHERE it's important THE system SHALL be secure
  - "Important" is not a testable context

## Combined Patterns

### Complex Event Conditions (WHEN...AND...THEN)
For requirements with multiple triggering conditions:

**Pattern**: WHEN [event] AND [condition1] AND [condition2] THEN [system] SHALL [response]

**Examples:**
- WHEN payment fails AND retry count < 3 AND error is retryable THEN Payment Service SHALL automatically retry after exponential backoff (2s, 4s, 8s)
- WHEN user clicks delete AND item is not in use AND user confirms action THEN Item Service SHALL permanently delete item and emit deletion event

### Complex State Conditions (IF...AND...THEN)
For requirements with multiple state checks:

**Pattern**: IF [condition1] AND [condition2] THEN [system] SHALL [response]

**Examples:**
- IF user is authenticated AND has "admin" role AND feature flag is enabled THEN Admin Panel SHALL display advanced settings section
- IF request size exceeds 10MB AND user is on free plan THEN Upload Service SHALL reject upload with upgrade suggestion

## Subject Selection Guidelines

> **Critical**: Always use **concrete, specific names**, never generic placeholders like "the system" or "the application"

| Project Type | Subject Examples | Anti-Patterns |
|-------------|------------------|---------------|
| **Software/SaaS** | Payment Service, Auth Module, Email Worker, API Gateway | ❌ "the system", "the app", "backend" |
| **Microservices** | User Service, Order Service, Notification Service | ❌ "service A", "the microservice" |
| **Process/Workflow** | Support Team, Review Process, Approval Workflow | ❌ "the team", "the process" |
| **Infrastructure** | Load Balancer, Redis Cache, PostgreSQL Database | ❌ "the cache", "the database" |

**Why This Matters:**
- Code is a "lossy projection" of specs (Sean Grove). Specific subjects preserve implementation intent.
- Generic subjects create ambiguity about component boundaries
- Concrete names enable automated requirement→code traceability

## Quality Criteria Checklist

Before accepting an EARS requirement, verify:

**Precision:**
- [ ] Subject is a concrete system/service name (not "the system")
- [ ] Response includes specific, measurable behavior (numbers, limits, outputs)
- [ ] Event/condition is observable and testable
- [ ] No ambiguous terms ("fast", "user-friendly", "robust", "scalable" without metrics)

**Testability:**
- [ ] Clear pass/fail conditions
- [ ] Automated test can be written to validate this requirement
- [ ] Manual validation steps are obvious

**Atomicity:**
- [ ] One behavior per statement
- [ ] Not hiding multiple requirements in a single EARS statement
- [ ] Dependencies between requirements are explicit

**Traceability:**
- [ ] Links to specific requirement IDs
- [ ] Maps to specific design components
- [ ] Intent documented for non-obvious behaviors

**Modal Verbs:**
- Use **SHALL** for mandatory requirements (99% of requirements)
- Use **SHOULD** for recommended but not critical requirements
- Use **MAY** for optional capabilities
- Use **SHALL NOT** for explicit prohibitions

## Common Anti-Patterns and Fixes

| ❌ Anti-Pattern | ✅ Corrected Version | Why It's Better |
|----------------|---------------------|-----------------|
| WHEN user saves THEN the system SHALL save it | WHEN user clicks "Save" button THEN Profile Service SHALL persist changes to PostgreSQL within 500ms and display success confirmation | Specific action, system, response, and timing |
| IF error occurs THEN show error | IF API returns 500 error THEN Error Handler SHALL display user-friendly message "Service temporarily unavailable" and log full error with request ID | Specific condition, system, and detailed response |
| WHILE loading THEN show spinner | WHILE data fetch is in progress THE UI Component SHALL display animated spinner and disable form submission | Specific condition, component, and complete behavior |
| The system SHALL be secure | WHERE user password is transmitted THE Auth Service SHALL use TLS 1.3 encryption AND SHALL hash passwords with bcrypt (work factor 12) before storage | Specific context, system, and measurable security controls |

## Intent Documentation Pattern

For complex or non-obvious requirements, always document intent:

```markdown
**Requirement 1.2:** WHEN user deletes account THEN User Service SHALL soft-delete user record, anonymize PII, and schedule permanent deletion after 30 days

**Intent:** 30-day retention allows account recovery (REQ-1.1) while complying with GDPR "right to erasure" timelines. Soft delete prevents cascade failures in related services.
```

## Examples by Domain

### E-Commerce
```markdown
- WHEN user adds item to cart THEN Cart Service SHALL update cart total within 100ms and persist cart to Redis with 24-hour TTL
- IF cart total exceeds $1000 THEN Checkout Service SHALL require billing address verification and fraud check before payment
- WHILE payment is processing THE Checkout Service SHALL poll payment provider every 2 seconds for up to 30 seconds
- WHERE user is in EU region THE Price Service SHALL display prices in EUR including VAT per EU tax regulations
```

### SaaS Platform
```markdown
- WHEN free trial expires AND user has not upgraded THEN Subscription Service SHALL downgrade account to read-only mode and email upgrade reminder
- IF workspace has 10+ members THEN Admin Panel SHALL enforce SSO requirement per enterprise security policy
- WHILE file sync is in progress THE Sync Service SHALL display live progress bar and allow user cancellation
- WHERE API rate limit is exceeded THE API Gateway SHALL return 429 status with Retry-After header
```

### Healthcare System
```markdown
- WHEN patient data is accessed THEN Audit Service SHALL log user ID, timestamp, data accessed, and access reason per HIPAA requirements
- IF prescription has drug interaction THEN Prescription System SHALL block submission and display interaction warning with severity level
- WHILE patient is in examination room THE Monitor Service SHALL capture vitals every 30 seconds and alert if values exceed safe thresholds
- WHERE data contains PHI THE Storage Service SHALL encrypt at rest using AES-256 and encrypt in transit using TLS 1.3 per HIPAA Security Rule
```

---

**Remember**: EARS requirements are the foundation of executable specifications. They should be precise enough to compile into automated tests, clear enough for non-technical stakeholders to review, and detailed enough to guide implementation without ambiguity.
