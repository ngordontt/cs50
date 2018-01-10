import sqlite3
from passlib.context import CryptContext


#setup established hasing scheme
myctx = CryptContext(schemes=["sha256_crypt"])


conn = sqlite3.connect('finance.db')
db = conn.cursor()


# query database for username
username = "my"
db.execute('''SELECT * FROM users WHERE username=?''', (username,))
rows = db.fetchone()
# print(rows)

hash1 = myctx.hash("my")
# print(hash1)

myctx.verify("my", hash1)

# ensure username exists and password is correct
hash_tb = rows[2]


if not myctx.verify("mt", hash_tb):
    print("invalid")

# print(rows[2])

# close database connection    
conn.close()