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
      print(r.content)
      if(cont["graphql"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["has_next_page"] == False):
        x=5
        cont = cont["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]
        
      else:
        next_id = cont["graphql"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["end_cursor"]
        cont = cont["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]
        print(cont)
        link = self.link+hashtag+"/?__a=1&max_id="+next_id
        time.sleep(3)
        print(cont)
      for post in cont:
              feed.append(cont)
      
    return feed
  def test(self):
        
        header =({
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': self.accept_language,
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'www.instagram.com',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'User-Agent': self.user_agent,
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest'
        })