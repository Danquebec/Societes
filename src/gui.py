#!/usr/bin/python
# -*- coding:utf-8 -*-

# Sociétés © 2015 Daniel Dumaresq
# e-mail: danquebec01@yahoo.ca
# Jabber: danquebec@linkmauve.fr

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame
from time import time

pygame.init()

cell_size = 64

map_screen_size_x = 10 * cell_size
map_screen_size_y = 10 * cell_size


class Camera(object):
    '''That doesn’t work yet. Link Mauve, don’t look into it.'''
    speed = 0.15
    tick = False
    moving = False
    toward_where = None

    def __init__(self, pos):
        self.pos = pos

    def move(self):
        def outside_map(axis):
            if axis < 0:
                return True
            else:
                return False
        if self.toward_where == 'right':
                self.pos[0] += 1
        elif self.toward_where == 'left':
            if not outside_map(self.pos[0]-1):
                self.pos[0] -= 1
        elif self.toward_where == 'down':
            self.pos[1] += 1
        elif self.toward_where == 'up':
            if not outside_map(self.pos[1]-1):
                self.pos[1] -= 1
        print(self.pos)

    def start_moving(self):
        self.move()
        self.tick = time()
        self.moving = True

    def continue_moving(self):
        if time() - self.tick >= self.speed:
            self.move()
            self.tick = time()


class DialogBox(object):
    '''Builds a dialog box that appears on right click. It allows the
player to make various contextual actions.
Each element in the dialog box has a background color (bg_color) and
a font color (font_color). These colors change when they are selected
(in other words, when the player has moved his cursor to an element)
(bg_selected_color, font_selected_color).
These elements are rendered first then stored in tupples (surfaces,
selected_surfaces).
A list, “rects”, is created for the rectangles of the elements.
The width of the dialog box is the width of the widest element.
The topleft is where the player has clicked. It is the topleft of the
dialog box.
The dialog box is contextual, so the dialog box that appears is
different depending on what the player has clicked on. This is the use
of the “present” lists (“present_surfaces”, “present_selected_surfaces”
and “present_rects”). These are the contextual lists containing the
pertinent elements of the lists “surfaces”, “selected_surfaces” and
“rects”.
The player moves up or down in the dialog box to choose his prefered
option. The position at which he is in the dialog box is kept track of
by the variable “selected”. It will serve as an index position for the
lists.'''

    displayed = False

    font = pygame.font.Font('freesansbold.ttf', 13)

    bg_color =            (255, 255, 255)
    bg_selected_color =   (0, 0, 255)
    font_color =          (0, 0, 0)
    font_selected_color = (255, 255, 255)

    surfaces =          (font.render(u'Informations sur la région', True,
                            font_color, bg_color),
                        font.render(u'Informations sur l’unité', True,
                            font_color, bg_color),
                        font.render(u'Déplacer l’unité à cet endroit', True,
                            font_color, bg_color))

    selected_surfaces = (font.render(u'Informations sur la région', True,
                            font_selected_color, bg_selected_color),
                        font.render(u'Informations sur l’unité', True,
                            font_selected_color, bg_selected_color),
                        font.render(u'Déplacer l’unité à cet endroit', True,
                            font_selected_color, bg_selected_color))

    rects = [element.get_rect() for element in surfaces]

    width = max([element.width for element in rects])

    topleft = None

    present_surfaces =          []
    present_selected_surfaces = []
    present_rects =             []

    selected = None

    def create(self, selected_object, clicked_object, click_pos):
        '''Assigns a topleft position, from the position of the click,
and loads the “present” lists with the pertinent elements from the base
lists.'''
        self.topleft = click_pos
        self.present_surfaces.append(self.surfaces[0])
        self.present_selected_surfaces.append(self.selected_surfaces[0])
        self.present_rects.append(self.rects[0])
        try:
            if clicked_object.__class__.__name__ == 'NomadGroup':
                self.present_surfaces.append(self.surfaces[1])
                self.present_selected_surfaces.append(
                    self.selected_surfaces[1])
                self.present_rects.append(self.rects[1])
        except AttributeError:
            pass
        try:
            if selected_object.__class__.__name__ == 'NomadGroup':
                self.present_surfaces.append(self.surfaces[2])
                self.present_selected_surfaces.append(
                    self.selected_surfaces[2])
                self.present_rects.append(self.rects[2])
        except AttributeError:
            pass
        self.displayed = True
        self.selected = 0

    def draw(self):
        '''Places each of the option rectangles of the dialog box at
their right positions. Draws them with the right color depending on
their status (selected or not).'''
        # from the first rectangle of the dialog box to the last
        for index, pixel in enumerate(xrange(
                    self.topleft[1],
                    (self.topleft[1] + sum([rect.height for rect in
                     self.present_rects])),
                    self.present_rects[0].height)):
            #try:
            self.present_rects[index].topleft = (self.topleft[0], pixel)
            #except IndexError:
            #    break
            if index == self.selected:
                DISPLAYSURF.blit(self.present_selected_surfaces[index],
                                 self.present_rects[index])
            else:
                DISPLAYSURF.blit(self.present_surfaces[index],
                                 self.present_rects[index])

    def destroy(self):
        '''Destroys the dialog box.'''
        self.present_surfaces =          []
        self.present_selected_surfaces = []
        self.present_rects =             []
        self.selected =                  None
        self.displayed =                 False

    def change_selection(self, move_key_up):
        '''Depending on the movement key pressed by the player, moves
him up or down in the dialog box.'''
        if move_key_up == 'down':
            if self.selected+1 > len(self.present_surfaces)-1:
                self.selected = 0
            else:
                self.selected += 1
        if move_key_up == 'up':
            if self.selected-1 < 0:
                self.selected = len(self.present_surfaces)-1
            else:
                self.selected -= 1


