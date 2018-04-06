
from database import InstaDB
from InstagramAPI import InstagramAPI

API = InstagramAPI("", "")

API.login() # login
db = InstaDB()
db.connect()
db_follow = db.get_following_all()
actual_following = API.getTotalSelfFollowings()
actual_follower  = API.getTotalSelfFollowers()
print("%s accounts follow you" % (len(actual_follower)))
print("You are following %s accounts" % (len(actual_following)))
print("%s Database entries" %(len(db_follow)))

#print(API.LastJson)
follow_no_refollow = []
not_in_db  = []
simple_following = []
simple_follower = []
simple_db = []
whitelist = []
follow_not_in_wl = []
for entry in db_follow:
    if(entry[2] == 1):
        whitelist.append(entry[1])
for entry in actual_follower:
    simple_follower.append(entry["username"])
for entry in actual_following:
    simple_following.append(entry["username"])
for entry in db_follow:
    simple_db.append(entry[1])
    

for following in simple_following:
    if(following not in simple_follower):
        follow_no_refollow.append(following)
        
for follow in simple_following:
    if(follow not in simple_db):    
        not_in_db.append(follow)
        
for follow in whitelist:
    if(follow not in simple_follower):
        follow_not_in_wl.append(follow)
        
#print(follow_no_refollow)
#print(not_in_db)
print(follow_not_in_wl)
print("Following accounts are in your whitelist, but do not follow you back(y = insert whitelist, n = insert not whitelist")

for follow in follow_not_in_wl:
    decision = ""
    while(decision != 'y' and decision !='n'):
        
        decision = input(follow+":")
        
    if(decision=="y"):
        print("Inserted into whitelist")
    else:
        print("Account will be unfollowed soon")     
