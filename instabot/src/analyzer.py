from datacollector import Collector
import time
from database import InstaDB
from InstagramAPI import InstagramAPI

class Analyzer:
  def __init__(self,
              name,pw
              ):
    #self.accounts_to_watch = accounts_to_watch
    self.api  = InstagramAPI(name,pw)
    self.api.login()
    self.db = InstaDB()
    self.db.connect()
  def getAccountStats(self):
    
    return ""
  def getHashtagRating(self):
    actual_follower = self.api.getTotalSelfFollowers()
    print(len(actual_follower))
    all_follow = self.db.get_all_follow()
    simple_follower = {}
    rating = {}
    count = 0
    for entry in actual_follower:
      simple_follower[str(entry["pk"])] = entry["username"]
    for entry in all_follow:
      if (entry[0]) in simple_follower:
        if(entry[2] in rating):
          rating[entry[2]] += 1
        else:
          rating[entry[2]] = 0
        count +=1
    print(rating)
    print(count)
  
anal = Analyzer("***REMOVED***","***REMOVED***1")
anal.getHashtagRating()  