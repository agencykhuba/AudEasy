# Standard Operating Guidelines
**Comprehensive Framework for Project Collaboration and Quality Assurance**

## Core Principles

### Quality Over Speed Always (QOSA) Framework
**Definition**: QOSA prioritizes systematic analysis, thorough verification, and sustainable solutions over rapid execution that may introduce errors or technical debt.

**QOSA Score (0-100)**:
- Systematic analysis completion (+20 points)
- Historical context verification (+15 points)
- Pre-execution validation (+15 points)
- Root cause identification (+20 points)
- Complete documentation (+10 points)
- Successful implementation (+20 points)

## Process And Damage Control (PDC) Framework

### PDC Methodology
**Requirement**: For all critical fixes or changes, conduct PDC assessment before and after modifications.

### PDC Assessment Components
1. **Git History Analysis**: Review recent commits for potential damage patterns
2. **File Integrity Check**: Validate syntax and structure of critical files
3. **Last Working State Identification**: Locate safe rollback points
4. **Recovery Options Generation**: Provide multiple paths forward with risk assessment

### PDC Implementation Triggers
- Syntax errors in production
- Failed deployments
- Multiple rapid commits without validation
- Emergency fixes that may have introduced new problems

## Fallback Framework (FF) Protocol

### FF Mandatory Requirements
**Before ANY file modification, deletion, or update**: Execute FF evaluation and backup procedure.

### FF File Importance Classification
**CRITICAL**: Core application files (code/app.py, requirements.txt, database schemas)
**IMPORTANT**: Configuration files (.py, .sql, .yml, Dockerfile)
**SUPPORTING**: Documentation files (.md, .txt, .html)

## Windows Environment Standards

### Environment Constants
**Development Environment**: Windows + VS Code + Git Bash
**Encoding Requirements**: UTF-8 with BOM handling
**Terminal Compatibility**: Git Bash heredoc limitations

### Code Block Standards
**Mandatory Requirements**:
- No emojis or Unicode characters in heredoc blocks
- Use ASCII characters only in code templates
- Validate syntax immediately after file creation
- Test all heredoc operations in Git Bash environment

## Communication Standards

### Command Block Requirements
1. **Directory Navigation**: Every code block must begin with correct directory path
2. **Complete Copy-Paste Blocks**: No fragmented commands
3. **Pre-Execution Validation**: Simulate command execution before providing
4. **Clear Objectives**: State purpose and expected outcome

### Prohibited Communication Patterns
- Fragmented commands (incomplete cat statements, missing EOF terminators)
- Ambiguous instructions (immediately run, quickly execute)
- Assumption-based guidance (solutions without systematic verification)
- Directory omission (code blocks without explicit navigation)

## Combined Framework Implementation Order
1. **FF (Fallback Framework)**: Backup critical files
2. **PDC (Process and Damage Control)**: Assess current state and damage
3. **BSA (Best Solution Analysis)**: Determine optimal implementation route
4. **Execute**: Implement solution with continuous monitoring
5. **Validate**: Confirm successful implementation and document lessons learned

## Quality Assurance Protocols

### Root Cause Analysis (5 Whys) Framework
**Process**:
1. Problem Statement: Clear description of the observed issue
2. Why 1: Immediate cause identification
3. Why 2: Underlying factor analysis
4. Why 3: Systemic issue exploration
5. Why 4: Process or methodology evaluation
6. Why 5: Fundamental root cause identification

### Testing Requirements
1. Unit Testing: Individual component validation
2. Integration Testing: Component interaction verification
3. Environment Testing: Deployment target compatibility
4. User Acceptance Testing: End-user workflow validation
5. Regression Testing: Existing functionality preservation

## Version Control Standards

### Commit Message Format
[Type]: [Brief Description]
- Detailed change 1
- Detailed change 2

**Types**: Fix, Feature, Update, Refactor, Documentation, Test

## Continuous Improvement Framework

### Learning Integration
- Success Factor Analysis: Identify what worked well
- Failure Mode Review: Understand what caused problems
- Process Refinement: Update procedures based on experience
- Knowledge Documentation: Capture insights for future reference

## Conclusion

**Core Commitment**: Quality Over Speed Always (QOSA) - the unwavering principle that guides all project activities toward long-term success and effectiveness.

## ELF Framework (Evidence-Led Fixing)

### Core Principle
Never debug by assumption. Always follow evidence to the root cause.

### The ELF Process

#### E - Evidence Collection (15 minutes maximum)
1. **Read Actual Logs**: Check Render/server logs for exact error messages
2. **Verify Service State**: Confirm what's actually running vs crashed
3. **Document Symptoms**: Record what works vs what fails
4. **Check Recent Changes**: Review git log and environment modifications

#### L - Local Reproduction (10 minutes maximum)
1. **Run Locally**: Test the failing component on development machine
2. **Compare Behavior**: Local failure = code issue, Remote-only failure = environment issue
3. **Isolate Variables**: Test one component at a time
4. **Log Everything**: Add logging to track execution flow

#### F - Fix Systematically (varies)
1. **Apply 5 Whys**: Use existing root cause analysis from SOG
2. **Minimal Change**: Fix ONE thing based on evidence
3. **Test Before Deploy**: Verify fix locally first
4. **Deploy and Verify**: Confirm fix resolves the issue
5. **Document Solution**: Record what worked for future reference

### ELF Anti-Patterns (What NOT to Do)
- Changing multiple things without testing each
- Assuming root cause without reading logs
- Deploying untested fixes
- Skipping local reproduction step
- Ignoring evidence that contradicts assumptions

### ELF Success Criteria
- Issue resolved in under 30 minutes for simple bugs
- Clear understanding of root cause before fixing
- No collateral damage from fixes
- Documented solution for knowledge base

### Integration with Existing SOG Frameworks
- **After PDC**: Use ELF when damage is identified
- **Before BSA**: ELF provides evidence for solution analysis
- **With FF**: ELF guides which backups to examine

### Example: Health Endpoint Debug Session

**Wrong Approach (What We Did):**
1. Assumed credential rotation without evidence
2. Changed database URLs multiple times
3. Did not read actual health endpoint code
4. Spent 2+ hours troubleshooting

**ELF Approach (What We Should Have Done):**
1. E: Read logs, see 500 error on /health
2. E: Check code, grep health endpoint
3. E: Found missing return statement in 2 minutes
4. L: Would have caught this in local testing
5. F: Add return statement, deploy, verify
**Total time: 20 minutes**

### ELF Quick Reference Card
