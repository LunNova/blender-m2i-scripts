import bpy
import os
import struct

from .wow_common import *

def DoImport(FileName):
	MeshList = []
	BoneList = []
	AttachmentList = []
	CameraList = []
	
	# open stream
	File = open(FileName, 'rb')
	DataBinary = CDataBinary(File, EEndianness.Little)
	
	# load header
	SignatureIn = DataBinary.ReadUInt32()
	if SignatureIn != MakeFourCC(b'M2I0'):
		File.close()
		return
	VersionMajor = DataBinary.ReadUInt16()
	VersionMinor = DataBinary.ReadUInt16()
	Version = MakeVersion(VersionMajor, VersionMinor)
	
	if not (Version >= MakeVersion(4, 5) and Version <= MakeVersion(4, 9)) and not(Version >= MakeVersion(8, 0) and Version <= MakeVersion(8, 1)):
		File.close()
		raise Exception('Unsupported M2I version ' + str("%d.%d") % (VersionMajor , VersionMinor))

	print("M2I Version: " + str("%d.%d") % (VersionMajor , VersionMinor))

	# load mesh list
	MeshCount = DataBinary.ReadUInt32()
	for i in range(0, MeshCount):
		Mesh = CMesh()
		Mesh.ID = DataBinary.ReadUInt16()
		if Version >= MakeVersion(4, 6):
			Mesh.Description = DataBinary.ReadNullterminatedString()
		if Version >= MakeVersion(4, 7):
			Mesh.MaterialOverride = DataBinary.ReadSInt16()

			if Version >= MakeVersion(8, 1):
				print("Entered")
				Mesh.ShaderId = DataBinary.ReadSInt32()
				Mesh.BlendMode = DataBinary.ReadSInt16()
				Mesh.RenderFlags = DataBinary.ReadUInt16()
				for j in range(0, 4):
					Mesh.TextureTypes[j] = DataBinary.ReadSInt16()
					Mesh.TextureNames[j] = DataBinary.ReadNullterminatedString()
			else:
				print("Entered old")
				if Version >= MakeVersion(4, 9):
					DataBinary.ReadUInt8() != 0 # HasCustomTexture
				Mesh.TextureNames[0] = DataBinary.ReadNullterminatedString()
				if len(Mesh.TextureNames[0]) > 0:
					Mesh.TextureTypes[0] = 0 # final hardcoded
					Mesh.RenderFlags = 0x4 # TwoSided
				if Version >= MakeVersion(4, 9):
					Mesh.BlendMode = DataBinary.ReadUInt16()
					DataBinary.ReadUInt8() != 0 # has gloss
				else:
					Mesh.BlendMode = 2 # decal
				Mesh.TextureNames[1] = DataBinary.ReadNullterminatedString()
				if len(Mesh.TextureNames[1]) > 0:
					Mesh.ShaderId = 32769 # gloss shader id
					Mesh.TextureTypes[1] = 0 # final hardcoded

		if Version >= MakeVersion(8, 0):
			Mesh.OriginalMeshIndex = DataBinary.ReadSInt32()

		Mesh.Level = DataBinary.ReadUInt16()
		VertexCount = DataBinary.ReadUInt32()
		
		for j in range(0, VertexCount):
			Vertex = CMesh.CVertex()
			Vertex.Position[0] = DataBinary.ReadFloat32()
			Vertex.Position[1] = DataBinary.ReadFloat32()
			Vertex.Position[2] = DataBinary.ReadFloat32()
			Vertex.BoneWeights[0] = DataBinary.ReadUInt8()
			Vertex.BoneWeights[1] = DataBinary.ReadUInt8()
			Vertex.BoneWeights[2] = DataBinary.ReadUInt8()
			Vertex.BoneWeights[3] = DataBinary.ReadUInt8()
			Vertex.BoneIndices[0] = DataBinary.ReadUInt8()
			Vertex.BoneIndices[1] = DataBinary.ReadUInt8()
			Vertex.BoneIndices[2] = DataBinary.ReadUInt8()
			Vertex.BoneIndices[3] = DataBinary.ReadUInt8()
			Vertex.Normal[0] = DataBinary.ReadFloat32()
			Vertex.Normal[1] = DataBinary.ReadFloat32()
			Vertex.Normal[2] = DataBinary.ReadFloat32()
			Vertex.Texture[0] = DataBinary.ReadFloat32()
			Vertex.Texture[1] = DataBinary.ReadFloat32()
			if Version >= MakeVersion(8, 0):
				Vertex.Texture2[0] = DataBinary.ReadFloat32()
				Vertex.Texture2[1] = DataBinary.ReadFloat32()

			Mesh.VertexList.append(Vertex)

		TriangleCount = DataBinary.ReadUInt32()

		for j in range(0, TriangleCount):
			Triangle = CMesh.CTriangle()
			Triangle.A = DataBinary.ReadUInt16()
			Triangle.B = DataBinary.ReadUInt16()
			Triangle.C = DataBinary.ReadUInt16()
			Mesh.TriangleList.append(Triangle)
			
		MeshList.append(Mesh)
	
	# load bone list
	BoneCount = DataBinary.ReadUInt32()
	for i in range(0, BoneCount):
		Bone = CBone()
		Bone.Index = DataBinary.ReadUInt16()
		Bone.Parent = DataBinary.ReadSInt16()
		Bone.Position[0] = DataBinary.ReadFloat32()
		Bone.Position[1] = DataBinary.ReadFloat32()
		Bone.Position[2] = DataBinary.ReadFloat32()

		if Version >= MakeVersion(4, 8):
			Bone.HasData = DataBinary.ReadUInt8() != 0
			Bone.Flags = DataBinary.ReadUInt32()
			Bone.SubmeshId = DataBinary.ReadUInt16()
			Bone.Unknown[0] = DataBinary.ReadUInt16()
			Bone.Unknown[1] = DataBinary.ReadUInt16()

		BoneList.append(Bone)
	
	# load attachment list
	AttachmentCount = DataBinary.ReadUInt32()
	for i in range(0, AttachmentCount):
		Attachment = CAttachment()
		Attachment.ID = DataBinary.ReadUInt32()
		Attachment.Parent = DataBinary.ReadSInt16()
		Attachment.Position[0] = DataBinary.ReadFloat32()
		Attachment.Position[1] = DataBinary.ReadFloat32()
		Attachment.Position[2] = DataBinary.ReadFloat32()
		Attachment.Scale = DataBinary.ReadFloat32()
		AttachmentList.append(Attachment)
	
	# load camera list
	CameraCount = DataBinary.ReadUInt32()
	for i in range(0, CameraCount):
		Camera = CCamera()
		Camera.ID = i
		if Version >= MakeVersion(4, 9):
			Camera.HasData = DataBinary.ReadUInt8() != 0
		Camera.Type = DataBinary.ReadSInt32()
		Camera.FieldOfView = DataBinary.ReadFloat32()
		Camera.ClipFar = DataBinary.ReadFloat32()
		Camera.ClipNear = DataBinary.ReadFloat32()
		Camera.Position[0] = DataBinary.ReadFloat32()
		Camera.Position[1] = DataBinary.ReadFloat32()
		Camera.Position[2] = DataBinary.ReadFloat32()
		Camera.Target[0] = DataBinary.ReadFloat32()
		Camera.Target[1] = DataBinary.ReadFloat32()
		Camera.Target[2] = DataBinary.ReadFloat32()
		CameraList.append(Camera)
	
	# close stream
	File.close()
	
	#deselect all objects.
	bpy.ops.object.select_all(action = 'DESELECT')
	
	# instantiate armature
	bpy.ops.object.add(type = 'ARMATURE', enter_editmode = True, location = (0.0, 0.0, 0.0))
	BArmature = bpy.context.object
	for Bone in BoneList: # add bones to armature.
		BEditBone = BArmature.data.edit_bones.new('Bone' + str('%03d' % Bone.Index))
		BEditBone.head.x = -Bone.Position[1]
		BEditBone.head.y = Bone.Position[0]
		BEditBone.head.z = Bone.Position[2]
		BEditBone.tail.x = BEditBone.head.x
		BEditBone.tail.y = BEditBone.head.y + 0.1
		BEditBone.tail.z = BEditBone.head.z
		BEditBone.wow_props.HasData = Bone.HasData
		BEditBone.wow_props.Flags = Bone.Flags
		BEditBone.wow_props.SubmeshId = Bone.SubmeshId
		BEditBone.wow_props.Unknown0 = Bone.Unknown[0]
		BEditBone.wow_props.Unknown1 = Bone.Unknown[1]

	for Bone in BoneList: # link children to parents
		if Bone.Parent >= 0:
			BEditBone = BArmature.data.edit_bones['Bone' + str('%03d' % Bone.Index)]
			BEditBone.parent = BArmature.data.edit_bones['Bone' + str('%03d' % Bone.Parent)]
	bpy.context.scene.update() # update scene.
	bpy.ops.object.mode_set(mode = 'OBJECT') # return to object mode.
	
	# instantiate attachments
	for Attachment in AttachmentList:
		bpy.ops.object.add(type = 'EMPTY', location = (0.0, 0.0, 0.0))
		BAttachment = bpy.context.object
		BAttachment.name = 'Attach' + str('%02d' % Attachment.ID)
		BBone = BArmature.data.bones['Bone' + str('%03d' % Attachment.Parent)]
		BAttachment.location.x = -Attachment.Position[1] - BBone.head_local[0]
		BAttachment.location.y = Attachment.Position[0] - BBone.head_local[1] - 0.1
		BAttachment.location.z = Attachment.Position[2] - BBone.head_local[2]
		if Attachment.Parent >= 0:
			BAttachment.parent = BArmature
			BAttachment.parent_bone = 'Bone' + str('%03d' % Attachment.Parent)
			BAttachment.parent_type = 'BONE'
			#BAttachment.location.x -= -Attachment.Position[1]
			#BAttachment.location.y -= Attachment.Position[0]
			#BAttachment.location.z -= Attachment.Position[2]
			BAttachment.empty_draw_size = 0.1

	pi = 3.14159265			
	# instantiate cameras
	for Camera in CameraList:
		bpy.ops.object.add(type = 'CAMERA', location = (0.0, 0.0, 0.0))
		BCamera = bpy.context.object
		BCamera.name = 'Camera' + str('%02d' % Camera.ID)
		BCamera.location.x = -Camera.Position[1]
		BCamera.location.y = Camera.Position[0]
		BCamera.location.z = Camera.Position[2]
		
		BCamera.rotation_mode = 'XYZ'
		BCamera.rotation_euler[0] = pi / 2
		BCamera.rotation_euler[1] = 0
		BCamera.rotation_euler[2] = pi
		
		BCamera.data.angle = Camera.FieldOfView
		BCamera.data.lens_unit = 'FOV'
		
		BCamera.data.clip_start = Camera.ClipNear
		BCamera.data.clip_end = Camera.ClipFar
		
		BCamera.data.wow_props.HasData = Camera.HasData
		if Camera.Type == -1:
			BCamera.data.wow_props.Type = '-1'
		elif Camera.Type == 0:
			BCamera.data.wow_props.Type = '0'
		elif Camera.Type == 1:
			BCamera.data.wow_props.Type = '1'
		BCamera.data.wow_props.TargetX = -Camera.Target[1]
		BCamera.data.wow_props.TargetY = Camera.Target[0]
		BCamera.data.wow_props.TargetZ = Camera.Target[2]
		
		BCamera.parent = BArmature
	
	MeshResultNames = dict()
	# instantiate meshes
	for k, Mesh in enumerate(MeshList):
		bpy.ops.object.add(type = 'MESH', location = (0.0, 0.0, 0.0))
		BMesh = bpy.context.object
		meshName = 'Mesh' + str('%04d' % Mesh.ID)
		if Mesh.Description != '':
			meshName = meshName + '_' + Mesh.Description
		BMesh.name = meshName

		BMeshData = BMesh.data
		BMeshData.name = BMesh.name
		BMeshData.vertices.add(len(Mesh.VertexList)) # add vertices to mesh data.
		for i, Vertex in enumerate(Mesh.VertexList):
			BVertex = BMeshData.vertices[i]
			BVertex.co.x = -Vertex.Position[1]
			BVertex.co.y = Vertex.Position[0]
			BVertex.co.z = Vertex.Position[2]
			#BVertex.normal.x = -Vertex.Normal[1] # we don't need to import normals because they will be calculated automatically by Blender
			#BVertex.normal.y = Vertex.Normal[0]
			#BVertex.normal.z = Vertex.Normal[2]

		BMeshData.tessfaces.add(len(Mesh.TriangleList)) # add triangles to mesh data.

		BMeshTextureFaceLayer = BMeshData.tessface_uv_textures.new(name = 'Texture')
		BMeshTextureFaceLayer2 = BMeshData.tessface_uv_textures.new(name = 'Texture2')
		for i, Triangle in enumerate(Mesh.TriangleList):
			BFace = BMeshData.tessfaces[i]
			BFace.vertices = [Triangle.A, Triangle.B, Triangle.C]	# reverse the wind order so normals point out.

			BMeshTextureFace = BMeshTextureFaceLayer.data[i]
			BMeshTextureFace.uv1[0] = Mesh.VertexList[Triangle.A].Texture[0]
			BMeshTextureFace.uv1[1] = 1.0 - Mesh.VertexList[Triangle.A].Texture[1]
			BMeshTextureFace.uv2[0] = Mesh.VertexList[Triangle.B].Texture[0]
			BMeshTextureFace.uv2[1] = 1.0 - Mesh.VertexList[Triangle.B].Texture[1]
			BMeshTextureFace.uv3[0] = Mesh.VertexList[Triangle.C].Texture[0]
			BMeshTextureFace.uv3[1] = 1.0 - Mesh.VertexList[Triangle.C].Texture[1]

			BMeshTextureFace2 = BMeshTextureFaceLayer2.data[i]
			BMeshTextureFace2.uv1[0] = Mesh.VertexList[Triangle.A].Texture2[0]
			BMeshTextureFace2.uv1[1] = 1.0 - Mesh.VertexList[Triangle.A].Texture2[1]
			BMeshTextureFace2.uv2[0] = Mesh.VertexList[Triangle.B].Texture2[0]
			BMeshTextureFace2.uv2[1] = 1.0 - Mesh.VertexList[Triangle.B].Texture2[1]
			BMeshTextureFace2.uv3[0] = Mesh.VertexList[Triangle.C].Texture2[0]
			BMeshTextureFace2.uv3[1] = 1.0 - Mesh.VertexList[Triangle.C].Texture2[1]

			BFace.use_smooth = True

		for i, Vertex in enumerate(Mesh.VertexList):
			BVertex = BMeshData.vertices[i]
			for j in range(0, 4):
				if Vertex.BoneWeights[j] > 0:
					key = 'Bone' + str('%03d' % Vertex.BoneIndices[j])
					BVertexGroup = BMesh.vertex_groups.get(key)
					if BVertexGroup == None:
						BVertexGroup = BMesh.vertex_groups.new(key)

					BVertexGroup.add([i], float(Vertex.BoneWeights[j])/255.0, 'ADD')
		BMeshData.update()
		BArmatureModifier = BMesh.modifiers.new('Armature', 'ARMATURE')
		BArmatureModifier.object = BArmature
		BArmatureModifier.use_bone_envelopes = False
		BArmatureModifier.use_vertex_groups = True
		BMesh.parent = BArmature
		BMesh.select = False

		BMesh.data.wow_props.Description = Mesh.Description
		BMesh.data.wow_props.ShaderId = str(Mesh.ShaderId)
		BMesh.data.wow_props.RenderFlags = RenderFlagsToSet(Mesh.RenderFlags)
		BMesh.data.wow_props.BlendMode = str(Mesh.BlendMode)

		BMesh.data.wow_props.TextureType0 = str(Mesh.TextureTypes[0])
		BMesh.data.wow_props.TextureType1 = str(Mesh.TextureTypes[1])
		BMesh.data.wow_props.TextureType2 = str(Mesh.TextureTypes[2])
		BMesh.data.wow_props.TextureType3 = str(Mesh.TextureTypes[3])

		BMesh.data.wow_props.TextureName0 = Mesh.TextureNames[0]
		BMesh.data.wow_props.TextureName1 = Mesh.TextureNames[1]
		BMesh.data.wow_props.TextureName2 = Mesh.TextureNames[2]
		BMesh.data.wow_props.TextureName3 = Mesh.TextureNames[3]

		BMesh.data.wow_props.OriginalMeshIndex = Mesh.OriginalMeshIndex

		if Mesh.MaterialOverride is not None and Mesh.MaterialOverride >= 0:
			BMesh['TmpMaterialOverride'] = Mesh.MaterialOverride
		MeshResultNames[k] = BMesh.name

	# assign real mesh names to material overrides
	for ob in bpy.context.scene.objects:
		if ob.type == 'MESH' and ob.name.startswith('Mesh') and 'TmpMaterialOverride' in ob:
			ob.data.wow_props.MaterialOverride = MeshResultNames[ob['TmpMaterialOverride']]
			del ob['TmpMaterialOverride']

	BArmature.select = True
	bpy.context.scene.objects.active = BArmature
	
	print('M2I imported successfully: ' + FileName)


class M2IImporter(bpy.types.Operator):
	'''Import a M2 Intermediate file'''
	bl_idname = 'import.m2i'
	bl_label = 'Import M2I'
	
	filepath = bpy.props.StringProperty(name = 'File Path', description = 'Filepath used for importing the M2I file', maxlen = 1024, default = '')
	check_existing = bpy.props.BoolProperty(name = 'Check Existing', description = 'Check and warn on overwriting existing files', default = True, options = {'HIDDEN'})
	filter_glob = bpy.props.StringProperty(default = '*.m2i', options = {'HIDDEN'})
	#filepath = StringProperty(default = '*.c3d;*.csv', options = {'HIDDEN'})
	
	def execute(self, context):
		FilePath = self.properties.filepath
		if not FilePath.lower().endswith('.m2i'):
			FilePath += '.m2i'
		DoImport(FilePath)
		return {'FINISHED'}
	
	def invoke(self, context, event):
		WindowManager = context.window_manager
		WindowManager.fileselect_add(self)
		return {'RUNNING_MODAL'}
