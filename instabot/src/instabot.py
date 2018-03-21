#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath(os.path.join(__file__, '..', '..','..', 'apis', 'JodelBot'))
sys.path.append(lib_path)
lib_path = os.path.abspath(os.path.join(__file__, '..', '..','..', 'apis', 'instagramapi_headless'))

sys.path.append(lib_path)
from database import InstaDB
from instagramapi_headless import InstagramAPI
#from JodelBot import JodelBot
from PIL import Image
from instapy_cli.cli import InstapyCli
import random
import time
import signal
import atexit
from datacollector import Collector
class Instabot:
    def __init__(self,
                 username               = "",
                 passwort               = "",
                 post_caption           = "",
                 max_followers_per_hour = 0,
                 max_unfollows_per_hour = 0,
                 max_likes_per_hour     = 0,
                 max_posts_per_day      = 0,
                 max_likes_per_tag      = 1000000,
                 max_likes_per_picture  = 1000000,
                 max_like_newsfeed_per_hour = 0,
                 max_followers_on_follower = 1000000,
                 min_followers_on_follower = 0,
                 blacklist_usertags        = [],
                 tag_list                   = ['hashtag'],
                 time_to_unfollow           = 3 * 60*60*24,
                 days_to_refollow           = 300,
                 chromedriver_path          ='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe'
                 ):
        
        
        self.username                   = username
        self.passwort                   = passwort
        self.post_caption               = post_caption
        self.max_followers_per_hour     = max_followers_per_hour
        self.max_unfollows_per_hour     = max_unfollows_per_hour
        self.max_likes_per_hour         = max_likes_per_hour
        self.max_like_newsfeed_per_hour = max_like_newsfeed_per_hour
        self.max_posts_per_day          = max_posts_per_day
       
        self.time_to_unfollow           = time_to_unfollow
        self.days_to_refollow           = days_to_refollow
        self.like_newsfeed_count        = 0
        self.like_count                 = 0
        self.follow_count               = 0
        self.unfollow_count             = 0
        self.post_count                 = 0
        self.max_likes_per_tag          = max_likes_per_tag
        self.max_likes_per_picture      = max_likes_per_picture
        self.max_followers_on_follower  = max_followers_on_follower
        self.min_followers_on_follower  = min_followers_on_follower
        self.blacklist_usertags         = blacklist_usertags
        self.tag_list                   = tag_list
        
        
        self.period                     = 60*60
        self.max_followers_per_period             = self.max_followers_per_hour * (self.period/(60*60))
        self.max_unfollows_per_period             = self.max_unfollows_per_hour * (self.period/(60*60))
        self.max_likes_per_period                 = self.max_likes_per_hour * (self.period/(60*60))
        self.max_like_newsfeed_per_period         = self.max_like_newsfeed_per_hour * (self.period/(60*60))
        self.between_like               = self.safe_div(self.period,self.max_likes_per_period)
        self.between_like_newsfeed      = self.safe_div(self.period,self.max_like_newsfeed_per_period)
        self.between_follow             = self.safe_div(self.period,self.max_followers_per_period)
        self.between_unfollow           = self.safe_div(self.period,self.max_unfollows_per_period)
        self.between_post               = self.safe_div(60*60*24,self.max_posts_per_day)
        
        self.likes_per_tag_left         = self.init_tags()
        self.period_like_count          = self.max_likes_per_period
        self.period_follow_count        = self.max_followers_per_period
        self.period_unfollow_count      = self.max_unfollows_per_period
        self.period_like_newsfeed_count        = self.max_like_newsfeed_per_period
        self.period_post_count          = self.max_posts_per_day
      
        self.next_iteration             = {"Like": time.time()+(self.between_like/2)-12, "Follow":  0, "Unfollow": time.time()+(self.between_unfollow/2), "Like_NewsFeed": 0,"Post":0}
        self.start_time                 = 0.0
        self.end_time                   = 0.0
        self.day_count                  = 0.0
      
        self.database                   = InstaDB()
        self.collector                  = Collector()
        self.get_post_api               = None
        self.api                        = None
        self.post_instagram_api         = None
        self.chromedriver_path          = chromedriver_path
        
        signal.signal(signal.SIGTERM, self.cleanup)
        atexit.register(self.cleanup)
        
        
        
    def safe_div(self,x,y):
        if y == 0:
            return 0
        return x / y        
    def init_tags(self):
        tag_list_left ={}
        for tag in self.tag_list:
            tag_list_left[tag] = self.max_likes_per_tag
        return tag_list_left
        
    def containsBadKeyWord(self,name):
      
      for bad in self.blacklist_usertags:
        
        if bad in str(name).lower(): 
          return bad
      return None
  
  
    def worthy(self,info):
      try:
        info = info["node"]
        if self.database.check_to_follow(info["owner"]["id"]) == True:
          #print("Media %s and %s soon to be liked and followed!" %(info["pk"],info["user"]["username"]))
          return False
        if info["edge_liked_by"]["count"] > self.max_likes_per_picture:
         # print("Media %s has too many likes" %(info["pk"]))
          return False
        if  self.database.check_following(info["owner"]["id"]):
         # print("You are already following %s" %(info["user"]["username"]))
          return False
        if self.database.check_blacklist_refollow(info["owner"]["id"]) == False:
         # print("You have followed  %s in the last 30 days"%(info["user"]["username"]))
          return False
       
        resp = self.collector.getMediaInfo(info["shortcode"])
      
        bad = self.containsBadKeyWord(resp["graphql"]["shortcode_media"]["owner"]["username"])
        if  bad != None:
          print("%s contains %s !" %  (resp["graphql"]["shortcode_media"]["owner"]["username"],bad))
          
          return False 
        bad = self.containsBadKeyWord(resp["graphql"]["shortcode_media"]["owner"]["full_name"]))
        if  bad != None:
         # print("%s contains %s !" %  (info["user"]["username"],bad))
          print("%s contains %s !" %  (resp["graphql"]["shortcode_media"]["owner"]["username"],bad))
          return False 
          
        resp = self.collector.getUserInfo(resp["graphql"]["shortcode_media"]["owner"]["username"])
        
         
        if resp["user"]["edge_followed_by"]["count"] > self.max_followers_on_follower:
          #print("%s has too many follower" % (info["user"]["username"]))
          return False
        
        if resp["user"]["edge_followed_by"]["count"] < self.min_followers_on_follower:
        #  print("%s has too little follower" % (info["user"]["username"]))
          return False
          
        print("Hier")
        return resp["user"]["username"]
      except:
        return False
      
    def post_picture(self):
        #print(os.path.abspath(os.path.join(__file__)))
        self.get_post_api.scanTopPost(400)
        img = self.get_post_api.getBestImage()
        path = os.path.abspath('') + "/temp.jpg"
        #img[0].show()
        img[0].save(path,quality = 100)
        self.post_instagram_api.upload(path,(self.post_caption  %(img[1])))

    def like_newsfeed(self):
     
      return self.api.likeNewsFeedMedia
  
    def follow(self):
     
      to_follow_list = self.database.get_to_follows(liked=1)
      if(len(to_follow_list) == 0):
        to_follow_list = self.database.get_to_follows()
      if(len(to_follow_list) == 0):
          return False
      
      follower = random.choice(to_follow_list)
      if(self.api.follow(follower[1]) == False):
          self.database.delete_to_follow(follower[0])
          return False
      self.database.insert_follower(follower[0],follower[1],0,time.time() + self.time_to_unfollow,follower[2])
      if(follower[3] == 1):
        self.database.delete_to_follow(follower[0])
      else:
        self.database.update_to_follow(follower[0],followed=1)
        
      print("#%i Follow User %s" %(self.follow_count,follower[1])) 
      
      return True
      
    def unfollow(self):
     
      unfollower_list = self.database.get_unfollows()
      if(len(unfollower_list) == 0):
        return False
      unfollower = random.choice(unfollower_list)
      self.api.unfollow(unfollower[1])
      self.database.delete_follower(unfollower[0])
      self.database.insert_blacklist(unfollower[0],unfollower[1])
      print("#%i unfollow User %s"%(self.unfollow_count,unfollower[1])) 
      
      return True
      
    def like(self):
        to_follow_list = self.database.get_to_follows(followed=1)
        if(len(to_follow_list) == 0):
            to_follow_list = self.database.get_to_follows()
        if(len(to_follow_list) == 0):
            return False
        
        follower = random.choice(to_follow_list)
        if(self.api.likeRandomUserMedia(follower[1]) == False):
            self.database.delete_to_follow(follower[0])
            return False
        self.database.insert_follower(follower[0],follower[1],0,time.time() + self.time_to_unfollow,follower[2])
        if(follower[4] == 1):
            self.database.delete_to_follow(follower[0])
        else:
            self.database.update_to_follow(follower[0],liked=1)
        print("#%i Liked Random User Media %s" %(self.like_count,follower[1]))     
        return True
    def get_random_tag(self,tag_list):
      return random.choice(tag_list)
  
    def login(self):
      self.api = InstagramAPI(self.username,self.passwort,self.chromedriver_path)
      self.api.login()
      self.database.connect()
      
     # time.sleep(random.randint(15, 30))

      self.post_instagram_api= InstapyCli(self.username,self.passwort)
    def reset_period_counter(self):
      print ("This time period #%i Media got liked"      %(self.max_likes_per_period-self.period_like_count))
      print ("This time period #%i Accounts got followed"%(self.max_followers_per_period-self.period_follow_count))
      print ("This time period #%i Accounts got followed"%(self.max_unfollows_per_period-self.period_unfollow_count))
      self.period_like_count          = self.max_likes_per_period
      self.period_follow_count        = self.max_followers_per_period
      self.period_unfollow_count      = self.max_unfollows_per_period
      self.period_like_newsfeed_count = self.max_like_newsfeed_per_period
    def run(self):
        self.login()
        self.start_time = time.time()
        self.end_time   = self.start_time + self.period
        self.day_count  = self.start_time + 60*60*24
        period_count    = 0
        tag_feed = {}
        tag_list = self.tag_list[:]
        tag = ""
        print("Follow every %i seconds"% (self.between_follow))
        print("Unfollow every %i seconds"% (self.between_unfollow))
        print("Like every %i seconds"% (self.between_like))
        print("Like NewsFeed every %i seconds"% (self.between_like_newsfeed))
        print("Post every %i seconds"% (self.between_post))
        while True:
          if(time.time() > self.day_count):
              self.period_post_count = self.max_posts_per_day
              self.day_count = time.time() + 60*60*24
          if(time.time() > self.end_time):
            self.reset_period_counter()
            self.end_time = time.time()+self.period
            period_count += 1
          if len(tag_feed) == 0:
            if len(tag_list) == 0:
              tag_list = self.tag_list[:]
              
            tag = self.get_random_tag(tag_list)
            del tag_list[tag_list.index(tag)]
            print("Now search on #%s"%(tag))
            print("Available Likes #%i"%(self.likes_per_tag_left[tag]))
            tag_feed = self.collector.getHashtagFeed(tag,3)
          
          if (len(tag_feed) > 0  and self.database.get_to_follow_count() < 30 ):
            username = self.worthy(tag_feed[0])
            if (username != False):
              self.database.insert_to_follow(tag_feed[0]["node"]["owner"]["id"],username,tag)
            del tag_feed[0]
          
          if time.time() > self.next_iteration["Post"] and self.period_post_count > 0:
              self.post_picture()
              print("Posted picture!")
              self.next_iteration["Post"] = time.time() + self.between_post 
              
          if time.time() > self.next_iteration["Like_NewsFeed"] and self.period_like_newsfeed_count > 0 and self.like_newsfeed():
            print("#%i Liked NewsFeed" %(self.like_newsfeed_count))
            self.like_newsfeed_count += 1
            self.period_like_newsfeed_count -=1
            self.next_iteration["Like_NewsFeed"] = time.time() + self.between_like_newsfeed 
            #time.sleep(random.randint(3, 20))

          if time.time() > self.next_iteration["Follow"] and self.period_follow_count > 0 and self.follow():
            self.follow_count += 1
            self.period_follow_count -= 1
            self.next_iteration["Follow"] = time.time() + self.between_follow
            print("Period Count : #%s"%(period_count))
            #time.sleep(random.randint(7, 20))
          if time.time() > self.next_iteration["Like"] and self.period_like_count > 0 and self.like():
            self.like_count += 1
            self.period_like_count -= 1
            self.next_iteration["Like"] = time.time() + self.between_like
           
            #time.sleep(random.randint(7, 20))  
          if time.time() > self.next_iteration["Unfollow"] and self.period_unfollow_count > 0 and self.unfollow():  
            self.unfollow_count += 1
            self.period_unfollow_count -= 1
            self.next_iteration["Unfollow"] = time.time() + self.between_unfollow
            #time.sleep(random.randint(7, 20))
          time.sleep(3) 
         
       
    def cleanup(self):
      self.database.disconnect()
      self.api.logout()
