#! /usr/bin/env python
# -*- coding: utf-8 -*-

from solid.utils import *
import behaviours as bh
from dotmap import DotMap

# from http://www.thingiverse.com/thing:8174 by whosawhatsis, used with permission -->
# www.thingiverse.com/thing:537516


# =================================================================================
# COMPONENT DIMENSIONS
# =================================================================================


# -- Basic
holder_x_size = 1.0     # width of the orifice
holder_y_size = 20.0    # depth of the orifice
holder_height = 15.0    # height of the holder
wall_thickness = 1.85   # how thick are the walls. Hint: 6*extrusion width produces the best results.
holder_x_count = 2      # how many times to repeat the holder on X axis
holder_y_count = 1      # how many times to repeat the holder on Y axis
corner_radius = 40.0    # orifice corner radius (roundness). Needs to be less than min(x,y)/2.
taper_ratio = 1.0       # Use values less than 1.0 to make the bottom of the holder narrow

# -- Advanced
holder_offset = 0.0         # offset from the peg board, typically 0 unless you have an object that needs clearance
strength_factor = 0.20      # what ratio of the holders bottom is reinforced to the plate [0.0-1.0]
closed_bottom = 0.0         # for bins: what ratio of wall thickness to use for closing the bottom
holder_cutout_side = 0.85   # what percentage cu cut in the front (example to slip in a cable or make the tool snap
                            # from the side)
holder_angle = 0.0          # set an angle for the holder to prevent object from sliding or to view it better from
                            # the top

# -- Hidden
holder_sides = max(50.0, min(20.0, holder_x_size*2))    # what is the $fn parameter

# dimensions the same outside US?
hole_spacing = 25.4
hole_size = 6.0035
board_thickness = 5.0

holder_total_x = wall_thickness + holder_x_count*(wall_thickness+holder_x_size)
holder_total_y = wall_thickness + holder_y_count*(wall_thickness+holder_y_size)
holder_total_z = round(holder_height/hole_spacing)*hole_spacing
holder_roundness = min(corner_radius, holder_x_size/2, holder_y_size/2) 

fn = 32     # what is the $fn parameter for holders

epsilon = 0.1

clip_height = 2*hole_size + 2


def round_rect_ex(x1, y1, x2, y2, z, r1, r2):
    fn_ = int(holder_sides)
    brim = z/10

    return hull()(
        translate([-x1/2 + r1, y1/2 - r1, z/2-brim/2])(
            cylinder(r=r1, h=brim, center=True, segments=fn_)) +
        translate([x1/2 - r1, y1/2 - r1, z/2-brim/2])(
            cylinder(r=r1, h=brim, center=True, segments=fn_)) +
        translate([-x1/2 + r1, -y1/2 + r1, z/2-brim/2])(
            cylinder(r=r1, h=brim, center=True, segments=fn_)) +
        translate([x1/2 - r1, -y1/2 + r1, z/2-brim/2])(
            cylinder(r=r1, h=brim, center=True, segments=fn_)) +

        translate([-x2/2 + r2, y2/2 - r2, -z/2+brim/2])(
            cylinder(r=r2, h=brim, center=True, segments=fn_)) +
        translate([x2/2 - r2, y2/2 - r2, -z/2+brim/2])(
            cylinder(r=r2, h=brim, center=True, segments=fn_)) +
        translate([-x2/2 + r2, -y2/2 + r2, -z/2+brim/2])(
            cylinder(r=r2, h=brim, center=True, segments=fn_)) +
        translate([x2/2 - r2, -y2/2 + r2, -z/2+brim/2])(
            cylinder(r=r2, h=brim, center=True, segments=fn_))
        )


def pin(clip):
    assembly = [rotate([0, 0, 15])(
                    cylinder(r=hole_size / 2, h=board_thickness * 1.5 + epsilon, center=True, segments=12))]

    if clip:
        assembly.append(
            rotate([0, 0, 90])(intersection()(
                translate([0, 0, hole_size-epsilon])(
                    cube([hole_size+2 * epsilon, clip_height, 2 * hole_size], center=True)) +


                translate([0, hole_size / 2 + 2, board_thickness / 2])(
                    rotate([0, 90, 0])(
                        rotate_extrude(convexity=5, segments=20)(
                            translate([5, 0, 0])(
                                circle(r=(hole_size * 0.95) / 2))))) +

                translate([0, hole_size / 2 + 2 - 1.6, board_thickness / 2])(
                    rotate([45, 0, 0])(
                        translate([0, -0, hole_size * 0.6])(
                            cube([hole_size+2 * epsilon, 3 * hole_size, hole_size], center=True)))))
            )
        )
    return assembly


