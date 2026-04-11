import sqlite3
conn = sqlite3.connect('z_compressor.db')
cursor = conn.cursor()

# Saara data delete karne ki command
cursor.execute("DELETE FROM inventory")

conn.commit()
conn.close()
print("✅ Database ekdum saaf! Saare 'Not Specified' products delete ho gaye.")