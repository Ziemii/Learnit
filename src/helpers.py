import sqlite3

conn = sqlite3.connect('database/learn!t.db')
cur = conn.cursor();
for row in cur.execute('SELECT * FROM users;'):
        print(row)