def set_mode():
    '''Sets the mode.'''
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode((map_screen_size_x,
                                          map_screen_size_y),
                                          pygame.locals.HWSURFACE)


def fill():
    '''Paints everything in pitch black.'''
    # TODO: No need to fill everything at each FPS tick. Make something
    # more intelligent.
    DISPLAYSURF.fill((0, 0, 0))


def draw_cells(images_loaded, array):
    '''Draws the cells on the map.'''
    for x_nbr, x in enumerate(array):
        for y_nbr, y in enumerate(x):
            try:
                # creates the name of the biome’s image
                str_biome = str(array[x_nbr][y_nbr]['biome'][0]) + ',' + \
                            str(array[x_nbr][y_nbr]['biome'][1])
                DISPLAYSURF.blit(images_loaded[str_biome],
                                 ((x_nbr*cell_size),
                                 (y_nbr*cell_size)))
            except IndexError:
                pass


def draw_objects(images_loaded, nomad_groups):
    '''Draws the objects on the map'''
    for nomad_group in nomad_groups:
        try:
            DISPLAYSURF.blit(images_loaded['hunter-gatherers'],
                             (((nomad_group.pos[0])*cell_size),
                             ((nomad_group.pos[1])*cell_size)))
        except IndexError:
            pass


def draw_grid():
    '''Draws a grid separating the cells in the map.'''
    for x in xrange(0, map_screen_size_x, cell_size):
        pygame.draw.line(DISPLAYSURF, (0, 0, 0),
                         (x, 0), (x, map_screen_size_y), 1)
    for y in xrange(0, map_screen_size_y, cell_size):
        pygame.draw.line(DISPLAYSURF, (0, 0, 0),
                         (0, y), (map_screen_size_x, y), 1)


def click_on_cell(mouse):
    '''If the player clicks inside the map, this function will return
the cell it clicked on. If he or she clicks left of the map, it will
print “Interface” for no reason.'''
    if mouse[0] < map_screen_size_x:
        selected_cell = [0, 0]
        selected_cell[0] = int(mouse[0] / cell_size)
        selected_cell[1] = int(mouse[1] / cell_size)
        return selected_cell
    else:
        print('Interface')


def draw_field_of_move(images_loaded, array, reachable_squares):
    '''Draws stripes on the cells that the selected unit can’t
reach.'''
    for x_index, x in enumerate(array):
        for y_index, cell in enumerate(x):
            if [x_index, y_index] not in reachable_squares:
                DISPLAYSURF.blit(images_loaded['unreachable_squares'],
                 ((x_index*cell_size), (y_index*cell_size)))
