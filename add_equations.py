import sqlite3
import random

con = sqlite3.connect("data/equations.db")
cur = con.cursor()
for i in range(100):
    eq = str(random.randint(1, 500)) + random.choice(['+', '-']) + str(random.randint(1, 499))
    otv = str(eval(eq))
    cur.execute("""INSERT INTO primeri(type, example, answer) VALUES(?, ?, ?)""", ('example', eq, otv))
for i in range(100):
    a = random.choice([random.randint(2, 10), random.randint(-10, -2)])
    b = random.choice([a * random.randint(2, 8), a * random.randint(-8, -2)])
    if b > 0:
        eq = str(a) + 'x' + '+' + str(b) + '=0'
    else:
        eq = str(a) + 'x' + '-' + str(-b) + '=0'
    otv = str(int(-b / a))
    cur.execute("""INSERT INTO primeri(type, example, answer) VALUES(?, ?, ?)""", ('lin_equation', eq, otv))
for i in range(100):
    x1 = random.choice([random.randint(2, 15), random.randint(-15, -2)])
    x2 = random.choice([random.randint(2, 15), random.randint(-15, -2)])
    b = -x1 - x2
    c = x1 * x2
    if b == 0:
        continue
    if b > 0:
        if c > 0:
            eq = 'x**2+' + str(b) + 'x+' + str(c) + '=0'
        else:
            eq = 'x**2+' + str(b) + 'x-' + str(-c) + '=0'
    else:
        if c > 0:
            eq = 'x**2-' + str(-b) + 'x+' + str(c) + '=0'
        else:
            eq = 'x**2-' + str(-b) + 'x-' + str(-c) + '=0'
    otv = str(x1) + ',' + str(x2)
    cur.execute("""INSERT INTO primeri(type, example, answer) VALUES(?, ?, ?)""", ('quad_equation', eq, otv))
con.commit()