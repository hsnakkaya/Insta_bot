from moviepy.editor import *
from moviepy.video.fx.all import crop

for i in range(1):

    i = i + 29

    # read the video file

    clip = VideoFileClip("thang/thang (" + str(i) + ").mp4")

    # crop to the smallest dimension in square ratio

    w = clip.size[0]
    h = clip.size[1]

    if w > h:
        clip = crop(clip, width=h-(h/20), height=h-(h/20), x_center=w/2, y_center=h/2)
    else:
        clip = crop(clip, width=w-(w/20), height=w-(w/20), x_center=w / 2, y_center=h / 2)

    # resize video to 1080x1080

    clip = clip.resize(height=1080)

    # trim the clip if longer than 60 sec

    if clip.duration > 60:
        clip = clip.cutout(0, 60)

    # read the watermark image

    logo = ((ImageClip("makina_dunyasi.png")
            .set_duration(clip.duration)
            .set_pos(("right", "top"))))

    # overlay the watermark image

    clip.save_frame("thumbnail/makina_dunyasi_" + str(i) + ".jpg")

    '''

    final = CompositeVideoClip([clip, logo])

    # write the file to export folder

    print("video number: " + str(i) + " being processed")

    final.write_videofile("export/makina_dunyasi_" + str(i) + ".mp4", audio=False, threads=4, progress_bar=None)
    
    '''
    print(str(i+1) + " files processed")
    clip.reader.close()


