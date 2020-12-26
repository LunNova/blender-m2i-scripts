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
	bl_idname = 'OBJECT_PT_wow_tools_hide_operators'
	bl_region_type = 'UI'
	bl_space_type = 'VIEW_3D'
	bl_category = 'WoW'
	#bl_space_type = 'PROPERTIES'
	#bl_region_type = 'WINDOW'
	#bl_context = 'scene'
	
	def draw(self, context):
		layout = self.layout.split()
		
		layout_col1 = layout.column()
		layout_col1.label(text="Hide", icon='RESTRICT_VIEW_ON')
		layout_col1.operator('scene.wow_hide_all', text='All')
		layout_col1.operator('scene.wow_hide_attachments', text='Attach')
		layout_col1.operator('scene.wow_hide_armature', text='Armature')
		layout_col1.operator('scene.wow_hide_cameras', text='Camera')
		layout_col1.operator('scene.wow_hide_facial', text='Facial')
		layout_col1.operator('scene.wow_hide_hair', text='Hair')
		layout_col1.operator('scene.wow_hide_accessory', text='Accessory')
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
		layout_col2.operator('scene.wow_show_accessory', text='Accessory')
		layout_col2.operator('scene.wow_show_armors', text='Armor')
		layout_col2.operator('scene.wow_show_cloak', text='Cloak')
		layout_col2.operator('scene.wow_show_body', text='Body')

		props = context.scene.wow_props
		layout_col3 = layout.column()
		layout_col3.label(text='Index')
		layout_col3.label(text='')
		layout_col3.label(text='')
		layout_col3.label(text='')
		layout_col3.label(text='')
		row = layout_col3.row()
		row.label(text=str(props.CurrentFacialIndex))
		row.operator('scene.wow_next_facial', text='', icon='RIGHTARROW')
		row = layout_col3.row()
		row.label(text=str(props.CurrentHairIndex))
		row.operator('scene.wow_next_hair', text='', icon='RIGHTARROW')
		row = layout_col3.row()
		row.label(text=str(props.CurrentAccessoryIndex))
		row.operator('scene.wow_next_accessory', text='', icon='RIGHTARROW')

### HIDE ###
class OBJECT_OT_Hide_All(bpy.types.Operator):
	bl_idname = 'scene.wow_hide_all'
	bl_label = 'Hide All'
	bl_description = 'Hide All.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			ob.hide_set(True)
		return {'FINISHED'}
		
class OBJECT_OT_Hide_Attach(bpy.types.Operator):
	bl_idname = 'scene.wow_hide_attachments'
	bl_label = 'Hide Attachments'
	bl_description = 'Hide Attachments.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'EMPTY' and ob.name.startswith('Attach'):
				ob.hide_set(True)
		return {'FINISHED'}

class OBJECT_OT_Hide_Armature(bpy.types.Operator):
	bl_idname = 'scene.wow_hide_armature'
	bl_label = 'Hide Armature'
	bl_description = 'Hide Armature.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'ARMATURE' and ob.name == 'Armature':
				ob.hide_set(True)
		return {'FINISHED'}

class OBJECT_OT_Hide_Camera(bpy.types.Operator):
	bl_idname = 'scene.wow_hide_cameras'
	bl_label = 'Hide Cameras'
	bl_description = 'Hide Cameras.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'CAMERA':
				ob.hide_set(True)
		return {'FINISHED'}
		
class OBJECT_OT_Hide_Face(bpy.types.Operator):
	bl_idname = 'scene.wow_hide_facial'
	bl_label = 'Hide Facial'
	bl_description = 'Hide Facial.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and IsMeshType(ob.name, WoWMeshType.Facial):
				ob.hide_set(True)
		return {'FINISHED'}
		
class OBJECT_OT_Hide_Hair(bpy.types.Operator):
	bl_idname = 'scene.wow_hide_hair'
	bl_label = 'Hide Hairstyle'
	bl_description = 'Hide Hairstyle.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and IsMeshType(ob.name, WoWMeshType.Hair):
				ob.hide_set(True)
		return {'FINISHED'}

