import random
from time import sleep
import sys
import os
import argparse

class ChristmasTree():

    def __init__(self, height):
        self.height = height if height > 4 else 5
        self.yellow = 93
        self.tree = []

    def _paint_bulb(self, bulb, c=None):
        colors = [91, 92, 93, 96, 95]
        if c == None: c = random.choice(colors)
        color = {
            "start": "\033[" + str(c)
            + "m",
            "end": "\033[0m"
        }
        return color["start"] + bulb + color["end"]

    def _generate_bulb(self, color=None):
        bulb = u'\u25cf'.encode('utf-8').decode("utf-8")
        return self._paint_bulb(bulb, color)

    def _add_bulbs_in_row(self, part, index, find, snow=False):
        number_bulbs = 1
        if 5    <= index < 8:  number_bulbs = 2
        elif 8  <= index < 15: number_bulbs = 3
        elif 15 <= index < 22: number_bulbs = 4
        elif 22 <= index: number_bulbs = 5
        counter = []
        for index, char in enumerate(part[1:len(part)-1]):
            if char.endswith(find):
                counter.append(index)
        new_part = list(part)
        if snow and len(counter) > 1 : counter.remove(counter[0])
        for i in range(number_bulbs):
            new_part[random.choice(counter)] = self._generate_bulb()
        new_part = "".join(new_part)
        return new_part

    def _add_bulbs(self, snow=False):
        find = { "start": "\\", "end": "/"}
        if snow:
            find = { "start": "/", "end": "\\"}
        new_tree = []
        for i, part in enumerate(self.tree):
            if 2 <= i < len(self.tree) - 1:
                if i % 2 == 0:
                    new_part = self._add_bulbs_in_row(part, i, find["start"], snow)
                    new_tree.append(new_part)
                else:
                    new_part = self._add_bulbs_in_row(part, i, find["end"], snow)
                    new_tree.append(new_part)
            else:
                new_tree.append(part)
        return new_tree

    def _assemble_tree(self):
        new_tree = ""
        for part in self.tree:
            new_tree += part
        return new_tree

    def generate_tree(self):
        self.tree = []
        top = " ".ljust(self.height-2) + self._generate_bulb(self.yellow).ljust(self.height-2) + "\n".ljust(self.height-2) + self._generate_bulb(self.yellow)*3 + "\n".ljust(self.height-2)
        trunk = "".ljust(self.height-4) + "[___]\n".ljust(self.height-4)
        sides = {
            "start": "/",
            "end": "_\\\n"
        }
        self.tree.append(top)
        for i in range(self.height-3):
            mid = "_/" * i if i % 2 == 0 else "_\\" * i
            mid_row = sides["start"] + mid + sides["end"].ljust(self.height -i-1)
            self.tree.append(mid_row)
        self.tree.append(trunk)

        self.tree = self._add_bulbs()
    
    def generate_tree_with_snow(self, trigger):
        self.tree = []
        snow = self.add_snow(trigger)
        sides = {
            "start": "/",
            "end": "_\\"
        }

        star_one = snow[0][:int(len(snow[0])/2)+1] + self._generate_bulb(self.yellow)   + snow[0][int(len(snow[0])/2):] + "\n"
        star_two = snow[1][:int(len(snow[1])/2)]   + self._generate_bulb(self.yellow)*3 + snow[1][int(len(snow[1])/2):] + "\n"
        
        boundary = len(snow[0])

        star_one = star_one[:-3] + "\n"
        star_two = star_two[:-4] + "\n"
        self.tree.append(star_one)
        self.tree.append(star_two)
        for i in range(self.height-3):
            new_snow = ""
            mid = "_/" * i if i % 2 == 0 else "_\\" * i
            mid_row = sides["start"] + mid + sides["end"]
            index = int(len(snow[i])/2-i)
            new_snow += snow[i][:index] + mid_row + snow[i][index:] + "\n"
            new_snow = new_snow[:boundary] + "\n"
            self.tree.append(new_snow)

        trunk = snow[-1][:int(len(snow[-1])/2)-1] + "[___]" + snow[-1][int(len(snow[-1])/2):] + "\n"
        trunk = trunk[:-5] + "\n"
        self.tree.append(trunk)

        self.tree = self._add_bulbs(True)

    def add_snow(self, trigger):
        snow = []
        for i in range(self.height):
            if trigger:
                snow.append("* " * self.height*2)
                trigger = not trigger
            else:
                snow.append(" *" * self.height*2)
                trigger = not trigger
        return snow

    def print_tree(self):
        print(self._assemble_tree(), end="\r")

    def run(self, snow=False):
        tree = ChristmasTree(self.height)
        trigger = True
        while(True):
            trigger = not trigger
            os.system('cls' if os.name == 'nt' else 'clear')
            if snow: tree.generate_tree_with_snow(trigger)
            else: tree.generate_tree()
            tree.print_tree()
            sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("height", help="Height of the tree")
    parser.add_argument("--snow", action="store_true", help="Adding animated snow")
    args = parser.parse_args()
    height = int(args.height)
    snow = args.snow

    ChristmasTree(height).run(snow)
