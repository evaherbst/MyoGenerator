# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Test_Addon",
    "author" : "Niccolo Fioritti",
    "description" : "TestAddon",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}


import bpy
#import bpy.utilis

from . test_op import Nico_Test_Op

from . test_panel import Nico_Test_Panel

classes =(Nico_Test_Op, Nico_Test_Panel)
register, unregister = bpy.utils.register_classes_factory(classes)


# REF FOR BUTTON TO MAKE BUTTONS: https://blender.stackexchange.com/questions/57545/can-i-make-a-ui-button-that-makes-buttons-in-a-panel

#OTHER REF GENERAL BLENDER ADDONS: https://b3d.interplanety.org/en/calling-functions-by-pressing-buttons-in-blender-custom-ui/

#REF GRAYOUT BUTTONS: https://blenderartists.org/t/gray-out-a-panel-button/522047/2

#REF GRAOUT BUTTONS 2 https://blender.stackexchange.com/questions/160883/contextually-grey-out-panel-element-in-python-2-8