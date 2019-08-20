bl_info = {
	'name': 'WoW Tools',
	'author': 'Suncurio, Freeman',
	'version': (1, 0, 0),
	'blender': (2, 80, 0),
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
from bpy_extras.io_utils import ImportHelper

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

class ImportM2I(bpy.types.Operator, ImportHelper):
	"""Import M2Mod itermediate file (.m2i)."""
	bl_idname = "wow_toolls.import_m2i"
	bl_label = "Import M2I"

	# ImportHelper mixin class uses this
	filename_ext = ".m2i"

	filter_glob: bpy.props.StringProperty(
		default="*.m2i",
		options={'HIDDEN'},
		maxlen=1024,  # Max internal buffer length, longer would be clamped.
	)

	def execute(self, context):
		DoImport(self.filepath)
		return {'FINISHED'}

# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
	self.layout.operator(ImportM2I.bl_idname, text="M2Mod intermediate (.m2i)")

classes = (
	ImportM2I,
	Wow_Camera_Props,
	Wow_EditBone_Props,
	Wow_Mesh_Props,
	Wow_Scene_Props,
)

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
	register_classes()
	bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
	
def unregister():
	unregister_classes()
	bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

if __name__ == '__main__':
	register()
