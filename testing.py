import urllib
from urllib.request import urlopen
import sqlite3

conn = sqlite3.connect('assets/PyProject.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM items")
rows = cursor.fetchall()
inc = 0
for row in rows:
    print(f'{row[1]} in progress #:{inc}')
    resource = urlopen(row[4])
    filename = "images/"+ row[1] + '.jpg'
    cursor.execute(f"UPDATE items SET image='{filename}' WHERE id={row[0]}")
    output = open(filename, "wb")
    output.write(resource.read())
    output.close()
    inc += 1
    conn.commit()
    print(f'{row[1]} finished')

