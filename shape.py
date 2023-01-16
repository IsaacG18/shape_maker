import random

class Shape:
    def __init__(self, num_lines):
        self.num_lines = num_lines
        self.lines = []
        self.generate_lines()

    def generate_lines(self):
        for i in range(self.num_lines):
            x1, y1, x2, y2 = random.randint(0, 100), random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)
            self.lines.append((x1, y1, x2, y2))
            self.check_intersection(x1, y1, x2, y2)

    def check_intersection(self, x1, y1, x2, y2):
        for i in range(len(self.lines)):
            x3, y3, x4, y4 = self.lines[i]
            if self.do_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
                self.lines.pop()
                self.generate_lines()
                return

    def do_intersect(self, x1, y1, x2, y2, x3, y3, x4, y4):
        denominator = ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        if denominator == 0:
            return False

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

        if 0 <= t <= 1 and 0 <= u <= 1:
            return True
        return False

    def display_shape(self):
        for line in self.lines:
            print(line)

shape = Shape(10)
shape.display_shape()