class OBJECT_OT_Hide_Accessory(bpy.types.Operator):
	bl_idname = 'scene.wow_hide_accessory'
	bl_label = 'Hide Accessory'
	bl_description = 'Hide Accessory.'

	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and IsMeshType(ob.name, WoWMeshType.Accessory):
				ob.hide_set(True)
		return {'FINISHED'}

class OBJECT_OT_Hide_Armors(bpy.types.Operator):
	bl_idname = 'scene.wow_hide_armors'
	bl_label = 'Hide Armors'
	bl_description = 'Hide Armors.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and IsMeshType(ob.name, WoWMeshType.Armor):
				ob.hide_set(True)
		return {'FINISHED'}
		
class OBJECT_OT_Hide_Cloak(bpy.types.Operator):
	bl_idname = 'scene.wow_hide_cloak'
	bl_label = 'Hide Cloak'
	bl_description = 'Hide Cloak.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and IsMeshType(ob.name, WoWMeshType.Cloak):
				ob.hide_set(True)
		return {'FINISHED'}
		
class OBJECT_OT_Hide_Body(bpy.types.Operator):
	bl_idname = 'scene.wow_hide_body'
	bl_label = 'Hide Body'
	bl_description = 'Hide Body.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and IsMeshType(ob.name, WoWMeshType.Body):
				ob.hide_set(True)
		return {'FINISHED'}
		
		
### SHOW ###
class OBJECT_OT_Show_All(bpy.types.Operator):
	bl_idname = 'scene.wow_show_all'
	bl_label = 'Show All'
	bl_description = 'Show All.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			ob.hide_set(False)
		return {'FINISHED'}
		
class OBJECT_OT_Show_Attach(bpy.types.Operator):
	bl_idname = 'scene.wow_show_attachments'
	bl_label = 'Show Attachments'
	bl_description = 'Show Attachments.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'EMPTY' and ob.name.startswith('Attach'):
				ob.hide_set(False)
		return {'FINISHED'}
		
class OBJECT_OT_Show_Armature(bpy.types.Operator):
	bl_idname = 'scene.wow_show_armature'
	bl_label = 'Show Armature'
	bl_description = 'Show Armature.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'ARMATURE' and ob.name == 'Armature':
				ob.hide_set(False)
		return {'FINISHED'}

class OBJECT_OT_Show_Camera(bpy.types.Operator):
	bl_idname = 'scene.wow_show_cameras'
	bl_label = 'Show Cameras'
	bl_description = 'Show Cameras.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'CAMERA':
				ob.hide_set(False)
		return {'FINISHED'}

class OBJECT_OT_Show_Face(bpy.types.Operator):
	bl_idname = 'scene.wow_show_facial'
	bl_label = 'Show Facial'
	bl_description = 'Show Facial.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and IsMeshType(ob.name, WoWMeshType.Facial):
				ob.hide_set(False)
		return {'FINISHED'}

class OBJECT_OT_Show_Hair(bpy.types.Operator):
	bl_idname = 'scene.wow_show_hair'
	bl_label = 'Show Hairstyle'
	bl_description = 'Show Hairstyle.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and IsMeshType(ob.name, WoWMeshType.Hair):
				ob.hide_set(False)
		return {'FINISHED'}

class OBJECT_OT_Show_Accessory(bpy.types.Operator):
	bl_idname = 'scene.wow_show_accessory'
	bl_label = 'Show Accessory'
	bl_description = 'Show Accessory.'

	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and IsMeshType(ob.name, WoWMeshType.Accessory):
				ob.hide_set(False)
		return {'FINISHED'}

class OBJECT_OT_Show_Armors(bpy.types.Operator):
	bl_idname = 'scene.wow_show_armors'
	bl_label = 'Show Armors'
	bl_description = 'Show Armors.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and IsMeshType(ob.name, WoWMeshType.Armor):
				ob.hide_set(False)
		return {'FINISHED'}
		
class OBJECT_OT_Show_Cloak(bpy.types.Operator):
	bl_idname = 'scene.wow_show_cloak'
	bl_label = 'Show Cloak'
	bl_description = 'Show Cloak.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and IsMeshType(ob.name, WoWMeshType.Cloak):
				ob.hide_set(False)
		return {'FINISHED'}

