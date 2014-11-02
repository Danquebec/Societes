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

from os import listdir
from pygame import image

def load_images():
    images_loaded = {}
    for png_file in [f[:-4] for f in listdir('../art') if f[-4:] == '.png']:
        images_loaded[png_file] = image.load(
                '../art/{}.png'.format(png_file))
    for png_file in [f[:-4] for f in listdir('../art/biomes') if f[-4:] == '.png']:
        images_loaded[png_file] = image.load(
                '../art/biomes/{}.png'.format(png_file)).convert()
    return images_loaded
