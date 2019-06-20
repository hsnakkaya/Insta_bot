from InstagramAPI import InstagramAPI
from credentials import*
import datetime


def upload_video(i):
    api = InstagramAPI(username, password)
    if api.login():
        print(str(datetime.datetime.now()) + " Login success!")
    else:
        print(str(datetime.datetime.now()) + " Can't login!")

    video = "export/makina_dunyasi_" + str(i) + ".mp4"
    thumbnail = "thumbnail/makina_dunyasi_" + str(i) + ".jpg"
    api.uploadVideo(video, thumbnail, caption=None, upload_id=None, is_sidecar=None)
