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
from pygame.locals import *
import sys


def set_allowed():
    pygame.event.set_allowed([QUIT, MOUSEMOTION, MOUSEBUTTONDOWN,
                              MOUSEBUTTONUP, KEYDOWN, KEYUP])


def handling(player_input):
    '''Handles every event. It returns the updates of the mouse
position and of the state of the mouse (did it click? is the mouse
pressed?).'''
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            player_input['mouse'] = event.pos
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                player_input['left clicked'] = True
                player_input['left mouse down'] = True
            if event.button == 3:
                player_input['right clicked']= True
                player_input['right mouse down'] = True
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                player_input['left mouse down'] = False
            if event.button == 3:
                player_input['right mouse down'] = False
            mousex, mousey = event.pos
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                pass
            elif event.key == K_LEFT:
                pass
            elif event.key == K_DOWN:
                pass
            elif event.key == K_UP:
                pass
            elif event.key == 304:
                player_input['shift'] = True
        elif event.type == KEYUP:
            if event.key == K_t:
                player_input['key up'] = 't'
            elif event.key == K_a:
                player_input['key up'] = 'a'
            elif event.key == K_c:
                player_input['key up'] = 'c'
            elif event.key == K_e:
                player_input['key up'] = 'e'
            elif event.key == K_h:
                player_input['key up'] = 'h'
            elif event.key == K_i:
                player_input['key up'] = 'i'
            elif event.key == K_p:
                player_input['key up'] = 'p'
            elif event.key == K_m:
                player_input['key up'] = 'm'
            elif event.key == K_s:
                player_input['key up'] = 's'
            elif event.key == K_w:
                player_input['key up'] = 'w'
            elif event.key == K_v:
                player_input['key up'] = 'v'
            elif event.key == K_z:
                player_input['key up'] = 'z' # this is for tests
            elif event.key == 42: # K_0 bépo
                player_input['key up'] = 0
            elif event.key == 34: # K_1 bépo
                player_input['key up'] = 1
            elif event.key == 171: # K_2 bépo
                player_input['key up'] = 2
            elif event.key == 187: # K_3 bépo
                player_input['key up'] = 3
            elif event.key == 13: # Enter bépo
                player_input['key up'] = 'Enter'
            elif event.key == 304: # Shift
                player_input['shift'] = False
            elif event.key == K_RIGHT:
                player_input['arrow key up'] = 'right'
            elif event.key == K_LEFT:
                player_input['arrow key up'] = 'left'
            elif event.key == K_DOWN:
                player_input['arrow key up'] = 'down'
            elif event.key == K_UP:
                player_input['arrow key up'] = 'up'
            else:
                print(event.key)
    return player_input
