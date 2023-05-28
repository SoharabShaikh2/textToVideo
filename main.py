import moviepy.video.fx.all as vfx
import json

from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip

f = open('001/Surah_001001.json', encoding="utf-8")

data = json.load(f)
# print(data)
f.close()
jsonData = data
# for i in data["wbw"]:
# print(i)

print(jsonData)


def convertAyatToVideo(jsonData):
    screensize = (1080, 1920)
    clip = VideoFileClip("back.mp4", audio=False)
    mainAudio = AudioFileClip("back_mp3.mp3")

    clip_resized = clip.fx(vfx.resize, width=1080, height=1920)

    audio = AudioFileClip(jsonData["ayat_mp3"])
    audio1 = audio.set_start(0)
    videoDuration = audio.duration + (len(jsonData["wbw"]) * 5) + 1

    clip1 = vfx.loop(clip_resized, duration=videoDuration)
    mainAudio1 = vfx.loop(mainAudio, duration=videoDuration)

    clipArray = []
    audioArry = []
    clipArray.append(clip1)
    audioArry.append(mainAudio1)
    audioArry.append(audio1)

    txt_clip = TextClip(jsonData["arabic"], fontsize=100, color='white', align='center', size=screensize,
                        method='caption')
    txt_clip = txt_clip.set_position('center').set_duration(audio.duration+1).set_start(0)
    txt_clip_new = txt_clip.fx(vfx.margin, bottom=600, opacity=0)

    txt_clip_new = vfx.fadein(txt_clip_new, 1)
    #txt_clip_new = vfx.fadeout(txt_clip_new, 1)
    #new_txt_Clip = txt_clip_new.set_audio(audio)
    clipArray.append(txt_clip_new)

    txt_clip2 = TextClip(jsonData["bengali"], font='Bangla.ttc', fontsize=70, color='white', align='center',
                         size=screensize, method='caption')
    txt_clip2 = txt_clip2.set_position('center').set_duration(audio.duration+1).set_start(0)
    txt_clip2 = vfx.fadein(txt_clip2, 1)
    #txt_clip2 = vfx.fadeout(txt_clip2, 1)
    clipArray.append(txt_clip2)

    txt_clip3 = TextClip(jsonData["english"], fontsize=70, color='white', align='center', size=screensize,
                         method='caption')
    txt_clip3 = txt_clip3.set_position('center').set_duration(audio.duration+1).set_start(0)
    txt_clip3_new = txt_clip3.fx(vfx.margin, top=600, opacity=0)
    txt_clip3_new = vfx.fadein(txt_clip3_new, 1)
    #txt_clip3_new = vfx.fadeout(txt_clip3_new, 1)
    clipArray.append(txt_clip3_new)

    wordBword = jsonData["wbw"]
    i = 0
    while i < len(wordBword):
        print(wordBword[i])
        time = 0
        if i == 0:
            time = audio.duration
        else:
            time = audio.duration + (i * 5)

        child_clip1 = TextClip(wordBword[i]["arabic"], fontsize=200, color='white')
        child_clip1 = child_clip1.set_position("center").set_duration(5).set_start(time)
        child_clip1_new = child_clip1.fx(vfx.margin, bottom=600, opacity=0)
        child_clip1_new = vfx.fadein(child_clip1_new, 1)
        #child_clip1_new = vfx.fadeout(child_clip1_new, 1)
        child_audio = AudioFileClip(wordBword[i]["ar_mp3"])
        #new_child_clip1 = child_clip1_new.set_audio(child_audio.set_start(time))
        child_audio1 = child_audio.set_start(time)
        audioArry.append(child_audio1)

        clipArray.append(child_clip1_new)

        child_clip2 = TextClip(wordBword[i]["bengali"], font='Bangla.ttc', fontsize=100, color='white')
        child_clip2 = child_clip2.set_position("center").set_duration(5).set_start(time)
        child_clip2 = vfx.fadein(child_clip2, 1)
        #child_clip2 = vfx.fadeout(child_clip2, 1)
        # child_clip2 = child_clip2.margin(20)
        clipArray.append(child_clip2)

        child_clip3 = TextClip(wordBword[i]["english"], fontsize=100, color='white')
        child_clip3 = child_clip3.set_position("center").set_duration(5).set_start(time)
        child_clip3_new = child_clip3.fx(vfx.margin, top=600, opacity=0)
        child_clip3_new = vfx.fadein(child_clip3_new, 1)
        #child_clip3_new = vfx.fadeout(child_clip3_new, 1)
        # child_clip3 = child_clip3.margin(20)
        clipArray.append(child_clip3_new)

        i += 1

    audioMixed = CompositeAudioClip(audioArry)
    # Overlay the text clip on the first video clip
    video = CompositeVideoClip(clipArray)
    video = video.set_audio(audioMixed)
    # showing video
    video.write_videofile("newfile.mp4")


convertAyatToVideo(jsonData)
