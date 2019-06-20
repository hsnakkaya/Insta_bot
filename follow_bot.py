import json
import time
import datetime
import random
from InstagramAPI import InstagramAPI
from credentials import*
from datetime import timedelta
import dropbox
from dropbox.files import WriteMode


def upload_dropbox():

    dbx = dropbox.Dropbox(access_token)

    print('uploading files to Dropbox... ')

    with open('variables/self_followers.json', 'rb') as f:
        dbx.files_upload(f.read(), '/variables/self_followers.json', mode=dropbox.files.WriteMode.overwrite)
    with open('variables/self_following.json', 'rb') as f:
        dbx.files_upload(f.read(), '/variables/self_following.json', mode=dropbox.files.WriteMode.overwrite)
    with open('variables/users_interacted.json', 'rb') as f:
        dbx.files_upload(f.read(), '/variables/users_interacted.json', mode=dropbox.files.WriteMode.overwrite)
    with open('variables/users_to_follow.json', 'rb') as f:
        dbx.files_upload(f.read(), '/variables/users_to_follow.json', mode=dropbox.files.WriteMode.overwrite)
    with open('variables/users_to_unfollow.json', 'rb') as f:
        dbx.files_upload(f.read(), '/variables/users_to_unfollow.json', mode=dropbox.files.WriteMode.overwrite)
    with open('variables/variables.json', 'rb') as f:
        dbx.files_upload(f.read(), '/variables/variables.json', mode=dropbox.files.WriteMode.overwrite)
    print('Upload done.')


def download_dropbox():

    dbx = dropbox.Dropbox(access_token)

    print('downloading files from dropbox...')

    with open("variables/self_followers.json", "wb") as f:
        metadata, res = dbx.files_download(path="/variables/self_followers.json")
        f.write(res.content)
    with open("variables/self_following.json", "wb") as f:
        metadata, res = dbx.files_download(path="/variables/self_following.json")
        f.write(res.content)
    with open("variables/users_interacted.json", "wb") as f:
        metadata, res = dbx.files_download(path="/variables/users_interacted.json")
        f.write(res.content)
    with open("variables/users_to_follow.json", "wb") as f:
        metadata, res = dbx.files_download(path="/variables/users_to_follow.json")
        f.write(res.content)
    with open("variables/users_to_unfollow.json", "wb") as f:
        metadata, res = dbx.files_download(path="/variables/users_to_unfollow.json")
        f.write(res.content)
    with open("variables/variables.json", "wb") as f:
        metadata, res = dbx.files_download(path="/variables/variables.json")
        f.write(res.content)
    print('Download done.')


def deconstruct_datetime(a):
    b = [a.year, a.month, a.day, a.hour, a.minute, a.second]
    return b


def construct_datetime(b):
    a = datetime.datetime(b[0], b[1], b[2], b[3], b[4], b[5])
    return a


def upload_video(i):
    api = InstagramAPI(username, password)
    if api.login():
        print(str(datetime.datetime.now()) + " Login success!")
    else:
        print(str(datetime.datetime.now()) + " Can't login!")

    video = "export/makina_dunyasi_" + str(i) + ".mp4"
    thumbnail = "thumbnail/makina_dunyasi_" + str(i) + ".jpg"
    api.uploadVideo(video, thumbnail, caption=None, upload_id=None, is_sidecar=None)


def next_session():

    with open("variables/variables.json", 'r') as f:
        variables_json = json.loads(f.read())
    session_hours = variables_json["session_hours"]
    sessions_today = variables_json["sessions_today"]
    video_to_upload = variables_json["video_to_upload"]

    next_session_minute = 0

    # calculate next session time

    while 1:
        if sessions_today < len(session_hours):
            next_session_minute = random.randint(1, 60)
            print('Waiting for next session at ' + str(session_hours[sessions_today]) + ':' + str(next_session_minute))
        break

    # wait for next session time, and initiate session

    while 1:
        date = datetime.datetime.now()
        if date.hour == session_hours[sessions_today] and date.minute == next_session_minute:
            instagram_session()  # initiate session
            with open("variables/variables.json", 'r') as f:
                variables_json = json.loads(f.read())
            session_hours = variables_json["session_hours"]
            sessions_today = variables_json["sessions_today"]
            video_to_upload = variables_json["video_to_upload"]

            x = 1
            while x:
                if sessions_today < len(session_hours):
                    next_session_minute = random.randint(1, 60)
                    print('Waiting for next session at '
                          + str(session_hours[sessions_today]) + ':' + str(next_session_minute))
                x = 0

        else:
            time.sleep(60)  # wait 60 second


