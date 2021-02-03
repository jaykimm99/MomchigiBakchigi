class Pattern:
    def __init__(self):
        self.count = 0
        self.pairs = []
    def getPairs(self, my_list):
        for i in range(len(my_list[1:9])):
            if my_list[i+1] > 0:
                self.pairs.append(tuple([i, my_list[i]]))
        return
