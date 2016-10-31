bl_info = {
	'name': 'WoW Tools',
	'author': 'Suncurio, Freeman',
	'version': (1, 0, 0),
	'blender': (2, 73, 0),
	'api': 36302,
	'location': 'File -> Import/Export',
	'description': 'Tools to work with M2I format',
	'warning': '',
	'wiki_url': '',
	'tracker_url': 'https://bitbucket.org/suncurio/blender-m2i-scripts',
	'support': 'COMMUNITY',
	'category': 'Import-Export'}

from .io_export_wow_m2i import *
from .io_import_wow_m2i import *
from .wow_tools import *
from .wow_pose_tools import *

import bpy
import re

def menu_import_func(self, context):
	default_path = os.path.splitext(bpy.data.filepath)[0] + '.m2i'
	self.layout.operator(M2IImporter.bl_idname, text = 'M2 Intermediate (.m2i)').filepath = default_path
	
def menu_export_func(self, context):
	default_path = os.path.splitext(bpy.data.filepath)[0] + '.m2i'
	self.layout.operator(M2IExporter.bl_idname, text = 'M2 Intermediate (.m2i)').filepath = default_path
	
def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_file_import.prepend(menu_import_func)
	bpy.types.INFO_MT_file_export.prepend(menu_export_func)
	
def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.INFO_MT_file_import.remove(menu_import_func)
	bpy.types.INFO_MT_file_export.remove(menu_export_func)

if __name__ == '__main__':
	register()
