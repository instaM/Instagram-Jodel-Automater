import sqlite3
class DBWrapper:
    def __init__(self,dbname):
        self.conn = sqlite3.connect(dbname)
        c = self.conn.cursor()
        try:
            c.execute('''CREATE TABLE posts (post varchar(1000), votes int, city varchar(255),color varchar(255),used int)''')
            self.conn.commit()
        except:
            return
    def addTop(self,text, votes,color,city):
        c = self.conn.cursor()
        c.execute("Select count(*) from posts where post = ? AND city = ?",(text,city))
        #print(c.fetchone())
        if c.fetchone() == (0,):
            c.execute("INSERT INTO posts(post,votes,city,color,used) values (?,?,?,?,0)", (text, votes, city,color))
        else:
            c.execute("UPDATE posts SET votes = ? where post = ? AND city = ? ",(votes,text,city))

        self.conn.commit()
    def getTop(self,used = False): #
        c = self.conn.cursor()
        if used == True:
            c.execute("SELECT post, votes, city, color used From posts where votes = (SELECT Max(votes) from posts)")
        else:
            c.execute("SELECT post, votes, city, color used From posts where votes = (SELECT Max(votes) from posts where used = 0) AND used = 0")
        temp = c.fetchone()
        if temp is not None:
            c.execute("UPDATE posts SET used = 1 where post = ? ",(temp[0],))
            self.conn.commit()
        return temp
