import random
from time import sleep
import sys
import os


class ChristmasTree():

    def __init__(self, height):
        self.height = height
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

    def _add_bulbs_in_row(self, part, index, find):
        number_bulbs = 1
        if 5 <= index < 8: number_bulbs = 2
        elif 8 <= index < 15: number_bulbs = 3
        elif 15 <= index < 22: number_bulbs = 4
        elif 22 <= index: number_bulbs = 5

        counter = []
        for index, char in enumerate(part[1:len(part)-1 ]):
            if char.endswith(find):
                counter.append(index)
        new_part = list(part)

        for i in range(number_bulbs):
            new_part[random.choice(counter)] = self._generate_bulb()
        new_part = "".join(new_part)
        return new_part

    def _add_bulbs(self):
        new_tree = []
        for i, part in enumerate(self.tree):
            if 2 <= i < len(self.tree) - 1:
                if i % 2 == 0:
                    new_part = self._add_bulbs_in_row(part, i, "\\")
                    new_tree.append(new_part)
                else:
                    new_part = self._add_bulbs_in_row(part, i, "/")
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
        top = " ".ljust(self.height-2) + self._generate_bulb(self.yellow) + "\n".ljust(self.height-2) + self._generate_bulb(self.yellow)*3 + "\n".ljust(self.height-2)
        trunk = "".ljust(self.height-4) + "[___]\n"
        sides = {
            "start": "/",
            "end": "_\ \n"
        }
        self.tree.append(top)
        for i in range(self.height-3):
            mid = "_/" * i if i % 2 == 0 else "_\\" * i
            mid_row = sides["start"] + mid + sides["end"].ljust(self.height - i)
            self.tree.append(mid_row)
        self.tree.append(trunk)

        self.tree = self._add_bulbs()
        
    def print_tree(self):
        print(self._assemble_tree(), end="\r")


if __name__ == "__main__":
    height = int(sys.argv[1])
    height = height if height > 4 else 5
    tree = ChristmasTree(height)
    while(True):
        os.system('cls' if os.name == 'nt' else 'clear')
        tree.generate_tree()
        tree.print_tree()
        sleep(1)        
