#! /usr/bin/env python
# -*- coding: utf-8 -*-

from solid_utils import *
import behaviours as bh
from dotmap import DotMap
from behaviours import *

# ======  METRIC HOLE SIZES
TAP = 0.75
M1_5 = 1.5
M2 = 2.0
M2_5 = 2.5
M3 = 3.0
M4 = 4.0
M5 = 5.0
M6 = 6.0

AWG_16_I = 3.0  # insulated 16 gauge wire




class four_posts(General_Assembly):

    def __init__(self, x, y, h=5, hole_bot_length=0):
        super().__init__(self)
        post = screw_mount_post(height=h, hole_bot_length=hole_bot_length)
        assembly = (post + translate([0, y])(post) + translate([x, 0])(post) + translate([x, y])(post))
        self.size = [x + post.diameter, y + post.diameter, h]
        self.length = x + post.diameter
        self.width = y + post.diameter
        self.height = h
        self.children.append(assembly)


 # =================================================================================
# COMPONENT MOUNTING POSTS
# =================================================================================
def pi_posts():
    """Four posts spaced for raspberry pi 3"""
    return four_posts(58, 49, hole_bot_length=3)


class riorand_buck_converter_posts(General_Assembly):

    """Four posts spaced for buck converter"""
    def __init__(self, h=5):
        super().__init__(self)
        length = 29.972
        width = 16.002
        height = h
        posts = four_posts(length, width, height)
        assembly = translate([-length/2, -width/2, -height/2])(posts)
        self.set_attributes(posts)
        self.children.append(assembly)

class wingoneer_relay(General_Assembly):
    """Four posts spaced for relay"""

    def __init__(self, h=5):
        super().__init__(self)
        length = 28
        width = 20.5
        height = h
        posts = four_posts(length, width, height)
        assembly = translate([-length/2, -width/2, -height/2])(posts)
        self.set_attributes(posts)
        self.children.append(assembly)


# =================================================================================
# SCREW HOLES, POSTS AND MOUNTS
# =================================================================================
class screw_hole(General_Assembly):

    def __init__(self, hole_size=M3, length=5.0, hole_bot_length=0.0, hole_top_length=0.0,
               countersink_bot=False, countersink_top=False, tap=False):
        """ creates a 'hole' for a screw to pass through or tap into.

        Use hole_bot_length and hole_top_length to extend teh hole longer than the actual object, can also use in
        conjunction with countersink (set to negative) to pull countersink back into the surface of the assembly.

        hole_size:          diameter of the hole
        height:             length of the hole
        hole_bot_length:    length to extend the hole towards the bottom
        hole_top_length:    length to extend the hole towards the bottom
        countersink_bot:    set true to add a 90 deg countersink to the bottom of the hole, is added to end of height
        countersink_top:    set true to add a 90 deg countersink to the top of the hole, is added to end of height
        tap:                set true to reduce the diameter by 75% to allow for tapping of hte screw into hole

        returns an assembly that is an OpenSCAD hole()
        """
        super().__init__(self)
        assembly = []

        dia = hole_size * TAP if tap else hole_size

        if countersink_bot:
            h = length / 2
            assembly.append(translate([0, 0, -h / 2 - length / 2 - hole_bot_length])(
                    cylinder(h=h, d1=dia+h*2, d2=dia, center=True)))
        if countersink_top:
            h = 5
            assembly.append(translate([0, 0, h / 2 + length / 2 + hole_top_length])(
                    cylinder(h=h, d2=dia+h*2, d1=dia, center=True)))

        assembly.append(
                    translate([0, 0, -hole_bot_length/2+hole_top_length/2])(
                        cylinder(d=dia, h=length + EPSILON * 2 + hole_bot_length + hole_top_length, center=True))
                    )
        assembly = hole()(color('green')(union()(assembly)))
        self.diameter = dia
        self.radius = dia/2
        self.size = [dia, dia, length + hole_bot_length + hole_top_length]
        self.children.append(assembly)


