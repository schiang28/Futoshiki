import sqlite3

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute(
    """CREATE TABLE users (
                username text,
                password text,
                games integer
                )"""
)

conn.commit()
test = "hi"
currentuser = cursor.execute("""SELECT * FROM users WHERE username=?""", (test,),)

print(currentuser.fetchall())
