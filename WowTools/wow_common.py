import os
import struct

import bpy
import re
from enum import IntEnum

def MakeFourCC(Value):
	return struct.unpack('<I', Value)[0]

def MakeVersion(Major, Minor):
	return Major << 16 | Minor

class EEndianness:
	Native = '@'
	Little = '<'
	Big = '>'

class CDataBinary:
	def __init__(self, File, Endianness):
		self.File = File
		self.Endianness = Endianness
	def ReadUInt8(self):
		return struct.unpack(self.Endianness + 'B', self.File.read(1))[0]
	def ReadSInt8(self):
		return struct.unpack(self.Endianness + 'b', self.File.read(1))[0]
	def ReadUInt16(self):
		return struct.unpack(self.Endianness + 'H', self.File.read(2))[0]
	def ReadSInt16(self):
		return struct.unpack(self.Endianness + 'h', self.File.read(2))[0]
	def ReadUInt32(self):
		return struct.unpack(self.Endianness + 'I', self.File.read(4))[0]
	def ReadSInt32(self):
		return struct.unpack(self.Endianness + 'i', self.File.read(4))[0]
	def ReadFloat32(self):
		return struct.unpack(self.Endianness + 'f', self.File.read(4))[0]
	def ReadNullterminatedString(self):
		buf = ''
		while True:
			b = self.ReadUInt8()
			if b is None or b == 0:
				return buf
			else:
				buf = buf + chr(b)
	def WriteUInt8(self, Value):
		self.File.write(struct.pack(self.Endianness + 'B', Value))
	def WriteSInt8(self, Value):
		self.File.write(struct.pack(self.Endianness + 'B', Value))
	def WriteUInt16(self, Value):
		self.File.write(struct.pack(self.Endianness + 'H', Value))
	def WriteSInt16(self, Value):
		self.File.write(struct.pack(self.Endianness + 'h', Value))
	def WriteUInt32(self, Value):
		self.File.write(struct.pack(self.Endianness + 'I', Value))
	def WriteSInt32(self, Value):
		self.File.write(struct.pack(self.Endianness + 'i', Value))
	def WriteFloat32(self, Value):
		self.File.write(struct.pack(self.Endianness + 'f', Value))
	def WriteNullterminatedString(self, Value):
		self.File.write(bytes(Value, 'UTF-8'))
		self.WriteUInt8(0)

class CMesh:
	class CVertex:
		def __init__(self):
			self.Position = [0.0, 0.0, 0.0]
			self.BoneWeights = [0, 0, 0, 0]
			self.BoneIndices = [0, 0, 0, 0]
			self.Normal = [0.0, 0.0, 0.0]
			self.Texture = [0.0, 0.0]
			self.Texture2 = [0.0, 0.0]
			self.Index = 0

		def Compare(self, B):
			return (self.Position == B.Position) and (self.Normal == B.Normal) and (self.Texture == B.Texture) and (self.Texture2 == B.Texture2)

	class CTriangle:
		def __init__(self):
			self.A = 0
			self.B = 0
			self.C = 0
	
	def __init__(self):
		self.ID = 0
		self.Description = ''
		self.VertexList = []
		self.TriangleList = []
		self.VertexDict = {}
		self.MaterialOverride = None
		self.ShaderId = -1
		self.BlendMode = -1
		self.RenderFlags = 0
		self.TextureTypes = [ -1, -1, -1, -1 ]
		self.TextureNames = ["", "", "" ,"" ]
		self.OriginalMeshIndex = -1

		#self.HasCustomTexture = False
		#self.GlossTexture = ""
		#self.HasGloss = False
		#self.TextureStyle = 0
		#self.CustomTexture = ""

	def AddTriangle(self, VertexA, VertexB, VertexC):
		Triangle = CMesh.CTriangle()
		Triangle.A = self.AddVertex(VertexA)
		Triangle.B = self.AddVertex(VertexB)
		Triangle.C = self.AddVertex(VertexC)
		self.TriangleList.append(Triangle)
	
	def AddVertex(self, Vertex):
		# find existing vertex
		if not Vertex.Position[0] in self.VertexDict:
			self.VertexDict[Vertex.Position[0]] = []
		Bucket = self.VertexDict[Vertex.Position[0]]
		for i in range(0, len(Bucket)):
			if Bucket[i].Compare(Vertex):
				return Bucket[i].Index
		# add new vertex
		Vertex.Index = len(self.VertexList)
		self.VertexList.append(Vertex)
		self.VertexDict[Vertex.Position[0]].append(Vertex)
		return Vertex.Index

