# -*- coding: utf-8 -*-

from code.player import Player
from code.tile import TILE

def parseMazeTextFile(fileName):
    mazeStr = []
    w = -1
    h = 0
    # Parse the text file
    with open("maze/" + fileName + ".txt") as mazeTxt:
        for line in mazeTxt:
            lenLineStriped = len(line.strip("\n"))
            if w == -1:
                w = lenLineStriped
            elif w != lenLineStriped:
                raise ValueError("Your maze is not rectangular")
            mazeLine = []
            for char in line:
                if char in (".", " "):
                    mazeLine.append(TILE.free)
                elif char == "X":
                    mazeLine.append(TILE.wall)
            mazeStr.append(mazeLine)
            h += 1
    # Automatically add the player on the bottom left, goal on top right and walls on side
    mazeStr[h-1][0] = "J"
    mazeStr[0][w-1] = "G"
    ## Vertical lines on each side
    for line in mazeStr:
        line.insert(0, TILE.wall)
        line.append(TILE.wall)
    ## Horizontal on top and bottom
    mazeStr.insert(0, [TILE.wall for _ in range(w+2)])
    mazeStr.append([TILE.wall for _ in range(w + 2)])
    return mazeStr


def transp(mazeStr):
    return [[mazeStr[j][i] for j in range(len(mazeStr))] for i in range(len(mazeStr[0]))]


class Maze:
    def __init__(self, maze):
        self._maze = maze
        self._player = None

        self._initPlayer()

    def _initPlayer(self):
        found = False
        for i in range(len(self._maze)):
            line = self._maze[i]
            for j in range(len(line)):
                tile = line[j]
                if tile == TILE.player:
                    if found:
                        raise ValueError("Their is more than one player")
                    self._player = Player(self, j, i)
                    self._maze[i][j] = TILE.free
                    found = True
        if not found:
            raise ValueError("Their is no player")

    def getPlayer(self):
        return self._player

    def getWidth(self):
        return len(self._maze[0])

    def getHeight(self):
        return len(self._maze)

    def getTileAtPosition(self, x, y):
        return self._maze[y][x]

    def isTileAtPosition(self, x, y, tile):
        return self.getTileAtPosition(x, y) == tile

    def isPlayerOnGoal(self):
        player = self.getPlayer()
        return self.isTileAtPosition(player.getX(), player.getY(), TILE.goal)

    def printMaze(self):
        player = self.getPlayer()
        s = ""
        for y in range(len(self._maze)):
            line = self._maze[y]
            for x in range(len(line)):
                tile = line[x]
                char = str(tile)
                if player.isPosition(x, y):
                    char = str(player)
                s += char
            s += "\n"
        print(s)