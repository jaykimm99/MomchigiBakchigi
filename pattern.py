class Pattern:
    def __init__(self):
        self.count = 0
        self.pairs = []
    def getPairs(self, my_list):
        for i in range(len(my_list[1:9])): # i 0~8 / (0 0 3 0 0 12 0 0 0)
            if my_list[i+1] > 0:
                self.pairs.append(tuple([i, my_list[i]])) # (2,3) (5,12) / activation area라는 리스트는 0부터 시작이니까 그거에 맞게
        return
