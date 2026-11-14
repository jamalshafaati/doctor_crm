# Architecture Notes

## Modular Monolith

Each domain lives in its own Django app under `apps/`.

Business logic → `services/`
Queries → can be extended with `selectors/` later
Views stay thin (forms + call service + render)

## Roles

- doctor / admin → full clinical access
- receptionist → patients + appointments + check-in only
- patient → portal only (Phase 7)

## Encounter Lifecycle

Draft → In Progress → Pending Review → Finalized
Finalized records are locked.
Amendments create a new versioned row with reason + actor + timestamp.

## Dates

Stored as Gregorian (DateTimeField / DateField) in the database.
Display layer will convert to Jalali when LANGUAGE_CODE == 'fa'.
