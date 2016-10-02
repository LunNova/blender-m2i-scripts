#----------------------------------------------------------
# File shapekey_pin.py
#----------------------------------------------------------
bl_info = {
	'name': 'WoW Tools',
	'author': 'Freeman',
	'version': (1, 2, 0),
	'blender': (2, 73, 0),
	'api': 36302,
	#'location': 'Properties space > Scene tab > WoW Tools panel',
	'location': 'VIEW 3D > Tools > WoW Tools panel',
	'description': 'WoW Tools',
	'warning': '',
	'wiki_url': 'http://forums.darknestfantasyerotica.com/member.php?105498-Freeman',
	'tracker_url': '',
	'support': 'COMMUNITY',
	'category': '3D View'}
 
#******************************
#---===Import declarations===
#******************************
import bpy
import re

#******************************
#---===GUI===
#******************************
class OBJECT_PT_WoW(bpy.types.Panel):
	
	bl_label = 'WoW Tools'
	#bl_space_type = 'PROPERTIES'
	#bl_region_type = 'WINDOW'
	#bl_context = 'scene'
	bl_idname = 'WoWTools'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = 'Tools'
	
	def draw(self, context):
		layout = self.layout.split()
		
		layout_col1 = layout.column()
		layout_col1.label(text="Hide", icon='RESTRICT_VIEW_ON')
		layout_col1.operator('scene.wow_hide_all', text='All')
		layout_col1.operator('scene.wow_hide_attachments', text='Attach')
		layout_col1.operator('scene.wow_hide_armature', text='Armature')
		layout_col1.operator('scene.wow_hide_cameras', text='Camera')
		layout_col1.operator('scene.wow_hide_facial', text=' Facial')
		layout_col1.operator('scene.wow_hide_hair', text='Hair')
		layout_col1.operator('scene.wow_hide_armors', text='Armor')
		layout_col1.operator('scene.wow_hide_cloak', text='Cloak')
		layout_col1.operator('scene.wow_hide_body', text='Body')

		layout_col2 = layout.column()
		layout_col2.label(text="Show", icon='RESTRICT_VIEW_OFF')
		layout_col2.operator('scene.wow_show_all', text='All')
		layout_col2.operator('scene.wow_show_attachments', text='Attach')
		layout_col2.operator('scene.wow_show_armature', text='Armature')
		layout_col2.operator('scene.wow_show_cameras', text='Camera')
		layout_col2.operator('scene.wow_show_facial', text='Facial')
		layout_col2.operator('scene.wow_show_hair', text='Hair')
		layout_col2.operator('scene.wow_show_armors', text='Armor')
		layout_col2.operator('scene.wow_show_cloak', text='Cloak')
		layout_col2.operator('scene.wow_show_body', text='Body')

### HIDE ###
class OBJECT_OP_Hide_All(bpy.types.Operator):
	bl_idname = 'scene.wow_hide_all'
	bl_label = 'Hide All'
	bl_description = 'Hide All.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			ob.hide = True
		return {'FINISHED'}
		
class OBJECT_OP_Hide_Attach(bpy.types.Operator):
	bl_idname = 'scene.wow_hide_attachments'
	bl_label = 'Hide Attachments'
	bl_description = 'Hide Attachments.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'EMPTY' and ob.name.startswith('Attach'):
				ob.hide = True
		return {'FINISHED'}

class OBJECT_OP_Hide_Armature(bpy.types.Operator):
	bl_idname = 'scene.wow_hide_armature'
	bl_label = 'Hide Armature'
	bl_description = 'Hide Armature.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'ARMATURE' and ob.name == 'Armature':
				ob.hide = True
		return {'FINISHED'}

class OBJECT_OP_Hide_Camera(bpy.types.Operator):
	bl_idname = 'scene.wow_hide_cameras'
	bl_label = 'Hide Cameras'
	bl_description = 'Hide Cameras.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'CAMERA':
				ob.hide = True
		return {'FINISHED'}
		
class OBJECT_OP_Hide_Face(bpy.types.Operator):
	bl_idname = 'scene.wow_hide_facial'
	bl_label = 'Hide Facial'
	bl_description = 'Hide Facial.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and re.search('^Mesh(01|02|03|17)', ob.name):
				ob.hide = True
		return {'FINISHED'}
		
class OBJECT_OP_Hide_Hair(bpy.types.Operator):
	bl_idname = 'scene.wow_hide_hair'
	bl_label = 'Hide Hairstyle'
	bl_description = 'Hide Hairstyle.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and re.search('^Mesh(00)(?!00)', ob.name):
				ob.hide = True
		return {'FINISHED'}
		
