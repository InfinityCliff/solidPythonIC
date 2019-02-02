#! /usr/bin/env python
# -*- coding: utf-8 -*-

# from solid import *
from solid.utils import *

DRAWER_WIDTH = 50
DRAWER_LENGTH = 100
DRAWER_HEIGHT = 20
DRAWER_WALL_THICKNESS = 3
DRAWER_BOTTOM_THICKNESS = 3
DRAWER_CORNER_THICKNESS = 10  # 0 for square corners or less than or equal to wall_thickness for square inside corners
epsilon = 0.01


def clip(length, width=2, height=1, flip=False):
    clip_ = right(width/2)(
            union()(
            up(height / 2)(
                    cube([width, length, height], center=True)),
            right(3 * width / 8)(up(height * 1.5)(
                    cube([width / 4, length, height + 1], center=True)))))
    if flip:
        clip_ = mirror([1, 0, 0])(clip_)
    return clip_


def basic_box(width=DRAWER_WIDTH, length=DRAWER_LENGTH, height=DRAWER_HEIGHT, box_offset=0):
    return hull()(
            translate([width / 2 - box_offset, length / 2 - box_offset, height / 2])(
                    cylinder(h=height, r=box_offset, center=True)),
            translate([-(width / 2 - box_offset), length / 2 - box_offset, height / 2])(
                    cylinder(h=height, r=box_offset, center=True)),
            translate([width / 2 - box_offset, -(length / 2 - box_offset), height / 2])(
                    cylinder(h=height, r=box_offset, center=True)),
            translate([-(width / 2 - box_offset), -(length / 2 - box_offset), height / 2])(
                    cylinder(h=height, r=box_offset, center=True))
    )


def drawer_tray(width=DRAWER_WIDTH, length=DRAWER_LENGTH, height=DRAWER_HEIGHT,
                wall_thickness=3,
                bottom_thickness=3,
                corner_radius=5,
                left_clip="none",  # clips allowed values are none, over, under
                right_clip="none"):
    corner_radius = {True: 0.01, False: corner_radius}[corner_radius <= 0]  # check radius too small, set to 0.01
    corner_radius = {True: width / 2, False: corner_radius}[
        corner_radius >= width / 2]  # check radius too big, set to width/2
    # inner_offset = {True: wall_thickness, False: corner_radius}[corner_radius <= wall_thickness]
    inner_offset = {True: corner_radius - wall_thickness, False: 0.01}[corner_radius >= wall_thickness]

    dt = basic_box(width, length, height, corner_radius) - up(bottom_thickness)(
                                                                resize([width - wall_thickness*2,
                                                                        length-wall_thickness*2,
                                                                        height-bottom_thickness + epsilon])(
                                                                basic_box(width, length, height, inner_offset)))

    r_clip = right(width / 2)(clip(length=length-corner_radius*2, flip={"over": True, "under": False}[right_clip]))
    l_clip = left(width / 2)(clip(length=length - corner_radius * 2, flip={"over": False, "under": True}[left_clip]))

    dt = {"over": dt - r_clip, "under": dt + r_clip}[right_clip]
    dt = {"over": dt - l_clip, "under": dt + l_clip}[left_clip]
    return dt


if __name__ == '__main__':
    tray = drawer_tray(right_clip="under", left_clip="under")
    scad_render_to_file(tray, '../drawer_divider.solid.scad')
