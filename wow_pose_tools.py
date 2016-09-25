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
		self.layout.operator('scene.wow_create_modifiers', text='Create armature mods');
		self.layout.operator('scene.wow_apply_modifiers', text='Apply armature mods');
		self.layout.operator('scene.wow_apply_pose', text='Apply pose');

class OBJECT_OP_Apply_Modifiers(bpy.types.Operator):
	bl_idname = 'scene.wow_apply_modifiers'
	bl_label = 'Apply armature modifiers'
	bl_description = 'Apply armature modifiers to all meshes.'
	
	def execute(self, context):
		#bpy.ops.object.select_all(action = 'DESELECT')
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
		if bpy.context.active_object is None or bpy.context.active_object.mode != 'POSE':
			self.report({'ERROR'}, "Must be in Pose mode")
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

bpy.types.WindowManager.iWowTools_WeightThreshold = bpy.props.FloatProperty(
	name="iWowTools_WeightThreshold",
	description="maximum vertex weight to be cleared",
	default=0.001,
	subtype='FACTOR',
	unit='NONE',
	min=0.0,
	max=1.0,
	soft_max=1.0)
	
class DATA_PT_wowtools_vertex_props(bpy.types.Panel):
	bl_label = "WowTools"
	bl_idname = "wowtools.vertex_ops"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "data"

	def draw(self, context):

		layout = self.layout

		oTargetObject = context.active_object
		oWM = context.window_manager

		box = layout.box()
		split = box.split(percentage=0.4)
		col = split.column()
		col.label(text="Weight Threshold:")
		col = split.column()
		col.prop(oWM, "iWowTools_WeightThreshold", text="", slider=True)
		row = box.row()
		row.operator("wowtools.cleanup_weights", text="Cleanup weights")

class DATA_OT_wowtools_cleanup_weights(bpy.types.Operator):

	bl_idname = "wowtools.cleanup_weights"
	bl_label = "Wow Tools Bone Weight Cleanup"

	@classmethod
	def poll(cls, context):

		return context.active_object is not None

	def execute(self, context):

		oTargetObject = context.active_object

		usedVertexGroups = dict()
		for i, Vertex in enumerate(oTargetObject.data.vertices):
			weightsToRemove = []
			for g in Vertex.groups:
				usedVertexGroups[g.group] = 1
				if g.weight < context.window_manager.iWowTools_WeightThreshold:
					weightsToRemove.append(g.group)
					
			for group in weightsToRemove:
				oTargetObject.vertex_groups[group].remove([i])
				
		groupsToRemove = []
		for i, VertexGroup in enumerate(oTargetObject.vertex_groups):
			if VertexGroup.index not in usedVertexGroups:
				groupsToRemove.append(VertexGroup)


		for group in groupsToRemove:
			oTargetObject.vertex_groups.remove(group)


		self.report({'INFO'}, "Vertex weights cleaned up")
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