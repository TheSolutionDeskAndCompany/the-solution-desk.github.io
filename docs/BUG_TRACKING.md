# Bug Tracking System

This document serves as a centralized log for tracking bugs identified during development and testing of The Solution Desk application. All team members should use this format when reporting issues.

## How to Use This Bug Log

1. Add new bugs to the bottom of the appropriate section based on severity
2. Update status as bugs progress through the workflow
3. Include PR/commit references when fixes are implemented
4. Move fixed bugs to the "Resolved Issues" section after verification

## Current Open Issues

### Critical (Blocking/Data Loss/Security)

| ID | Description | Steps to Reproduce | Environment | Reported By | Assigned To | Status | Date Reported |
|----|-------------|-------------------|------------|-------------|------------|--------|--------------|
| C-001 | *Example:* User authentication bypass | 1. Navigate to login page<br>2. Enter any email with admin@<br>3. Submit without password | Chrome 119.0 | | | Open | YYYY-MM-DD |

### High (Feature Breaking/Major UI)

| ID | Description | Steps to Reproduce | Environment | Reported By | Assigned To | Status | Date Reported |
|----|-------------|-------------------|------------|-------------|------------|--------|--------------|
| H-001 | *Example:* Projects not appearing in dashboard | 1. Create new project<br>2. Navigate to dashboard<br>3. Project is missing | All browsers | | | Open | YYYY-MM-DD |

### Medium (Functional Issues/Minor UI)

| ID | Description | Steps to Reproduce | Environment | Reported By | Assigned To | Status | Date Reported |
|----|-------------|-------------------|------------|-------------|------------|--------|--------------|
| M-001 | *Example:* Sort order of ideas list resets after page refresh | 1. Go to ideas list<br>2. Sort by priority<br>3. Refresh page | All browsers | | | Open | YYYY-MM-DD |

### Low (Cosmetic/Enhancement)

| ID | Description | Steps to Reproduce | Environment | Reported By | Assigned To | Status | Date Reported |
|----|-------------|-------------------|------------|-------------|------------|--------|--------------|
| L-001 | *Example:* Button text alignment issue in Firefox | 1. View any form<br>2. Look at submit button | Firefox 118.0 | | | Open | YYYY-MM-DD |

## Resolved Issues

| ID | Description | Environment | Fixed By | PR/Commit | Resolution | Date Closed |
|----|-------------|------------|----------|-----------|------------|------------|
| C-999 | *Example:* Password reset email not sending | All | @developer | #123 | Fixed SMTP configuration | YYYY-MM-DD |

## Status Definitions

- **Open**: Bug reported, not yet assigned
- **In Progress**: Bug assigned and being worked on
- **Ready for Review**: Fix implemented and awaiting code review
- **In Testing**: Fix merged to development and under QA
- **Resolved**: Fix verified and closed
- **Deferred**: Will not be fixed in current release
- **Won't Fix**: Not considered a bug or not worth fixing
- **Duplicate**: Duplicate of another reported issue

## Severity Definitions

- **Critical**: System crash, data loss, security breach, complete feature failure
- **High**: Major functionality broken, significant impact on user experience
- **Medium**: Feature doesn't work as intended but has workarounds
- **Low**: Cosmetic issues, minor inconveniences

## Testing and Verification Process

1. Developer implements fix on a feature branch
2. Developer runs tests and verifies the fix
3. PR is created and reviewed
4. Fix is merged to development branch
5. QA tests the fix following the original reproduction steps
6. If verified, bug is marked as Resolved
7. If not fixed, bug is reopened with additional details

## Integration with CI/CD

The bug tracking system integrates with our CI/CD pipeline as follows:

1. Bug IDs should be referenced in commit messages
2. PR descriptions should link to the corresponding bug report
3. Automated tests should be added to prevent regression
4. Coverage reports should verify that the fix is properly tested

This centralized tracking system ensures all team members have visibility into known issues and their status, promoting accountability and efficient resolution of bugs.
