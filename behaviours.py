#! /usr/bin/env python
# -*- coding: utf-8 -*-

from solid.utils import *


def rotate_in_place(assembly, origin_, rotation):
    return translate(origin_)(rotate(rotation)(translate(list(map(lambda x: x * -1, origin_)))(assembly)))


#def position(assembly, direction, size, center):
#    rotation = spin(direction)
#    if not center:
#        translation = origin(size[0], size[1], size[2], direction)
#    else:
#        translation = [0, 0, 0]
#    return attributes((rotate(rotation)(translate(translation)(assembly))), direction, size)


if __name__ == '__main__':
    a = cylinder(r=5, h=30)
    scad_render_to_file(a, '../behaviors.solid.scad', file_header='$fn=20;')