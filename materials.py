#! /usr/bin/env python
# -*- coding: utf-8 -*-

from solid.utils import *
import behaviours as bh
from dotmap import DotMap

DUPONT_PITCH = 2.54
epsilon = 0.1
DUPONT_WALL_THICKNESS = 0.5
DUPONT_LENGTH = 10
LIB = 'D:/OneDrive/home/3D Objects/lib/'


def logo(direction='xz', size=10, depth=1, center=False):
    """Screw mount with chamfer on one corner

    direction:  orientation of mount first letter is direction of hole, second is direction of face,
                any combination of x, y, z
    size:       dimensions of the logo
    depth:      depth of the logo in the surface
    center:     set True to not offset assembly to the origin/direction

    returns DotMap containing assembly and information about the assembly,
        use screw_mount_chamfer().assembly to access object
    """
    x = size
    y = size
    z = depth

    assembly = color('red')(translate([-x/2, -y/2, -z/2])(resize([x, y])((linear_extrude(height=z+EPSILON))(import_dxf(file=LIB + 'InfinitycliffLogo.dxf')))))

    modification = [1, 1, -1]

#    if direction in ['xz', '-x-z', 'x-y', 'y-z', 'yx', '-y-x', '-yz' 'z-x', 'zy', '-z-y']:
#        modification = [-1, 1, 1]

    rotation = bh.spin(direction)
    if not center:
        translation = bh.origin(x, y, z, direction, modification)
    else:
        translation = [0, 0, 0]

    return DotMap({'assembly': rotate(rotation)(translate(translation)(assembly)),
                   'length': z,
                   'width':  x,
                   'height': y})

def dupont_connector(size=(2, 2), pitch=DUPONT_PITCH, length=DUPONT_LENGTH, dc_wall_thickness=DUPONT_WALL_THICKNESS):
    dc = union()
    dc_unit = cube([pitch, pitch, length]) - translate([dc_wall_thickness, dc_wall_thickness, -epsilon])(
                                                cube([pitch - dc_wall_thickness * 2, pitch - dc_wall_thickness * 2,
                                                      length + epsilon * 2]))

    for x in range(size[0]):
        for y in range(size[1]):
            dc.add(forward(y * (pitch - dc_wall_thickness))(
                   right(x * (pitch - dc_wall_thickness))(
                        dc_unit)))

    return color([0.6, 0.6, 0.6])(dc)


def wire(length=40, gauge=22, size=(1, 1), pitch=DUPONT_PITCH):
    dia = 1.5 if gauge == 22 else 0.1
    wire_ = union()
    for x in range(size[0]):
        for y in range(size[1]):
            wire_.add(
                translate([x * (pitch - DUPONT_WALL_THICKNESS), y * (pitch - DUPONT_WALL_THICKNESS), 0])(
                    cylinder(h=length, d=dia, segments=32)))

    return color([1, 0, 0])(wire_)


def jumper_wire(wire_length=40, size=(2, 1), pitch=DUPONT_PITCH, conn_length=10, wire_gauge=22):
    return union()(
                    dupont_connector(size=size, length=conn_length),
                    translate([0, 0, wire_length + conn_length])(
                        dupont_connector(size=size, length=conn_length)),
                    translate([pitch/2, pitch/2, conn_length])(
                        wire(wire_length, wire_gauge, size, pitch))
                    )


if __name__ == '__main__':
    # -------------------------------
    # MATERIALS
    # -------------------------------

    # obj = dupont_connector(size=(2, 3))
    # obj = wire(size=[3, 3])
    obj = logo(size=10, depth=1).assembly

    scad_render_to_file(obj, '../lib/materials.solid.scad')
