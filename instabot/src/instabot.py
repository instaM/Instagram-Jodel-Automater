#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath(os.path.join(__file__, '..', '..','..', 'apis', 'JodelBot'))
sys.path.append(lib_path)
lib_path = os.path.abspath(os.path.join(__file__, '..', '..','..', 'apis', 'instagramapi_browser'))

sys.path.append(lib_path)
from database import InstaDB
from instagramapi_browser import InstagramAPI
from JodelBot import JodelBot
from PIL import Image
from instapy_cli.cli import InstapyCli
import random
import time
import signal
import atexit
class Instabot:
    def __init__(self):
        self.username                   = "topdailyjodel"
        self.passwort                   =  "resurrect123"
        self.post_caption               = u"Dein täglicher Jodel!\nFolge @topdailyjodel für lustige Jodel aus ganz Deutschland \n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n#%s#fun #jodel #germany #instajodel #jodelgermany #funnyquote #quote #quoteoftheday #instafun #jodelapp #funny #study #uni #university #student #lifestyle #studentenlifestyle #lustig #sprüche"
        self.max_followers_per_hour     = 0
        self.max_unfollows_per_hour     = 0
        self.max_likes_per_hour         = 1
        self.max_like_newsfeed_per_hour = 0
        self.max_posts_per_day          = 15
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
        
        self.time_to_unfollow           = 3*60*60*24
        self.days_to_refollow           = 30
        self.like_newsfeed_count        = 0
        self.like_count                 = 0
        self.follow_count               = 0
        self.unfollow_count             = 0
        self.max_likes_per_tag          = 100
        self.max_likes_per_picture      = 600
        self.max_followers_on_follower  = 1500
        self.min_followers_on_follower  = 100
        self.blacklist_usertags         = ["alex","lukas","michael","daniel","philipp","jonas","fabian","marcel","tim","kevin","jan","david","tom","markus","sebastian","julian","leon","christoph","simon",
                                            "felix","andreas","nils","nico","***REMOVED***","max","florian","dennis","patrick","thomas","christopher","moritz","nick","chris","paul","jonathan","tobias","jakob","christian",                                            
                                            "adrian","matthias","dominik","stefan","rene","ali","marco","vincent","mohamed","kai","erik","ludwig","hendrik","mario","oliver","lucas","anton","timo","sven","marc","andre",
                                            "gabriel","leo","arthur","maximilian","ben","jannik","niklas","mark","noah","peter","mark","johannes","konrad","alexander","pierre","jason","frank","marvin","till","artur","luca",
                                            "fabio","lasse","jens","konstantin","tamino","william","luis","alihan","ricardo","victor","jeremy","brian","dustin","janis,niels","jesse","phil","yoda","muhammed","bako","gerrit",
                                            "stefan","***REMOVED***","photo","fitness","traveller","wedding","food","guy","click","city","design","artwork","world","traveller","backpack","atelier","beard","blog","beautiful","beauty",
                                            "buzz","feed","call","cafe","daily","earth","fashion","motivation","full","film","interi","tech","henry","inspi","irela","music","official","love","life","magic","fanpage","raymond","adam",
                                            "abdul","zsolt","toni","photographe","boy","travel"]
        self.tag_list = ['viennagirl','munichgirl',"viennagirls","viennacitygirl","viennacitygirls","viennaparty","viennamodel","viennanights",
                          "viennabynight","austriangirl","yogavienna","viennafashion","viennagram","viennastyle","viennanightlife","viennanights",
                         "munichgirls","munichstyle","munichnightlife","munichnights","munichnightlife","munichmodels","munichblogger","munichnights","089","vienna","munich","viennagirl","munichgirl","austriangirl"]
       # self.tag_list = ["Nikon", "Vienna", "portraitpage", "canon", "Austria", "saltyhair", "Portrait", "photography", "Brandymelville"]
        self.likes_per_tag_left         = self.init_tags()
        self.period_like_count          = self.max_likes_per_period
        self.period_follow_count        = self.max_followers_per_period
        self.period_unfollow_count      = self.max_unfollows_per_period
        self.period_like_newsfeed_count        = self.max_like_newsfeed_per_period
        self.database                   = InstaDB()
        self.api                        = None
        self.get_post_api               = JodelBot()
        self.post_instagram_api         = None
        self.next_iteration             = {"Like": 0, "Follow": 0, "Unfollow": time.time()+(self.between_unfollow/2), "Like_NewsFeed": 0,"Post":0}
        self.start_time                 = 0.0
        self.end_time                   = 0.0
        self.timeline                   = {}
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
        
    def get_tag_feed(self,tag, next_max):
      feed = []
      next_max_id = ''
      for n in range(next_max):
          self.api.getHashtagFeed(tag,next_max_id) 
          temp = self.api.LastJson
          for post in temp["items"]:
              feed.append(post)
          #time.sleep(2) 
          try:
              next_max_id = temp["next_max_id"]     
          except Exception:
              
              print("error next_max. Tag: ", tag)
              return feed    
      return feed
    def containsBadKeyWord(self,name):
      for bad in self.blacklist_usertags:
        
        if bad in str(name):
          return bad
      return None
    def worthy(self,info):
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
     
      resp = self.api.getMediaInfo(info["shortcode"])
      if(resp == None):
        return False
      if(resp["graphql"]["shortcode_media"]["owner"]["followed_by_viewer"]):
        return False
      bad = self.containsBadKeyWord(resp["graphql"]["shortcode_media"]["owner"]["username"])
      if  bad != None:
       # print("%s contains %s !" %  (info["user"]["username"],bad))
        return False 
      
      resp = self.api.getUserInfo("",username=resp["graphql"]["shortcode_media"]["owner"]["username"])
      if(resp == None):
        return False
      
      
      if resp["user"]["followed_by"]["count"] > self.max_followers_on_follower:
        #print("%s has too many follower" % (info["user"]["username"]))
        return False
      
      if resp["user"]["followed_by"]["count"] < self.min_followers_on_follower:
      #  print("%s has too little follower" % (info["user"]["username"]))
        return False
        
      
      return resp["user"]["username"]

    def post_picture(self):
        #print(os.path.abspath(os.path.join(__file__)))
        self.get_post_api.scanTopPost(400)
        img = self.get_post_api.getBestImage()
        path = os.path.abspath('') + "/temp.jpg"
        #img[0].show()
        img[0].save(path,quality = 100)
        self.post_instagram_api.upload(path,(self.post_caption  %(img[1])))

    def like_newsfeed(self):
      if(len(self.timeline) == 0):
        self.timeline = self.api.getTimeline()
        

      if(len(self.timeline) == 0):
        return False
      if("id" in self.timeline[0]["node"]):
        if(self.timeline[0]["node"]["viewer_has_liked"] or ("ad_metadata" in self.timeline[0]["node"])):
          del self.timeline[0]
          return False
        self.api.like(self.timeline[0]["node"]["id"])
     
        print("#%i Liked TimeLine-Media with id %s name : %s" %(self.like_newsfeed_count,self.timeline[0]["node"]["id"],self.timeline[0]["node"]["owner"]["username"]))
        del self.timeline[0]
        return True
      else:
        del self.timeline[0]
        return False
    
    def like_and_follow(self):
      
      to_follow_list = self.database.get_to_follows()
      if(len(to_follow_list) == 0):
        return False
      follower = random.choice(to_follow_list)
      self.api.follow(follower[0])
      self.database.insert_follower(follower[0],follower[1],0,time.time() + self.time_to_unfollow,follower[2])
      self.database.delete_to_follow(follower[0])
      print("#%i Follow User %s" %(self.follow_count,follower[1])) 
      time.sleep(random.randint(7, 20))
      self.api.likeRandomUserMedia(follower[0],username=follower[1])
      #print("#%i Liked Media with id %s" %(self.like_count,follower[3])) 
      return True
      
    def follow(self):
     
      to_follow_list = self.database.get_to_follows()
      if(len(to_follow_list) == 0):
        return False
      follower = random.choice(to_follow_list)
      self.api.follow(follower[0])
      self.database.insert_follower(follower[0],follower[1],0,time.time() + self.time_to_unfollow,follower[2])
      self.database.delete_to_follow(follower[0])
      print("#%i Follow User %s" %(self.follow_count,follower[1])) 
      
      return True
      
    def unfollow(self):
     
      unfollower_list = self.database.get_unfollows()
      if(len(unfollower_list) == 0):
        return False
      unfollower = random.choice(unfollower_list)
      self.api.unfollow(unfollower[0])
      self.database.delete_follower(unfollower[0])
      self.database.insert_blacklist(unfollower[0],unfollower[1])
      print("#%i unfollow User %s"%(self.unfollow_count,unfollower[1])) 
      
      return True
      
    def like(self):
      to_like_list = self.database.get_to_like()
      if(len(to_like_list) == 0):
        return False
      like = random.choice(to_like_list)
      self.api.like(like[0])
      self.database.delete_to_like(like[0])
      print("#%i Liked Media with id %s" %(self.like_count,like[0])) 
      
      return True
    def get_random_tag(self,tag_list):
      return random.choice(tag_list)
  
    def login(self):
      self.api = InstagramAPI(self.username,self.passwort)
      self.api.login()
      self.database.connect()
      
      time.sleep(random.randint(15, 30))

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
        period_count    = 0
        tag_feed = {}
        tag_list = self.tag_list[:]
        tag = ""
        print("Follow every %i seconds"% (self.between_follow))
        print("Unfollow every %i seconds"% (self.between_unfollow))
        print("Like every %i seconds"% (self.between_like))
        print("Like every %i seconds"% (self.between_like_newsfeed))
        print("Post every %i seconds"% (self.between_post))
        while True:
          if(time.time() > self.end_time):
            self.reset_period_counter()
            self.end_time = time.time()+self.period
            period_count += 1
          if len(tag_feed) > 0:
            if len(tag_list) == 0:
              tag_list = self.tag_list[:]
              
            tag = self.get_random_tag(tag_list)
            del tag_list[tag_list.index(tag)]
            print("Now search on #%s"%(tag))
            print("Available Likes #%i"%(self.likes_per_tag_left[tag]))
            tag_feed = self.api.getHashtagFeed(tag,3)
          
          if (len(tag_feed) > 0  and self.database.get_to_follow_count() < 30 ):
            username = self.worthy(tag_feed[0])
            if (username != False):
              self.database.insert_to_follow(tag_feed[0]["node"]["owner"]["id"],username,tag,tag_feed[0]["node"]["id"])
            del tag_feed[0]
          
          if time.time() > self.next_iteration["Post"]:
              self.post_picture()
              print("Posted picture!")
              self.next_iteration["Post"] = time.time() + self.between_post 
          if time.time() > self.next_iteration["Like_NewsFeed"] and self.period_like_newsfeed_count > 0 and self.like_newsfeed():
            self.like_newsfeed_count += 1
            self.period_like_newsfeed_count -=1
            self.next_iteration["Like_NewsFeed"] = time.time() + self.between_like_newsfeed 
            #time.sleep(random.randint(3, 20))

          if time.time() > self.next_iteration["Follow"] and self.period_follow_count > 0 and self.like_and_follow():
            self.follow_count += 1
            self.period_follow_count -= 1
            self.like_count += 1
            self.period_like_count -= 1
            self.next_iteration["Follow"] = time.time() + self.between_follow
            self.next_iteration["Like"] = time.time() + self.between_like
            print("Period Count : #%s"%(period_count))
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