class screw_mount_post(General_Assembly):

    def __init__(self, post_dia=6, hole_dia=M3, height=5, hole_top_length=0, hole_bot_length=0):
        """Circular mounting post with round hole in center"""
        super().__init__(self, 'union', {})

        assembly = translate([0, 0, height/2])(cylinder(d=post_dia, h=height, center=True) +
                                           screw_hole(hole_size=hole_dia, length=height, hole_top_length=hole_top_length,
                                                  hole_bot_length=hole_bot_length))
        self.size = [post_dia, post_dia, height]
        self.diameter = post_dia
        self.radius = post_dia / 2
        self.children.append(assembly)

class screw_mount_chamfer(General_Assembly):
    """Screw mount with chamfer on one corner

    direction:  orientation of mount first letter is direction of hole, second is direction of face,
                any combination of x, y, z
    size:       dimensions of the mount
    hole_size:  hole diameter
    tap:        True to reduce hole size for tapping
    center:     set True to not offset assembly to the origin/direction

    returns DotMap containing assembly and information about the assembly,
        use screw_mount_chamfer().assembly to access object
    """
    def __init__(self, direction='', size=(6, 6, 10), hole_size=M3, tap=True, center=False):
        super().__init__(self, 'union', {})
        x = size[0]
        y = size[1]
        z = size[2]

        assembly = (translate([-x/2, -y/2, -z/2])((linear_extrude(height=z)(
                        polygon([[0, 0], [0, y/2], [x/2, y], [x, y], [x, 0]])))) +
                        translate([0, 0, 2])(
                                screw_hole(hole_size=hole_size, tap=tap, length=z-2))
                    )
        # TODO fix orientation diraction
        modification = [1, 1, 1]

        if direction in ['xz', '-x-z', 'x-y', 'y-z', 'yx', '-y-x', '-yz' 'z-x', 'zy', '-z-y']:
            modification = [-1, 1, 1]

        self.size = size
        self.length = x
        self.width = y
        self.height = z
        self.children.append(assembly)


class screw_mount_square(General_Assembly):
    """Square screw mount

    direction:  orientation of mount first letter is direction of hole, second is direction of face,
                any combination of x, y, z
    size:       dimensions of the mount
    hole_size:  hole diameter
    tap:        True to reduce hole size for tapping
    center:     set True to not offset assembly to the origin/direction

    returns DotMap containing assembly and information about the assembly,
        use screw_mount_square().assembly to access object
    """
    def __init__(self, size=(6, 6, 13), hole_size=M3, tap=True):
        super().__init__(self, 'union', {})
        z = size[2]
        assembly = cube(size, center=True) - translate([0, 0, 2])(screw_hole(hole_size=hole_size, length=z-2, tap=tap))

        self.size = scad_size()(assembly)
        self.length = self.size[0]
        self.width = self.size[1]
        self.height = self.size[2]
        self.children.append(assembly)


class screw_mount_wedge(General_Assembly):
    """Wedge shaped screw mount

    direction:  orientation of mount first letter is direction of hole, second is direction of face,
                any combination of x, y, z
    size:       dimensions of the mount [long dim on back, width, height]
    hole_size:  hole diameter
    tap:        True to reduce hole size for tapping
    center:     set True to not offset assembly to the origin/direction

    returns DotMap containing assembly and information about the assembly,
        use screw_mount_wedge().assembly to access object
    """
    def __init__(self, direction='', size=(17.5, 6, 10), hole_size=M3, tap=False, center=False):
        super().__init__(self, 'union', {})

        x = size[0]
        y = size[1]
        z = size[2]

        pt1 = [0, 0]
        pt2 = [x/3, y]
        pt3 = [2*x/3, y]
        pt4 = [x, 0]

        assembly = (translate([-x/2, -y/2, -z/2])(
                        linear_extrude(height=z)(polygon([pt1, pt2, pt3, pt4]))) +
                            screw_hole(hole_size=hole_size, length=z, tap=tap)
                    )

        self.size = scad_size()(assembly)
        print(self.size)
        self.length = self.size[0]
        self.width = self.size[1]
        self.height = self.size[2]
        self.children.append(assembly)


