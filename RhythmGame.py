import cv2
import time
from utils import *
from statistics import median_high
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path
import tf_pose.common as common

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

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

# called every frame; checks if the player scored
def match(config, match_list, centers, hp, play_time, score):
    BodyColors = common.TestColor.CocoColors

    for i in match_list:
        if not i[4] == 0:
            pass
        for j in range(18):
            center = (int(centers[j][0]), int(centers[j][1]))
            color = [BodyColors[j][2],BodyColors[j][1],BodyColors[j][0]]
            config.named_window = cv2.circle(config.named_window,
                                             center, 10, color, thickness=-1)
        for j in i[5:]:
            if i[0] - 3 < play_time < i[0]:
                circle_ratio = (play_time - (i[0] - 3)) / 3
                box_x = int((config.activation_areas[j[0]][0][0] + config.activation_areas[j[0]][1][0]) / 2)
                box_y = int((config.activation_areas[j[0]][0][1] + config.activation_areas[j[0]][1][1]) / 2)

                color = [BodyColors[j[1]][2], BodyColors[j[1]][1], BodyColors[j[1]][0]]

                config.named_window = cv2.circle(config.named_window,
                           (box_x, box_y), 20,
                           color, thickness=-1)
                config.named_window = cv2.circle(config.named_window,
                           (box_x, box_y),
                           60 - int(40 * circle_ratio), color, thickness=2)

            if int(config.activation_areas[j[0]][0][0]) < centers[j[1]][0] < int(config.activation_areas[j[0]][1][0]) and int(config.activation_areas[j[0]][0][1]) < centers[j[1]][1] < int(config.activation_areas[j[0]][1][1]):
                score += 5
                if hp < 10:
                    hp += 2
                if hp > 10:
                    hp = 10
                    match_list.remove(i)

    return match_list


def start_game(config, params):
    cam = cv2.VideoCapture(0)
    ret, named_window = cam.read()


    # hp(health point) attributes
    hp_x = config.imWidth//2 + 400
    hp_y = config.imHeight//2 - 345
    hp_yy = config.imHeight//2 - 300
    hp_w = 50
    hp_h = 42
    hp_image = cv2.imread('images/heart.png')
    score_img = cv2.imread('images/score.png')

    w = 432
    h = 368
    e = TfPoseEstimator(get_graph_path('mobilenet_thin'), target_size=(w, h), trt_bool=str2bool("False"))

    while True:
        params["restart"] = False
        hp = 10
        cur_order = 0
        score = 0

        game_patterns = []

        for i in params["patterns"]:
            list = []
            if i[10]:
                time1 = i[0] - 6.6
                time2 = i[0]
            else:
                time1 = i[0] - 3
                time2 = i[0] + 1
            list.extend([i[0], time1, time2, False, i[10]])

            for j in range(1, 10): # j = 1 ~ 9
                if i[j]:
                    list.append(tuple([j - 1, i[j] - 1]))
            game_patterns.append(list)

        match_list = [] # sets to be checked for scoring; reset each frame

        start_time = time.time()
        play_music(params["song"], 0)

        while True: # game play
            ret, named_window = cam.read()
            config.named_window = cv2.resize(named_window, dsize=(1312, 736), interpolation=cv2.INTER_AREA)
            config.named_window = cv2.flip(config.named_window, 1)
            print(named_window.shape)
            humans = e.inference(named_window, resize_to_default=(w > 0 and h > 0), upsample_size=4.0)
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

            play_time = time.time() - start_time
            pattern = game_patterns[cur_order]

            if game_patterns[cur_order][1] < play_time and game_patterns[cur_order] not in match_list:
                match_list.append(game_patterns[cur_order])
                cur_order += 1
                if cur_order > len(game_patterns) - 1:
                    cur_order = len(game_patterns) - 1
            if match_list:
                match_list = match(config, match_list, centers, hp, play_time, score)
            if match_list and match_list[0][2] < play_time: # and 아직 있으면
                hp -= 1
                del match_list[0]

            cv2.putText(config.named_window, 'score:', (int(config.imWidth / 2 - 600), int(config.imHeight / 2 - 300)), cv2.FONT_HERSHEY_PLAIN, 4,
                        (255, 255, 255), 7, cv2.LINE_8)
            cv2.putText(config.named_window, '%d' % score, (int(config.imWidth / 2 - 600), int(config.imHeight / 2 - 250)), cv2.FONT_HERSHEY_PLAIN, 4,
                        (255, 255, 255), 7, cv2.LINE_8)

            if cur_order == len(game_patterns):
                config.named_window = score_img
                clear_menu(params, score)

            if cv2.waitKey(1) & 0xFF == ord('p'):
                params["exit"] = True

            if hp <= 0 or play_time > game_patterns[len(game_patterns) - 1][2] + 5:
                mixer.music.stop()
                death_menu(params)


            if params["exit"] == True:
                break
            if params["restart"] == True:
                break
            if params["menu"] == True:
                break

            for i in range(hp):
                if i < 5:
                    show_hp(config.named_window, hp_image, hp_x + i * hp_w, hp_y, hp_w, hp_h)
                if i >= 5:
                    show_hp(config.named_window, hp_image, hp_x + (i - 5) * hp_w, hp_yy, hp_w, hp_h)

            cv2.imshow('McgBcg', config.named_window)

        if params["exit"] == True:
            break
        if params["menu"] == True:
            break

# Well Done!
def clear_menu(params, score):
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

# Game Over..
def death_menu(params):
    play_sound(sound_disappointed)
    gameover_img = cv2.imread('images/gameover.png')
    config.named_window = gameover_img
    while True:
        a = cv2.waitKey(1)
        cv2.imshow('McgBcg', config.named_window)
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