import sqlite3

conn = sqlite3.connect("finance.db")
c = conn.cursor()

# Remove duplicate categories, keeping only unique ones
c.execute("""
    DELETE FROM categories 
    WHERE id NOT IN (
        SELECT MIN(id) FROM categories GROUP BY type, name
    );
""")

conn.commit()
conn.close()

print("Duplicate categories removed successfully!")
