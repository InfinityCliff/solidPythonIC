#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Original:
# https://www.thingiverse.com/thing:1666929

from solid.utils import *
from parts import *
from materials import *

# -----------------------------------------------------------------------------------------
# DRAWER CONFIGURATION
#
# Number lists in the main list are the number of rows (compartments from front to back).
# Number of items in the list is the number of columns (compartments from side to side).
# The value of the number in the list is the subdivision for that compartment, perpendicular to front |.
# Additionally, any item can be a tuple for which the compartment row will be subdivided parallel to front -.
#
# i.e.  [[1, 1],
#        [1, 1],
#        [1, 1]]  2x3 row of compartments 2 across front, 3 to the back
#
#       [[1, 1],
#        [1, 1],
#        [2, 1]]  2x3 row of compartments 2 across front, 3 to the back, with front left divided in two

DRAWER_CONFIGURATION = [[1, 1, 1, 1],
                        [1, 1, 1, 1],
                        [1, 1, 1, 1],
                        [1, 1, 1, 1],
                       ]
DRAWER_DIN = 2

# -----------------------------------------------------------------------------------------

X = 112  # dimension of shelf in X direction
Y = 126  # dimension of shelf in Y direction
Z = 123  # dimension of shelf in Z direction
WALL = 2  # wall thickness

# for comparison the stl of the originals are imported
orig_shelf = solid.import_("D:/OneDrive/home/3D Objects/Small_items_organizer/files/Shelf.stl")
orig_drawer = solid.import_('D:/OneDrive/home/3D Objects/Small_items_organizer/files/Drawer_16_compartments.stl')

RAIL_T = 2  # Thickness of the shelf support rails
RAIL_L = 5  # length of the shelf support rails
N_RAILS = 4  # number of shelf support rails

HOLE_DIA = 10  # diameter of holes along sides


# =========================================================================================
#    SHELF ASSEMBLY
# =========================================================================================
def peg():
    """Return a peg th fill holes that are then used for stacking and interconnecting"""
    return right(WALL)(rotate([0, -90, 0])(cylinder(d=HOLE_DIA, h=WALL) + up(WALL)(cylinder(d=HOLE_DIA - 0.4, h=WALL))))


def pegs(d):
    """Returns set of  pegs aligning with the holes

    d: Width of the side of the shelf that the holes being cut from
    """
    return translate([0, (d - N_RAILS * RAIL_T - WALL * 2) / (N_RAILS + 1) / 2 + WALL, (Z - N_RAILS) / 8 + WALL])(
        peg()) + \
           translate([0, (d - N_RAILS * RAIL_T - WALL * 2) / (N_RAILS + 1) / 2 + WALL + (
                       (d - N_RAILS * RAIL_T - WALL * 2) / (N_RAILS + 1) + WALL) * 4, (Z - N_RAILS) / 8 + WALL])(
               peg()) + \
           translate([0, (d - N_RAILS * RAIL_T - WALL * 2) / (N_RAILS + 1) / 2 + WALL + (
                       (d - N_RAILS * RAIL_T - WALL * 2) / (N_RAILS + 1) + WALL) * 4, 7 * (Z - N_RAILS) / 8 + WALL])(
               peg()) + \
           translate([0, (d - N_RAILS * RAIL_T - WALL * 2) / (N_RAILS + 1) / 2 + WALL, 7 * (Z - N_RAILS) / 8 + WALL])(
               peg())


def peg_test():
    """Return a male and female peg to test for sizing and fitting """
    return up(WALL / 2)(cylinder(d=15, h=WALL, center=True)) + up(WALL)(rotate([0, 90, 0])(peg())) + \
           right(20)(up(WALL / 2)(cylinder(d=15, h=WALL, center=True)) - up(WALL)(rotate([0, 90, 0])(peg())))


def hole():
    """Returns a 'hole' for the side of shelf"""
    return translate([0, Y + 5, 0])(rotate([90, 0, 0])(cylinder(d=HOLE_DIA, h=Y + 10)))


def holes(d):
    """Returns a set of holes for the side of the shelf

    d: Width of the side of the shelf that the holes being cut from
    """
    h = cylinder(d=0, h=0)
    Z_ = Z - N_RAILS
    X_ = d - WALL * 2
    for x in range(N_RAILS + 1):
        offset_x = (d - N_RAILS * RAIL_T - WALL * 2) / (N_RAILS + 1) / 2 + WALL + (
                    (d - N_RAILS * RAIL_T - WALL * 2) / (N_RAILS + 1) + WALL) * x
        for z in range(7):
            offset_ = Z_ / 8 + Z_ / 8 * z
            h = h + translate([offset_x, 0, offset_ + ((Z - Z_) / 2)])(hole())
    return h


