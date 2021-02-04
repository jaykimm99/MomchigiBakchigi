# MomchigiBakchigi

Most of the motion-based games on the market require players to purchase extra devices such as motion controllers and sensors. However, they can actually enjoy motion games with just one webcam if motion sensor is replaced by pose estimation algorithm. We developed a webcam-based rhythm game in which players tag circles on the screen with their body parts.</br>

We used https://github.com/ildoonet/tf-pose-estimation as our base architecture.

Demo: ![sample1.gif](./etcs/sample1.gif)

## Install

See [install.md](./etcs/install.md)


## [파일 설명]
| File | Description |
|:--   |:--   |
|Rythmgame.py | Proceeds the game by capturing motion and scoring points. |
|run_webcam.py | Main function that controls the overall game flow. |
|utils.py | Functions for game settings. |
|sunset_glow.xlsx | Excel file with game patterns we set. |
