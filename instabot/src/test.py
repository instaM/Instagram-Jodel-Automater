import os
import sys
lib_path = os.path.abspath(os.path.join(__file__, '..', '..','..', 'apis', 'instagramapi_browser'))

sys.path.append(lib_path)

from datacollector import InstaHashtag
from instagramapi_browser import InstagramAPI

bot = InstagramAPI("thefineclubs","BaQDWf8HeP1")
bot.login()
#bot.getUserInfo("4629965945")
#bot.getTimeline()
bot.likeRandomUserMedia("4629965945",username="mayra.d.angelo.342")
#hashtagfeed = bot.getHashtagFeed("instalunz",4)
#bot.follow("4629965945")
#print(len(hashtagfeed))
#for post in hashtagfeed:
 #   print(post["node"]["id"])
bot.logout()