class OBJECT_OP_Hide_Armors(bpy.types.Operator):
	bl_idname = 'scene.wow_hide_armors'
	bl_label = 'Hide Armors'
	bl_description = 'Hide Armors.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and re.search('^Mesh(04|05|08|09|10|11|13|18|20).(?!1)', ob.name):
				ob.hide = True
		return {'FINISHED'}
		
class OBJECT_OP_Hide_Cloak(bpy.types.Operator):
	bl_idname = 'scene.wow_hide_cloak'
	bl_label = 'Hide Cloak'
	bl_description = 'Hide Cloak.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and re.search('^Mesh(12|15)', ob.name):
				ob.hide = True
		return {'FINISHED'}
		
class OBJECT_OP_Hide_Body(bpy.types.Operator):
	bl_idname = 'scene.wow_hide_body'
	bl_label = 'Hide Body'
	bl_description = 'Hide Body.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and re.search('^Mesh(0000|07|19|0401|0501|1301|2001)', ob.name):
				ob.hide = True
		return {'FINISHED'}
		
		
### SHOW ###
class OBJECT_OP_Show_All(bpy.types.Operator):
	bl_idname = 'scene.wow_show_all'
	bl_label = 'Show All'
	bl_description = 'Show All.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			ob.hide = False
		return {'FINISHED'}
		
class OBJECT_OP_Show_Attach(bpy.types.Operator):
	bl_idname = 'scene.wow_show_attachments'
	bl_label = 'Show Attachments'
	bl_description = 'Show Attachments.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'EMPTY' and ob.name.startswith('Attach'):
				ob.hide = False
		return {'FINISHED'}
		
class OBJECT_OP_Show_Armature(bpy.types.Operator):
	bl_idname = 'scene.wow_show_armature'
	bl_label = 'Show Armature'
	bl_description = 'Show Armature.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'ARMATURE' and ob.name == 'Armature':
				ob.hide = False
		return {'FINISHED'}

class OBJECT_OP_Show_Camera(bpy.types.Operator):
	bl_idname = 'scene.wow_show_cameras'
	bl_label = 'Show Cameras'
	bl_description = 'Show Cameras.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'CAMERA':
				ob.hide = False
		return {'FINISHED'}

class OBJECT_OP_Show_Face(bpy.types.Operator):
	bl_idname = 'scene.wow_show_facial'
	bl_label = 'Show Facial'
	bl_description = 'Show Facial.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and re.search('^Mesh(01|02|03|17)', ob.name):
				ob.hide = False
		return {'FINISHED'}
		
class OBJECT_OP_Show_Hair(bpy.types.Operator):
	bl_idname = 'scene.wow_show_hair'
	bl_label = 'Show Hairstyle'
	bl_description = 'Show Hairstyle.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and re.search('^Mesh(00)(?!00)', ob.name):
				ob.hide = False
		return {'FINISHED'}
		
class OBJECT_OP_Show_Armors(bpy.types.Operator):
	bl_idname = 'scene.wow_show_armors'
	bl_label = 'Show Armors'
	bl_description = 'Show Armors.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and re.search('^Mesh(04|05|08|09|10|11|13|18|20).(?!1)', ob.name):
				ob.hide = False
		return {'FINISHED'}
		
class OBJECT_OP_Show_Cloak(bpy.types.Operator):
	bl_idname = 'scene.wow_show_cloak'
	bl_label = 'Show Cloak'
	bl_description = 'Show Cloak.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and re.search('^Mesh(12|15)', ob.name):
				ob.hide = False
		return {'FINISHED'}

class OBJECT_OP_Show_Body(bpy.types.Operator):
	bl_idname = 'scene.wow_show_body'
	bl_label = 'Show Body'
	bl_description = 'Show Body.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and re.search('^Mesh(0000|07|19|0401|0501|1301|2001)', ob.name):
				ob.hide = False
		return {'FINISHED'}

