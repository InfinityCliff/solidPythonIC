#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Original:
# https://www.thingiverse.com/thing:3063845

# PI 3B+ MECHANICAL DRAWING
# https://www.raspberrypi.org/documentation/hardware/raspberrypi/mechanical/rpi_MECH_3bplus.pdf

from solid.utils import *
from parts import *

# for comparison the stl of the originals are imported
orig_base = color('purple')(translate([123.2, 118.6])(rotate([90, 0, -90])(
            solid.import_("D:/OneDrive/home/3D Objects/Ender 3/AiO_Ender_3_Octoprint_Set_Up_with_Power_and_Light_Remote_Control/files/octoprint_base.STL"))))

X = 123.2
Y = 113
Z = 40
WALL = 1.8


# =========================================================================================
#    CASE ASSEMBLY
# =========================================================================================


def case():

    mount1 = screw_mount_wedge('zy', size=(17.5, 6, 10))
    mount2 = screw_mount_wedge('z-y', size=(17.5, 6, 10))
    mount3 = screw_mount_square('xy', size=(6, 6, 14))
    mount4 = screw_mount_square('x-y', size=(6, 6, 14))
    mount5 = screw_mount_chamfer('xy', size=[6, 6, 18])
    mount6 = screw_mount_chamfer('xz', size=[6, 6, 18])

    ground_bar1 = grounding_bar_pk4gta('z-y')
    ground_bar2 = grounding_bar_pk4gta('zy')
    ground_bar3 = grounding_bar_pk4gta('zx')

    posts = (translate([39.4 + WALL, 10.3 + WALL, WALL])(screw_mount_post(height=2, hole_bot_length=3)) +
             translate([39.4 + 58 + WALL, 10.3 + WALL, WALL])(screw_mount_post(height=2, hole_bot_length=3)) +
             translate([20 + WALL, 71.4 + 28 + WALL, WALL])(screw_mount_post(height=2, hole_bot_length=3)) +
             translate([75 + 20.5 + WALL, 71.4 + 28 + WALL, WALL])(screw_mount_post(height=2, hole_bot_length=3))
             )

    return(
            cube([X, Y, Z]) - translate([WALL, WALL, WALL])(cube([X-WALL+EPSILON, Y-WALL*2, Z-WALL+EPSILON])) +  # case
            translate([36, WALL, Z-mount1.height])(mount1.assembly) +  # LT rear
            translate([95.6, WALL, Z - 6])(resize([0, 0, 6])(mount1.assembly)) +  # LT front
            translate([36, Y-WALL, Z - mount2.height])(mount2.assembly) +  # RT rear
            translate([95.6, Y - WALL, Z - 6])(resize([0, 0, 6])(mount2.assembly)) +  # RT front
            translate([X - WALL - 0.5 - mount3.height, WALL, Z - mount3.length])(mount3.assembly) +  # LT front
            translate([X - WALL - 0.5 - mount4.height, Y-WALL, Z - mount4.length])(mount4.assembly) +  # RT front
            translate([0, WALL, Z-4])(cube([40, WALL, 4])) +  # support over side fan
            translate([52.5, Y-WALL + ground_bar1.wall,
                       Z-ground_bar1.height-6])(ground_bar1.assembly) +  # RT ground bar
            translate([52.5, WALL - ground_bar2.wall,                                               # LT ground bar
                       Z - ground_bar2.height - 6])(ground_bar2.assembly) +
            translate([WALL - ground_bar3.wall,                                                 # back LT ground bar
                       Y - ground_bar3.length*2 - WALL + ground_bar3.wall*2,
                       Z-ground_bar3.height-6])(ground_bar3.assembly) +
            translate([WALL - ground_bar3.wall,                                                 # back RT ground bar
                       Y - ground_bar3.length - WALL + ground_bar3.wall,
                       Z - ground_bar3.height - 6])(ground_bar3.assembly) +
            posts +
            translate([X - WALL - 0.5 - mount5.length, WALL,     WALL])(mount5.assembly) +
            translate([X - WALL - 0.5 - mount6.length, Y - WALL, WALL])(mount6.assembly) +
            translate([4, 0, 6])(fan_opening_30mmx30mm_open('-yz').assembly) +
            translate([X-WALL -0.5, WALL+5.5, WALL ])(support_bar_chamfer('z-x', size=(Y-10, 2, 3.5)).assembly) +
            translate([0, Y, 5])(ender_3_dual_rail('xy', length=X-10).assembly)
            #+ orig_base`
            + translate([WALL, WALL, 4])(base_plate())
            )

# =========================================================================================
#    BASE PLATE ASSEMBLY
# =========================================================================================


base_plate_offset = 0.5
relay = wingoneer_relay(True, h=6.5)



def wire_clips():
    spacing = 3.6
    x1 = 74.
    x2 = 46.5
    x3 = 19.1
    x4 = 9.6
    x5 = 22.7
    x6 = 50.2
    x7 = 77.7

    y1 = 74
    y2 = 19.0
    y3 = 49
    y4 = 98.3

    return color('green')(translate([0, 0, WALL])(
                translate([x1, y1, 0])(zip_tie_clip('xz').assembly) +
                translate([x2, y1, 0])(wire_clip_above(AWG_16_I, 'zx', count=6, spacing=0.75).assembly) +
                translate([x3, y1, 0])(wire_clip_above(AWG_16_I, 'zx', count=6, spacing=0.75).assembly) +
                translate([x4, y2, 0])(wire_clip_above(AWG_16_I, 'zy', count=3, spacing=0.6).assembly) +
                translate([x4, y3, 0])(wire_clip_above(AWG_16_I, 'zy', count=3, spacing=0.6).assembly) +
                translate([x5, y4, 0])(wire_clip_above(AWG_16_I, 'zy', count=4, spacing=0.75).assembly) +
                translate([x6, y4, 0])(wire_clip_above(AWG_16_I, 'zy', count=4, spacing=0.75).assembly) +
                translate([x7, y4, 0])(wire_clip_above(AWG_16_I, 'zy', count=4, spacing=0.75).assembly)
            ))


def base_plate():
    return (
            translate([2, 6.5, 0])(cube([X-WALL*2-base_plate_offset-6, Y-WALL*2-13, WALL])) +       # plate
            translate([39.4, 10.3, WALL])(pi_posts()) +                                      # pi screw mounts
            translate([23, 20, WALL])(rotate([0, 0, 90])(riorand_buck_converter_posts(h=6.5))) +  # converter screw mounts
            translate([20, 71.4])(relay) +                                                   # relay screw mounts
            translate([47.5, 71.4])(relay) +
            translate([75, 71.4])(relay)
            # + wire_clips()                                                                     # wire clips
            )


if __name__ == '__main__':
    base_ = True
    case_ = False
    if base_:  # if true create base assembly and write to file
        a = base_plate()
        scad_render_to_file(a, '../ender_3_case/base.solid.scad',
                            file_header='$fn=20;')

    if case_:  # if true create case assembly and write to file
        a = case()
        #a = a + translate([WALL+base_plate_offset, WALL+base_plate_offset, WALL+5])(base_plate())
        scad_render_to_file(a, '../ender_3_case/case.solid.scad',
                            file_header='$fn=20;')

