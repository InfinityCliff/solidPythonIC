#! /usr/bin/env python
# -*- coding: utf-8 -*-

from solid.utils import *


class General_Assembly(OpenSCADObject):

    def __init__(self, *args, **kwargs):
        kwargs['id'] = 'assembly'
        OpenSCADObject.__init__(self, 'union', kwargs)

    def set_attributes(self, obj):
        for attr in ['size', 'length', 'width', 'height', 'diameter', 'radius']:
            try:
                self.__setattr__(attr, obj.__getattribute__(attr))
            except AttributeError:
                pass

    def add_assembly(self, assembly):
        self.children.append(assembly)

    def build(self):
        pass

def half(size):
    return list(map(lambda x: x/2, size))


def attributes(assembly, direction, size):
    assembly.direction = direction
    assembly.size = size
    assembly.length = size[0]
    assembly.wight = size[1]
    assembly.height = size[2]
    return assembly


def spin(direction_='zy'):

    try:
        rotation = {'zx':   [0, 0, -90],
                    'z-x':  [0, 0, 90],
                    '-zx':  [180, 0, 90],
                    '-z-x': [180, 0, -90],

                    'zy':   [0, 0, 0],
                    'z-y':  [0, 0, 180],
                    '-zy':  [180, 0, 0],
                    '-z-y': [180, 0, 0],

                    'xy':   [0, 90, 0],
                    'x-y':  [0, -90, 180],
                    '-xy':  [90, 0, 0],
                    '-x-y': [90, 180, 0],

                    'xz':   [90, 0, 90],
                    'x-z':  [-90, 0, -90],
                    '-xz':  [90, 0, -90],
                    '-x-z': [-90, 0, 90],

                    'yx':   [-90, -90, 0],
                    'y-x':  [-90, 90, 0],
                    '-yx':  [90, 90, 0],
                    '-y-x': [90, -90, 0],

                    'yz':   [-90, 180, 0],
                    'y-z':  [-90, 0, 0],
                    '-yz':  [90, 0, 0],
                    '-y-z': [90, 180, 0]
                    }[direction_]
    except KeyError:
        rotation = [0, 0, 0]

    return rotation


def move(length, width, height, direction_, modifier=None):
    l = length / 2
    w = width / 2
    h = height / 2
    if modifier is not None:
        l = modifier[0] * l
        w = modifier[1] * w
        h = modifier[2] * h

    try:
        translation = {'zx':   [-l, w, h],
                       'z-x':  [l, w, h],
                       '-zx':  [l, w, h],
                       '-z-x': [-l, w, h],

                       'zy':   [l, w, h],
                       'z-y':  [-l, w, h],
                       '-zy':  [l, -w, h],  # facing wrong direction
                       '-z-y': [l, w, h],

                       'xy':   [-l, w, h],
                       'x-y':  [l, w, h],
                       '-xy':  [l, w, h],
                       '-x-y': [-l, w, -h],

                       'xz':   [l, w, h],
                       'x-z':  [-l, w, h],
                       '-xz':  [-l, w, h],
                       '-x-z': [l, w, h],

                       'yx':   [l, w, h],
                       'y-x':  [-l, w, h],
                       '-yx':  [-l, w, h],
                       '-y-x': [l, w, h],

                       'yz':   [-l, w, h],
                       'y-z':  [l, w, h],
                       '-yz':  [l, w, h],
                       '-y-z': [-l, w, -h]
                       }[direction_]
    except KeyError:
        translation = [0, 0, 0]

    return translation


class section(OpenSCADObject):

    def __init__(self, plane='x', slice_size=10, offset=0, cutter_size=500):
        OpenSCADObject.__init__(self, 'intersection', {})

        offset = offset + slice_size/2
        rotation = {'x': [0, 0, 90], 'y': [0, 0, 0], 'z': [90, 0, 0]}[plane]
        translation = {'x': [offset, 0, 0], 'y': [0, offset, 0], 'z': [0, 0, offset]}[plane]

        size = [cutter_size, slice_size, cutter_size]

        cutter = translate(translation)(rotate(rotation)(cube(size, center=True)))
        self.children.append(cutter)


BUILT_IN_ASSEMBLY = ['union', 'difference', 'translate', 'rotate', 'color']


