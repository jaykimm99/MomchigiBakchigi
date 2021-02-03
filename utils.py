import cv2
from pygame import mixer
import pandas as pd
from config import GameConfig
import time

config = GameConfig()


def play_music(music_file, time=0.0):  # music 함수
    mixer.init()
    mixer.music.load(music_file)
    mixer.music.play(1, time)
    # clock = pygame.time.Clock()
    # clock.tick(10)


def play_sound(sound_file):  # sound effect 함수
    mixer.init()
    sound = mixer.Sound(sound_file)
    mixer.Sound.play(sound)


# 효과음
sound_effect1 = 'musics/sound1.wav'
sound_effect2 = 'musics/sound2.wav'
sound_applause = 'musics/applause.wav'
sound_disappointed = 'musics/disappointed.wav'


def main_menu(config, params):
    '''
    :param config: initial configuration
    :param params: 이 중에 diff, exit 쓸 것
    :return: None
    '''

    diff = None  # 뒤에서 'easy' or 'hard'
    exit = None  # True or False

    # 메인메뉴 기본화면
    bgImg = cv2.imread('images/main_menu.png')
    # bgImg = cv2.resize(bgImg, (1080, 720))

    # 버튼 눌렀을 때의 메뉴화면
    button1 = cv2.imread('./images/easy_preview.png')
    button2 = cv2.imread('./images/easy_start.png')
    button3 = cv2.imread('./images/hard_preview.png')
    button4 = cv2.imread('./images/hard_start.png')
    buttonQ = cv2.imread('./images/quit.png')

    # 버튼 눌린 상태 유지를 위해 while문 밖에 따로 변수 지정했음
    key = 0
    keyQ = 0

    # 티저 음악들 불러오기
    sunset_teaser = 'musics/sunset_glow_teaser.wav'
    bingo_teaser = 'musics/bingo_teaser.wav'

    # 처음 시작할 때는 기본메뉴화면으로 화면 설정
    config.named_window = bgImg

    while True:
        a = cv2.waitKey(0)

        if a & 0xFF == ord('1'):  # 1번 누르면
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
            #play_sound(sound_effect1)
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

        # 바뀐 화면을 유지해주기 위해 while 밖에
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

        # 이미지 띄우기
        cv2.imshow('McgBcg', config.named_window)

        if exit == True:
            print('Exit')
            break
        if params["exit"] is True:  # main menu에서 종료 버튼
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
    print("diff = ", diff, "exit = ", exit)  # ex) diff = easy exit = False

    params["restart"] = False
    params["menu"] = False
    params["resume"] = False
    cv2.destroyAllWindows()


def get_number(list):
    ret_list = []
    for i in range(len(list)):
        ret_list.append(list[i][0:11])
    return ret_list


def load_pattern(config, params):
    '''
    :param config:
    :param params: 이 중에 diff, pattern 씀
    :return: None
    '''

    pattern = None

    # 여기부터 주석박스 전까지 짜는 코드!
    df = None  # excel에서 한칸
    data = None  # excel에서 value 값

    print("Choose easy / hard \n")
    diff = params["diff"]

    # def excel(diff):
    if diff == 'easy':
        df = pd.read_excel('sunset_glow.xlsx', sheet_name='sunset')
        data = pd.concat([df[0:39]]).values.tolist()
        pattern = get_number(data)
    elif diff == 'hard':
        df = pd.read_excel('sunset_glow.xlsx', sheet_name='bingo')
        data = pd.concat([df[0:137]]).values.tolist()
        pattern = get_number(data)

    params["patterns"] = pattern
    print("patterns = ", pattern)  # ex) [[0, 0, 0,..], [0, 0, 0, ..], ...]
    return


def load_song(config, params):
    """
    :param config:
    :param params: 이 중 diff랑 song 쓸 것
    :return: None
    """

    song = None

    if params["diff"] == 'easy':
        song = "musics/sunset_glow.wav"  # 난이도 easy일 때 붉은노을
    if params["diff"] == 'hard':
        song = "musics/bingo.wav"  # 난이도 hard일 때 빙고

    ##################################################################################
    ## TODO:
    ##  diff에 따라 노래를 다르게 load 시킬 것
    ##  song = "sunset_glow.wav" 이런 식으로
    ##################################################################################

    params["song"] = song
    print("song = ", song)  # ex) song = "sunset_glow.wav"


# 실루엣 띄우는 함수 -> 이제 안쓰는듯
def show_pose(bgImg, pose, x_offset, y_offset, x_resize, y_resize):
    pose = cv2.resize(pose, (x_resize, y_resize))
    rows, cols, channels = pose.shape
    roi = bgImg[y_offset: rows + y_offset, x_offset: x_offset + cols]

    img2gray = cv2.cvtColor(pose, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    bgImg_bg = cv2.bitwise_and(roi, roi, mask=mask)
    pose_fg = cv2.bitwise_and(pose, pose, mask=mask_inv)
    dst = cv2.add(bgImg_bg, pose_fg)
    bgImg[y_offset: y_offset + rows, x_offset:x_offset + cols] = dst
