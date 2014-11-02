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

from random import random
from time import time # for test

# quantity of effort asked
making_bows = 3
making_javelins = 1

max_hunting_effort = 10

# bonus at hunting small game if your group is specialized in
# hunting small game.
small_game_specialization_bonus = 1.7

# growth of population in a group
low_growth = 1.0004
medium_growth = 1.0008
high_growth = 1.0016


class NomadGroup(object):
    move_pts = 60 # normaly, 250
    present_move_pts = move_pts
    growth = medium_growth
    hunting = None
    specialization = None
    industry = None
    hunting_effort = max_hunting_effort
    reachable_squares = 199999

    def __init__(self, is_hero, pos, pop):
        self.is_hero = is_hero
        self.pos     = pos
        self.pop     = pop
        self.food    = self.pop

    def __str__(self):
        return '''pop = {}
growth = {}
food = {}
hunting = {}
specialization = {}
industry = {}
hunting_effort = {}'''.format(self.pop, self.growth, self.food, self.hunting,
self.specialization, self.industry, self.hunting_effort)

    def change_hunting_to(self, animal):
        self.hunting = animal

    def change_industry_to(self, weapon):
        '''First, it removes the removes the malus to the effort at
hunting. Then, it defines which weapon is made, in self.industry. And
finally, it adds the malus to the effort at hunting.'''
        if self.industry == 'bows':
            self.hunting_effort += making_bows
        if self.industry == 'javelins':
            self.hunting_effort += making_javelins
        self.industry = weapon
        if what == 'bows':
            self.hunting_effort -= making_bows
        if what == 'javelins':
            self.hunting_effort -= making_javelins

    def change_specialization_to(self, animal):
        self.specialization = animal

    def gather(self, region):
        food_gathered = int(round((region['vegetation']*0.00001) * self.pop))
        self.food += food_gathered
        print('Vous avez obtenu {} points de nourriture par la ceui{}'.format(
              food_gathered, 'llette.'))

    def fish(self):
        # TODO
        pass

    def hunt(self, region):

        def hunt_small_game(bonus):
            return int(round(
                       (
                       (
                       ((region['small_game']*0.00001)*bonus)*self.pop
                       )/max_hunting_effort
                       )*self.hunting_effort)
                       )

        if self.hunting == 'small game':
            if self.specialization == 'small game':
                if self.industry == 'bows':
                    food_gathered = hunt_small_game(
                                    small_game_specialization_bonus)
                if self.industry == 'javelins':
                    print('Ce n’est pas possible de chasser le peti{}'.format(
                          't gibier avec des lances. Le petit gibie{}'.format(
                          'r sera donc chassé avec des outils de base.')))
                    food_gathered = hunt_small_game(1)
            if self.specialization != 'small game':
                food_gathered = hunt_small_game(1)
            self.food += food_gathered
            print('Vous avez obtenu {} points de nourriture par la{}.'.format(
                  food_gathered, ' chasse au petit gibier.'''))

    def grow(self):
        '''Result is the quantity of new adults this month. If it is
equal or superior to one, let’s say it is 2.83, it will add 2 to
self.pop, and that will leave 83% chance of there being another one.
So a random() function will be called to determine if there’s an
additional adult.
If it is inferior to 1, it will simply check whether if there’s a
new adult or not by calling a random() function and comparing it
to the digits after the dot. So 0.43 means there’s 43% chance of there
being a new adult this month.
Additional pop is what will be returned. It will be added to self.pop.
The function does not add directly to self.pop because the next
method called is eat(). The month end’s methods must be finished before
updating self.pop.'''
        result = (self.pop * self.growth) - self.pop
        if result >= 1:
            inted_result = int(result)
            chance_of_another_one = inted_result - result
            if random() <= chance_of_another_one:
                add_to_inted_result = 1
            else:
                add_to_inted_result = 0
            additional_pop = inted_result + add_to_inted_result
            if (inted_result + add_to_inted_result) == 1:
                print('Une jeune personne de votre bande est devenu{}'.format(
                      'e un adulte.'))
            else:
                print('{} personnes de votre bande sont devenues des '.format(
                      inted_result + add_to_inted_result, 'adultes.'))
        if result < 1:
            # result is the chance of there being a new adult this month
            if random() <= result:
                additional_pop = 1
                print('Une jeune personne de votre bande est devenu{}'.format(
                      'e un adulte.'))
            else:
                additional_pop = 0
        return additional_pop

    def eat(self):
        if self.food / float(self.pop) < 0.5:
            pass # TODO: Enter in famine
        if (self.food / float(self.pop) >= 0.5 and
                self.food / float(self.pop) < 1):
            self.growth = low_growth
        if (self.food / float(self.pop) >= 1 and
                self.food / float(self.pop) < 2):
            self.growth = medium_growth
        if self.food / float(self.pop) > 2:
            self.growth = high_growth
        print('')

    def field_of_move(self, array):
        '''“squares” is the dictionary that tells the number of move
points left for each pos.
“to_move_from” is a list that serves as an index for squares. It is
used once we reached surrounding positions from a given position, for
using these surrounding positions as new starting positions to move to
other surrounding positions.
“pos_reached” is a the list we want out of that method. It will be used
to tell the player which cells he can reach with his unit and to
prevent him from going to cells his unit cannot reach.'''

        def add_pos(squares, pos, direction, move_pts, to_move_from, pos_reached):
            '''First, it reduces the move_pts by the cost of the
movement. Then it checks whether move_pts went under 0 or not. If it
did, the function ends, since the unit cannot reach this cell. If it
is 0 or higher, the unit reached the cell.
It then checks if “squares” already has a move_pts value for this cell
that is lower than the move_pts we have right now. If it has, we add
the move_pts we have right now in place of the other move_pts, since
the first one is higher (so we reached this cell with less movement).
If there’s no move_pts value for this cell yet (it’s the first time we
reach this cell), we check whether or not it is outside the map, then
we add the move_pts value to this new cell in “squares”.
In each of these cases, it will also add a new position to start from
(in “to_move_from”, and a new position in pos_reached.'''
            # we are supposed to look at the region’s terrain type,
            # but for now it will be without
            # it will be 21 pts, or 32 pts in diagonal
            if direction in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                move_pts -= 23
            else: # diagonal
                move_pts -= 32
            if move_pts < 0:
                return squares, to_move_from, pos_reached
            explored_pos = [pos[0]+direction[0],
                            pos[1]+direction[1]]
            # if the square is already marked, check if the value
            # is lower than the move_pts value. If it is, mark it with
            # the move_pts value.
            # If it is not marked, mark it with the move_pts value.
            try:
                if move_pts > squares[str(explored_pos)]:
                    squares[str(explored_pos)] = move_pts
                    to_move_from.append(explored_pos)
                    pos_reached.append(explored_pos)
            except KeyError:
                if explored_pos[0] >= 0 and explored_pos[1] >= 0: # if not outside map
                    squares[str(explored_pos)] = move_pts
                    to_move_from.append(explored_pos)
                    pos_reached.append(explored_pos)
            return squares, to_move_from, pos_reached

        move_pts = self.move_pts
        pos = self.pos
        directions = [(0,  1), (0, -1), (1,  0), (-1,  0),
                      (1,  1), (1, -1), (-1, 1), (-1, -1)]

        squares = {}

        squares[str(pos)] = move_pts
        pos_reached = [] # pos plural

        to_move_from = [pos]

        number_of_squares = 0 # for test

        a = time()

        while True:
            if to_move_from: # are there movements to make left?
                pos = to_move_from.pop(0)
                move_pts = squares[str(pos)]
                
                for direction in directions:
                    try:
                        # if it’s not water 
                        if array[pos[0]+direction[0]][
                                 pos[1]+direction[1]][
                                 'biome'][0] != 12:
                            squares, to_move_from, pos_reached = add_pos(
                                    squares, pos, direction, move_pts, to_move_from, pos_reached)
                            number_of_squares += 1
                            a = time()
                    except IndexError:
                        pass
            else:
                break
        self.reachable_squares = pos_reached

    def move(self, clicked_cell):
        print('move')


def place_test_stuff():
    list_of_nomad_groups = []
    list_of_nomad_groups.append(NomadGroup(True,  [0,0], 20))
    list_of_nomad_groups.append(NomadGroup(False, [1,0], 20))
    return list_of_nomad_groups


def end_of_turn(list_of_nomad_groups, array):
    '''For each nomad group, it removes their food, makes them gather
in their region and makes them hunt in their region.
It then figures how much more pop they will have at the end of the
turn.
And then, it makes them eat the food they have acquired in their
hunting and gathering.
Finally, it updates the population number of the nomad group.'''
    for group in list_of_nomad_groups:
        group.food = 0
        region = array[group.pos[0]][group.pos[1]]
        group.gather(region)
        if group.hunting:
            group.hunt(region)
        additional_pop = group.grow()
        group.eat()
        group.pop += additional_pop
