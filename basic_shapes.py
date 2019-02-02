#! /usr/bin/env python
# -*- coding: utf-8 -*-

from solid.utils import *


def rounded_box(width, length, height, radius=0):
    return hull()(
            translate([width / 2 - radius, length / 2 - radius, height / 2])(
                    cylinder(h=height, r=radius, center=True)),
            translate([-(width / 2 - radius), length / 2 - radius, height / 2])(
                    cylinder(h=height, r=radius, center=True)),
            translate([width / 2 - radius, -(length / 2 - radius), height / 2])(
                    cylinder(h=height, r=radius, center=True)),
            translate([-(width / 2 - radius), -(length / 2 - radius), height / 2])(
                    cylinder(h=height, r=radius, center=True)))