# -*- coding: utf-8 -*-

import random

"""
Exemple d'Intelligence artificielle,
va chaque étape le joueur à :
 1. 20% de chance de tourner à gauche 20% de chance de tourner à droite
 2. Avance devant
Comme elle est très aléatoire, elle à peu de chance d'arriver à la sortie dans le temps imparti
"""
def stepRandom(game):
    r = random.randint(0, 100)
    if r <= 20:
        game.turnLeft()
    elif r >= 80:
        game.turnRight()
    game.moveForward()


"""
Exemple d'Intelligence artificielle montré dans la présentation,
Elle est très mauvaise et ne permetra pas de résoudre la plupart des labyrinthes,
mais tu peux t'en servir comme modème pour commencer
"""
def stepExample(game):
    if game.isFreeForward() or game.isGoalForward():
        game.moveForward()
    else:
        if game.direction() == "up":
            game.turnRight()
        else:
            game.turnLeft()


"""
Définis l'action qu'effectuera le joueur à chaque étape
"""
def step(game):
    stepExample(game)