# =================================================================================
# REUSABLE COMPONENTS
# =================================================================================

def shelf_rail(direction='', size=(2, 5, 100), center=False):
    """

    direction:  orientation of container first letter is direction of top, second is direction of face,
                any combination of x, y, z
    size:       0 - length; 1 - height; 2 - thickness
    center:     set True to not offset assembly to the origin/direction

    returns DotMap containing assembly and information about the assembly,
        use shelf_rail().assembly to access object
    """
    x = size[0]     # rail thickness
    y = size[1]     # rail width
    z = size[2]     # rail length

    assembly = cube([x, y, z], center=True) + translate([0, y/2, 0])(rotate([0, 0, 0])(
                    cylinder(d=x, h=z, center=True)))

    rotation = bh.spin(direction)
    if not center:
        translation = bh.origin(x, y, z, direction)
    else:
        translation = [0, 0, 0]

    return DotMap({'assembly': rotate(rotation)(translate(translation)(assembly)),
                   'length':   x,
                   'width':    y,
                   'height':   z})


def zip_tie_clip(direction='', space=2, size=(10, 2, 2), center=False):
    """

    direction:  orientation of container first letter is direction of top, second is direction of face,
                any combination of x, y, z
    space:      space from base to bottom of ring
    size:       0 - diameter of ring; 1 - ring thickness; 2 ring width
    center:     set True to not offset assembly to the origin/direction

    returns DotMap containing assembly and information about the assembly,
        use zip_tie_clip().assembly to access object
    """
    x = size[0]
    y = size[1]
    z = size[2]
    #assembly = translate([0, -(x-y)/2 + space, 0])(cylinder(d=x, h=z, center=True) - cylinder(d=x-y, h=z+EPSILON, center=True)
    #           ) - translate([0, -x/2, 0])(cube([x, x, z+EPSILON], center=True))
    assembly = cube([x, y + space, z], center=True) - color('green')(translate([0, -y/2, 0])(cube([x-y*2, space, z+EPSILON], center=True)))
    rotation = bh.spin(direction)
    if not center:
        translation = bh.origin(x, y+space, z, direction)
    else:
        translation = [0, 0, 0]

    return DotMap({'assembly': rotate(rotation)(translate(translation)(assembly)),
                   'length': x,
                   'width':  y,
                   'height': z})


class grounding_bar_pk4gta(General_Assembly):

    """
    Receptacle for Square D Terminal Grounding Bar
    https://smile.amazon.com/gp/product/B00173B1LQ/ref=ppx_yo_dt_b_asin_title_o00__o00_s00?ie=UTF8&psc=1

    direction:  orientation of container first letter is direction of top, second is direction of face,
                any combination of x, y, z
    size:       internal dimensions of the container
    center:     set True to not offset assembly to the origin/direction

    returns DotMap containing assembly and information about the assembly,
        use grounding_bar_pk4gta().assembly to access object
    """
    def __init__(self, *args, **kwargs):
        super().__init__('union', {})
        i_length, i_width, i_height = [42.7, 8.06, 11.12]

        wall = 1
        x = i_length + wall * 2
        y = i_width + wall * 2
        z = i_height + wall

        hole_r = 3.13
        hole_spacing = hole_r*2 + 1.64

        holes = translate([0, y / 2 - wall / 2 - EPSILON, 0])(rotate([-90, 0, 0])(
                translate([0, 0, EPSILON])(cylinder(r=hole_r, h=wall + EPSILON * 2, center=True)) +
                translate([-hole_spacing, 0, EPSILON])(cylinder(r=hole_r, h=wall + EPSILON * 2, center=True)) +
                translate([-hole_spacing * 2, 0, EPSILON])(cylinder(r=hole_r, h=wall + EPSILON * 2, center=True)) +
                translate([hole_spacing, 0, EPSILON])(cylinder(r=hole_r, h=wall + EPSILON * 2, center=True)) +
                translate([hole_spacing * 2, 0, EPSILON])(cylinder(r=hole_r, h=wall + EPSILON * 2, center=True))
        ))

        casing = (cube([x, y, z], center=True) -
                  translate([0, 0, wall/2])(
                           cube([i_length, i_width, i_height + EPSILON], center=True)))

        self.assembly = (casing - holes)
        self.wall = wall
        self.size = [x, y, z]
        self.length = x
        self.width = y
        self.height = z
        #self.id = 'assembly'
        #kwargs['wall'] = wall
        #kwargs['size'] = size
        self.children.append(self.assembly)

    #def __call__(self, *args, **kwargs):
    #    return self


