import bpy
import os
import struct

from .wow_common import *

# sorts a list of vertex influences from heaviest to lightest
def VertexInfluenceSortKey(A):
	return -A[1]

def DoExport(FileName):
	MeshList = []
	BoneList = []
	AttachmentList = []
	CameraList = []
	
	# find root object
	for ob in bpy.context.scene.objects:
		if ob.type == 'ARMATURE' and ob.name == 'Armature':
			BArmature = ob
	
	# gather Blender objects
	BMeshList = []
	BEmptyList = []
	BCameraList = []
	for BObject in BArmature.children:
		if BObject.type == 'MESH' and BObject.name.startswith('Mesh'):
			BMeshList.append(BObject)
		elif BObject.type == 'EMPTY' and BObject.name.startswith('Attach'):
			BEmptyList.append(BObject)
		elif BObject.type == 'CAMERA' and BObject.name.startswith('Camera'):
			BCameraList.append(BObject)
	
	MeshIndexesByName = dict()
	# first fill indexes meshes
	for i, BMesh in enumerate(BMeshList):
		MeshIndexesByName[BMesh.name] = i

	# extract meshes
	for BMesh in BMeshList:
		Mesh = CMesh()
		name = BMesh.name.split('.')[0]
		parts = name.split('_')
		id = int(parts[0][4:])

		props = BMesh.data.wow_props

		if len(props.MaterialOverride) > 0:
			if props.MaterialOverride not in MeshIndexesByName:
				raise Exception('Mesh \'' + BMesh.name + '\' has MaterialOverride property \'' + props.MaterialOverride +  '\' that doesn\'t correspond to any mesh')
			Mesh.MaterialOverride = MeshIndexesByName[props.MaterialOverride]
		else:
			Mesh.MaterialOverride = -1

		Mesh.TextureTypes[0] = int(props.TextureType0)
		Mesh.TextureNames[0] = props.TextureName0
		Mesh.BlendMode = int(props.BlendMode)

		if props.MenuType == '0':
			Mesh.RenderFlags = RenderFlagsFromSet({ '3' }) # TwoSided

			if len(props.TextureName1) > 0:
				Mesh.ShaderId = 32769
				Mesh.TextureTypes[1] = 0 # Hardcoded
				Mesh.TextureNames[1] = props.TextureName1
		elif props.MenuType == '1':
			Mesh.ShaderId = int(props.ShaderId)
			Mesh.RenderFlags = RenderFlagsFromSet(props.RenderFlags)

			Mesh.TextureTypes[1] = int(props.TextureType1)
			Mesh.TextureTypes[2] = int(props.TextureType2)
			Mesh.TextureTypes[3] = int(props.TextureType3)

			Mesh.TextureNames[1] = props.TextureName1
			Mesh.TextureNames[2] = props.TextureName2
			Mesh.TextureNames[3] = props.TextureName3

		Mesh.OriginalMeshIndex = props.OriginalMeshIndex

		Mesh.Description = props.Description

		Mesh.ID = id

		for iFace, BFace in enumerate(BMesh.data.polygons):
			FaceUVs = []
			FaceUVs2 = []

			for i in BFace.loop_indices: # <-- python Range object with the proper indices already set.
				l = BMesh.data.loops[i] # The loop entry this polygon point refers to.

				tFound = False
				t2Found = False
				for j, ul in enumerate(BMesh.data.uv_layers):
					if ul.name == 'Texture' or ul.name == 'UVMap':
						tFound = True
						FaceUVs.append([ul.data[l.index].uv[0], ul.data[l.index].uv[1]])
					elif ul.name == 'Texture2':
						t2Found = True
						FaceUVs2.append([ul.data[l.index].uv[0], ul.data[l.index].uv[1]])

				if not tFound:
					FaceUVs.append([0, 0])
				if not t2Found:
					FaceUVs2.append([0, 0])

			# build vertex list for this face
			FaceVertexList = []
			for iFaceVertex, VertexIndex in enumerate(BFace.vertices):
				BVertex = BMesh.data.vertices[VertexIndex]
				Vertex = CMesh.CVertex()
				# position
				Vertex.Position[0] = BVertex.co.y
				Vertex.Position[1] = -BVertex.co.x
				Vertex.Position[2] = BVertex.co.z
				# normal
				if BFace.use_smooth:
					Vertex.Normal[0] = BVertex.normal.y
					Vertex.Normal[1] = -BVertex.normal.x
					Vertex.Normal[2] = BVertex.normal.z
				else:
					Vertex.Normal[0] = BFace.normal.y
					Vertex.Normal[1] = -BFace.normal.x
					Vertex.Normal[2] = BFace.normal.z
				# texture
				Vertex.Texture[0] = FaceUVs[iFaceVertex][0]
				Vertex.Texture[1] = 1.0-FaceUVs[iFaceVertex][1]

				Vertex.Texture2[0] = FaceUVs2[iFaceVertex][0]
				Vertex.Texture2[1] = 1.0-FaceUVs2[iFaceVertex][1]
				#
				VertexInfluences = []
				for BVertexGroupElement in BVertex.groups:
					if BVertexGroupElement.weight > 0.0:
						VertexInfluences.append([BMesh.vertex_groups[BVertexGroupElement.group].name, BVertexGroupElement.weight])
				VertexInfluences.sort(key = VertexInfluenceSortKey)
				VertexInfluences = VertexInfluences[:4]
				WeightSum = 0.0
				for VertexInfluence in VertexInfluences:
					WeightSum += VertexInfluence[1]
				if WeightSum > 0.0:
					for iBone, VertexInfluence in enumerate(VertexInfluences):
						Vertex.BoneWeights[iBone] = int(VertexInfluence[1] / WeightSum * 255.0)
						Vertex.BoneIndices[iBone] = int(VertexInfluence[0][4:].split('.')[0])
				WeightSum = Vertex.BoneWeights[0] + Vertex.BoneWeights[1] + Vertex.BoneWeights[2] + Vertex.BoneWeights[3]
				if WeightSum > 0:
					while WeightSum < 255:
						for iBone in range(0, 4):
							if Vertex.BoneWeights[iBone] > 0 and Vertex.BoneWeights[iBone] < 255:
								Vertex.BoneWeights[iBone] += 1
								WeightSum += 1
								break
				FaceVertexList.append(Vertex)
			# add triangle to mesh
			if len(FaceVertexList) == 3:
				Mesh.AddTriangle(FaceVertexList[0], FaceVertexList[1], FaceVertexList[2])
			elif len(FaceVertexList) == 4:
				Mesh.AddTriangle(FaceVertexList[0], FaceVertexList[1], FaceVertexList[2])
				Mesh.AddTriangle(FaceVertexList[2], FaceVertexList[3], FaceVertexList[0])
		MeshList.append(Mesh)
	
	# extract bones
	BoneMap = {}
	bpy.ops.object.select_all(action = 'DESELECT')
	#bpy.ops.object.select_name(name = BArmature.name, extend = False)
	BArmature.select_set(True)
	bpy.context.view_layer.objects.active = BArmature
	isHidden = BArmature.hide_get()
	BArmature.hide_set(False)
	bpy.ops.object.mode_set(mode = 'EDIT', toggle = False)
	
	for BBone in BArmature.data.edit_bones:
		Bone = CBone()
		if not BBone.name.startswith('Bone'):
			raise Exception('Bone \'' + BBone.name + '\' is not named properly. Proper convention is \'Bone[index]\'.')
		if BBone.parent != None:
			if not BBone.parent.name.startswith('Bone'):
				raise Exception('Bone \'' + BBone.parent.name + '\' is not named properly. Proper convention is \'Bone[index]\'.')
		Bone.Index = int(BBone.name[4:].split('.')[0])
		if BBone.parent != None:
			Bone.Parent = int(BBone.parent.name[4:].split('.')[0])
		Bone.Position[0] = BBone.head.y
		Bone.Position[1] = -BBone.head.x
		Bone.Position[2] = BBone.head.z

		props = BBone.wow_props
		Bone.HasData = props.HasData
		Bone.Flags = props.Flags
		Bone.SubmeshId = props.SubmeshId
		Bone.Unknown[0] = props.Unknown0
		Bone.Unknown[1] = props.Unknown1

		BoneList.append(Bone)
		BoneMap[BBone.name] = BBone
	bpy.ops.object.mode_set(mode = 'OBJECT', toggle = False)
	
	# extract attachments
	for BEmpty in BEmptyList:
		Attachment = CAttachment()
		Attachment.ID = int(BEmpty.name[6:].split('.')[0])
		Attachment.Parent = int(BEmpty.parent_bone[4:].split('.')[0])
		BBone = BArmature.data.bones[BEmpty.parent_bone]
		Attachment.Position[0] = BEmpty.location.y + BBone.head_local[1] + 0.1
		Attachment.Position[1] = -BEmpty.location.x - BBone.head_local[0]
		Attachment.Position[2] = BEmpty.location.z + BBone.head_local[2]
		Attachment.Scale = 1.0
		AttachmentList.append(Attachment)
	
	# extract cameras
	for BCamera in BCameraList:
		Camera = CCamera()

		props = BCamera.data.wow_props
		Camera.HasData = props.HasData
		Camera.Type = int(props.Type)
		Camera.Position[0] = BCamera.location.y
		Camera.Position[1] = -BCamera.location.x
		Camera.Position[2] = BCamera.location.z
		Camera.Target[0] = props.TargetY
		Camera.Target[1] = -props.TargetX
		Camera.Target[2] = props.TargetZ

		Camera.FieldOfView = BCamera.data.angle
		Camera.ClipNear = BCamera.data.clip_start
		Camera.ClipFar = BCamera.data.clip_end

		CameraList.append(Camera)
	
	BArmature.hide_set(isHidden)
	
	# open stream
	File = open(FileName, 'wb')
	DataBinary = CDataBinary(File, EEndianness.Little)
	
	# save header
	DataBinary.WriteUInt32(MakeFourCC(b'M2I0'))
	DataBinary.WriteUInt16(8)
	DataBinary.WriteUInt16(1)
	
	# save mesh list
	DataBinary.WriteUInt32(len(MeshList))
	for Mesh in MeshList:
		DataBinary.WriteUInt16(Mesh.ID)
		DataBinary.WriteNullterminatedString(Mesh.Description)
		DataBinary.WriteSInt16(Mesh.MaterialOverride)

		DataBinary.WriteSInt32(Mesh.ShaderId)
		DataBinary.WriteSInt16(Mesh.BlendMode)
		DataBinary.WriteUInt16(Mesh.RenderFlags)
		for i in range(0, 4):
			DataBinary.WriteSInt16(Mesh.TextureTypes[i])
			DataBinary.WriteNullterminatedString(Mesh.TextureNames[i])

		DataBinary.WriteSInt32(Mesh.OriginalMeshIndex)

		DataBinary.WriteUInt16(0) # Level.
		DataBinary.WriteUInt32(len(Mesh.VertexList))
		
		for Vertex in Mesh.VertexList:
			DataBinary.WriteFloat32(Vertex.Position[0])
			DataBinary.WriteFloat32(Vertex.Position[1])
			DataBinary.WriteFloat32(Vertex.Position[2])
			DataBinary.WriteUInt8(Vertex.BoneWeights[0])
			DataBinary.WriteUInt8(Vertex.BoneWeights[1])
			DataBinary.WriteUInt8(Vertex.BoneWeights[2])
			DataBinary.WriteUInt8(Vertex.BoneWeights[3])
			DataBinary.WriteUInt8(Vertex.BoneIndices[0])
			DataBinary.WriteUInt8(Vertex.BoneIndices[1])
			DataBinary.WriteUInt8(Vertex.BoneIndices[2])
			DataBinary.WriteUInt8(Vertex.BoneIndices[3])
			DataBinary.WriteFloat32(Vertex.Normal[0])
			DataBinary.WriteFloat32(Vertex.Normal[1])
			DataBinary.WriteFloat32(Vertex.Normal[2])
			DataBinary.WriteFloat32(Vertex.Texture[0])
			DataBinary.WriteFloat32(Vertex.Texture[1])
			DataBinary.WriteFloat32(Vertex.Texture2[0])
			DataBinary.WriteFloat32(Vertex.Texture2[1])

		DataBinary.WriteUInt32(len(Mesh.TriangleList))

		for Triangle in Mesh.TriangleList:
			DataBinary.WriteUInt16(Triangle.A)
			DataBinary.WriteUInt16(Triangle.B)
			DataBinary.WriteUInt16(Triangle.C)

	# save bone list
	DataBinary.WriteUInt32(len(BoneList))
	for Bone in BoneList:
		DataBinary.WriteUInt16(Bone.Index)
		DataBinary.WriteSInt16(Bone.Parent)
		DataBinary.WriteFloat32(Bone.Position[0])
		DataBinary.WriteFloat32(Bone.Position[1])
		DataBinary.WriteFloat32(Bone.Position[2])
		DataBinary.WriteUInt8(Bone.HasData)
		DataBinary.WriteUInt32(Bone.Flags)
		DataBinary.WriteUInt16(Bone.SubmeshId)
		DataBinary.WriteUInt16(Bone.Unknown[0])
		DataBinary.WriteUInt16(Bone.Unknown[1])

	# save attachment list
	DataBinary.WriteUInt32(len(AttachmentList))
	for Attachment in AttachmentList:
		DataBinary.WriteUInt32(Attachment.ID)
		DataBinary.WriteSInt16(Attachment.Parent)
		DataBinary.WriteFloat32(Attachment.Position[0])
		DataBinary.WriteFloat32(Attachment.Position[1])
		DataBinary.WriteFloat32(Attachment.Position[2])
		DataBinary.WriteFloat32(Attachment.Scale)
		
	# save camera list
	DataBinary.WriteUInt32(len(CameraList))
	for Camera in CameraList:
		DataBinary.WriteUInt8(Camera.HasData)
		DataBinary.WriteSInt32(Camera.Type)
		DataBinary.WriteFloat32(Camera.FieldOfView)
		DataBinary.WriteFloat32(Camera.ClipFar)
		DataBinary.WriteFloat32(Camera.ClipNear)
		DataBinary.WriteFloat32(Camera.Position[0])
		DataBinary.WriteFloat32(Camera.Position[1])
		DataBinary.WriteFloat32(Camera.Position[2])
		DataBinary.WriteFloat32(Camera.Target[0])
		DataBinary.WriteFloat32(Camera.Target[1])
		DataBinary.WriteFloat32(Camera.Target[2])
	
	# close stream
	File.close()
	
	print('M2I exported successfully: ' + FileName)

class M2IExporter(bpy.types.Operator):
	"""Export a M2 Intermediate file"""
	bl_idname = "export.m2i"
	bl_label = "Export M2I"

	filepath: bpy.props.StringProperty(name = 'File Path', description = 'Filepath used for exporting the M2I file', maxlen = 1024, default = '')
	check_existing: bpy.props.BoolProperty(name = 'Check Existing', description = 'Check and warn on overwriting existing files', default = True, options = {'HIDDEN'})
	filter_glob: bpy.props.StringProperty(default = '*.m2i', options = {'HIDDEN'})
	
	def execute(self, context):
		FilePath = self.properties.filepath
		if not FilePath.lower().endswith('.m2i'):
			FilePath += '.m2i'
		DoExport(FilePath)
		return {'FINISHED'}
	
	def invoke(self, context, event):
		WindowManager = context.window_manager
		WindowManager.fileselect_add(self)
		return {'RUNNING_MODAL'}
