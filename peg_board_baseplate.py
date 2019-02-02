#! /usr/bin/env python
# -*- coding: utf-8 -*-

# from solid import *
from solid.utils import *

include("../lib/peg_board_dimensions.scad")


# Baseplate dimensions
basePlateThickness = 1       # Thickness of plate - can be 0 if pins are attached to back of piece
basePlateHeight = 0          # Height in number of holes
basePlateWidth = 2           # Width in number of holes
basePlateBottomExtension = 5 # Distance base plate will extend below bottom pin
basePlateSideExtension = 0.5
basePlateTopExtension = 0.5

# Pin Parameters
addBottomPins = True        # True to add pins to bottom: false only pins/clips on top
topPinsAll = False          # True to add pins/clips to all top hole locations: false only pins/clips on corners
bottomPinsAll = False       # True to add pins to all bottom hole locations: false only pins on corners


clip_height = 2 * hole_size + 2

epsilon = 0.1


def basePlateTrueWidth():
    return (basePlateWidth - 1) * hole_spacing + hole_sizeini