import sqlite3


conn = sqlite3.connect('assets/PyProject.db')
cursor = conn.cursor()

conn.execute("ALTER TABLE Users ADD COLUMN avatar VARCHAR(255)")
