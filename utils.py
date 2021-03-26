import cv2
from pygame import mixer
import pandas as pd
from config import GameConfig
import time

config = GameConfig()

def play_music(music_file, time=0.0):
    try:
        mixer.init()
        mixer.music.load(music_file)
        mixer.music.play(1, time)
    except:
        print("Failed to play the music.")

def play_sound(sound_file):
    try:
        mixer.init()
        sound = mixer.Sound(sound_file)
        mixer.Sound.play(sound)
    except:
        print("Failed to play the sound effect.")

sound_effect1 = 'musics/sound1.wav'
sound_effect2 = 'musics/sound2.wav'
sound_applause = 'musics/applause.wav'
sound_disappointed = 'musics/disappointed.wav'

# player chooses song & difficulty
def main_menu(config, params):
    diff = None
    exit = None

    bgImg = cv2.imread('images/main_menu.png')

    button1 = cv2.imread('./images/easy_preview.png')
    button2 = cv2.imread('./images/easy_start.png')
    button3 = cv2.imread('./images/hard_preview.png')
    button4 = cv2.imread('./images/hard_start.png')
    buttonQ = cv2.imread('./images/quit.png')

    key = 0

    sunset_teaser = 'musics/sunset_glow_teaser.wav'
    bingo_teaser = 'musics/bingo_teaser.wav'

    config.named_window = bgImg

    while True:
        a = cv2.waitKey(0)

        if a & 0xFF == ord('1'):
            play_sound(sound_effect1)
            diff = 'easy'
            play_music(sunset_teaser)
            key = 1
            config.named_window = button1

        if a & 0xFF == ord('2'):
            play_sound(sound_effect2)
            diff = 'easy'
            key = 2
            config.named_window = button2

        if a & 0xFF == ord('3'):
            play_sound(sound_effect1)
            diff = 'hard'
            play_music(bingo_teaser)
            key = 3
            config.named_window = button3

        if a & 0xFF == ord('4'):
            play_sound(sound_effect2)
            diff = 'hard'
            key = 4
            config.named_window = button4

        if a & 0xFF == ord('q'):
            exit = True
            key = 5
            config.named_window = buttonQ

        if key == 1:
            config.named_window = button1
        if key == 2:
            config.named_window = button2
        if key == 3:
            config.named_window = button3
        if key == 4:
            config.named_window = button4
        if key == 5:
            config.named_window = buttonQ

        cv2.imshow('McgBcg', config.named_window)

        if exit == True:
            print('Exit')
            break
        if params["exit"] is True:
            print('Exit')
            break

        if key == 2:
            print('Easy')
            break
        if key == 4:
            print('Hard')
            break

    params["diff"] = diff
    params["exit"] = exit
    print("diff = ", diff, "exit = ", exit)

    params["restart"] = False
    params["menu"] = False
    params["resume"] = False
    cv2.destroyAllWindows()

def get_number(list):
    ret_list = []
    for i in range(len(list)):
        ret_list.append(list[i][0:11])
    return ret_list

# load appropriate game pattern
def load_pattern(config, params):
    pattern = None

    df = None
    data = None

    print("Choose easy / hard \n")
    diff = params["diff"]

    if diff == 'easy':
        df = pd.read_excel('game_patterns.xlsx', sheet_name='sunset')
        data = pd.concat([df[0:39]]).values.tolist()
        pattern = get_number(data)
    elif diff == 'hard':
        df = pd.read_excel('game_patterns.xlsx', sheet_name='bingo')
        data = pd.concat([df[0:137]]).values.tolist()
        pattern = get_number(data)

    params["patterns"] = pattern
    print("patterns = ", pattern)
    return


# load appropriate song
def load_song(config, params):
    song = None

    if params["diff"] == 'easy':
        song = "musics/sunset_glow.wav"
    if params["diff"] == 'hard':
        song = "musics/bingo.wav"

    params["song"] = song
    print("song = ", song)
