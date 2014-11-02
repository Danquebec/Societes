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

import gui
import event
import loader
import world
import humans

FPS = 40


def main():
    '''Declares variables, loads images, loads the game map, and starts
the game loop.'''
    global FPSCLOCK
    FPSCLOCK = pygame.time.Clock()

    # “mouse” is the position of the mouse cursor.
    # “left clicked”, “left mouse down”, “right clicked” and “right
    # mouse down” are all about the mouse buttons.
    # “key up” is when a general character key of the keyboard was
    # pressed.
    # “shift” is when shift is down.
    # “arrow key up” is when an arrow key has been pressed.
    player_input = {'mouse':(0, 0),
                    'left clicked': False, 'left mouse down':False,
                    'right clicked':False, 'right mouse down':False,
                    'key up':None, 'shift':False,
                    'arrow key up': None}

    gui.set_mode()
    pygame.display.set_caption('Sociétés')

    start_load = time()
    images_loaded = loader.load_images()
    print('Images loaded!  Time spent:{}'.format(time() - start_load))
    map_ = world.Map()  # game map
    print('Map instanced! Time spent: {}'.format(time() - start_load))
    world_time = world.Time()  # what time is it?

    # list of nomad groups on the game map
    list_of_nomad_groups = humans.place_test_stuff()

    event.set_allowed()

    dialog_box = gui.DialogBox()

    main_loop(player_input, images_loaded, map_, world_time,
              list_of_nomad_groups, dialog_box)


def main_loop(player_input, images_loaded, map_, world_time,
              list_of_nomad_groups, dialog_box, selected_cell=None,
              selected_object=None):
    ''''''
    while True:



        ### that which is reinitiated at each tick ###

        player_input['left clicked']  = False
        player_input['right clicked'] = False
        player_input['key up']        = None
        player_input['arrow key up']  = None
        # clicked object will be used when the player right clicks
        clicked_object                = None
        # this one is everytime an object is selected
        new_selected_object           = False



        ### draw ###

        gui.fill()
        gui.draw_cells(images_loaded, map_.array)
        gui.draw_objects(images_loaded, list_of_nomad_groups)
        gui.draw_grid()
        if selected_object:
            gui.draw_field_of_move(images_loaded, map_.array,
                                   list_of_nomad_groups[0].reachable_squares)
        if dialog_box.displayed:
            dialog_box.draw()



        ### player input ###

        player_input = event.handling(player_input)



        ### result of player input ###

        if player_input['left clicked']:
            clicked_cell = gui.click_on_cell(player_input['mouse'])
            for group in list_of_nomad_groups:
                if group.pos == clicked_cell:
                    selected_object = group
                    new_selected_object = True
                    print('Group selected')
            if new_selected_object == False and selected_object:
                list_of_nomad_groups[0].move(clicked_cell)
                selected_object = None
            if dialog_box.displayed:
                dialog_box.destroy()


        if player_input['right clicked']:
            dialog_box.destroy()
            clicked_cell = gui.click_on_cell(player_input['mouse'])
            for group in list_of_nomad_groups:
                if group.pos == clicked_cell:
                    clicked_object = group
            dialog_box.create(selected_object, clicked_object,
                              player_input['mouse'])

        if player_input['key up']:
            if player_input['key up'] == 'Enter':
                if dialog_box.displayed:
                    if dialog_box.present_selected_surfaces[
                            dialog_box.selected
                            ] == dialog_box.selected_surfaces[0]:
                        dialog_box.destroy()
                        clicked_cell = gui.click_on_cell(player_input[
                            'mouse'])
                        print('cell:{},{}'.format(clicked_cell[0],
                              clicked_cell[1]))
                        print(map_.array[clicked_cell[0]][clicked_cell[1]])
                        print('')
                    elif dialog_box.present_selected_surfaces[
                            dialog_box.selected
                            ] == dialog_box.selected_surfaces[1]:
                        dialog_box.destroy()
                        clicked_cell = gui.click_on_cell(player_input[
                            'mouse'])
                        for group in list_of_nomad_groups:
                            if group.pos == clicked_cell:
                                print(group)
                    elif dialog_box.present_selected_surfaces[
                            dialog_box.selected
                            ] == dialog_box.selected_surfaces[2]:
                        list_of_nomad_groups[0].move(clicked_cell)
                        
                else:
                    humans.end_of_turn(list_of_nomad_groups, map_.array)
                    world_time.pass_one_month()


            if player_input['key up'] == 's':
                print('Changer la spécialisation à :')
                print('x: annuler')
                print('p: petit gibier')
                for value, animal in enumerate(world.animals):
                    print('{}: {}'.format(value, animal))
                choice = raw_input('> ')
                if choice == 'x':
                    pass
                if choice == 'p':
                    list_of_nomad_groups[0].change_specialization_to(
                        'small game')
                else:
                    try:
                        list_of_nomad_groups[0].change_specialization_to(
                            world.animals[int(choice)])
                    except IndexError:
                        pass
                print('')

            if player_input['key up'] == 'c':
                print('Commencer à chasser :')
                print('x: annuler')
                print('p: petit gibier')
                choice = raw_input('> ')
                if choice == 'x':
                    pass
                if choice == 'p':
                    list_of_nomad_groups[0].change_hunting_to('small game')
                print('')

            if player_input['key up'] == 'i':
                print('Changer l’industrie à :')
                print('x: annuler')
                print('a: arcs et flêches')
                print('j: javelots')
                choice = raw_input('> ')
                if choice == 'x':
                    pass
                if choice == 'a':
                    list_of_nomad_groups[0].change_industry_to('bows')
                if choice == 'j':
                    list_of_nomad_groups[0].change_industry_to('javelins')
                print('')

        if player_input['arrow key up']:
            if dialog_box.displayed:
                dialog_box.change_selection(player_input['arrow key up'])
            else:
                pass



        ### an object has just been selected ###

        if new_selected_object:
            if selected_object == list_of_nomad_groups[0]:
                list_of_nomad_groups[0].field_of_move(map_.array)

        pygame.display.update()
        #print(FPSCLOCK.get_fps())
        FPSCLOCK.tick(FPS)


main()