class Wow_Mesh_Props(bpy.types.PropertyGroup):
	
	@classmethod
	def register(Wow_Mesh_Props):

		Wow_Mesh_Props.Description = bpy.props.StringProperty(name="Description",
			description="Mesh description")
		Wow_Mesh_Props.HasCustomTexture = bpy.props.BoolProperty(
			name="", 
			description="Mesh has custom texture assigned",
			default=False)
		Wow_Mesh_Props.CustomTexture = bpy.props.StringProperty(name="Custom Texture", 
			description="Path to texture")
		Wow_Mesh_Props.TextureStyle = bpy.props.EnumProperty(
			name='Texture style',
			description='Style of texture (blending mode)',
			items=[('0', 'Opaque', 'Opaque texture'),
				('1', 'Mod', ''),
				('2', 'Decal', 'Use for textures with transparencies'),
				('3', 'Add', ''),
				('4', 'Mod2x', ''),
				('5', 'Fade', ''),
				('6', 'Unknown6', ''),
				('7', 'Unknown7', '')],
			default='2'
			)

		Wow_Mesh_Props.MaterialOverride = bpy.props.StringProperty(name="Material Override", 
			description="Mesh from which material should be copied")
			
		Wow_Mesh_Props.HasGloss = bpy.props.BoolProperty(
			name="", 
			description="Mesh has gloss effect assigned",
			default=False)
		Wow_Mesh_Props.GlossTexture = bpy.props.StringProperty(name="Gloss Texture", 
			description="Path to gloss texture")

		bpy.types.Mesh.wow_props = bpy.props.PointerProperty(type=Wow_Mesh_Props, 
			name="WoW Mesh Properties", 
			description="WoW Mesh Properties")
	@classmethod
	def unregister(cls):
		del bpy.types.Mesh.wow_props

class Wow_Camera_Props(bpy.types.PropertyGroup):

	@classmethod
	def register(Wow_Camera_Props):

		Wow_Camera_Props.HasData = bpy.props.BoolProperty(
			name="", 
			description="Camera has custom data assigned",
			default=False)
		Wow_Camera_Props.TargetX = bpy.props.FloatProperty(
			name="TargetX",
			description="X coordinate of camera target",
			default=0.0,
			subtype='FACTOR',
			unit='NONE')
		Wow_Camera_Props.TargetY = bpy.props.FloatProperty(
			name="TargetY",
			description="Y coordinate of camera target",
			default=0.0,
			subtype='FACTOR',
			unit='NONE')
		Wow_Camera_Props.TargetZ = bpy.props.FloatProperty(
			name="TargetZ",
			description="Z coordinate of camera target",
			default=0.0,
			subtype='FACTOR',
			unit='NONE')	
		Wow_Camera_Props.CameraType = bpy.props.EnumProperty(
			name='Camera type',
			description='Style of texture',
			items=[('-1', 'FlyBy', 'FlyBy camera (movies)'),
				('0', 'Portrait', 'Portrait camera (character bar)'),
				('1', 'Paperdoll', 'Portrait camera (character menu)')],
			)

		bpy.types.Camera.wow_props = bpy.props.PointerProperty(type=Wow_Camera_Props, 
			name="WoW Camera Properties", 
			description="WoW Camera Properties")
	@classmethod
	def unregister(cls):
		del bpy.types.Camera.wow_props

class Wow_EditBone_Props(bpy.types.PropertyGroup):

	@classmethod
	def register(Wow_EditBone_Props):

		Wow_EditBone_Props.HasData = bpy.props.BoolProperty(
			name="", 
			description="Bone has custom data assigned",
			default=False)
		Wow_EditBone_Props.Flags = bpy.props.IntProperty(
			name="Flags",
			description="Flags",
			default=0,
			min=0,
			max=2147483647)
		Wow_EditBone_Props.SubmeshId = bpy.props.IntProperty(
			name="Submesh Id",
			description="Index of a submesh that bone belongs to",
			default=0,
			min=0,
			max=65535)
		Wow_EditBone_Props.Unknown0 = bpy.props.IntProperty(
			name="Unknown 0",
			default=0,
			min=0,
			max=65535)
		Wow_EditBone_Props.Unknown1 = bpy.props.IntProperty(
			name="Unknown 1",
			default=0,
			min=0,
			max=65535)

		bpy.types.EditBone.wow_props = bpy.props.PointerProperty(type=Wow_EditBone_Props, 
			name="WoW EditBone Properties", 
			description="WoW EditBone Properties")
	@classmethod
	def unregister(cls):
		del bpy.types.EditBone.wow_props
	