def rails(rails_configuration=1):
    """Returns a set of rails of count N_RAILS"""
    r = []
    rails_to_skip = {0: [0, 1, 2, 3, 4, 5],
                     1: [],
                     2: [2, 4],
                     3: [3, 4],
                     4: [2, 3, 4]}[rails_configuration]

    for o, d in enumerate(['zy', 'z-y']):
        for x in range(1, N_RAILS + 1):
            if x in rails_to_skip:
                continue
            x_offset = ((X - N_RAILS * RAIL_T - WALL * 2) / (N_RAILS + 1) + WALL) * x
            r.append(translate([x_offset, WALL+o*(Y-WALL*2), WALL])(shelf_rail(d, [RAIL_T, RAIL_L, Z-WALL]).assembly))

    return r


def shelf_assembly(stackable=True, solid_top=False, interlock=True, rails_configuration=1):
    """ Return full shelf assembly

    stackable:  True to include pegs on top
    solid_top:  True to make top solid
    interlock:  True to include pegs on left side
    rails_2:    True to add only two rails (i.e. 3 draws with the bottom two being double height)
    """
    hole_shift = 30 if solid_top else 0     # holes are created by subtracting cylinders from box,
                                            # this shits the cylinders down so they do not cut out the top

    assembly = [cube([X, Y, Z]) - translate([WALL, WALL, WALL])(
                                            cube([X - WALL * 2, Y - WALL * 2, Z - WALL + EPSILON * 3])) +
                rails(rails_configuration) - holes(X) - translate([X + hole_shift, 0, 0])(rotate([0, 0, 90])(holes(Y)))]
    if stackable:
        assembly.append(pegs(Y))
    if interlock:
        assembly.append(translate([X, 0, 0])(rotate([0, 0, 90])(pegs(X))))
    # a_ = a_ + color('green')(translate([18+WALL+1, -1, Z+WALL+4])(rotate([0, -90, 0])(drawer)))
    # uncomment previous line and end of line before previous to include original shelf for size comparison
    return union()(assembly)


# =========================================================================================
#    DRAWER ASSEMBLY
# =========================================================================================


DRAW_SIZE = 120.0
DRAW_H = 19.0
DRAW_CORNER_D = 6.0
LONG = DRAW_SIZE - DRAW_CORNER_D / 2
SHORT = DRAW_CORNER_D / 2
DRAWER_WALL = 1.0


def tag_holder(h=DRAW_H):
    """Returns one tag holder set 3 units past the Wall thickness and at the front of the drawer"""
    return translate([DRAW_SIZE, DRAWER_WALL + 3])(cube([2, DRAW_SIZE / 2 - 10, h - 2])) - \
           translate([DRAW_SIZE, DRAWER_WALL + 3.5, 1])(cube([1, DRAW_SIZE / 2 - 11, h - 2])) - \
           translate([DRAW_SIZE + 1, DRAWER_WALL + 5, 2])(cube([1, DRAW_SIZE / 2 - 14, h - 2]))


def faceplate(h=DRAW_H):
    """Returns faceplate (both tags and drawer pull) positioned at the front of the drawer"""
    return (tag_holder() + translate([0, DRAW_SIZE / 2])(tag_holder(h)) +
            translate([DRAW_SIZE, DRAW_SIZE / 2 - 1])(cube([7, 2, h - 2])) +
            translate([DRAW_SIZE + 7, DRAW_SIZE / 2 + 1, (h - 2) / 2])(
               rotate([90, 0, 0])(cylinder(d=h - 2, h=2)))) #+ \
            #hole()(translate([DRAW_SIZE, DRAW_SIZE/4, -10])(logo('xz', depth=1).assembly))


def drawer_compartment(x=None, y=None, x_shift=DRAWER_WALL, y_shift=DRAWER_WALL, _z=0, h=DRAW_H):
    """Returns one drawer compartment -- i.e. the negative space of teh drawer

    x: width of compartment
    y: length of compartment
    x_shift: how far to shift in the x axis
    y_shift: how far to shift in the y axis
    _z: shift distance for z direction, used for testing, do not change
    """
    shift = DRAW_CORNER_D / 2   # reduces the size of hte space to account for the radius of the sphere so the final
                                # dimensions will equal the passed x, y

    compartment = union()(translate([shift, shift, shift + DRAWER_WALL])(sphere(d=DRAW_CORNER_D)),  # create the space
                   translate([x - shift, shift, shift + DRAWER_WALL])(sphere(d=DRAW_CORNER_D)),
                   translate([shift, y - shift, shift + DRAWER_WALL])(sphere(d=DRAW_CORNER_D)),
                   translate([x - shift, y - shift, shift + DRAWER_WALL])(sphere(d=DRAW_CORNER_D)))

    # move into position before return
    return translate([x_shift, y_shift, _z])(hull()(compartment, translate([0, 0, h])(compartment)))


