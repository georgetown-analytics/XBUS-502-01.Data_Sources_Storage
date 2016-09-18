# sqljoins.py

# SQL Joins

"""
In sql, a JOIN is a means for combining fields from two tables by using values common to each.
More resources:
- [Tutorials point](http://www.tutorialspoint.com/sql/sql-using-joins.htm)
- [W3 schools](http://www.w3schools.com/sql/sql_join.asp)
- [A visual explanation of sql joins](http://blog.codinghorror.com/a-visual-explanation-of-sql-joins/)


![SQL Joins](figures/sqljoins.jpg)
"""

import sqlite3

DBPATH = 'superheroes.db'
conn = sqlite3.connect(DBPATH)

cursor = conn.cursor()

sql = (
    "CREATE TABLE IF NOT EXISTS Superheroes ("
    "    id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "    name TEXT NOT NULL"
    ")"
)

cursor.execute(sql)

sql = "INSERT INTO Superheroes (name) VALUES (?)"
cursor.execute(sql, ("Iron Man",))
cursor.execute(sql, ("Ant-Man",))
cursor.execute(sql, ("Deadpool",))
cursor.execute(sql, ("Black Widow",))
cursor.execute(sql, ("Captain America",))
cursor.execute(sql, ("Hawkeye",))
cursor.execute(sql, ("Hulk",))
cursor.execute(sql, ("Starlord",))
conn.commit()

sql = (
    "CREATE TABLE IF NOT EXISTS Movies ("
    "    id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "    title TEXT NOT NULL,"
    "    superhero_id INTEGER"
    ")"
)

cursor.execute(sql)

sql = "INSERT INTO Movies (title, superhero_id) VALUES (?,?)"
cursor.execute(sql, ("Iron Man", 1))
cursor.execute(sql, ("Iron Man 2", 1))
cursor.execute(sql, ("Iron Man 3", 1))
cursor.execute(sql, ("Guardians of the Galaxy", 8))
cursor.execute(sql, ("Ant-Man", 2))
cursor.execute(sql, ("Deadpool", 3))
cursor.execute(sql, ("The Incredible Hulk", 7))
cursor.execute(sql, ("Captain America: The First Avenger", 5))

conn.commit()

sql = (
    "CREATE TABLE IF NOT EXISTS RealNames ("
    "    id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "    name TEXT NOT NULL,"
    "    superhero_id INTEGER"
    ")"
)

cursor.execute(sql)

sql = "INSERT INTO RealNames (name, superhero_id) VALUES (?,?)"
cursor.execute(sql, ("Tony Stark", 1))
cursor.execute(sql, ("Bruce Banner", 7 ))
cursor.execute(sql, ("Natasha Romanov", 4))
cursor.execute(sql, ("Scott Lang", 2))
cursor.execute(sql, ("Hank Pym", 2))
cursor.execute(sql, ("Steve Rogers", 5))
cursor.execute(sql, ("Clint Barton", 6))
cursor.execute(sql, ("Wade Wilson", 3))
cursor.execute(sql, ("Peter Quill", 8))
cursor.execute(sql, ("Nick Fury", "NULL"))

conn.commit()


cursor.execute("SELECT id FROM RealNames WHERE name=?", ("Peter Quill",))
print cursor.fetchone()

cursor.execute("SELECT name FROM Superheroes WHERE id=?", (1,))
print cursor.fetchone()

cursor.execute("SELECT title FROM Movies WHERE superhero_id=?", (1,))
print cursor.fetchone()
print cursor.fetchone()
print cursor.fetchone()
