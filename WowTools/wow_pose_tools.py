#******************************
#---===Import declarations===
#******************************
import bpy
import re

class OBJECT_OP_Create_Modifiers(bpy.types.Operator):
	bl_idname = 'scene.wow_create_modifiers'
	bl_label = 'Create armature modifiers'
	bl_description = 'Create armature modifiers on all meshes, which are children to selected armature.'

	@classmethod
	def poll(cls, context):
		return context.active_object is not None and context.active_object.type == 'ARMATURE'

	def execute(self, context):
		armature = context.active_object

		for ob in bpy.context.scene.objects:
			if ob.type != 'MESH' or ob.parent != armature:
				continue

			found=False
			#chech mesh already has armature modifier
			for mod in ob.modifiers:
				if mod.type == 'ARMATURE' and mod.object == armature:
					found=True
					break
			if found == False:
				mod = ob.modifiers.new('Armature', 'ARMATURE')
				mod.object = armature
		return {'FINISHED'}

class OBJECT_OP_Apply_Modifiers(bpy.types.Operator):
	bl_idname = 'scene.wow_apply_modifiers'
	bl_label = 'Apply armature modifiers'
	bl_description = 'Apply armature modifiers to all meshes, which are children to selected armature.'

	@classmethod
	def poll(cls, context):
		return context.active_object is not None and context.active_object.type == 'ARMATURE'

	def execute(self, context):
		if bpy.context.active_object is None or bpy.context.active_object.type != 'ARMATURE':
			self.report({'ERROR'}, "Armature must be selected")
			return {'FINISHED'}

		armature = bpy.context.active_object;
		#bpy.ops.object.select_all(action = 'DESELECT')
		for ob in bpy.context.scene.objects:
			if ob.type == 'MESH':
				bpy.context.scene.objects.active = ob
				for mod in ob.modifiers:
					if mod.type == 'ARMATURE' and mod.object == armature:
						bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)
		return {'FINISHED'}

class OBJECT_OP_Apply_Pose(bpy.types.Operator):
	bl_idname = 'scene.wow_apply_pose'
	bl_label = 'Apply armature pose'
	bl_description = 'Apply currently selected armature pose as rest pose. Original Blender function is bugged - it does not respect attachments.'

	@classmethod
	def poll(cls, context):
		return context.active_object is not None and context.active_object.type == 'ARMATURE'

	def execute(self, context):
		if bpy.context.active_object.mode != 'POSE':
			bpy.ops.object.mode_set(mode = 'POSE') 

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
	bl_label = "Weights cleanup"
	bl_idname = "wowtools.vertex_ops"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "data"

	@classmethod
	def poll(cls, context):
		return context.active_object is not None and context.active_object.type == 'MESH'

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
	bl_description = "Removes weights from vertices that are below threshold and remove unused vertex groups"

	@classmethod
	def poll(cls, context):
		return context.active_object is not None and context.active_object.type == 'MESH'

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
#---===GUI===
#******************************
class OBJECT_PT_WoW_Pose(bpy.types.Panel):
	bl_label = 'WoW Pose Tools'
	bl_idname = 'WoWPoseTools'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = 'WoW'

	def draw(self, context):
		self.layout.operator('scene.wow_create_modifiers', text='Create armature modifiers');
		self.layout.operator('scene.wow_apply_modifiers', text='Apply armature modifiers');
		self.layout.operator('scene.wow_apply_pose', text='Apply armature pose');
