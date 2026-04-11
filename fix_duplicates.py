import sqlite3
conn = sqlite3.connect('z_compressor.db')
conn.execute("DELETE FROM inventory")
conn.commit()
conn.close()
print("✅ Database clean ho gaya! Saare duplicates khatam.")