def drawer_compartments(size, h=DRAW_H, X_=DRAW_SIZE, Y_=DRAW_SIZE, X_shift=DRAWER_WALL, Y_shift=DRAWER_WALL, _z=0):
    """Uses recursion to create teh drawer compartment spaces based on DRAWER_CONFIGURATION

    The convention is that rows are increasing along the y axis and columns are increasing along x axis.

    X_: size of the compartment along x axis
    Y_: size of the compartment along y axis
    row_offset: essentially the width of the previous row
    _z: used for testing, do not change
    """
    num_rows = len(size)

    num_cols = len(size[0]) if type(size[0]) == list else size[0]

    a_ = []  # list will contain all the compartment elements to be added together at teh end of the recursion

    for r, row in enumerate(size):
        for c, col in enumerate(row):
            x = (X_ - DRAWER_WALL * (num_rows + 1)) / num_rows
            y = (Y_ - DRAWER_WALL * (num_cols + 1)) / num_cols
            x_shift = X_shift + (DRAWER_WALL + x) * r
            y_shift = Y_shift + (DRAWER_WALL + y) * c
            if type(col) == tuple:
                new_size = [[1] for _ in range(col[0])]
                x = x + DRAWER_WALL*2
                y = y + DRAWER_WALL*2
                a_.append(drawer_compartments(new_size, x, y, x_shift, y_shift, _z=_z))
            elif col > 1:
                new_size = [1 for _ in range(col)]
                x = x + DRAWER_WALL*2
                y = y + DRAWER_WALL
                a_.append(drawer_compartments([new_size], x, y, x_shift, y_shift, _z=_z))
            else:
                a_.append(drawer_compartment(x, y, x_shift, y_shift, _z=_z, h=h))

    return union()(a_)  # union list before returning


def drawer_assembly(din=3):
    """Return full drawer assembly based on specified configuration DRAWER_CONFIGURATION"""

    h = DRAW_H * din + (din-1)*3
    return hull()(translate([SHORT, SHORT, 0])(cylinder(d=DRAW_CORNER_D, h=h)),
                  translate([LONG, SHORT, 0])(cylinder(d=DRAW_CORNER_D, h=h)),
                  translate([SHORT, LONG, 0])(cylinder(d=DRAW_CORNER_D, h=h)),
                  translate([LONG, LONG, 0])(cylinder(d=DRAW_CORNER_D, h=h))) - \
           drawer_compartments(DRAWER_CONFIGURATION, h=h) + \
           translate([0, 0, h-DRAW_H])(faceplate())
        #  + color('green')(translate([X+13, -4, 0])(drawer_orig))      # uncomment this line to include
                                                                        # the original shelf for size comparison.


if __name__ == '__main__':
    shelf = False  # set true to return the shelf
    drawer_ = True  # set true to return a drawer

    stack = True        # set true to stackable (pegs on top)
    solid_top = True    # set true for solid top
    interlock = False    # set true for interlock (pegs on left side)
    rails_configuration = 4     # 0 no rails (Quint DIN)
                                # 1 - four rails (5 single DIN drawers)
                                # 2 - 2 rails (2 double DIN drawers, 1 single DIN on top)
                                # 3 - 2 rails (1 triple DIN, 2 single DIN on top)
                                # 4 - 1 rail (1 quad DIN, 1 single DIN on top)

    # following lines add respective text to output file name if stackable, solid, or interlocking
    stack_text = '_stackable' if stack else ''
    solid_top_text = '_solidTop' if solid_top else ''
    interlock_text = '_interlock' if interlock else ''

    if drawer_:  # if true create drawer assembly and write to file
        a = drawer_assembly(din=DRAWER_DIN)
        scad_render_to_file(a, '../Small_items_organizer/drawer.solid.scad',
                            file_header='$fn=15;')

    if shelf:  # if true return shelf assembly and write to file
        a = shelf_assembly(stackable=stack, solid_top=solid_top, interlock=interlock,
                           rails_configuration=rails_configuration)
        scad_render_to_file(a, '../Small_items_organizer/shelf.solid.scad')  # .format(stack_text,
        #scad_render_to_file(a, '../Small_items_organizer/small_items_organizer{}{}{}.solid.scad')#.format(stack_text,
                                                                                                 #       solid_top_text,
                                                                                                 #      interlock_text))
    # un comment nex two lines to create peg test assembly and write to file
    # Peg test - to test size of peg and hole opening
    # scad_render_to_file(peg_test(), '../Small_items_organizer/peg_size_test.solid.scad')
