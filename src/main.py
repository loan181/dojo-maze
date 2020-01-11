# -*- coding: utf-8 -*-

from code import test as test

# Temps d'attente entre deux étapes
SLEEP_TIME = 0.3

"""
Début du code
C'est ici que tu décidera quoi tester (un seul niveau ? tous ? étape par étape?) 
"""
if __name__ == '__main__':
    # Fichiers sur lesquels on veut tester notre code d'IA
    filesName = (
        "easy1",
        "easy2",

        "medium1",
        "medium2",

        "hard1",
        "hard2",
    )

    test.debug("example", False) # Permet de tester sur un seul fichier
    #test.test(filesName)        # Permet de tester plusieurs fichier (avec score d'efficacité)

