import cv2
import time
from utils import *
from statistics import median_high
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path
import tf_pose.common as common
import pygame

score = 0

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

def shownum(named_window, target_time, play_time, image):
    if target_time - 3 <= play_time <= target_time :
        cv2.imshow('McgBcg', cv2.imread(image))
    elif play_time > target_time - 3.5:
        cv2.putText(named_window, '1', (config.imWidth - 555, config.imHeight - 160), cv2.FONT_HERSHEY_TRIPLEX, 4, (0, 0, 255), 7, cv2.LINE_8) # 1일 때 빨간색
    elif play_time > target_time - 4.5:
        cv2.putText(named_window, '2', (config.imWidth - 555, config.imHeight - 160), cv2.FONT_HERSHEY_TRIPLEX, 4, (255, 255, 255), 7, cv2.LINE_8)
    elif play_time > target_time - 6.5:
        cv2.putText(named_window, '3', (config.imWidth - 555, config.imHeight - 160), cv2.FONT_HERSHEY_TRIPLEX, 4, (255, 255, 255), 7, cv2.LINE_8)

def show_hp(bgImg, hp_img, x_offset, y_offset, x_resize, y_resize):
    hp_img = cv2.resize(hp_img, (x_resize, y_resize))
    rows, cols, channels = hp_img.shape
    roi = bgImg[y_offset: rows + y_offset, x_offset: x_offset + cols]

    img2gray = cv2.cvtColor(hp_img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    bgImg_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    hp_fg = cv2.bitwise_and(hp_img, hp_img, mask=mask)
    dst = cv2.add(bgImg_bg, hp_fg)
    bgImg[y_offset: y_offset + rows, x_offset:x_offset + cols] = dst

def match(config, match_list, centers, hp, play_time):
    BodyColors = [[255, 0, 0],
                  [0, 0, 0],
                  [0, 0, 0],
                  [255, 102, 0],
                  [255, 255, 0],
                  [0, 0, 0],
                  [255, 102, 0],
                  [255, 255, 0],
                  [0, 153, 0],
                  [0, 0, 0],
                  [0, 0, 255],
                  [0, 153, 0],
                  [0, 0, 0],
                  [0, 0, 255],
                  [0, 0, 0],
                  [0, 0, 0],
                  [0, 0, 0],
                  [0, 0, 0]]
    for i in match_list:  # 예)i = [4.0, 3.5, 4.2, F, 0 or PATH, (2, 3), (5, 12)] # 여기 ~ 33 !!
        if not i[4] == 0:
            pass
        for j in range(18):
            center = (int(centers[j][0]), int(centers[j][1]))
            color = [BodyColors[j][2],BodyColors[j][1],BodyColors[j][0]]
            config.named_window = cv2.circle(config.named_window,
                                             center, 10, color, thickness=-1)
        for j in i[5:]:  # 5 인덱스부터 끝까지 예)j = (2, 3)
            if i[0] - 3 < play_time < i[0]:
                circle_ratio = (play_time - (i[0] - 3)) / 3  # 3.7 ~ 최대 4.0초
                box_x = int((config.activation_areas[j[0]][0][0] + config.activation_areas[j[0]][1][0]) / 2)
                box_y = int((config.activation_areas[j[0]][0][1] + config.activation_areas[j[0]][1][1]) / 2)

                color = [BodyColors[j[1]][2], BodyColors[j[1]][1], BodyColors[j[1]][0]]

                config.named_window = cv2.circle(config.named_window,
                           (box_x, box_y), 20,
                           color, thickness=-1)
                config.named_window = cv2.circle(config.named_window,
                           (box_x, box_y),
                           60 - int(40 * circle_ratio), color, thickness=2)

            if int(config.activation_areas[j[0]][0][0]) < centers[j[1]][0] < int(config.activation_areas[j[0]][1][0]) and int(config.activation_areas[j[0]][0][1]) < centers[j[1]][1] < int(config.activation_areas[j[0]][1][1]): # ?? 범
                  # and i[4] == False: 지움 !!
                global score
                score += 5
                if hp < 10:
                    hp += 2
                if hp > 10:
                    hp = 10
                    match_list.remove(i)

    return match_list  # global화 시키기 위해서 return


def start_game(config, params):
    cam = cv2.VideoCapture(0)
    ret, named_window = cam.read()


    # 실루엣 맞추기: 카메라 키고, (사진 띄우고, point 4개 범위 안에 들어오면) X 3번 loop 나가
    # sil = ["1.png", "2.png", "3.png"] # 이런 식

    # 게임 시작: clear_menu, pause_menu, death_menu 중에 하나로 끝남
    pause_img = cv2.imread('images/pause.png')
    score_img = cv2.imread('images/score.png')
    gameover_img = cv2.imread('images/gameover.png')

    # 목숨 관련 변수들
    hp_x = config.imWidth//2 + 400
    hp_y = config.imHeight//2 - 345
    hp_yy = config.imHeight//2 - 300
    hp_w = 50
    hp_h = 42
    hp_image = cv2.imread('images/heart.png')

    w = 432
    h = 368
    e = TfPoseEstimator(get_graph_path('mobilenet_thin'), target_size=(w, h), trt_bool=str2bool("False"))

    global score
    while True:  # restart 하면 여기로 돌아오지 (실루엣 다시 안 해도 됨)
        params["restart"] = False
        hp = 10 # death까지의 목숨(?) (10번 못 맞추면 death_menu)
        cur_order = 0
        # params

        score = 0

        game_patterns = [] # 재구성할 리스트

        for i in params["patterns"]: # ex) i = [4.0, 0, 0, 3, 0, 0, 12, 0, 0, 0] 여기 ~ 89 !!
            list = []
            if i[10]:
                time1 = i[0] - 6.6
                time2 = i[0]
            else:
                time1 = i[0] - 3 # 여기 ~ 81!!
                time2 = i[0] + 1
            list.extend([i[0], time1, time2, False, i[10]])
            # 구역 9개에 대해서 리스트에다가 (영역, 부위) 튜플을 원소로 append
            for j in range(1, 10): # j = 1 ~ 9
                if i[j]:
                    list.append(tuple([j - 1, i[j] - 1]))
            game_patterns.append(list)

        # params["patterns"][0] = [4,0, 0, 0, 3, 0, 0, 12, 0, 0, 0]
        #   -> game_patterns[0] = [4.0, 3.5, 4.2, False, (2, 3), (5, 12)]
        match_list = [] # 주어진 시간 안에 해당되는, match 해볼 규칙들

        #a = input('Press...')

        start_time = time.time()
        resume_time = 0.0
        resume_start = 0.0
        play_music(params["song"], 0)
        while True: # game play

            ret, named_window = cam.read()
            config.named_window = cv2.resize(named_window, dsize=(1312, 736), interpolation=cv2.INTER_AREA)
            config.named_window = cv2.flip(config.named_window, 1)
            print(named_window.shape)
            humans = e.inference(named_window, resize_to_default=(w > 0 and h > 0), upsample_size=4.0) # 4 / 1 ??
            if not humans:
                continue

            human = humans[0]

            image_h, image_w = config.named_window.shape[:2]
            centers = []
            for i in range(common.CocoPart.Background.value):
                if i not in human.body_parts.keys():
                    centers.append((0, 0))
                else:
                    body_part = human.body_parts[i]
                    center = (image_w - int(body_part.x * image_w + 0.5), int(body_part.y * image_h + 0.5))
                    centers.append(center)


            # 실루엣
            play_time = time.time() - start_time  # 플레이 시간 측정
            pattern = game_patterns[cur_order]

            # 어떤 규칙이 time1을 지나면 & 아직 match_list에 없으면(= 첫번째 조건 만족해도 중복 append 방지 위해)
            if game_patterns[cur_order][1] < play_time and game_patterns[cur_order] not in match_list:
                match_list.append(game_patterns[cur_order])
                # cur_pattern = Pattern()
                cur_order += 1
                if cur_order > len(game_patterns) - 1:
                    cur_order = len(game_patterns) - 1
            if match_list:
                # centers resize, flip
                match_list = match(config, match_list, centers, hp, play_time)
            if match_list and match_list[0][2] < play_time: # and 아직 있으면
                hp -= 1
                del match_list[0] # 고침!! 항상 [0]일 테니끼 right?
                # match_list.remove(game_patterns[cur_order]) 도 됨

            cv2.putText(config.named_window, 'score:', (int(config.imWidth / 2 - 600), int(config.imHeight / 2 - 300)), cv2.FONT_HERSHEY_PLAIN, 4,
                        (255, 255, 255), 7, cv2.LINE_8)
            cv2.putText(config.named_window, '%d' % score, (int(config.imWidth / 2 - 600), int(config.imHeight / 2 - 250)), cv2.FONT_HERSHEY_PLAIN, 4,
                        (255, 255, 255), 7, cv2.LINE_8)

            if cur_order == len(game_patterns): # 이런 식
                config.named_window = score_img
                clear_menu(params, score)

            if cv2.waitKey(1) & 0xFF == ord('p'):
                params["exit"] = True
                # mixer.music.stop()
                # config._window = pause_img
                # resume_start = time.time()
                # # while 문 밖에서 선언해서 global 선언 해줘야됨
                # resume_time = pause_menu(play_time, params, resume_start)

            if hp <= 0 or play_time > game_patterns[len(game_patterns) - 1][2] + 5:
                mixer.music.stop()
                death_menu(params)


            if params["exit"] == True:
                break
            if params["restart"] == True: # 같은 게임 다시 시작
                break
            if params["menu"] == True:
                break

            for i in range(hp):
                if i < 5:
                    show_hp(config.named_window, hp_image, hp_x + i * hp_w, hp_y, hp_w, hp_h)
                if i >= 5:
                    show_hp(config.named_window, hp_image, hp_x + (i - 5) * hp_w, hp_yy, hp_w, hp_h)

            cv2.imshow('McgBcg', config.named_window) #image_h, image_w

        if params["exit"] == True:
            break
        if params["menu"] == True:
            break


def clear_menu(params, score): # 게임 잘 끝냈을 때

    play_sound(sound_applause)
    # show score
    cv2.putText(config.named_window, '%d' % score, (int(config.imWidth / 2 - 390), int(config.imHeight / 2 + 90)), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 7, (0,0,0), 15, cv2.LINE_8)
    cv2.putText(config.named_window, '%d'%score, (200, 480), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 7, (255,255,255), 15, cv2.LINE_8)
    cv2.imshow('McgBcg!', config.named_window)

    a = cv2.waitKey(0)
    while True:
        if a & 0xFF == ord('1'):
            play_sound(sound_effect2)
            params["menu"] = True
            print("menu")
            break
        if a & 0xFF == ord('1'):
            play_sound(sound_effect2)
            params["restart"] = True
            print("restart")
            break
        if a & 0xFF == ord('1'):
            play_sound(sound_effect2)
            params["exit"] = True
            print("exit")
            break
#
# def pause_menu(play_time, params, resume_start):
#
#     cv2.imshow('Pause', config.named_window)
#
#     a = cv2.waitKey(0)
#
#     if a & 0xFF == ord('1'):# resume (이어서; 싱크 맞추기 어려운 작업)
#         play_sound(sound_effect2)
#         print('resume')
#         play_music(params["song"], play_time - 5) # 5초 전부터 재생
#         return time.time() - resume_start
#
#     if a & 0xFF == ord('2'): # restart
#         play_sound(sound_effect2)
#         print('restart')
#         params["restart"] = True
#
#     if a & 0xFF == ord('3'): # menu
#         play_sound(sound_effect2)
#         print('menu')
#         params["menu"] = True
#
#     if a & 0xFF == ord('4'): # exit
#         play_sound(sound_effect2)
#         print('exit')
#         params["exit"] = True


def death_menu(params): # 너무 못해서 알아서 게임이 멈춤
    play_sound(sound_disappointed)
    image = cv2.imread('images/gameover.png')
    while True:
        a = cv2.waitKey(1)
        cv2.imshow('McgBcg', image)
        if a & 0xFF == ord('1'): # restart
            play_sound(sound_effect2)
            print('restart')
            params["restart"] = True
            break
        if a & 0xFF == ord('2'): # menu
            play_sound(sound_effect2)
            print('menu')
            params["menu"] = True
            break
        if a & 0xFF == ord('3'): # exit
            play_sound(sound_effect2)
            print('exit')
            params["exit"] = True
            break
    cv2.destroyAllWindows()