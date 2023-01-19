import random
import scipy.stats as stats
import math
import matplotlib.pyplot as plt
import numpy as np


class ShapeLib:
    def __init__(self):
        self.paths = {}

    def generatePaths(self,count, min, max, sdMin, sdMax):
        for i in range(count):
            s = Shape(random.randint(min, max), random.randint(sdMin, sdMax))
            self.paths[s.distance] = s.lines

    def returnLines(self, start, end, min, max):
        lines = []
        length = self.length(start, end)
        accesstableLines, length = self.findSuitipleLines(length, min, max)
        for line in accesstableLines:
           lines.append(self.orientLine(line, start, np.arctan2(end[1]-start[1], end[0]-start[0])))

    def findSuitipleLines(self, length, min, max):
        accesstableLines = []
        minLenght, maxLenght = length - min, length - max
        for distance in self.paths:
            if  minLenght <= distance and maxLenght >= distance:
                accesstableLines.append(self.paths[distance])
        return accesstableLines, length

    def orientLine(self, line, start, facing):
        rotation = np.array([[math.cos(facing * np.pi), math.sin(facing * np.pi)],
                    [-math.sin(facing * np.pi), math.cos(facing * np.pi)]])
        return (line @ rotation) + start + np.array(math.cos(facing * np.pi), math.sin(facing * np.pi))

    def length(self, start, end):
        return math.sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2)

class Shape:
    def __init__(self, num_lines, sd):
        self.num_lines = num_lines
        self.lines = np.zeros((num_lines+1,2))
        self.facing = 0
        self.distance = 0
        self.sd = sd
        self.generate_lines()
        
    def generate_lines(self):
        a, b = -0.4, 0.4
        mu, sigma = 0.0, self.sd 
        dist = stats.truncnorm((a - mu) / sigma, (b - mu) / sigma, loc=mu, scale=sigma)
        values = dist.rvs(self.num_lines)
        for i,value in enumerate(values):
            self.facing += value
            self.lines[i+1][0], self.lines[i+1][1] = math.cos(self.facing * np.pi) + self.lines[i][0], math.sin(self.facing * np.pi)+ self.lines[i][1]
        self.distance = self.length()
    
    def length(self):
        return math.sqrt(self.lines[-1][0]**2 + self.lines[-1][1]**2)

    # def check_intersection(self, x1, y1, x2, y2):
    #     for i in range(len(self.lines)):
    #         x3, y3, x4, y4 = self.lines[i]
    #         if self.do_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    #             self.lines.pop()
    #             self.generate_lines()
    #             return

    # def do_intersect(self, x1, y1, x2, y2, x3, y3, x4, y4):
    #     denominator = ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    #     if denominator == 0:
    #         return False

    #     t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
    #     u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

    #     if 0 <= t <= 1 and 0 <= u <= 1:
    #         return True
    #     return False

    # def display_shape(self):
    #     for line in self.lines:
    #         print(line)

# lib = ShapeLib()
# lib.generatePaths(1000, 10, 30, 0.05, 0.2)
shape = Shape(10, 0.2)