from main import step
from maze import Maze
from player import Player, DIRECTION
from tile import TILE


class Game:
    def __init__(self, maze_str, debug=False, stepByStep=False):
        self._debug = debug
        self._stepByStep = stepByStep
        self._stepN = 0
        self._action_point = 0
        self._maze = Maze(maze_str)
        self._player: Player = self._maze.getPlayer()

    def startGame(self):
        self._stepN = 0
        self._action_point = 0
        self._won = False

        for self._stepN in range(1, 1000):
            step(self) # User defined

            if self._debug:
                self.printMaze()

            if self._maze.isPlayerOnGoal():
                self._won = True
                break

        if self._debug:
            if self._won:
                print("Bravo! (", self._action_point, "actions )")
            else:
                print("Echec! Tu as dépassé le nombre d'actions permises")
        return (self._won, self._action_point, self._stepN)

    def moveForward(self):
        self._action_point += 5
        self._player.moveForward()

    def turnLeft(self):
        self._action_point += 2
        self._player.turnLeft()

    def turnRight(self):
        self._action_point += 2
        self._player.turnRight()

    def isFreeForward(self):
        self._action_point += 1
        return self._player.isForwardTile(TILE.free)

    def isGoalForward(self):
        self._action_point += 1
        return self._player.isForwardTile(TILE.goal)

    def direction(self):
        self._action_point += 0
        dir = self._player.getDirection()
        if dir == DIRECTION.right:
            return "right"
        elif dir == DIRECTION.down:
            return "down"
        elif dir == DIRECTION.up:
            return "up"
        elif dir == DIRECTION.left:
            return "left"

    def printMaze(self):
        if self._debug:
            print("Etape {} ({} actions): ".format(self._stepN, self._action_point))
            self._maze.printMaze()
            if self._stepByStep:
                input("( press enter to continue ... )")
            print()