class OBJECT_OT_Show_Body(bpy.types.Operator):
	bl_idname = 'scene.wow_show_body'
	bl_label = 'Show Body'
	bl_description = 'Show Body.'
	
	def execute(self, context):
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH' and IsMeshType(ob.name, WoWMeshType.Body):
				ob.hide_set(False)
		return {'FINISHED'}

class OBJECT_OT_Next_Facial(bpy.types.Operator):
	bl_idname = 'scene.wow_next_facial'
	bl_label = 'Next facial'
	bl_description = 'Next facial'

	def execute(self, context):
		props = context.scene.wow_props
		props.CurrentFacialIndex = props.CurrentFacialIndex + 1

		obs = []
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH':
				if IsMeshType(ob.name, WoWMeshType.Facial):
					obs.append(ob)

		if props.CurrentFacialIndex >= len(obs):
			props.CurrentFacialIndex = 0

		for i, ob in enumerate(obs):
			if i == props.CurrentFacialIndex:
				ob.hide_set(False)
			else:
				ob.hide_set(True)

		return {'FINISHED'}

class OBJECT_OT_Next_Hair(bpy.types.Operator):
	bl_idname = 'scene.wow_next_hair'
	bl_label = 'Next hair'
	bl_description = 'Next hair'

	def execute(self, context):
		props = context.scene.wow_props
		props.CurrentHairIndex = props.CurrentHairIndex + 1

		obs = []
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH':
				if IsMeshType(ob.name, WoWMeshType.Hair):
					obs.append(ob)

		if props.CurrentHairIndex >= len(obs):
			props.CurrentHairIndex = 0

		for i, ob in enumerate(obs):
			if i == props.CurrentHairIndex:
				ob.hide_set(False)
			else:
				ob.hide_set(True)

		return {'FINISHED'}

class OBJECT_OT_Next_Accessory(bpy.types.Operator):
	bl_idname = 'scene.wow_next_accessory'
	bl_label = 'Next accessory'
	bl_description = 'Next accessory'

	def execute(self, context):
		props = context.scene.wow_props
		props.CurrentAccessoryIndex = props.CurrentAccessoryIndex + 1

		obs = []
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH':
				if IsMeshType(ob.name, WoWMeshType.Accessory):
					obs.append(ob)

		if props.CurrentAccessoryIndex >= len(obs):
			props.CurrentAccessoryIndex = 0

		for i, ob in enumerate(obs):
			if i == props.CurrentAccessoryIndex:
				ob.hide_set(False)
			else:
				ob.hide_set(True)

		return {'FINISHED'}

