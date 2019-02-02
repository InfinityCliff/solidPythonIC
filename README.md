# SolidPythonIC

### Note: Under development
* Object(assemblies) were initially created by returning an assembly(OpenSCAD object) from a function.  I am in the process of converting them to a class to work with `section`, `scadSize`, and `orient` (and any future tools I may develop)

Objects and tools for use with [SolidPython](https://github.com/SolidCode/SolidPython) by [SolidCode](https://github.com/SolidCode)

**Table of Contents**

1. **basic_shapes.py**
Simple shapes not defined in OpenSCAD

* **behaviours.py**
To be removed in future commit

* **door_latch.py**
A latch to go over the cabinet door to keep the dog out of the trash (first item I designed and printed, wife loves it!)

* **drawer_divider.py**
Customizable desk drawer organizer

* **ender_3_case.py**
modification of [this](https://www.thingiverse.com/thing:3063845) case on thingiverse.com.  Its a case to hold a PI that will control the Ender 3 Printer.  Primary change is addition of a plate to hold the components, to allow assembly/wiring/testing outside of the case

* **materials.py**
various items used to help size other components *not intended to be printed*

* **parts.py**
Component parts to be used for development of more complex assemblies

* **peg_board_baseplate.py**
base plate to be used on peg board

* **peg_board_wizard.py**
An attempt to convert [this](from http://www.thingiverse.com/thing:8174 by whosawhatsis) to solidPython - *still working on it*

* **small_items_organizer.py**
My remix of a shelf and drawer to organize small items, [(check it out)](https://www.thingiverse.com/thing:3328888)

* **solid_utils.py**
tools to make 3D modeling easier
  * section() - cut a section of any OpenSCAD assembly
  * orient() - easily rotate assemblies/components to the desired orientation, and positioned with a [0,0,0] origin to allow for easier placement.
  * scadSize() - calculate the size of any assembly - *still working on this, need to figure out how to handle intersections and differences*

* **tools.py** - physical tools to be used for better sizing of things *not intended to be printed*

* **truck.py** - stuff for by 2005 Ford F-150 *working on replacing the ashtray with a useful storage compartment and phone charger*
