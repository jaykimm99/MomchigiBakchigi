import argparse
import logging

from RhythmGame import *
from config import GameConfig
from utils import *

import cv2


if __name__ == '__main__':
    config = GameConfig()
    params = {'diff': None, 'patterns': None, 'song': None, 'exit': None, 'menu': None, 'restart': None}

    logger = logging.getLogger('TfPoseEstimator-WebCam')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
    parser.add_argument('--camera', type=int, default=0)

    parser.add_argument('--resize', type=str, default='0x0',
                        help='if provided, resize images before they are processed. default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ')
    parser.add_argument('--resize-out-ratio', type=float, default=4.0,
                        help='if provided, resize heatmaps before they are post-processed. default=1.0')

    parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin / mobilenet_v2_large / mobilenet_v2_small')
    parser.add_argument('--show-process', type=bool, default=False,
                        help='for debug purpose, if enabled, speed for inference is dropped.')
    
    parser.add_argument('--tensorrt', type=str, default="False",
                        help='for tensorrt process.')
    args = parser.parse_args()

    # load pattern and song, start game
    while True:
        try:
            main_menu(config, params)
        except:
            print("Failed to load main_menu. 메인 메뉴 불러오기 실패")

        if params["exit"] is True:
            cv2.destroyAllWindows()
            break

        try:
            print('load_pattern')
            load_pattern(config, params)
            print('load_song')
            load_song(config, params)
            print('start_game')
            start_game(config, params)
        except:
            print("Failed to load the game data. 게임 정보 불러오기 실패")

    cv2.waitKey(0)
    cv2.destroyAllWindows()