def wire_clip_bar(length, awg, direction='', center=False):

    size = [length, 2, 2]
    x = size[0]
    y = size[1]
    z = size[2]

    assembly = translate([0, 0, awg + 0.5])(rotate([0, 90, 0])(
                        translate([-(length/2+1)/2, 0, 0])(cube([length/2-1, 2, 2], center=True)) +
                        translate([(length/2+1)/2, 0, 0])(cube([length/2-1, 2, 2], center=True))))

    rotation = bh.spin(direction)
    if not center:
        translation = bh.origin(*size, direction)
    else:
        translation = [0, 0, 0]

    return DotMap({'assembly': rotate(rotation)(translate(translation)(assembly)),
                   'length':   size[0],
                   'width':    size[1],
                   'height':   size[2]})


def wire_clip_above(awg, direction='', count=4, center=False, thickness=2, spacing=0.6):
    """
    Clip to hold wire to casing, etc.
    awg:         wire gauge size mm
    direction:   orientation of clip first letter is direction of top, second is direction of face,
                        any combination of x, y, z
    count:       number of clips in strip
    center:      set True to not offset assembly to the origin/direction
    thickness:   thickness of clip

    returns DotMap containing assembly and information about the assembly,
        use wire_clip().assembly to access object
    """
    clip_height = 3        # height of clip

    x = clip_height + spacing
    y = clip_height
    z = thickness
    assembly = []

    for c in range(count):
        shift = c*x - x/2*(count-1)

        assembly.append(translate([shift, 0, -(2-awg/2)/2])(
                            translate([0, 0, 1])(cube([x, z, 2], center=True)) -
                            rotate([90, 0, 0])(translate([0, 0, 0])(
                                    cylinder(d=awg, h=z + EPSILON * 2, center=True)))
                        ))

    size = [x*count, z, 2+awg/2]

    rotation = bh.spin(direction)
    if not center:
        translation = bh.origin(*size, direction)
    else:
        translation = [0, 0, 0]

    return DotMap({'assembly': rotate(rotation)(translate(translation)(assembly)),
                   'length': size[0],
                   'width':  size[1],
                   'height': size[2]})


def wire_clip(awg, direction='', count=4, center=False, thickness=2, spacing=0.6):
    """
    Clip to hold wire to casing, etc.
    awg:         wire gauge size mm
    direction:   orientation of clip first letter is direction of top, second is direction of face,
                        any combination of x, y, z
    count:       number of clips in strip
    center:      set True to not offset assembly to the origin/direction
    thickness:   thickness of clip

    returns DotMap containing assembly and information about the assembly,
        use wire_clip().assembly to access object
    """
    clip_height = 3        # height of clip

    x = clip_height + spacing
    y = clip_height
    z = thickness
    assembly = []
    for c in range(count):
        shift = c*x - x/2*(count-1)
        assembly.append(rotate([90, 0, 0])(translate([shift, 0, 0])(cube([x, y, z], center=True) -
                        translate([0, y/2-0.75*awg/2, 0])(cylinder(d=awg, h=z+EPSILON*2, center=True)))))

    size = [x*count, z, y]

    rotation = bh.spin(direction)
    if not center:
        translation = bh.origin(*size, direction)
    else:
        translation = [0, 0, 0]

    return DotMap({'assembly': rotate(rotation)(translate(translation)(assembly)),
                   'length': size[0],
                   'width':  size[1],
                   'height': size[2]})


