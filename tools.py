#! /usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------
# TOOLS
# -------------------------------

# from solid import *
from solid.utils import *


def kobalt_screwdriver():
    h1=0
    h2 = 28
    h3 = 35
    h4 = 23
    dia = 50
    t = dia/2+10
    return union()(
        translate([0, 0, h1])(
            cylinder(h=h2, d1=26, d2=30)) +
        translate([0, 0, h1 + h2])(
            cylinder(h=h3, d1=30, d2=20)) +
        translate([0, 0, h1 + h2 + h3])(
            cylinder(h=18, d=30) -
            rotate_extrude(convexity=5)(
                translate([t, 0, 0])(
                    circle(d=dia)))))


def precision_screwdriver():

    h1 = 8
    h2 = 24
    h3 = 20
    h4 = 17
    h5 = 35

    return translate([0, 0, h1])(
            rotate([0, 180, 0])(
                union()(
                    color([0, 0, 0])(
                        cylinder(h=h1, r1=20 / 2, r2=11 / 2)) +
                    color([0, 0.35, 1])(
                        translate([0, 0, h1])(
                            cylinder(h=h2, r1=11 / 2, r2=8 / 2))) +
                    translate([0, 0, h1 + h2])(
                        cylinder(h=h2, r1=8 / 2, r2=11 / 2)) +
                    color([0, 0, 0])(
                        translate([0, 0, h1 + h2 * 2])(
                            cylinder(h=h3, r1=11 / 2, r2=11 / 2))) +
                    color([0, 0.35, 1])(
                        translate([0, 0, h1 + h2 * 2 + h3])(
                            cylinder(h=h4, r1=11 / 2, r2=7 / 2))) +
                    color([1, 1, 1])(
                        translate([0, 0, h1 + h2 * 2 + h3 + h4])(
                            cylinder(h=h5, r1=3 / 2, r2=3 / 2))))))


if __name__ == '__main__':

    # obj = kobalt_screwdriver()
    obj = precision_screwdriver()

    scad_render_to_file(obj, '../lib/tools.solid.scad')
