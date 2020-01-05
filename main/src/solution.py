### TEACHER CODE ###

"""
Ia qui longera le mur de droite tant qu'elle pourra.

Cette IA trouvera TOUJOURS la sortie, mais n'est pas toujours efficace
"""
def stepLonger(game):
    game.turnRight()
    if game.isFreeForward() or game.isGoalForward():
        game.moveForward()
    else:
        game.turnLeft()
        if game.isFreeForward() or game.isGoalForward():
            game.moveForward()
        else:
            game.turnLeft()


"""
Utilise une heuristique pour diriger le joueur.
Etant donné que la solution se trouve en haut à droite et qu'on commence en bas à gauche,
on peut partir de l'hypothèse qu'un mouvement vers la droite/haut nous rapprochera de l'objectif
Cette IA se coince facilement dans les culs de sacs, elle ne trouve donc pas toujours la sortie
"""
def stepSmart(game):
    dir = game.direction()

    if dir in ("right", "up"):
        if game.isFreeForward() or game.isGoalForward():
            game.moveForward()
        else:
            contourner(game)
    else:
        if dir == "left":
            game.turnRight()
        elif dir == "down":
            game.turnLeft()


def contourner(game):
    dir = game.direction()

    if dir == "right":
        game.turnLeft()
        while not game.isFreeForward():
            game.turnLeft()
            if game.isFreeForward():
                game.moveForward()
            else:
                game.turnLeft()
            game.turnRight()

    elif dir == "up":
        game.turnRight()
        while not game.isFreeForward():
            game.turnRight()
            if game.isFreeForward():
                game.moveForward()
            else:
                game.turnRight()
            game.turnLeft()

### END OF TEACHER CODE ###