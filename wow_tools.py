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

		self.layout.operator('scene.wow_apply_modifiers', text='Apply armature mods');
		self.layout.operator('scene.wow_create_modifiers', text='Create armature mods');
		self.layout.operator('scene.wow_apply_pose', text='Apply pose');

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

class OBJECT_OP_Apply_Modifiers(bpy.types.Operator):
	bl_idname = 'scene.wow_apply_modifiers'
	bl_label = 'Apply armature modifiers'
	bl_description = 'Apply armature modifiers to all meshes.'
	
	def execute(self, context):
		bpy.ops.object.select_all(action = 'DESELECT')
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH':
				bpy.context.scene.objects.active = ob
				for mod in ob.modifiers:
					if mod.type == 'ARMATURE':
						bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)
		return {'FINISHED'}
		
class OBJECT_OP_Create_Modifiers(bpy.types.Operator):
	bl_idname = 'scene.wow_create_modifiers'
	bl_label = 'Create armature modifiers'
	bl_description = 'Create armature modifiers on all meshes, which does not have any. Mesh\'s parent should be source armature.'
	
	def execute(self, context):
		#validate
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH':
				bpy.context.scene.objects.active = ob
				found=False
				#chech mesh already has armature modifier
				for mod in ob.modifiers:
					if mod.type == 'ARMATURE':
						found=True
						break
				if found == False:
					if ob.parent is None or ob.parent.type != 'ARMATURE':
						self.report({'ERROR'}, "Mesh '%s' does not have parent or parent is not armature" % ob.name)
						return {'FINISHED'}

		bpy.ops.object.select_all(action = 'DESELECT')
		#apply
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH':
				bpy.context.scene.objects.active = ob
				found=False
				#chech mesh already has armature modifier
				for mod in ob.modifiers:
					if mod.type == 'ARMATURE':
						found=True
						break
				if found == False:
					mod = ob.modifiers.new('Armature', 'ARMATURE')
					if ob.parent is not None and ob.parent.type == 'ARMATURE':
						mod.object = ob.parent
		return {'FINISHED'}
		
class OBJECT_OP_Apply_Pose(bpy.types.Operator):
	bl_idname = 'scene.wow_apply_pose'
	bl_label = 'Apply pose'
	bl_description = 'Apply current pose as rest pose. Original Blender function is bugged - it does not respect attachments.'

	def execute(self, context):
		if bpy.context.active_object.mode != 'POSE':
			self.report({'ERROR'}, "Must be in pose mode")
			return {'FINISHED'}
		BoneByAttach = dict()
		ParentByAttach = dict()
		# detach attachments
		for ob in bpy.context.scene.objects:
			if ob.type == 'EMPTY' and ob.name.startswith('Attach'):
				BoneByAttach[ob.name] = ob.parent_bone
				ParentByAttach[ob.name] = ob.parent
				ob.parent_bone = ''
				ob.parent = None
		#apply pose
		bpy.ops.pose.armature_apply()
		# attach back
		for ob in bpy.context.scene.objects:
			if ob.type == 'EMPTY' and ob.name.startswith('Attach'):
				ob.parent = ParentByAttach[ob.name]
				ob.parent_type = 'BONE'
				ob.parent_bone = BoneByAttach[ob.name]

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
