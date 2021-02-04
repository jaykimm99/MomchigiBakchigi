# MomchigiBakchigi

Most of the motion games on the market require players to purchase extra devices such as motion controllers and sensors. However, just one PC with a webcam is enough if the motion sensor is replaced by pose estimation algorithm.</br>

We developed a webcam-based rhythm game in which players use their body parts to tag circles that show up on the screen.</br>

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
