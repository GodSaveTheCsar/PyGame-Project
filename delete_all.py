import sqlite3


con = sqlite3.connect("data/equations.db")
cur = con.cursor()
cur.execute('''DELETE FROM primeri''')
con.commit()