#----------------------------------------------------------
# File wow_pose_tools.py
#----------------------------------------------------------
bl_info = {
	'name': 'WoW Pose Tools',
	'author': 'Suncurio',
	'version': (1, 0, 0),
	'blender': (2, 73, 0),
	'api': 36302,
	#'location': 'Properties space > Scene tab > WoW Tools panel',
	'location': 'VIEW 3D > Tools > WoW Pose Tools panel',
	'description': 'WoW Pose Tools',
	'warning': '',
	'wiki_url': '',
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
class OBJECT_PT_WoW_Pose(bpy.types.Panel):
	
	bl_label = 'WoW Pose Tools'
	#bl_space_type = 'PROPERTIES'
	#bl_region_type = 'WINDOW'
	#bl_context = 'scene'
	bl_idname = 'WoWPoseTools'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = 'Tools'
	
	def draw(self, context):
		self.layout.operator('scene.wow_apply_modifiers', text='Apply armature mods');
		self.layout.operator('scene.wow_create_modifiers', text='Create armature mods');
		self.layout.operator('scene.wow_apply_pose', text='Apply pose');

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

		#bpy.ops.object.select_all(action = 'DESELECT')
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

	if bpy.context.scene.get('CONFIG_WowPoseTools') != None:
		del bpy.context.scene['CONFIG_WowPoseTools']
	try:
		del bpy.types.Scene.CONFIG_WowPoseTools
	except:
		pass

if __name__ == '__main__':
	main()