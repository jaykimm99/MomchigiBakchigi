import argparse
import logging

from RhythmGame import *
from config import GameConfig
from utils import *

import cv2



if __name__ == '__main__':
    # config 안에 박
    config = GameConfig()
    params = {'diff': None, 'patterns': None, 'song': None, 'exit': None, 'menu': None, 'restart': None}

    # config.named_window = cv2.namedWindow('Momchigi')

    logger = logging.getLogger('TfPoseEstimator-WebCam')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    print(1)

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

    while True:
        main_menu(config, params)
        if params["exit"] is True:  # main menu에서 종료 버튼
            cv2.destroyAllWindows()
            break
        print('load_pattern')
        load_pattern(config, params)
        print('load_song')
        load_song(config, params)
        print('start_game')
        start_game(config, params)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
