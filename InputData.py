class InputData:
    def __init__(self, num=1, text="", mark=0):
        self.num = int(num)
        self.text = text
        self.mark = int(mark)

    def setMark(self, mark):
        self.mark = mark

    def setText(self, text):
        self.text = text

    def setNum(self, num):
        self.num = num

    def __str__(self):
        res = str(self.num)
        res += "," + self.text
        res += "," + str(self.mark) + "\n"
        return res
