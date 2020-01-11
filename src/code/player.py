# -*- coding: utf-8 -*-


from code.tile import TILE


class DIRECTION:
    right 	= "→"
    up 		= "↑"
    left 	= "←"
    down 	= "↓"

    _dirs = (right, up, left, down)

    def __init__(self, dir):
        self._dir = dir

    def _getIndexInDir(self):
        return self._dirs.index(self._dir)

    def rotateLeft(self):
        ind = self._getIndexInDir()
        self._dir = self._dirs[(ind+1) % len(self._dirs)]

    def rotateRight(self):
        ind = self._getIndexInDir()
        self._dir = self._dirs[(ind-1) % len(self._dirs)]

    def getForwardPosition(self, x, y):
        if self._dir == DIRECTION.right:
            return x + 1, y
        elif self._dir == DIRECTION.up:
            return x, y - 1
        elif self._dir == DIRECTION.left:
            return x - 1, y
        elif self._dir == DIRECTION.down:
            return x, y + 1

    def __str__(self):
        return self._dir

class Player:
    def __init__(self, maze, x, y):
        self._maze = maze
        self._x = x
        self._y = y

        self._direction = DIRECTION(DIRECTION.right)

    def isPosition(self, x, y):
        return self._x == x and self._y == y

    def isForwardTile(self, tile):
        forwardPos = self._direction.getForwardPosition(self._x, self._y)
        return self._maze.getTileAtPosition(forwardPos[0], forwardPos[1]) == tile

    def moveForward(self):
        forwardPos = self._direction.getForwardPosition(self._x, self._y)
        nextX, nextY = forwardPos
        forwardTile = self._maze.getTileAtPosition(nextX, nextY)
        if forwardTile in (TILE.free, TILE.goal):
            self._x, self._y = forwardPos

    def turnLeft(self):
        self._direction.rotateLeft()

    def turnRight(self):
        self._direction.rotateRight()

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def getDirection(self):
        return str(self._direction)

    def __str__(self):
        return str(self._direction)