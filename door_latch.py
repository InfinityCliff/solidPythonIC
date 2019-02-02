#! /usr/bin/env python
# -*- coding: utf-8 -*-

from solid.utils import *
from basic_shapes import *

HOLE_OFFSET = 45/2+8.5/2  # = 26.75
LENGTH = 70
WIDTH = 20
HEIGHT = 8
D = 10
OPEN_WIDTH = 40
epsilon = 0.01
OPEN_OFFSET = HOLE_OFFSET + D/2 - OPEN_WIDTH /2

def hole():
    return cylinder(d=D, h=HEIGHT + epsilon * 2)


def door_latch():
    return rounded_box(LENGTH, WIDTH, HEIGHT, 5) - down(epsilon)(left(HOLE_OFFSET)(hole())) - \
           right(OPEN_OFFSET)(back(3)(rounded_box(OPEN_WIDTH, D/2 + WIDTH / 2, HEIGHT, D/2))) - \
           back(WIDTH/2)(left(-OPEN_OFFSET+OPEN_WIDTH/2-D/2)(up(HEIGHT/2-epsilon)(cube([D, D, HEIGHT + epsilon*2], center=True)))) - \
           back(WIDTH / 2)(right(OPEN_OFFSET + OPEN_WIDTH / 2 - D/1.7)(up(HEIGHT / 2 - epsilon)(cube([D, D, HEIGHT + epsilon * 2], center=True)))) - \
           back(WIDTH/2)(right(OPEN_OFFSET - OPEN_WIDTH/2)(up(HEIGHT/2 + epsilon)(cube([D, D, HEIGHT + epsilon*2], center=True)))) + \
           color('red')(back(WIDTH/2-D/2)(right(OPEN_OFFSET - OPEN_WIDTH/2 - D/2)(hole())))



if __name__ == '__main__':
    latch = door_latch()
    scad_render_to_file(latch, '../door_latch.solid.scad')