class scad_size(object):
    all_sizes = []

    def __call__(self, *args, **kwargs):
        obj = args[0].__dict__
        print(obj)
        name = obj['name']
        if name == 'cylinder':
            self.cylinder(obj['params'])
        elif name == 'cube':
            self.cube(obj['params'])
        elif name == 'sphere':
            self.sphere(obj['params'])
        elif 'id' in obj.keys():
            if obj['id'] == 'assembly':
                self.assembly(obj['size'])
        elif name in BUILT_IN_ASSEMBLY:
            self.built_in_assembly(obj)
        elif name == 'difference':
            self.difference(obj)
        else:
            raise ValueError("solid_utils.scad_size says: Size computation for '{}' not supported.".format(name))
        computed_size = [0, 0, 0]
        for s in self.all_sizes:
            computed_size[0] = max(s[0], computed_size[0])
            computed_size[1] = max(s[1], computed_size[1])
            computed_size[2] = max(s[2], computed_size[2])
        self.size = computed_size

        return computed_size

    def cylinder(self, params):
        # size is tha max of parameter values that are not None for radius and diameter
        size_val = max(value for value in [params['r'], params['r1'], params['r2'],
                                           params['d'], params['d1'], params['d2']] if value is not None)
        if any(radius in {k: v for (k, v) in params.items() if v is not None}.keys() for radius in ['r', 'r1', 'r2']):
            size_val = size_val * 2
        self.all_sizes.append([size_val, size_val, params['h']])

    def cube(self, params):
        self.all_sizes.append(params['size'])

    def sphere(self, params):
        # size is tha max of parameter values that are not None
        size_val = max(value for value in [params['r'], params['d']] if value is not None)
        # if the parameter value(size) is a radius then need to double it to get actual size
        if any(radius in {k: v for (k, v) in params.items() if v is not None}.keys() for radius in ['r', 'r1']):
            size_val = size_val * 2
        self.all_sizes.append([size_val, size_val, size_val])

    def assembly(self, params):
        self.all_sizes.append(list(params))

    def hole(self, obj):
        pass

    def linear_extrude(self, obj):
        self.all_sizes.append([0, 0, obj['height']])

    def built_in_assembly(self, obj):
        for child_ in obj['children']:
            name = child_.__dict__['name']
            if name in BUILT_IN_ASSEMBLY:
                #func = 'child_.__dict__'
                self.built_in_assembly(child_.__dict__)
            else:
                func = "child_.__dict__['params']"
                exec('self.{0}({1})'.format(child_.__dict__['name'], func))

    #def translate(self, obj):
    #    pass

    #def union(self, obj):
    #    for child_ in obj['children']:
    #        name = child_.__dict__['name']
    #        if name in ['union']:
    #            func = 'child_.__dict__'
    #        else:
    #            func = "child_.__dict__['params']"
    #        exec('self.{0}({1})'.format(child_.__dict__['name'], func))

    #def difference(self, obj):
    #    for child_ in obj['children']:
    #        name = child_.__dict__['name']
    #        if name in ['union', 'difference']:
    #            func = 'child_.__dict__'
    #        else:
    #            func = "child_.__dict__['params']"
    #        exec('self.{0}({1})'.format(child_.__dict__['name'], func))

class orient(General_Assembly):

    def __init__(self, direction):
        super().__init__(self)
        self.direction = direction

    def __call__(self, *args, **kwargs):
        super().__call__(args)
        obj = args[0]
        try:
            size = obj.size
        except AttributeError:
            size = scad_size()(obj)
        rotation = spin(self.direction)
        translation = move(*size, self.direction)
        self.modifier = 'rotate({})translate({})'.format(rotation, translation)
        self.set_attributes(obj)
        return self


if __name__ == '__main__':
    # a = clip(plane='z', slice_size=2, offset=3)(cylinder(r=5, h=30))
    #cyl = cylinder(r=5, h=30)
    #cu = cube([10, 11, 12])
    #cu2 = cube(size=[10, 11, 12])
    #sp = sphere(r=10)
    #ci = circle(r=10)
    #gb1 = grounding_bar_pk4gta()
    #a = orient('xy')(cyl)
    #c = orient('zx')(gb1)
    d = union()(cube([20, 10, 10]) + (cube([10, 20, 10])))
    a = scad_size()(d)
    #print(scad_size()(d))
    scad_render_to_file(d, '../solid_utils.solid.scad', file_header='$fn=20;')


