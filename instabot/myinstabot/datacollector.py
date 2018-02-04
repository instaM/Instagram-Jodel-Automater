import requests 
import re
import time
class InstaHashtag:
  def __init__(self):
    self.link = "https://www.instagram.com/explore/tags/"
  def getHashtagContent(self,hashtag):
    link = self.link+hashtag+"/?__a=1"
    feed = []
    for x in range(0, 5):
   
      r = requests.get(link)

      cont = r.json()
      
      if(cont["graphql"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["has_next_page"] == False):
        x=5
        cont = cont["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]
          
      else:
        next_id = cont["graphql"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["end_cursor"]
        cont = cont["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]
        link = self.link+hashtag+"/?__a=1&max_id="+next_id
        time.sleep(3)
        
      for post in cont:
              feed.append(cont)
      
    return feed