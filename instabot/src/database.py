import sqlite3
import datetime
import time 
import os
import random
class InstaDB:
  def __init__(self):
    self.blacklist_re = "blacklist_refollow"
    self.following = "following"
    self.to_follow = "to_follow"
    self.all_follow = "all_follow"
    self.to_like = "to_like"
    self.db = os.path.abspath('../db/insta_db.sl3')
    self.con = None 
    self.cur = None
    self.days_to_unfollow = 3
    self.days_to_refollow = 30
  def connect(self):
    self.con = sqlite3.connect(self.db)
    self.cur = self.con.cursor()
    self.cur.execute("CREATE TABLE if not exists blacklist_refollow(uni_id char[50] primary key,name char[50],expire_date DATETIME)")
    self.cur.execute("CREATE TABLE if not exists following(uni_id char[50] primary key,name char[50],whitelist boolean, expire_date date);")
    self.cur.execute("CREATE TABLE if not exists to_follow(uni_id char[50] primary key,name char[50],hashtag char[50],liked boolean, followed boolean);")
    self.cur.execute("CREATE TABLE if not exists all_follow(uni_id char[50] primary key,name char[50],hashtag char[50]);")
    self.con.commit()
  def disconnect(self):
    if(self.con != None):
      self.con.close()
    
  def insert_blacklist(self,uni_id,name):
    
    self.cur.execute("REPLACE INTO %s VALUES('%s','%s','%s')" % (self.blacklist_re,uni_id,name,str(datetime.date.today()+datetime.timedelta(days=self.days_to_refollow ))))
    self.con.commit()
  def insert_follower(self,uni_id,name,whitelist,date,hashtag):
    self.cur.execute("REPLACE INTO %s VALUES('%s','%s',%i,'%s')" % (self.following,uni_id,name,whitelist,str(date)))
    self.cur.execute("REPLACE INTO %s VALUES('%s','%s','%s')" % (self.all_follow,uni_id,name,hashtag))
    self.con.commit()
  def insert_all_follow(self,uni_id,name,hashtag):
    self.cur.execute("INSERT INTO %s VALUES('%s','%s','%s')" % (self.all_follow,uni_id,name,hashtag))
    self.con.commit()
  def insert_to_follow(self,uni_id,name,hashtag):
    self.cur.execute("REPLACE INTO %s VALUES('%s','%s','%s',0,0)" % (self.to_follow,uni_id,name,hashtag))
    self.con.commit()
  def update_to_follow(self,uni_id, followed=0, liked=0):
    self.cur.execute("UPDATE %s SET followed=%i, liked=%i where uni_id=%s" % (self.to_follow,followed,liked,uni_id))
    self.con.commit()
  def check_blacklist_refollow(self,uni_id,never_refollow):
   
    self.cur.execute("SELECT * from %s where uni_id='%s'" % (self.blacklist_re,uni_id))
    row = self.cur.fetchone()
    if not row : return True 
    expire_date = datetime.datetime.strptime(row[2],"%Y-%m-%d").date()
  
    return (expire_date < datetime.date.today()) and not never_refollow
  def check_following(self,uni_id):
   
    self.cur.execute("SELECT * from %s where uni_id='%s'" % (self.following,uni_id))
    row = self.cur.fetchone()
    if not row : return False
   
    return True
  def check_to_follow(self,uni_id):
    self.cur.execute("SELECT * from %s where uni_id='%s'" % (self.to_follow,uni_id))
    row = self.cur.fetchone()
    if not row : return False
   
    return True
  def get_random_user(self):
    self.cur.execute("SELECT * from %s" % (self.following))
    row = self.cur.fetchall()

    return random.choice(row)[1]
  def get_all_follow(self):
    self.cur.execute("SELECT * from %s" % (self.all_follow))
    row = self.cur.fetchall()
    
    return row
  def get_following_all(self):
    self.cur.execute("SELECT * from %s" % (self.following))
    row = self.cur.fetchall()
    
    return row
  def get_to_follows(self,followed = 0, liked=0):
    self.cur.execute("SELECT * from %s where followed=%i and liked=%i limit 20" % (self.to_follow,followed,liked))
    row = self.cur.fetchall()
    
    return row
 
  def get_unfollows(self):
   
    self.cur.execute("SELECT * from %s where whitelist= 0 and expire_date < '%s' order by expire_date limit 20" % (self.following,str(time.time())))
    row = self.cur.fetchall()
    
    return row
  def get_to_follow_count(self):
    self.cur.execute("SELECT count(*) from %s" %(self.to_follow))

    res = self.cur.fetchone()
    return res[0]
  def delete_follower(self,uni_id):
    self.delete(uni_id,self.following)
  
  def delete_to_follow(self,uni_id):
    self.delete(uni_id,self.to_follow)
    
    
  def delete(self, uni_id,table):
    
    self.cur.execute("delete from %s where uni_id='%s'" % (table,uni_id))
    self.con.commit()
    