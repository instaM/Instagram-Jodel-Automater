import json
from database import InstaDB
from InstagramAPI import InstagramAPI


import sys

API = InstagramAPI("","")

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
follow_no_refollow = {}
simple_following = {}
simple_follower = {}
simple_db = {}
whitelist = {}
follow_not_in_wl = {}
fan = 0
for entry in db_follow:
    if(entry[2] == 1):
        whitelist[entry[0]]= entry[1]
    else:
        simple_db[entry[0]] = entry[1]
for entry in actual_follower:
    simple_follower[str(entry["pk"])] = entry["username"]
for entry in actual_following:
    simple_following[str(entry["pk"])] = entry["username"]

    
        
for entry in simple_follower:
    if entry not in simple_following:
        fan +=1

#Delete from Database accounts you are not following
for entry in list(simple_db):
    if entry not in simple_following:
        db.delete_follower(entry)
        del simple_db[entry]
        
for entry in list(whitelist):
    if entry not in simple_following:
        db.delete_follower(entry)
        del whitelist[entry]

print("%s remaining Database entries" % (len(db_follow)))
print("%s remaining Whitelist entries" % (len(whitelist)))        
#Not following from whitelist
for entry in whitelist:
    if(entry not in simple_follower):
        follow_not_in_wl[entry]= whitelist[entry] 
    
    del simple_following[entry]

#Entries which are already in database   
for entry in list(simple_following): 
    if entry in simple_db:
        del simple_following[entry]

#Entries which are not following you back        
for entry in list(simple_following):
    if entry not in simple_follower:
        follow_no_refollow[entry] = simple_following[entry]
        del simple_following[entry]
            

with open('follower.txt', 'w') as outfile:
    json.dump(simple_follower, outfile, indent=4, sort_keys=True)
with open('following.txt', 'w') as outfile:
    json.dump(simple_following, outfile, indent=4, sort_keys=True)
with open('whitelist.txt', 'w') as outfile:
    json.dump(whitelist, outfile, indent=4, sort_keys=True)

print("%s accounts are not following you back" %(len(follow_no_refollow)))
print("%s accounts are not following you from your whitelist" %(len(follow_not_in_wl)))
print("%s accounts are following you back not from your whitelist" %(len(simple_following)))
print("%s accounts are following you and you are not following back" % (fan))


print("Following accounts are in your whitelist, but do not follow you back(y = insert whitelist, n = insert not whitelist")
for follow in follow_not_in_wl:
    decision = ""
    while(decision != 'y' and decision !='n'):
        
        decision = input(follow_not_in_wl[follow]+":")
        
    if(decision=="y"):
        print("Inserted into whitelist")
        db.insert_follower(entry,simple_following[entry],1, 0, "sanitize")
    else:
        print("Account will be unfollowed soon")
        db.insert_follower(entry,simple_following[entry],0, 0, "sanitize")    
        
print("Following accounts are in not in your whitelist, but do follow you back(y = insert whitelist, n = insert not whitelist")
for entry in simple_following:
    decision = ""
    while(decision != 'y' and decision !='n'):
        
        decision = input(simple_following[entry]+":")
        
    if(decision=="y"):
        print(simple_following[entry]+ " inserted into whitelist")
        db.insert_follower(entry,simple_following[entry],1, 0, "sanitize")
    else:
        print("Account will be unfollowed soon")
        db.insert_follower(entry,simple_following[entry],0, 0, "sanitize")    

for entry in follow_no_refollow:
    db.insert_follower(entry,follow_no_refollow[entry],0, 0, "sanitize")
