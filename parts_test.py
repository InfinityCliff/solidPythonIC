from parts import *


def rail_test():
    return (cube([10, 35, 1]) +
            translate([0, 2, 1])(ender_3_rail('xz', length=10))+
            translate([0, 22, 1])(ender_3_rail('xz', length=10))
            )


def relay_test():
    return (cube([35, 30, 1]) +
            translate([3, 4, 1])(wingoneer_relay(h=3))
            )


def wire_clip_test():

    return (cube([10, 20, 1]) + translate([2, 2, 1])(wire_clip_above(3, 'zx', count=4).assembly) +
            translate([2, 0, 1])(cube([2, 2, 3.5])) + translate([2, 16.3, 1])(cube([2, 2, 3.5]))
            )


def zip_clip_test():
    return (cube([10, 14, 1]) +
            translate([4, 2, 1])(zip_tie_clip('xz').assembly)
            )


if __name__ == '__main__':
    a = zip_clip_test()

    scad_render_to_file(a, '../ender_3_case/parts_test.solid.scad',
                            file_header='$fn=20;')
