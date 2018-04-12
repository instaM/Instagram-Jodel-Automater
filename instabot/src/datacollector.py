import requests 
import json
import time
import logging
import sys
class Collector:
    url_user_detail = 'https://www.instagram.com/%s/?__a=1'
    url_tag = 'https://www.instagram.com/explore/tags/%s/?__a=1'
    url_media_detail = 'https://www.instagram.com/p/%s/?__a=1'
    logger = logging.getLogger("instalog.collector")
    def getUserInfo(self,username):
        info = {}
       
        try:    
            url_det = self.url_user_detail % (username)   
            r = requests.get(url_det)
            all_data = json.loads(r.text)
            
           
            return all_data["graphql"]
        except Exception as e:
            
            exc_type, exc_obj, exc_tb = sys.exc_info()
        
            self.logger.error(str(exc_type)+" - "+ exc_obj.message+" - "+ str(exc_tb.tb_lineno))
            
            return None
           
    def getMediaInfo(self,media_short):
        info = {}

        try:
           
                
            url_det = self.url_media_detail % (media_short)
                
            r = requests.get(url_det)
            all_data = json.loads(r.text)
            
           
            return all_data
        except Exception as e:
            
            exc_type, exc_obj, exc_tb = sys.exc_info()
        
            self.logger.error(str(exc_type)+" - "+ exc_obj.message+" - "+ str(exc_tb.tb_lineno))
            
            return None
      
    def getHashtagFeed(self, tag,max):
        
        feed = []
        next_id = None
   
        for x in range(0,max):    
       
            if(next_id == None):
                url_tag = self.url_tag % (tag)
            else:
                url_tag = self.url_tag % (tag)+"&max_id="+next_id   
            try:
                
                r = requests.get(url_tag)
               
               
                all_data = json.loads(r.text)
                
                if(all_data["graphql"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["has_next_page"] == False):
                    for post in all_data["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]:
                        feed.append(post)
                    return feed
                else:
                    next_id = all_data["graphql"]["hashtag"]["edge_hashtag_to_media"]["page_info"]["end_cursor"] 
                    
                for post in all_data["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]:
                    feed.append(post)
                
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
        
                self.logger.error(str(exc_type)+" - "+ exc_obj.message+" - "+ str(exc_tb.tb_lineno))
                return []
                        
              
        return feed
  