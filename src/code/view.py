# -*- coding: utf-8 -*-

import pygame
import math
import time
import sys
import os
import re
from code.tile import TILE
from code.player import DIRECTION

# Largeur de la fenêtre
WIDTH = 800
# Hauteur de la fenêtre
HEIGHT = 600
# Couleur (Rouge, Vert, Bleu) du fond du dessin
BACKGROUND_COLOR = (208, 208, 208)
# Couleur du texte dans l'en-tête
TEXT_COLOR = (48, 48, 48)
# Couleur du personnage du joueur
PLAYER_COLOR = (255, 200, 0)
# Répertoire où enregistrer les images png
SAVE_IMAGE_DIR = "./output"

class View:
    def __init__(self, maze):
        self._maze = maze # type: Maze
        self._width = maze.getWidth()
        self._height = maze.getHeight()

        # Initialise pygame
        pygame.init()

        # Supprime les images enregistrées lors d'une exécution passée
        self._cleanup_image_dir()
        self._image_counter = 0

        # Ouvre la fenêtre pygame pour le dessin
        self._screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self._screen.fill(BACKGROUND_COLOR)
        # Police pour les textes affichés
        self._font = pygame.font.Font(None, 25)

        self._computeScale()
        self._renderMaze()

    def _computeScale(self):
        (width, height) = self._screen.get_size()
        header_height = self._font.get_linesize() + 4
        height -= header_height
        scale_x = int(math.floor(width / self._width))
        scale_y = int(math.floor(height / self._height))
        self._scale = min(scale_x, scale_y)
        self._draw_width = self._width * self._scale
        self._draw_height = self._height * self._scale
        self._margin_top = int((height - self._draw_height) / 2) + header_height
        self._margin_left = int((width - self._draw_width) / 2)

    def _renderMaze(self):
        self._background = pygame.Surface((self._draw_width, self._draw_height))
        self._background.fill(BACKGROUND_COLOR)

        LIGHT_COLOR = (216, 216, 216)
        DARK_COLOR = (128, 128, 128)
        TILE_COLOR = (192, 192, 192)
        WALL_COLOR = (80, 80, 80)

        for y in range(self._height):
            tile_top = y * self._scale
            tile_bottom = (y + 1) * self._scale - 1
            for x in range(self._width):
                tile_left = x * self._scale
                tile_right = (x + 1) * self._scale - 1
                if self._maze.isTileAtPosition(x, y, TILE.wall):
                    rect = pygame.Rect(tile_left, tile_top, self._scale - 1, self._scale - 1)
                    pygame.draw.rect(self._background, WALL_COLOR, rect)
                else:
                    pygame.draw.line(self._background, LIGHT_COLOR, (tile_left, tile_top), (tile_right, tile_top))
                    pygame.draw.line(self._background, LIGHT_COLOR, (tile_left, tile_top), (tile_left, tile_bottom))
                    pygame.draw.line(self._background, DARK_COLOR, (tile_right, tile_top), (tile_right, tile_bottom))
                    pygame.draw.line(self._background, DARK_COLOR, (tile_left, tile_bottom), (tile_right, tile_bottom))
                    rect = pygame.Rect(tile_left + 1, tile_top + 1, self._scale - 3, self._scale - 3)
                    pygame.draw.rect(self._background, TILE_COLOR, rect)
                    if self._maze.isTileAtPosition(x, y, TILE.goal):
                        center = (tile_left + int(self._scale/2), tile_top + int(self._scale/2))
                        radius = math.floor(self._scale * 0.4)
                        pygame.draw.circle(self._background, (64, 255, 64), center, radius)
                        pygame.draw.circle(self._background, (0, 208, 0), center, radius, 1)

    def draw(self, step, action):
        self._screen.blit(self._background, (self._margin_left, self._margin_top))

        text = self._font.render("Etape {} ({} actions):".format(step, action), True, TEXT_COLOR)
        header_rect = (self._margin_left, 0, self._draw_width, self._margin_top)
        pygame.draw.rect(self._screen, BACKGROUND_COLOR, header_rect)
        self._screen.blit(text, (self._margin_left+2, 2))

        self._draw_player()

        pygame.display.flip()
        self._save_image()

    def _draw_player(self):
        player = self._maze.getPlayer()
        x = player.getX()
        y = player.getY()
        direction = player.getDirection()
        cell_x = int((x + 0.5) * self._scale) + self._margin_left
        cell_y = int((y + 0.5) * self._scale) + self._margin_top
        head = int(self._scale * 0.45)
        tail = int(self._scale * 0.4)
        wing = int(self._scale * 0.3)
        if direction == DIRECTION.up:
            points = [
                (cell_x-wing, cell_y+tail), (cell_x+wing, cell_y+tail), (cell_x, cell_y-head)
            ]
        if direction == DIRECTION.down:
            points = [
                (cell_x-wing, cell_y-tail), (cell_x+wing, cell_y-tail), (cell_x, cell_y+head)
            ]
        if direction == DIRECTION.left:
            points = [
                (cell_x+tail, cell_y+wing), (cell_x+tail, cell_y-wing), (cell_x-head, cell_y)
            ]
        if direction == DIRECTION.right:
            points = [
                (cell_x-tail, cell_y+wing), (cell_x-tail, cell_y-wing), (cell_x+head, cell_y)
            ]
        pygame.draw.polygon(self._screen, PLAYER_COLOR, points)

    def wait_key(self):
        """Wait until a key is pressed"""
        waiting = True
        while waiting:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit(1)
                waiting = False

    def escape_pressed(self):
        """Check if user pressed on escape"""
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit(1)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def _cleanup_image_dir(self):
        if not os.path.exists(SAVE_IMAGE_DIR):
            os.mkdir(SAVE_IMAGE_DIR)
        if not os.path.isdir(SAVE_IMAGE_DIR):
            return
        image_re = re.compile(r"^step\d+\.png$")
        for file in os.listdir(SAVE_IMAGE_DIR):
            if not image_re.match(file):
                continue
            full_path = os.path.join(SAVE_IMAGE_DIR, file)
            if not os.path.isfile(full_path):
                continue
            os.remove(full_path)

    def _save_image(self):
        """ Enregistre le contenu affiché à l'écran dans un fichier"""
        if os.path.isdir(SAVE_IMAGE_DIR):
            name = "step{i:03d}.png".format(i=self._image_counter)
            self._image_counter += 1
            filename = os.path.join(SAVE_IMAGE_DIR, name)
            pygame.image.save(self._screen, filename)
            """
            Une animation peut être créée avec la commande
            ffmpeg -y -framerate 10 -i output/step%03d.png maze.gif
            """
