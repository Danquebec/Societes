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

import pickle

animals = ('Hémione', 'Gazelle', 'Chèvre', 'Oryx', 'Auroch', 'Cerf rouge')

# the preferred biomes are the entire group of biomes between the first
# mentionned biome and the last. So “(3,0), (4,2)“ includes:
# (3,0), (3,1), (3,2), (4,0), (4,1) and (4,2).
preferred_biomes_and_ecoregions = {
'Onager':{
'biomes':((3,0), (10,4)), 
'ecoregions':('Levant', 'Mesopotamia', 'Iran', 'Arabia', 'Central Asia', 'Baktria', 'Indus valley', 'Indian peninsula', 'Kurdistan')
},
'Gazelle':{
'biomes':((7,0), (10,5)),
'ecoregions':('Maghreb', 'Sahara', 'Arabia', 'Levant', 'Mesopotamia', 'Sinai')
},
'Goat':{
'biomes':((7,0), (8,5)),
'ecoregions':('Iran', 'Kurdistan', 'Anatolia')
},
'Oryx':{
'biomes':((7,0), (10,3)),
'ecoregions':('Southern Africa', 'Sinai', 'Levant', 'Kurdistan', 'Mesopotamia', 'Arabia')
},
'Auroch':{
'biomes':((4,1), (9,8)),
'ecoregions':('Maghreb', 'Levant', 'Mesopotamia', 'Iran', 'Indus valley', 'Indian peninsula', 'Ganges', 'Baktria', 'Kurdistan', 'Central Europe', 'Mongolia', 'Northern China', 'Korea', 'Anatolia', 'Greece', 'Hispanic peninsula', 'France', 'Germany', 'East Europe', 'Balkans', 'Italian peninsula', 'Sicilia', 'Danemark', 'Sweden', 'Great Britain')
},
'Red deer':((5,3), (8,8)),
'ecoregions':('Ireland', 'Great Britain', 'France', 'Hispanic peninsula', 'Maghreb', 'Italian peninsula', 'Sicily', 'Germany', 'Danemark', 'Sweden', 'Norway', 'East Europe', 'Balkans', 'Greece', 'Anatolia', 'Levant', 'Kurdistan', 'Armenia', 'Iran', 'Central Asia')}


class Region(object):
    '''This class represents a region, which corresponds to a cell on
the map.'''
    biome = (0,0)
    ecoregion = 'Levant' # for now
    max_vegetation = 0
    max_small_game = 0
    vegetation = 0
    small_game = 0

    def __str__(self):
        return 'biome : {}\nvégétation : {}\npetit gibier : {}'.format(
              self.biome, self.vegetation, self.small_game)

    def regenerate(self):
        '''Regenerates the vegetation and the small game population of
this region. The regeneration goes on progressively as time passes.
Not sure, but I think it doesn’t work yet.'''
        self.vegetation += self.max_vegetation / 50
        if self.vegetation > self.max_vegetation:
            self.vegetation = self.max_vegetation
        self.small_game += self.max_small_game / 50
        if self.smal_game > self.max_small_game:
            self.small_game = self.small_game


class Map():
    '''The class representing the map.'''
    def __init__(self):
        self.array = pickle.load(open('../map/map', 'rb'))

    def modify(self, image, pos):
        self.array[pos[0]][pos[1]] = image


class Time(object):
    year_of_beginning = -10000
    month_of_beginning = 0

    actual_year = year_of_beginning
    actual_month = month_of_beginning

    months_names = {1:'Février', 2:'Mars', 3:'Avril', 4:'Mai', 5:'Juin',
                    6:'Juillet', 7:'Août', 8:'Septembre', 9:'Octobre',
                    10:'Novembre', 11:'Décembre'}

    def pass_one_month(self):
        if self.actual_month+1 > 11:
            if self.actual_year +1 == 0:
                self.actual_year = 1 # no 0 in gregorian calendar
            else:
                self.actual_year += 1
            self.actual_month = 0
            print('L’année est {}. Janvier.\n'.format(self.actual_year))
        else:
            self.actual_month += 1
            for month in self.months_names:
                if self.actual_month == month:
                    month_name = self.months_names[month]
            print('L’année est {}.\n'.format(month_name))

'''
class AnimalGroup(object):
    food_pts_max = 100000
    food_pts = food_pts_max

    def __init__(self, pos, species):
        self.pos = pos
        self.species = species

    def regenerate(self):
        # TODO
        pass

    def move(self, array):
        




        possible_moves = []

        right = (self.pos[0+1], self.pos[1])
        left  = (self.pos[0-1], self.pos[1])
        down  = (self.pos[0], self.pos[1-1])
        up    = (self.pos[0], self.pos[1+1])

        try:
            if array[right[0]][right[1]]:
                possible_moves.append(right)
        except IndexError:
            pass
        try:
            if array[left[0]][left[1]]:
                possible_moves.append(left)
        except IndexError:
            pass
        try:
            if array[down[0]][down[1]]:
                possible_moves.append(down)
        except IndexError:
            pass
        try:
            if array[up[0]][up[1]]:
                possible_moves.append(up)
        except IndexError:
            pass

        if possible_moves == []:
            pass # can’t move
        else:
            direction = randchoice(possible_moves)
            self.pos = direction
'''
