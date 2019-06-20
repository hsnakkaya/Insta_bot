from InstagramAPI import InstagramAPI
from credentials import*
import datetime
import time
import json
import pprint

api = InstagramAPI(username, password)
if api.login():
    print(str(datetime.datetime.now()) + " Login success!")
else:
    print(str(datetime.datetime.now()) + " Can't login!")

api.getTotalFollowers('2217541870')
selfFollowing = api.LastJson

followers = {}

for user in selfFollowing['users']:
    username = user['username']
    pk = user['pk']
    followers[str(pk)] = 'follow'

pprint.pprint(followers)

self_followers_json = {}
self_following_json = {}
users_interacted_json = {}
users_to_unfollow_json = {}
users_to_follow_json = followers


with open("users_to_follow.json", 'w') as f:
    json.dump(users_to_follow_json, f, indent=4)