def support_bar_chamfer(direction='', size=(17.5, 6, 6), center=False):
    """
    Support for faceplate, panels, etc., inset from edge

    direction:   orientation of bar first letter is direction of top, second is direction of face,
                        any combination of x, y, z
    size:        [length, width, height]
    center:      set True to not offset assembly to the origin/direction

    returns DotMap containing assembly and information about the assembly,
        use support_bar_chamfer().assembly to access object
    """

    size = list(size)

    x = size[0]
    y = size[1]
    z = size[2]

    pt1 = [0, 0]
    pt2 = [0, y]
    pt3 = [z/3, y]
    pt4 = [z, 0]
    assembly = rotate([90, 0, 90])(linear_extrude(height=x)(polygon([pt1, pt2, pt3, pt4])))

    assembly = translate([-x/2, -y/2, -z/2])(assembly)
    rotation = bh.spin(direction)
    if not center:
        translation = bh.origin(*size, direction)
    else:
        translation = [0, 0, 0]

    return DotMap({'assembly': rotate(rotation)(translate(translation)(assembly)),
                   'length': x,
                   'width':  y,
                   'height': z})


def fan_opening_30mmx30mm_open(direction='', wall=2, center=False, _test=True):
    """
    Full opening for 30mm x 30 mm fan

    direction:  orientation of fan holes first letter is direction of if opening (outward face), second is the wall
                orientation (i.e. z for vertical wall), any combination of x, y, z
    wall:       thickness of wall the hole will be cut into
    center:     set True to not offset assembly to the origin/direction
    _test:      set True to draw a cube to better visualize the hole configuration, for testing only,
                    do not change

    returns DotMap containing assembly and information about the assembly,
        use fan_opening_30mm_form1().assembly to access object
    """
    size = [30, 30, 2]
    spacing = 12
    assembly = []

    fan_screw_hole = screw_hole(hole_size=M3, length=wall, countersink_top=True, hole_top_length=-1.7)

    if _test:
        assembly.append(cube([35, 35, wall], center=True))

    assembly.append(color('green')(
        hole()(cylinder(d=28, h=wall + EPSILON * 2, center=True)) +
        translate([- spacing, spacing, 0])(fan_screw_hole) +   # fan mount holes
        translate([-spacing, -spacing, 0])(fan_screw_hole) +
        translate([spacing,   spacing, 0])(fan_screw_hole) +
        translate([spacing,  -spacing, 0])(fan_screw_hole)
    ))

    rotation = bh.spin(direction)
    if not center:
        translation = bh.origin(size[0], size[1], -size[2], direction)
    else:
        translation = [0, 0, 0]

    return DotMap({'assembly': rotate(rotation)(translate(translation)(assembly)),
                   'length': size[0],
                   'width':  size[1],
                   'height': size[2]})


def fan_opening_30mmx30mm_covered(direction='', wall=2, center=False, _test=True):

    opening = fan_opening_30mmx30mm_open(direction='', wall=wall, center=center, _test=_test)
    assembly = (opening.assembly -
                hole()(cube([30, 2, wall], center=True) +
                       cube([2, 30, wall], center=True) +
                       cylinder(d=10, h=wall, center=True)))

    size = [opening.length, opening.width, opening.height]

    rotation = bh.spin(direction)
    if not center:
        translation = bh.origin(size[0], size[1], -size[2], direction)
    else:
        translation = [0, 0, 0]

    return DotMap({'assembly': rotate(rotation)(translate(translation)(assembly)),
                   'length': size[0],
                   'width':  size[1],
                   'height': size[2]})