def instagram_session():

    # download Dropbox files

    download_dropbox()

    # read and store json files
    print('read and store json files')

    with open("variables/self_followers.json", 'r') as f:
        self_followers_json = json.loads(f.read())
    with open("variables/self_following.json", 'r') as f:
        self_following_json = json.loads(f.read())
    with open("variables/users_interacted.json", 'r') as f:
        users_interacted_json = json.loads(f.read())
    with open("variables/users_to_unfollow.json", 'r') as f:
        users_to_unfollow_json = json.loads(f.read())
    with open("variables/users_to_follow.json", 'r') as f:
        users_to_follow_json = json.loads(f.read())
    with open("variables/variables.json", 'r') as f:
        variables_json = json.loads(f.read())

    session_hours = variables_json["session_hours"]
    max_follows_per_day = variables_json["max_follows_per_day"]
    max_unfollows_per_day = variables_json["max_unfollows_per_day"]
    sessions_today = variables_json["sessions_today"]
    request_sleep_time = variables_json["request_sleep_time"]
    request_deviation_time = variables_json["request_deviation_time"]
    unfollow_days = timedelta(days=variables_json["unfollow_days"])
    video_to_upload = variables_json["video_to_upload"]
    upload_video(video_to_upload)

    video_to_upload += 1
    variables_json["video_to_upload"] = video_to_upload

    sessions_today += 1
    sessions_today = sessions_today % 4
    variables_json["sessions_today"] = sessions_today

    # login to Instagram

    api = InstagramAPI(username, password)
    if api.login():
        print(str(datetime.datetime.now()) + " Login success!")
    else:
        print(str(datetime.datetime.now()) + " Can't login!")

    # request self followers and store them
    print('request self followers and store them')

    followers_list = api.getTotalSelfFollowers()
    time.sleep(request_sleep_time + random.randint(-request_deviation_time, request_deviation_time))

    # extract follower pks

    self_follower_pk_list = []
    for pks in followers_list:
        self_follower_pk_list.append(pks['pk'])

    # check for new follows

    time_now = datetime.datetime.now()  # get current time
    for pk in self_follower_pk_list:  # for all users in new list
        if pk in self_followers_json:  # if is in old list
            pass  # old follower
        else:  # new follower
            # add to self_followers_json with timestamp
            self_followers_json[str(pk)] = deconstruct_datetime(time_now)

    # update users_to_unfollow_json

    # if follower followed unfollow_days before now, put in users_to_unfollow_json

    for pk in self_followers_json:
        follow_time = construct_datetime(self_followers_json[str(pk)])
        if datetime.datetime.now() - follow_time > unfollow_days:
            users_to_unfollow_json[str(pk)] = 'unfollow'

    # if user not followed back in unfollow_days, put in users_to_unfollow_json

    for pk in self_following_json:
        follow_time = construct_datetime(self_following_json[str(pk)])
        if datetime.datetime.now() - follow_time > unfollow_days:
            users_to_unfollow_json[str(pk)] = 'unfollow'

    # add self followers to users_interacted_json

    for pk in self_follower_pk_list:
        users_interacted_json[str(pk)] = 'follower'

    # follow users with random intervals

    users_count_to_follow = int(max_follows_per_day/len(session_hours))  # follows in this session
    if len(users_to_follow_json) > users_count_to_follow:  # check if enough users are due to follow
        for i in range(users_count_to_follow):
            pk = list(users_to_follow_json.keys())[0]  # get the first pk
            del users_to_follow_json[pk]  # delete that pk from users_to_follow_json
            api.follow(str(pk))  # follow that pk
            print('followed: ' + str(pk))
            self_following_json[str(pk)] = deconstruct_datetime(time_now)  # add to self_following_json with timestamp
            time.sleep(request_sleep_time + random.randint(-request_deviation_time, request_deviation_time))

    # unfollow users with random intervals

    users_count_to_unfollow = int(max_unfollows_per_day / len(session_hours))  # unfollows in this session
    if len(users_to_unfollow_json) > users_count_to_unfollow:  # check if enough users are due to unfollow
        for i in range(users_count_to_unfollow):
            pk = list(users_to_unfollow_json.keys())[0]  # get the first pk
            del users_to_unfollow_json[pk]  # delete that pk from users_to_unfollow_json
            api.unfollow(str(pk))
            print('unfollowed ' + str(pk))
            time.sleep(request_sleep_time + random.randint(-request_deviation_time, request_deviation_time))

    # write json files

    with open("variables/self_followers.json", 'w') as f:
        json.dump(self_followers_json, f, indent=4)
    with open("variables/self_following.json", 'w') as f:
        json.dump(self_following_json, f, indent=4)
    with open("variables/users_interacted.json", 'w') as f:
        json.dump(users_interacted_json, f, indent=4)
    with open("variables/users_to_unfollow.json", 'w') as f:
        json.dump(users_to_unfollow_json, f, indent=4)
    with open("variables/users_to_follow.json", 'w') as f:
        json.dump(users_to_follow_json, f, indent=4)
    with open("variables/variables.json", 'w') as f:
        json.dump(variables_json, f, indent=4)

    # upload files to Dropbox

    upload_dropbox()


next_session()


# upload_video(12)