def pinboard_clips():
    assembly = []
    for i in range(round(holder_total_x/hole_spacing+1)):
        for j in range(max(int(strength_factor), round(holder_height/hole_spacing+1))):
            assembly.append(translate([j*hole_spacing,
                            -hole_spacing*(round(holder_total_x/hole_spacing)/2) + i*hole_spacing,
                            0])(
                                pin(j == 0)))  # TODO - check that j==0 is passing correctly
            print(j)
            print(j==0)
    return rotate([0, 90, 0])(assembly)


def pinboard(clips):
    return(rotate([0, 90, 0])(
        translate([-epsilon, 0, -wall_thickness - board_thickness/2 + epsilon])(
        hull()(
            translate([-clip_height/2 + hole_size/2,
                -hole_spacing*(round(holder_total_x/hole_spacing)/2), 0])(
                cylinder(r=hole_size/2, h=wall_thickness)) +

            translate([-clip_height/2 + hole_size/2,
                hole_spacing*(round(holder_total_x/hole_spacing)/2), 0])(
                cylinder(r=hole_size/2,  h=wall_thickness)) +

            translate([max(strength_factor, round(holder_height/hole_spacing))*hole_spacing,
                -hole_spacing*(round(holder_total_x/hole_spacing)/2), 0])(
                cylinder(r=hole_size/2, h=wall_thickness)) +

            translate([max(strength_factor, round(holder_height/hole_spacing))*hole_spacing,
                hole_spacing*(round(holder_total_x/hole_spacing)/2), 0])(
                cylinder(r=hole_size/2,  h=wall_thickness))
        )))
    )


def holder(negative):
    assembly = []
    assembly1 = None
    for x in range(1, holder_x_count+1):
        print(x)
        for y in range(1, holder_y_count+1):
            if not negative:
                assembly1 = round_rect_ex(
                        (holder_y_size + 2 * wall_thickness),
                        holder_x_size + 2 * wall_thickness,
                        (holder_y_size + 2 * wall_thickness) * taper_ratio,
                        (holder_x_size + 2 * wall_thickness) * taper_ratio,
                        holder_height,
                        holder_roundness + epsilon,
                        holder_roundness * taper_ratio + epsilon)

            if negative > 1:
                assembly2 = round_rect_ex(
                        holder_y_size * taper_ratio,
                        holder_x_size * taper_ratio,
                        holder_y_size * taper_ratio,
                        holder_x_size * taper_ratio,
                        3 * max(holder_height, hole_spacing),
                        holder_roundness * taper_ratio + epsilon,
                        holder_roundness * taper_ratio + epsilon)
            else:
                assembly2 = round_rect_ex(
                            holder_y_size,
                            holder_x_size,
                            holder_y_size * taper_ratio,
                            holder_x_size * taper_ratio,
                            holder_height + 2 * epsilon,
                            holder_roundness + epsilon,
                            holder_roundness * taper_ratio + epsilon)

            assembly2 = translate([0, 0, closed_bottom * wall_thickness])(assembly2)

            assembly2 = assembly2 if assembly1 is None else assembly1 - assembly2

            if not negative:
                if holder_cutout_side > 0:
                    if negative > 1:
                        assembly2 = assembly2 - hull()(
                                scale([1.0, holder_cutout_side, 1.0])(
                                    round_rect_ex(
                                    holder_y_size * taper_ratio,
                                    holder_x_size * taper_ratio,
                                    holder_y_size * taper_ratio,
                                    holder_x_size * taper_ratio,
                                    3 * max(holder_height, hole_spacing),
                                    holder_roundness * taper_ratio + epsilon,
                                    holder_roundness * taper_ratio + epsilon)),
                                translate([0-(holder_y_size + 2 * wall_thickness), 0, 0])(
                                    scale([1.0, holder_cutout_side, 1.0])(
                                        round_rect_ex(
                                        holder_y_size * taper_ratio,
                                        holder_x_size * taper_ratio,
                                        holder_y_size * taper_ratio,
                                        holder_x_size * taper_ratio,
                                        3 * max(holder_height, hole_spacing),
                                        holder_roundness * taper_ratio + epsilon,
                                        holder_roundness * taper_ratio + epsilon))))
                    else:
                        assembly2 = assembly2 - hull()(
                                scale([1.0, holder_cutout_side, 1.0])(
                                    round_rect_ex(
                                    holder_y_size,
                                    holder_x_size,
                                    holder_y_size * taper_ratio,
                                    holder_x_size * taper_ratio,
                                    holder_height+2 * epsilon,
                                    holder_roundness + epsilon,
                                    holder_roundness * taper_ratio + epsilon)),
                                translate([0-(holder_y_size + 2 * wall_thickness), 0, 0])(
                                    scale([1.0, holder_cutout_side, 1.0])(
                                        round_rect_ex(
                                        holder_y_size,
                                        holder_x_size,
                                        holder_y_size * taper_ratio,
                                        holder_x_size * taper_ratio,
                                        holder_height+2 * epsilon,
                                        holder_roundness + epsilon,
                                        holder_roundness * taper_ratio + epsilon))))

            assembly.append(translate([
                                    -holder_total_y + y * (holder_y_size + wall_thickness) + wall_thickness,
                                    -holder_total_x / 2 + (holder_x_size + wall_thickness) / 2 + (x - 1) * (
                                            holder_x_size + wall_thickness) + wall_thickness / 2,
                                    0])(
                                rotate([0, holder_angle, 0])(
                                    translate([-wall_thickness * abs(sin(holder_angle)) - 0 * abs((holder_y_size / 2) *
                                                    sin(holder_angle)) - holder_offset - (holder_y_size + 2 *
                                                    wall_thickness) / 2 - board_thickness / 2,
                                               0,
                                               -(holder_height / 2) * sin(holder_angle) - holder_height / 2 + clip_height / 2]
                                    )
                                )
                            )(assembly2)
                            )

    return assembly


