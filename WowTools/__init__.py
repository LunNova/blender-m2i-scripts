# <pep8 compliant>
bl_info = {
	'name': 'WoW Tools',
	'author': 'Suncurio, Freeman, seperx86',
	'version': (1, 1, 0),
	'blender': (2, 80, 0),
	'location': 'File -> Import/Export',
	'description': 'Tools to work with M2I format',
	'warning': '',
	'wiki_url': 'https://forums.darknestfantasy.com/index.php?threads/m2mod-9-x-x-for-sl.36223/',
	'tracker_url': 'https://forums.darknestfantasy.com/index.php?threads/m2mod-9-x-x-for-sl.36223/',
	'support': 'COMMUNITY',
	'category': 'Import-Export'
}

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

# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
	self.layout.operator(M2IImporter.bl_idname, text="M2Mod intermediate (.m2i)")
def menu_func_export(self, context):
	self.layout.operator(M2IExporter.bl_idname, text="M2Mod intermediate (.m2i)")

classes = (
	M2IImporter,
	M2IExporter,
	Wow_Camera_Props,
	Wow_EditBone_Props,
	Wow_Mesh_Props,
	Wow_Scene_Props,
	OBJECT_PT_WoW,
	OBJECT_OT_Hide_All,
	OBJECT_OT_Hide_Attach,
	OBJECT_OT_Hide_Armature,
	OBJECT_OT_Hide_Camera,
	OBJECT_OT_Hide_Face,
	OBJECT_OT_Hide_Hair,
	OBJECT_OT_Hide_Accessory,
	OBJECT_OT_Hide_Armors,
	OBJECT_OT_Hide_Cloak,
	OBJECT_OT_Hide_Body,
	OBJECT_OT_Show_All,
	OBJECT_OT_Show_Attach,
	OBJECT_OT_Show_Armature,
	OBJECT_OT_Show_Camera,
	OBJECT_OT_Show_Face,
	OBJECT_OT_Show_Hair,
	OBJECT_OT_Show_Accessory,
	OBJECT_OT_Show_Armors,
	OBJECT_OT_Show_Cloak,
	OBJECT_OT_Show_Body,
	OBJECT_OT_Next_Facial,
	OBJECT_OT_Next_Hair,
	OBJECT_OT_Next_Accessory,
	OBJECT_PT_WoW_Pose,
	OBJECT_OT_Create_Modifiers,
	OBJECT_OT_Apply_Modifiers,
	OBJECT_OT_Apply_Pose,
	DATA_PT_wowtools_vertex_props,
	DATA_OT_wowtools_cleanup_weights,
	DATA_OT_wowtools_remove_unused_bones,
	DATA_PT_wowproperties_mesh_props,
	DATA_OT_wowtools_transfer_old_properties,
	DATA_PT_BoneMigratePanel,
	OpOpenBoneFile,
	OpDoMigrateVertexGroups,
)

register_classes, unregister_classes = bpy.utils.register_classes_factory(classes)

def register():
	register_classes()
	bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
	bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
	unregister_classes()
	bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
	bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

if __name__ == '__main__':
	register()
