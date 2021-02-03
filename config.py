class GameConfig:
    def __init__(self):
        self.imWidth = 1312 # 우리가 정할 크기
        self.imHeight = 736
        self.camera = 0
        self.resize_out_ratio = 4.0 # 이 밑으로 나도 뭔지 모르는데 일두씨 estimator.py 에서 보고 쓴거
        self.model = 'mobilenet_thin'
        self.show_process = False
        self.tensorrt = "False"
        self.named_window = 0 # 이건 우리가 쓸 창
        # self.activation_areas = [
        #             [(self.imWidth // 2 - 300, self.imHeight // 2 - 300), (self.imWidth // 2 - 200, self.imHeight // 2 - 200)],
        #             [(self.imWidth // 2 - 300, self.imHeight // 2 - 150), (self.imWidth // 2 - 200, self.imHeight // 2 - 50)],
        #             [(self.imWidth // 2 - 300, self.imHeight // 2), (self.imWidth // 2 - 200, self.imHeight // 2 + 100)],
        #             [(self.imWidth // 2 - 300, self.imHeight // 2 + 200), (self.imWidth // 2 - 200, self.imHeight // 2 + 300)],
        #             [(self.imWidth // 2 + 300, self.imHeight // 2 - 300), (self.imWidth // 2 + 200, self.imHeight // 2 - 200)],
        #             [(self.imWidth // 2 + 300, self.imHeight // 2 - 150), (self.imWidth // 2 + 200, self.imHeight // 2 - 50)],
        #             [(self.imWidth // 2 + 300, self.imHeight // 2), (self.imWidth // 2 + 200, self.imHeight // 2 + 100)],
        #             [(self.imWidth // 2 + 300, self.imHeight // 2 + 200), (self.imWidth // 2 + 200, self.imHeight // 2 + 300)],
        #             [(self.imWidth // 2 - 50, self.imHeight // 2 - 350), (self.imWidth // 2 + 50, self.imHeight // 2 - 250)]
        # ]

        self.activation_areas = [
                    [(self.imWidth // 2 - 300, self.imHeight // 2 - 300), (self.imWidth // 2 - 200, self.imHeight // 2 - 200)],
                    [(self.imWidth // 2 + 300, self.imHeight // 2 - 300), (self.imWidth // 2 + 200, self.imHeight // 2 - 200)],
                    [(self.imWidth // 2 - 300, self.imHeight // 2 - 150), (self.imWidth // 2 - 200, self.imHeight // 2 - 50)],
                    [(self.imWidth // 2 + 300, self.imHeight // 2 - 150), (self.imWidth // 2 + 200, self.imHeight // 2 - 50)],
                    [(self.imWidth // 2 + 300, self.imHeight // 2 - 300), (self.imWidth // 2 + 200, self.imHeight // 2 - 200)],
                    [(self.imWidth // 2 + 300, self.imHeight // 2), (self.imWidth // 2 + 200, self.imHeight // 2 + 100)],
                    [(self.imWidth // 2 + 300, self.imHeight // 2), (self.imWidth // 2 + 200, self.imHeight // 2 + 100)],
                    [(self.imWidth // 2 - 300, self.imHeight // 2 + 200), (self.imWidth // 2 - 200, self.imHeight // 2 + 300)],
                    [(self.imWidth // 2 - 50, self.imHeight // 2 - 350), (self.imWidth // 2 + 50, self.imHeight // 2 - 250)]
        ]