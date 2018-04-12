import datacollector import Collector
import time
class Analyzer:
  def __init__(self,
              accounts_to_watch = []):
    self.accounts_to_watch = accounts_to_watch
    
  def getAccountStats(self):
    val = {}
    for account in self.accounts_to_watch:
      info = Collector.getUserInfo(account)
      
      val[account]["followed"] = info["user"]["edge_followed_by"]["count"]
      val[account]["follows"]  = info["user"]["edge_follow"]["count"]
      time.sleep(3)
    return val
    
  