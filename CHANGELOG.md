# Changelog

## v0.2.0 - SQLAlchemy queue and audit trail

- Added SQLAlchemy models for tickets, rules, queue items, actions and history.
- Replaced raw SQLite writes with an ORM-backed workflow.
- Added state-transition audit records for every routed ticket.
- Added architecture docs and focused tests.

## v0.1.0 - Initial public foundation

- Added safe public project structure.
- Added synthetic sample data.
- Added minimal executable demo.
- Added roadmap, security notes and GitHub templates.
