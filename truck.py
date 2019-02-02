# -*- coding: utf-8 -*-

#from solid.utils import *
from parts import *
from solid_utils import *


class face_plate(General_Assembly):

    def __init__(self, *args, **kwargs):
        super().__init__(self, 'union', {})
        self.size = None
        self.length = None
        self. width = None
        self.height = None
        self.build()

    def build(self):
        WALL = 2.8
        x1 = 23.28
        x2 = x1 + 80.32
        x3 = x2 + 40
        x4 = 13
        y1 = 32
        y2 = y1 + 151
        y3 = y2 + y1
        y4 = 22
        y5 = 8
        print(y3)

        z1 = 12
        pin = rotate([0, 90, 0])(cylinder(h=11, d=5.2))
        tab = cube([x1, y1, WALL])
        assembly = (
                    translate([0, 0, 0])(tab) + translate([0, y2, 0])(tab) +
                    color('orange')(translate([x1-6, y4, 0])(cube([7, y3-y4*2, WALL]))) +
                    color('orange')(translate([x1, 0, 0])(cube([x2-x1, y3, WALL]))) +
                    color('green')(translate([x2, y4, 0])(rotate([0, 7, 0])(cube([x3-x2, y3-y4*2, WALL])))) +
                    color('blue')(translate([x3-WALL-0.3, y4, -24.4])(cube([WALL, y3-y4*2, 20]))) +
                    translate([x3-1, y3/2 - 78.22, -z1])(pin) +
                    translate([x3-1, y3/2, -12])(pin) +
                    translate([x3-1, y3/2 + 78.22, -z1])(pin) -
                    color('red')(translate([x1-6 + WALL, y4+WALL, -20])(cube([x3-x1-WALL*2+6-0.4, y3-y4*2-WALL*2, 30]))) -
                    color('red')(translate([x4, y5, -1])(cylinder(h=WALL+2, d=6.82))) -
                    color('red')(translate([x4, y3-y5, -1])(cylinder(h=WALL + 2, d=6.82)))
                    )

        self.size = [sum([x1, x2, x3]), sum([y1, y2, y3]), WALL]
        self.length = sum([x1, x2, x3])
        self. width = sum([y1, y2, y3])
        self.height = WALL
        print(self.size)
        print(scad_size()(assembly))
        self.add_assembly(assembly)


def panel_storage():
    return face_plate()


if __name__ == '__main__':
    a = panel_storage()

    scad_render_to_file(a,  '../truck.solid.scad',
                        file_header='$fn=20;')