def pegstr():
    b = hull()(
            pinboard(None),
            intersection()(
                translate([-holder_offset - (strength_factor - 0.5) * holder_total_y - wall_thickness / 4, 0, 0])(
                    cube([
                        holder_total_y + 2 * wall_thickness,
                        holder_total_x + wall_thickness,
                        2 * holder_height
                        ], center=True)),

                holder(0)
            )
        )

    if closed_bottom * wall_thickness < epsilon:
        b = b - holder(2)

    a = pinboard(None) + b + (
        color([0.7, 0, 0])(
            difference()(
                holder(0),
                holder(2)
            )
        ) +
        color([1, 0, 0])(
            pinboard_clips()
        ))

    c = a - holder(1) - (
        translate([-board_thickness / 2, -1, -clip_height+5])(
            rotate([-90, 0, 90])(
                intersection()(
                    union()(
                        difference()(
                            round_rect_ex(3, 10, 3, 10, 2, 1, 1),
                            round_rect_ex(2, 9, 2, 9, 3, 1, 1)
                        ),
                        translate([2.5, 0, 0])(
                            difference()(
                                round_rect_ex(3, 10, 3, 10, 2, 1, 1),
                                round_rect_ex(2, 9, 2, 9, 3, 1, 1)))
                        ),
                    translate([0, -3.5, 0])(
                        cube([20, 4, 10], center=True))
                )
            )
        ) -
        translate([1.25, -2.5, 0])(
            difference()(
                round_rect_ex(8, 7, 8, 7, 2, 1, 1),
                round_rect_ex(7, 6, 7, 6, 3, 1, 1),
                translate([3, 0, 0])(
                    cube([4, 2.5, 3], center=True))
            )
        ) -
        translate([2.0, -1.0, 0])(
            cube([8, 0.5, 2], center=True)
        ) -
        translate([0, -2, 0])(
            cylinder(r=0.25, h=2, center=True, segments=12)
        ) -
        translate([2.5, -2, 0])(
            cylinder(r=0.25, h=2, center=True, segments=12))
    )
    return c


if __name__ == '__main__':
    a = pegstr()
    scad_render_to_file(a,  '../peg_board.solid.scad',
                        file_header='$fn={};'.format(fn))