class CBone:
	def __init__(self):
		self.Index = 0
		self.Parent = -1
		self.Position = [0.0, 0.0, 0.0]
		self.HasData = 0
		self.Flags = 0
		self.SubmeshId = 0
		self.Unknown = [ 0, 0 ]

class CAttachment:
	def __init__(self):
		self.ID = 0
		self.Parent = -1
		self.Position = [0.0, 0.0, 0.0]
		self.Scale = 1.0

class CCamera:
	def __init__(self):
		self.ID = 0
		self.HasData = False
		self.Type = 0
		self.FieldOfView = 0.7
		self.ClipFar = 100.0
		self.ClipNear = 0.5
		self.Position = [0.0, 0.0, 0.0]
		self.Target = [0.0, 0.0, 0.0]

def RenderFlagsToSet(Flags):
	s = set()

	renderFlagItems = bpy.types.Mesh.bl_rna.properties['wow_props'].fixed_type.RenderFlags[1]['items']
	for renderFlagTuple in renderFlagItems:
		if (Flags & renderFlagTuple[4]) != 0:
			s.add(renderFlagTuple[0])

	return s

def RenderFlagsFromSet(Set):
	value = 0

	renderFlagItems = bpy.types.Mesh.bl_rna.properties['wow_props'].fixed_type.RenderFlags[1]['items']
	for renderFlagTuple in renderFlagItems:
		if renderFlagTuple[0] in Set:
			value |= renderFlagTuple[4]

	return value

opCountByShader = {
	32768: 2,
	32769: 2,
	32770: 2,
	32771: 3,
	32772: 2,
	32773: 2,
	32774: 2,
	32775: 2,
	32776: 2,
	32777: 3,
	32778: 2,
	32779: 2,
	32780: 2,
	32781: 2,
	32782: 2,
	32783: 2,
	32784: 2,
	32785: 3,
	32786: 1,
	32787: 1,
	32788: 3,
	32789: 2,
	32790: 2,
	32791: 2,
	32792: 3,
	32793: 1,
	32794: 2,
	32795: 3,
	32796: 2,
	32797: 2,
	32798: 3,
	32799: 3,
	32800: 1,
	32801: 2
}

class WoWMeshType(IntEnum):
	Empty = 0
	Facial = 1
	Hair = 2
	Armor = 4
	Cloak = 8
	Body = 16
	Head = 32
	Accessory = 64

def MeshIdToType(MeshId):
	match = re.search(r'^Mesh(\d+)', MeshId)
	if match:
		MeshId = match.group(1)

	MeshId = int(MeshId)

	GeosetHigh = int(MeshId / 100)
	GeosetLow = MeshId % 100

	if GeosetHigh == 0:
		if GeosetLow > 0:
			return WoWMeshType.Hair
		return WoWMeshType.Body

	if GeosetHigh in [1, 2, 3, 16, 34]:
		return WoWMeshType.Facial

	if GeosetHigh in [4, 5, 8, 9, 10, 11, 13, 18, 20, 22, 23]:
		if GeosetLow == 1:
			return WoWMeshType.Body
		return WoWMeshType.Armor

	if GeosetHigh in [6, 7, 19, 38, 40, 41]:
		return WoWMeshType.Body

	if GeosetHigh in [12, 14, 15]:
		return WoWMeshType.Cloak

	if GeosetHigh in [17, 33]:
		return WoWMeshType.Head | WoWMeshType.Body

	if GeosetHigh in [24, 25, 29, 30, 31, 35, 36, 37, 39]:
		return WoWMeshType.Accessory

	if GeosetHigh == 32:
		return WoWMeshType.Body

	return WoWMeshType.Empty

def IsMeshType(MeshId, Type):
	return int(MeshIdToType(MeshId)) & int(Type)
