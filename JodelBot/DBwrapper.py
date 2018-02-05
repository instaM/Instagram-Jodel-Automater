import sqlite3
class DBWrapper:
    def __init__(self,dbname):
        self.conn = sqlite3.connect(dbname)
        c = self.conn.cursor()
        #c.execute('''CREATE TABLE posts (post varchar(1000), votes int, city varchar(255),used int)''')


        print(c.fetchone())
    def addTop(self,text, votes,city):
        c = self.conn.cursor()
        c.execute("Select count(*) from posts where post = ? AND city = ?",(text,city))
        #print(c.fetchone())
        if c.fetchone() == (0,):
            c.execute("INSERT INTO posts(post,votes,city,used) values (?,?,?,0)", (text, votes, city))
        else:
            c.execute("UPDATE posts SET votes = ? where post = ? AND city = ? ",(votes,text,city))

        self.conn.commit()
    def getTop(self,used = False): #
        c = self.conn.cursor()
        c.execute("SELECT post, votes, city, used From posts where votes = (SELECT Max(votes) from posts where used = ?) AND used = ? ",(int(used),int(used)))
        temp = c.fetchall()
        c.execute("UPDATE posts SET used = 1 where votes = (SELECT Max(votes) from posts) ")
        self.conn.commit()
        return temp