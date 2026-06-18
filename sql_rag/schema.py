
DATABASE_SCHEMA = """
TABLE: claims

Columns:
- claim_id (TEXT)
- patient_id (TEXT)
- patient_name (TEXT)
- department (TEXT)
- claim_type (TEXT)
- diagnosis_code (TEXT)
- insurer (TEXT)
- claimed_amount (REAL)
- approved_amount (REAL)
- status (TEXT)
- submitted_date (TEXT)
- resolved_date (TEXT)

Possible status values:
- pending
- approved
- rejected


TABLE: maintenance_tickets

Columns:
- ticket_id (TEXT)
- equipment_name (TEXT)
- equipment_id (TEXT)
- category (TEXT)
- campus (TEXT)
- issue_type (TEXT)
- fault_code (TEXT)
- raised_by (TEXT)
- raised_date (TEXT)
- resolved_date (TEXT)
- status (TEXT)
- resolution_note (TEXT)

Possible status values:
- resolved
- in_progress
- escalated
"""