class Wow_Mesh_Props(bpy.types.PropertyGroup):
	
	@classmethod
	def register(Wow_Mesh_Props):

		Wow_Mesh_Props.Description = bpy.props.StringProperty(
			name="Description",
			description="Mesh description")

		Wow_Mesh_Props.MaterialOverride = bpy.props.StringProperty(
			name="Material Override", 
			description="Mesh from which material should be copied")

		Wow_Mesh_Props.ShaderId = bpy.props.IntProperty(
			name='Shader',
			description="Shader",
			default=-1,
			min=-1)

		Wow_Mesh_Props.OriginalMeshIndex = bpy.props.IntProperty(
			name='Originan mesh index',
			description="Mesh index from original skin file. Change only if you know what you do",
			default=-1,
			min=-1,
			max=1024)

		Wow_Mesh_Props.BlendMode = bpy.props.EnumProperty(
			name='Blend mode',
			description='Blend mode',
			items=[
				('-1', 'None', 'Not set'),
				('0', 'Opaque', 'Opaque texture'),
				('1', 'Mod', ''),
				('2', 'Decal', 'Use for textures with transparencies'),
				('3', 'Add', ''),
				('4', 'Mod2x', ''),
				('5', 'Fade', ''),
				('6', 'Unknown6', ''),
				('7', 'Unknown7', '')
				],
			default='-1'
			)

		Wow_Mesh_Props.RenderFlags = bpy.props.EnumProperty(
			name='Render flags',
			description='Render flags',
			items=[
				('0', 'None', '', '', 0),
				('1', 'Unlit', '', 'None', 0x1),
				('2', 'Unfogged', '', 'None', 0x2),
				('3', 'TwoSided', '', 'None', 0x4),
				('4', 'BillBoard', '', 'None', 0x8),
				('5', 'NoZBuffer', '', 'None', 0x10),
				('6', 'Unk6', '', 'None', 0x40),
				('7', 'Unk7', '', 'None', 0x80),
				('8', 'Unk8', '', 'None', 0x400),
				('9', 'Unk9', '', 'None', 0x800)
				],
			default={'3'},
			options={'ENUM_FLAG'}
			)

		Wow_Mesh_Props.ShaderId = bpy.props.EnumProperty(
			name='Shader Id',
			description='Shader Id',
			items=[
				( '-1', 'None', '' ),
				( '32768', '0 - Combiners_Opaque_Mod2xNA_Alpha - Diffuse_T1_Env', '' ),
				( '32769', '1 - Combiners_Opaque_AddAlpha - Diffuse_T1_Env', '' ),
				( '32770', '2 - Combiners_Opaque_AddAlpha_Alpha - Diffuse_T1_Env', '' ),
				( '32771', '3 - Combiners_Opaque_Mod2xNA_Alpha_Add - Diffuse_T1_Env_T1', '' ),
				( '32772', '4 - Combiners_Mod_AddAlpha - Diffuse_T1_Env', '' ),
				( '32773', '5 - Combiners_Opaque_AddAlpha - Diffuse_T1_T1', '' ),
				( '32774', '6 - Combiners_Mod_AddAlpha - Diffuse_T1_T1', '' ),
				( '32775', '7 - Combiners_Mod_AddAlpha_Alpha - Diffuse_T1_Env', '' ),
				( '32776', '8 - Combiners_Opaque_Alpha_Alpha - Diffuse_T1_Env', '' ),
				( '32777', '9 - Combiners_Opaque_Mod2xNA_Alpha_3s - Diffuse_T1_Env_T1', '' ),
				( '32778', '10 - Combiners_Opaque_AddAlpha_Wgt - Diffuse_T1_T1', '' ),
				( '32779', '11 - Combiners_Mod_Add_Alpha - Diffuse_T1_Env', '' ),
				( '32780', '12 - Combiners_Opaque_ModNA_Alpha - Diffuse_T1_Env', '' ),
				( '32781', '13 - Combiners_Mod_AddAlpha_Wgt - Diffuse_T1_Env', '' ),
				( '32782', '14 - Combiners_Mod_AddAlpha_Wgt - Diffuse_T1_T1', '' ),
				( '32783', '15 - Combiners_Opaque_AddAlpha_Wgt - Diffuse_T1_T2', '' ),
				( '32784', '16 - Combiners_Opaque_Mod_Add_Wgt - Diffuse_T1_Env', '' ),
				( '32785', '17 - Combiners_Opaque_Mod2xNA_Alpha_UnshAlpha - Diffuse_T1_Env_T1', '' ),
				( '32786', '18 - Combiners_Mod_Dual_Crossfade - Diffuse_T1', '' ),
				( '32787', '19 - Combiners_Mod_Depth - Diffuse_EdgeFade_T1', '' ),
				( '32788', '20 - Combiners_Opaque_Mod2xNA_Alpha_Alpha - Diffuse_T1_Env_T2', '' ),
				( '32789', '21 - Combiners_Mod_Mod - Diffuse_EdgeFade_T1_T2', '' ),
				( '32790', '22 - Combiners_Mod_Masked_Dual_Crossfade - Diffuse_T1_T2', '' ),
				( '32791', '23 - Combiners_Opaque_Alpha - Diffuse_T1_T1', '' ),
				( '32792', '24 - Combiners_Opaque_Mod2xNA_Alpha_UnshAlpha - Diffuse_T1_Env_T2', '' ),
				( '32793', '25 - Combiners_Mod_Depth - Diffuse_EdgeFade_Env', '' ),
				( '32794', '26 - Guild - Diffuse_T1_T2_T1', '' ),
				( '32795', '27 - Guild_NoBorder - Diffuse_T1_T2', '' ),
				( '32796', '28 - Guild_Opaque - Diffuse_T1_T2_T1', '' ),
				( '32797', '29 - Illum - Diffuse_T1_T1', '' ),
				( '32798', '30 - Combiners_Mod_Mod_Mod_Const - Diffuse_T1_T2_T3', '' ),
				( '32799', '31 - Combiners_Mod_Mod_Mod_Const - Color_T1_T2_T3', '' ),
				( '32800', '32 - Combiners_Opaque - Diffuse_T1', '' ),
				( '32801', '33 - Combiners_Mod_Mod2x - Diffuse_EdgeFade_T1_T2', '' )
				],
			default='-1'
			)

		textureTypeItems = [
				('-1', 'None', ''),
				('0', 'Hardcoded', ''),
				('1', 'Skin', ''),
				('2', 'ObjectSkin', ''),
				('3', 'WeaponBlade', ''),
				('4', 'WeaponHandle', ''),
				('5', 'Environment', ''),
				('6', 'Hair', ''),
				('7', 'FacialHair', ''),
				('8', 'SkinExtra', ''),
				('9', 'UiSkin', ''),
				('10', 'TaurenMane', ''),
				('11', 'Monster1', ''),
				('12', 'Monster2', ''),
				('13', 'Monster3', ''),
				('14', 'ItemIcon', ''),
				('15', 'GuildBackgroundColor', ''),
				('16', 'GuildEmblemColor', ''),
				('17', 'GuildBorderColor', ''),
				('18', 'GuildEmblem', ''),

				('19', 'Eyes', ''),
				('20', 'Accessory', ''),
				('21', 'SecondarySkin', ''),
				('22', 'SecondaryHair', ''),
				('23', 'SecondaryUnk', ''),
				('24', 'Unk24', '')
		]

		Wow_Mesh_Props.TextureType0 = bpy.props.EnumProperty(name='Texture type 0', description='Texture type 0', items=textureTypeItems, default='-1')
		Wow_Mesh_Props.TextureType1 = bpy.props.EnumProperty(name='Texture type 1', description='Texture type 1', items=textureTypeItems, default='-1')
		Wow_Mesh_Props.TextureType2 = bpy.props.EnumProperty(name='Texture type 2', description='Texture type 2', items=textureTypeItems, default='-1')
		Wow_Mesh_Props.TextureType3 = bpy.props.EnumProperty(name='Texture type 3', description='Texture type 3', items=textureTypeItems, default='-1')

		Wow_Mesh_Props.TextureName0 = bpy.props.StringProperty(name="Texture 0", description="Path to texture relative to WoW directory")
		Wow_Mesh_Props.TextureName1 = bpy.props.StringProperty(name="Texture 1", description="Path to texture relative to WoW directory")
		Wow_Mesh_Props.TextureName2 = bpy.props.StringProperty(name="Texture 2", description="Path to texture relative to WoW directory")
		Wow_Mesh_Props.TextureName3 = bpy.props.StringProperty(name="Texture 3", description="Path to texture relative to WoW directory")

		Wow_Mesh_Props.MenuType = bpy.props.EnumProperty(
			items=[
				('0', 'Simple', ''),
				('1', 'Extended', '')
			],
			default='1'
		)

		# legacy
		Wow_Mesh_Props.HasCustomTexture = bpy.props.BoolProperty(
			name="", 
			description="Mesh has custom texture assigned",
			default=False)
		Wow_Mesh_Props.CustomTexture = bpy.props.StringProperty(
			name="Custom Texture", 
			description="Path to texture")

		Wow_Mesh_Props.TextureStyle = bpy.props.EnumProperty(
			name='Texture style',
			description='Style of texture (blending mode)',
			items=[
				('0', 'Opaque', 'Opaque texture'),
				('1', 'Mod', ''),
				('2', 'Decal', 'Use for textures with transparencies'),
				('3', 'Add', ''),
				('4', 'Mod2x', ''),
				('5', 'Fade', ''),
				('6', 'Unknown6', ''),
				('7', 'Unknown7', '')],
			default='2'
			)

		Wow_Mesh_Props.HasGloss = bpy.props.BoolProperty(
			name="", 
			description="Mesh has gloss effect assigned",
			default=False)

		Wow_Mesh_Props.GlossTexture = bpy.props.StringProperty(
			name='Gloss Texture', 
			description="Path to gloss texture")
		# end legacy

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
			precision=5,
			subtype='FACTOR',
			unit='NONE')
		Wow_Camera_Props.TargetY = bpy.props.FloatProperty(
			name="TargetY",
			description="Y coordinate of camera target",
			default=0.0,
			precision=5,
			subtype='FACTOR',
			unit='NONE')
		Wow_Camera_Props.TargetZ = bpy.props.FloatProperty(
			name="TargetZ",
			description="Z coordinate of camera target",
			default=0.0,
			precision=5,
			subtype='FACTOR',
			unit='NONE')
		Wow_Camera_Props.Type = bpy.props.EnumProperty(
			name='Camera type',
			description='Camera type',
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
	bl_idname = "DATA_PT_wowproperties_mesh_props"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "object"

	def draw(self, context):
		layout = self.layout.column()

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
			#layout.operator("wowtools.transfer_old_properties")
			return

		if targetType == "MESH":
			props = oTargetObject.data.wow_props

			layout.prop(props, 'MenuType', expand=True)

			textureBox = layout.box()
			textureBox.prop(props, 'TextureType0', text='Custom texture')
			if props.TextureType0 == '0':
				textureBox.prop(props, 'TextureName0', text='Path')

			flagsBox = layout.box()
			flagsBox.prop(props, 'BlendMode', text='Blend Mode')

			if props.MenuType == '1' and props.BlendMode != '-1':
				flagsBox.prop(props, 'RenderFlags', text='Render Flags')

			if props.MenuType == '0':
				boxShader = layout.box();
				boxShader.prop(props, 'TextureName1', text="Gloss Texture")
			elif props.MenuType == '1':
				boxShader = layout.box();
				boxShader.prop(props, 'ShaderId', text="Shader")

				if props.ShaderId != '-1':
					if int(props.ShaderId) not in opCountByShader:
						props.ShaderId = '-1';
					else:
						textureCount = opCountByShader[int(props.ShaderId)]
						if textureCount > 1:
							boxShader.label("Select shader textures (%d):" % (textureCount - 1))
						for i in range(1, textureCount):
							box = boxShader.box()
							box.prop(props, 'TextureType' + str(i), text='Texture %d' % i)
							type = getattr(props, 'TextureType' + str(i))
							if type == '0':
								box.prop(props, 'TextureName' + str(i), text='Path')

			layout.prop_search(props, 'MaterialOverride', context.scene, "objects")
			layout.prop(props, 'OriginalMeshIndex')
			layout.prop(props, 'Description')
		elif targetType == "CAMERA":
			props = oTargetObject.data.wow_props
			layout.prop(props, 'HasData', text="Enable camera modify")
			box = layout.box()
			box.prop(props, 'Type')
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
		#layout.operator("wowtools.transfer_old_properties")
			
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
						ob.data.wow_props.Type = '-1'
					elif ob['Type'] == 0:
						ob.data.wow_props.Type = '0'
					elif ob['Type'] == 1:
						ob.data.wow_props.Type = '1'
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

class Wow_Scene_Props(bpy.types.PropertyGroup):

	@classmethod
	def register(Wow_Scene_Props):
		Wow_Scene_Props.BoneMigrationFile = bpy.props.StringProperty(name="Bone migrations Source",
			description="File with bone migration data")

		Wow_Scene_Props.CurrentHairIndex = bpy.props.IntProperty(name="Current hair index", min=0, default=0)
		Wow_Scene_Props.CurrentFacialIndex = bpy.props.IntProperty(name="Current facial index", min=0, default=0)
		Wow_Scene_Props.CurrentAccessoryIndex = bpy.props.IntProperty(name="Current accessory index", min=0, default=0)

		bpy.types.Scene.wow_props = bpy.props.PointerProperty(type=Wow_Scene_Props, 
			name="WoW Scene Properties", 
			description="WoW Scene Properties")

	@classmethod
	def unregister(cls):
		del bpy.types.Scene.wow_props

class DATA_PT_BoneMigratePanel(bpy.types.Panel):
	bl_label = "Bone migration"
	bl_region_type = 'UI'
	bl_space_type = 'VIEW_3D'
	bl_category = 'WoW'

	def draw(self, context):
		layout = self.layout
		props = context.scene.wow_props
		row = layout.row()
		row.prop(props, 'BoneMigrationFile')
		row.operator('wowtools.open_bone_file', text='', icon='FILE')
		layout.operator('wowtools.migrate_vertex_groups')

from bpy_extras.io_utils import ImportHelper
class OpOpenBoneFile(bpy.types.Operator, ImportHelper):

	bl_idname = "wowtools.open_bone_file"
	bl_label = "Open Bone Migration File"

	# ImportHelper mixin class uses this
	filename_ext = ".txt"

	filter_glob : bpy.props.StringProperty(
			default="*.txt",
			options={'HIDDEN'},
			)

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		context.scene.wow_props.BoneMigrationFile = self.properties.filepath
		return {'FINISHED'}

from .wow_common import *
class OpDoMigrateVertexGroups(bpy.types.Operator):

	bl_idname = "wowtools.migrate_vertex_groups"
	bl_label = "Migrate"

	@classmethod
	def poll(cls, context):
		return len(context.scene.wow_props.BoneMigrationFile) > 0 and len(bpy.context.selected_objects) > 0

	def loadBoneDiff(self, filePath):
		OldBoneToNewBone = dict()

		with open(filePath) as f:
			lines = f.readlines()

		lines = [line.strip() for line in lines]
		for line in lines:
			if line.startswith('#'):
				continue

			res = re.search('(\d+)\s*:\s*(.*)', line);
			if res is None:
				raise Exception('Wrong remap structure: ' + line)

			OldBoneId = int(res.group(1))
			newIndexes = res.group(2)
			res2 = re.findall('(\d+)', newIndexes)
			if res2 is None:
				raise Exception('Failed to parse new bone index for old bone#' + str(OldBoneId))

			if len(res2) != 1:
				raise Exception('Exactly one new bone index muse be specified for old bone #' + str(OldBoneId))

			NewBoneId = int(res2[0])

			if OldBoneId == NewBoneId:
				print('Skipped loading same bones remap #' + str(OldBoneId))
				continue

			OldBoneToNewBone['Bone' + str('%03d' % OldBoneId)] = 'Bone' + str('%03d' % NewBoneId)

		return OldBoneToNewBone

	def execute(self, context):
		Meshes = list()
		
		for SourceMesh in bpy.context.selected_objects:
			if SourceMesh.type == 'MESH':
				Meshes.append(SourceMesh)
				
		if len(Meshes) == 0:
			self.report({'ERROR'}, 'No meshes selected')
			return {'FINISHED'}

		try:
			OldBoneToNewBone = self.loadBoneDiff(context.scene.wow_props.BoneMigrationFile)
		except Exception as e:
			self.report({'ERROR'}, 'Failed to parse bone file: ' + str(e))
			return {'FINISHED'}

		if len(OldBoneToNewBone) == 0:
			self.report({'ERROR'}, 'No bone remaps loaded, file empty or corrupted')
			return {'FINISHED'}

		# modify vertex group names
		bpy.ops.object.mode_set(mode = 'OBJECT', toggle = False)

		for SourceMesh in Meshes:
			# rename groups to new names 
			for i, VertexGroup in enumerate(SourceMesh.vertex_groups):
				if VertexGroup.name in OldBoneToNewBone:
					VertexGroup.name = '_' + OldBoneToNewBone[VertexGroup.name]

			# remove tmp _ symbol (guaranteed uniqueness)
			for i, VertexGroup in enumerate(SourceMesh.vertex_groups):
				if VertexGroup.name.startswith('_'):
					VertexGroup.name = VertexGroup.name[1:]

		return {'FINISHED'}