class DATA_PT_wowproperties_mesh_props(bpy.types.Panel):
	bl_label = "WoW Properies"
	bl_idname = "wowtools.mesh_ops"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "object"

	def draw(self, context):

		layout = self.layout

		oTargetObject = context.active_object
		oTargetBone = bpy.context.active_bone

		targetType = ""
		if oTargetObject.data is not None:
			if oTargetObject.type == "MESH":
				targetType = "MESH"
			elif oTargetObject.type == "CAMERA":
				targetType = "CAMERA"
		if oTargetBone is not None and (bpy.context.active_object.mode == 'EDIT' or bpy.context.active_object.mode == 'POSE'):
			targetType = "BONE"
			
		if targetType == "":
			layout.operator("wowtools.transfer_old_properties")
			return

		if targetType == "MESH":
			props = oTargetObject.data.wow_props
			layout.prop(props, 'Description')
			layout.prop(props, 'HasCustomTexture', text="Enable custom texture")
			box = layout.box()
			box.prop(props, 'CustomTexture')
			box.prop(props, 'TextureStyle')
			if not props.HasCustomTexture:
				box.active = False

			layout.prop(props, 'HasGloss', text="Enable gloss texture")
			box = layout.box()
			box.prop(props, 'GlossTexture')
			layout.prop_search(props, "MaterialOverride", context.scene, "objects")
			if not props.HasGloss:
				box.active = False
		elif targetType == "CAMERA":
			props = oTargetObject.data.wow_props
			layout.prop(props, 'HasData', text="Enable camera modify")
			box = layout.box()
			box.prop(props, 'CameraType')
			box.prop(props, 'TargetX')
			box.prop(props, 'TargetY')
			box.prop(props, 'TargetZ')
			if not props.HasData:
				box.active = False
		elif targetType == "BONE":
			props = oTargetBone.wow_props
			layout.prop(props, 'HasData', text="Enable bone modify")
			box = layout.box()
			box.prop(props, 'Flags')
			box.prop(props, 'SubmeshId')
			box.prop(props, 'Unknown0')
			box.prop(props, 'Unknown1')
			if not props.HasData:
				box.active = False
		layout.operator("wowtools.transfer_old_properties")
			
class DATA_OT_wowtools_transfer_old_properties(bpy.types.Operator):

	bl_idname = "wowtools.transfer_old_properties"
	bl_label = "Transfer custom properties"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH':
				if 'Description' in ob:
					if ob['Description'] is not None and len(ob['Description']) > 0:
						ob.data.wow_props.Description = ob['Description']
					del ob['Description']
				if 'CustomTexture' in ob:
					if ob['CustomTexture'] is not None and len(ob['CustomTexture']) > 0:
						ob.data.wow_props.HasCustomTexture = True
						ob.data.wow_props.CustomTexture = ob['CustomTexture']
						ob.data.wow_props.TextureStyle = '2'	# decal
					del ob['CustomTexture']
				if 'GlossTexture' in ob:
					if ob['GlossTexture'] is not None and len(ob['GlossTexture']) > 0:
						ob.data.wow_props.HasGloss = True
						ob.data.wow_props.GlossTexture = ob['GlossTexture']
					del ob['GlossTexture']
			elif ob.type == 'CAMERA':
				fail = False
				hasData = False
				if 'Type' in ob:
					hasData = True
					if ob['Type'] == -1:
						ob.data.wow_props.CameraType = '-1'
					elif ob['Type'] == 0:
						ob.data.wow_props.CameraType = '0'
					elif ob['Type'] == 1:
						ob.data.wow_props.CameraType = '1'
					else:
						fail = True
					del ob['Type']
				else:
					fail = True
				if 'TargetX' in ob:
					hasData = True
					ob.data.wow_props.TargetX = ob['TargetX']
					del ob['TargetX']
				else:
					fail = True
				if 'TargetY' in ob:
					hasData = True
					ob.data.wow_props.TargetY = ob['TargetY']
					del ob['TargetY']
				else:
					fail = True
				if 'TargetZ' in ob:
					hasData = True
					ob.data.wow_props.TargetZ = ob['TargetZ']
					del ob['TargetZ']
				else:
					fail = True
				if hasData and not fail:
					ob.data.wow_props.HasData = True
			elif ob.type == 'ARMATURE':
				for bone in ob.data.edit_bones:
					fail = False
					hasData = False
					if 'Flags' in bone:
						hasData = True
						bone.wow_props.Flags = bone['Flags']
						del bone['Flags']
					else:
						fail = True
					if 'SubmeshId' in bone:
						hasData = True
						bone.wow_props.SubmeshId = bone['SubmeshId']
						del bone['SubmeshId']
					else:
						fail = True
					if 'Unknown0' in bone:
						hasData = True
						bone.wow_props.Unknown0 = bone['Unknown0']
						del bone['Unknown0']
					else:
						fail = True
					if 'Unknown1' in bone:
						hasData = True
						bone.wow_props.Unknown1 = bone['Unknown1']
						del bone['Unknown1']
					else:
						fail = True
					if hasData and not fail:
						bone.wow_props.HasData = True

		return {'FINISHED'}

#******************************
#---===Register===
#******************************
def register():
	bpy.utils.register_module(__name__)
	
def unregister():
	bpy.utils.unregister_module(__name__)

	if bpy.context.scene.get('CONFIG_WowTools') != None:
		del bpy.context.scene['CONFIG_WowTools']
	try:
		del bpy.types.Scene.CONFIG_WowTools
	except:
		pass

if __name__ == '__main__':
	main()
