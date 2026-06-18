import sqlite3

conn = sqlite3.connect(
    "data/db/mediassist.db"
)

cursor = conn.cursor()

print("\nCLAIMS\n")

cursor.execute(
    "SELECT * FROM claims LIMIT 5"
)

for row in cursor.fetchall():
    print(row)

print("\nMAINTENANCE\n")

cursor.execute(
    "SELECT * FROM maintenance_tickets LIMIT 5"
)

for row in cursor.fetchall():
    print(row)

conn.close()