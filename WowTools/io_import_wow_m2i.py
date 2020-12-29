import bpy
import os
import struct

from .wow_common import *
from bpy_extras.io_utils import ImportHelper

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
				Mesh.ShaderId = DataBinary.ReadSInt32()
				Mesh.BlendMode = DataBinary.ReadSInt16()
				Mesh.RenderFlags = DataBinary.ReadUInt16()
				for j in range(0, 4):
					Mesh.TextureTypes[j] = DataBinary.ReadSInt16()
					Mesh.TextureNames[j] = DataBinary.ReadNullterminatedString()
			else:
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


	## 2.79
	# bpy.context.scene.update() # update scene.
	dg = bpy.context.evaluated_depsgraph_get()
	dg.update()
	## other
	# bpy.context.view_layer.update()

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
			BAttachment.empty_display_size = 0.1

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
	for k, Mesh in enumerate(MeshList):
		faceOffs = 0
		faces = []
		vertices = []
		texFaces = []
		texFaces2 = []

		meshName = 'Mesh' + str('%04d' % Mesh.ID)
		for i, Vertex in enumerate(Mesh.VertexList):
			vertices.append((-Vertex.Position[1], Vertex.Position[0], Vertex.Position[2]))

		for i, Triangle in enumerate(Mesh.TriangleList):
			vertexA = Mesh.VertexList[Triangle.A]
			vertexB = Mesh.VertexList[Triangle.B]
			vertexC = Mesh.VertexList[Triangle.C]

			texFaces.append([vertexA.Texture[0], 1.0 - vertexA.Texture[1]])
			texFaces.append([vertexB.Texture[0], 1.0 - vertexB.Texture[1]])
			texFaces.append([vertexC.Texture[0], 1.0 - vertexC.Texture[1]])

			texFaces2.append([vertexA.Texture2[0], 1.0 - vertexA.Texture2[1]])
			texFaces2.append([vertexB.Texture2[0], 1.0 - vertexB.Texture2[1]])
			texFaces2.append([vertexC.Texture2[0], 1.0 - vertexC.Texture2[1]])

			faces.append((faceOffs + Triangle.A, faceOffs + Triangle.B, faceOffs + Triangle.C))

		faceOffs += len(Mesh.VertexList)

		mesh = bpy.context.blend_data.meshes.new(name=meshName)
		mesh.from_pydata(vertices, [], faces)

		profile_object = bpy.data.objects.new(meshName, mesh)

		bpy.context.collection.objects.link(profile_object)

		createTextureLayers(mesh, 'Texture', texFaces)
		createTextureLayers(mesh, 'Texture2', texFaces2)

		for i, Vertex in enumerate(Mesh.VertexList):
			BVertex = profile_object.data.vertices[i]
			for j in range(0, 4):
				if Vertex.BoneWeights[j] > 0:
					key = 'Bone' + str('%03d' % Vertex.BoneIndices[j])
					BVertexGroup = profile_object.vertex_groups.get(key)
					if BVertexGroup == None:
						BVertexGroup = profile_object.vertex_groups.new(name=key)
					BVertexGroup.add([i], float(Vertex.BoneWeights[j])/255.0, 'ADD')
		mesh.update()
		
		for f in mesh.polygons:
			f.use_smooth = True

		BArmatureModifier = profile_object.modifiers.new('Armature', 'ARMATURE')
		BArmatureModifier.object = BArmature
		BArmatureModifier.use_bone_envelopes = False
		BArmatureModifier.use_vertex_groups = True
		profile_object.parent = BArmature
		profile_object.select_set(False)

		profile_object.data.wow_props.Description = Mesh.Description
		profile_object.data.wow_props.ShaderId = str(Mesh.ShaderId)
		profile_object.data.wow_props.RenderFlags = RenderFlagsToSet(Mesh.RenderFlags)
		profile_object.data.wow_props.BlendMode = str(Mesh.BlendMode)

		profile_object.data.wow_props.TextureType0 = str(Mesh.TextureTypes[0])
		profile_object.data.wow_props.TextureType1 = str(Mesh.TextureTypes[1])
		profile_object.data.wow_props.TextureType2 = str(Mesh.TextureTypes[2])
		profile_object.data.wow_props.TextureType3 = str(Mesh.TextureTypes[3])

		profile_object.data.wow_props.TextureName0 = Mesh.TextureNames[0]
		profile_object.data.wow_props.TextureName1 = Mesh.TextureNames[1]
		profile_object.data.wow_props.TextureName2 = Mesh.TextureNames[2]
		profile_object.data.wow_props.TextureName3 = Mesh.TextureNames[3]

		profile_object.data.wow_props.OriginalMeshIndex = Mesh.OriginalMeshIndex

		if Mesh.MaterialOverride is not None and Mesh.MaterialOverride >= 0:
			profile_object['TmpMaterialOverride'] = Mesh.MaterialOverride
		MeshResultNames[k] = profile_object.name

	# assign real mesh names to material overrides
	for ob in bpy.context.scene.objects:
		if ob.type == 'MESH' and ob.name.startswith('Mesh') and 'TmpMaterialOverride' in ob:
			ob.data.wow_props.MaterialOverride = MeshResultNames[ob['TmpMaterialOverride']]
			del ob['TmpMaterialOverride']

	BArmature.select_set(True)
	bpy.context.view_layer.objects.active = BArmature
	
	print('M2I imported successfully: ' + FileName)

def createTextureLayers(me, name, texFaces):
	uvtex = me.uv_layers.new(name = name)
	for n, tf in enumerate(texFaces):
		datum = uvtex.data[n]
		datum.uv = [ tf[0], tf[1] ]

class M2IImporter(bpy.types.Operator, ImportHelper):
	"""Import M2Mod itermediate file (.m2i)."""
	bl_idname = "wow_tools.import_m2i"
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
