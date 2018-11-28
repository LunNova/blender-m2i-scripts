bl_info = {
	'name': 'WoW Tools',
	'author': 'Suncurio, Freeman',
	'version': (1, 0, 0),
	'blender': (2, 73, 0),
	'api': 36302,
	'location': 'File -> Import/Export',
	'description': 'Tools to work with M2I format',
	'warning': '',
	'wiki_url': 'https://forums.darknestfantasyerotica.com/index.php?threads/m2mod-4-8-13-for-legion.36223/',
	'tracker_url': 'https://forums.darknestfantasyerotica.com/index.php?threads/m2mod-4-8-13-for-legion.36223/',
	'support': 'COMMUNITY',
	'category': 'Import-Export'}

from .io_export_wow_m2i import *
from .io_import_wow_m2i import *
from .wow_tools import *
from .wow_pose_tools import *

import bpy
import re

from bpy.app.handlers import persistent

@persistent
def SetupFromOldProperties(props):
	if props.HasCustomTexture:
		props.HasCustomTexture = False
		props.TextureType0 = '0' # Hardcoded
		props.TextureName0 = props.CustomTexture
		props.BlendMode = props.TextureStyle
		props.RenderFlags = { '3' } # TwoSided

	if props.HasGloss:
		props.HasGloss = False
		props.ShaderId = '32769'
		props.TextureType1 = '0' # Hardcoded
		props.TextureName1 = props.GlossTexture

@persistent
def convert_properties(self):
	for obj in bpy.data.objects:
		if obj.type != "MESH":
			continue
		props = obj.data.wow_props
		SetupFromOldProperties(props)

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
	
	bpy.app.handlers.load_post.append(convert_properties)
	
def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.INFO_MT_file_import.remove(menu_import_func)
	bpy.types.INFO_MT_file_export.remove(menu_export_func)

if __name__ == '__main__':
	register()
