# -*- coding: utf-8 -*-

from code.game import Game
from code.maze import parseMazeTextFile

# Number of actions that will cost each level
effectiveAction = {
    "easy1": 170,
    "easy2": 170,
    "easy3": 220,

    "medium1": 230,
    "medium2": 200,
    "medium3": 180,

    "hard1": 350,
    "hard2": 350,
    "hard3": 220,

    "big1": 2400,
}

def debug(fileName, stepByStep=False):
    maze_str = parseMazeTextFile(fileName)
    game = Game(maze_str, True, stepByStep)
    game.startGame()

def test(filesName):
    success = 0

    effectivenessN = 0
    effectiveness = 0

    print("Test :")
    for fileName in filesName:
        maze_str = parseMazeTextFile(fileName)
        game = Game(maze_str, False)
        won, actions, steps = game.startGame()
        s = ""
        s += " - {} : ".format(fileName)

        curEffectiveness = 0

        if fileName in effectiveAction:
            effectivenessN += 1

        if won:
            s += " \tOK ({} actions en {} étapes)".format(actions, steps)
            success += 1

            # Compute efficiency score
            if fileName in effectiveAction:
                estimatedAction = effectiveAction[fileName]
                if actions <= estimatedAction:
                    curEffectiveness = 1
                else:
                    curEffectiveness = 1 - (actions/estimatedAction - 1)
                    if curEffectiveness < 0:
                        curEffectiveness = 0
                s += " \tScore : {}%".format(round(curEffectiveness*100, 2))
        else:
            s += "KO"
        effectiveness += curEffectiveness
        print(s)
    print()
    if effectivenessN > 0:
        score = round(100*effectiveness/effectivenessN, 2)
        print("Réussi : {}/{} \tScore : {}%".format(success, len(filesName), score))
    else:
        print("Réussi : {}/{}".format(success, len(filesName)))