def ender_3_rail(direction='', length=10, center=False):
    """
    V-slot rail for Ender 3

    direction:  orientation of rail first letter is direction of rail (length), second is the orientation of rail top,
                any combination of x, y, z
    length:     length of rail
    center:     set True to not offset assembly to the origin/direction

    returns DotMap containing assembly and information about the assembly,
        use ender_3_rail().assembly to access object
    """
    x1 = 1.96
    x2 = 7.65
    x3 = 9.61
    y1 = 2.2
    y2 = 3.64
    y3 = 5.6
    size = [x3, y3, length]
    assembly = rotate([0, 0, 0])(translate([-x3/2, -y3/2, -length/2])(linear_extrude(height=length)(
                    polygon([[x1, 0], [x1, y1], [0, y1], [0, y2], [x1, y3],
                             [x2, y3], [x3, y2], [x3, y1], [x2, y1], [x2, 0]]))))

    rotation = bh.spin(direction)
    if not center:
        translation = bh.origin(*size, direction)
    else:
        translation = [0, 0, 0]

    return DotMap({'assembly': rotate(rotation)(translate(translation)(assembly)),
                   'length': size[0],
                   'width':  size[1],
                   'height': size[2]})


def ender_3_dual_rail(direction='', length=10, center=False):
    """
    Dual V-slot rail for Ender 3

    direction:  orientation of rail first letter is direction of rail (length), second is the orientation of rail top,
                any combination of x, y, z
    length:     length of rail
    center:     set True to not offset assembly to the origin/direction

    returns DotMap containing assembly and information about the assembly,
        use ender_3_dual_rail().assembly to access object
    """
    RAIL_SEPARATION = 20
    rail = ender_3_rail(direction='', length=length, center=center)
    assembly = translate([-RAIL_SEPARATION/2, 0, 0])(rail.assembly + translate([RAIL_SEPARATION, 0, 0])(rail.assembly))

    size = [rail.length*2 + 20-rail.length, rail.width, rail.height]

    rotation = bh.spin(direction)
    if not center:
        translation = bh.origin(*size, direction)
    else:
        translation = [0, 0, 0]

    return DotMap({'assembly': rotate(rotation)(translate(translation)(assembly)),
                   'length': size[0],
                   'width':  size[1],
                   'height': size[2]})
# =================================================================================
# UNDER DEVELOPMENT
# =================================================================================


def support_form_1(count=2):
    x = 3.04    # space between bus risers
    y = 2
    z = 4
    h = 1.32    # height of bus base
    w = 2.92    # width of bus base
    bw = 12.24  # width of each bus riser
    a = []
    for c in range(count):
        a.append(translate([c*(bw+x), 0, 0])(cube([x, y, z])) -
                 translate([-EPSILON+c*(bw+x), y - h, z - w])(cube([x + EPSILON * 2, h + EPSILON, w + EPSILON])))
    return translate([0, -y, 0])(union()(a))


def wire_holder():
    return(
           cylinder(d=10)
           )


if __name__ == '__main__':
    orig_base = color('purple')(translate([-5.2, 5.6, -123.2])(rotate([0, 0, -90])(
            solid.import_(
                "D:/OneDrive/home/3D Objects/Ender 3/AiO_Ender_3_Octoprint_Set_Up_with_Power_and_Light_Remote_Control/files/octoprint_base.STL"))))

    b = wingoneer_relay()
    #a = orient('xy')(riorand_buck_converter_posts())
    #a = orient('xy')(screw_hole())
    #print(a.__dict__)

    a = orient('zx')(screw_mount_wedge())
    scad_render_to_file(a, '../parts.solid.scad',
                        file_header='$fn=20;')

