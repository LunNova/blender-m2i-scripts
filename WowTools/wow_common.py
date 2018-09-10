import os
import struct

def MakeFourCC(Value):
	return struct.unpack('<I', Value)[0]

def MakeVersion(Major, Minor):
	return Major << 16 | Minor

class EEndianness:
	Native = '@'
	Little = '<'
	Big = '>'

class CDataBinary:
	def __init__(This, File, Endianness):
		This.File = File
		This.Endianness = Endianness
	def ReadUInt8(This):
		return struct.unpack(This.Endianness + 'B', This.File.read(1))[0]
	def ReadSInt8(This):
		return struct.unpack(This.Endianness + 'b', This.File.read(1))[0]
	def ReadUInt16(This):
		return struct.unpack(This.Endianness + 'H', This.File.read(2))[0]
	def ReadSInt16(This):
		return struct.unpack(This.Endianness + 'h', This.File.read(2))[0]
	def ReadUInt32(This):
		return struct.unpack(This.Endianness + 'I', This.File.read(4))[0]
	def ReadSInt32(This):
		return struct.unpack(This.Endianness + 'i', This.File.read(4))[0]
	def ReadFloat32(This):
		return struct.unpack(This.Endianness + 'f', This.File.read(4))[0]
	def ReadNullterminatedString(This):
		buf = ''
		while True:
			b = This.ReadUInt8()
			if b is None or b == 0:
				return buf
			else:
				buf = buf + chr(b)
	def WriteUInt8(This, Value):
		This.File.write(struct.pack(This.Endianness + 'B', Value))
	def WriteSInt8(This, Value):
		This.File.write(struct.pack(This.Endianness + 'B', Value))
	def WriteUInt16(This, Value):
		This.File.write(struct.pack(This.Endianness + 'H', Value))
	def WriteSInt16(This, Value):
		This.File.write(struct.pack(This.Endianness + 'h', Value))
	def WriteUInt32(This, Value):
		This.File.write(struct.pack(This.Endianness + 'I', Value))
	def WriteSInt32(This, Value):
		This.File.write(struct.pack(This.Endianness + 'i', Value))
	def WriteFloat32(This, Value):
		This.File.write(struct.pack(This.Endianness + 'f', Value))
	def WriteNullterminatedString(This, Value):
		This.File.write(bytes(Value, 'UTF-8'))
		This.WriteUInt8(0)

class CMesh:
	class CVertex:
		def __init__(This):
			This.Position = [0.0, 0.0, 0.0]
			This.BoneWeights = [0, 0, 0, 0]
			This.BoneIndices = [0, 0, 0, 0]
			This.Normal = [0.0, 0.0, 0.0]
			This.Texture = [0.0, 0.0]
			This.Texture2 = [0.0, 0.0]
			This.Index = 0
			This.MeshSrcIndex = 0

		def Compare(A, B):
			return (A.MeshSrcIndex == B.MeshSrcIndex)

	class CTriangle:
		def __init__(This):
			This.A = 0
			This.B = 0
			This.C = 0
	
	def __init__(This):
		This.ID = 0
		This.Description = ''
		This.VertexList = []
		This.TriangleList = []
		This.VertexDict = {}
		This.MaterialOverride = None
		This.HasCustomTexture = False
		This.CustomTexture = ""
		This.TextureStyle = 0
		This.HasGloss = False
		This.GlossTexture = ""
		This.OriginalMeshIndex = -1

	def AddTriangle(This, VertexA, VertexB, VertexC):
		Triangle = CMesh.CTriangle()
		Triangle.A = This.AddVertex(VertexA)
		Triangle.B = This.AddVertex(VertexB)
		Triangle.C = This.AddVertex(VertexC)
		This.TriangleList.append(Triangle)
	
	def AddVertex(This, Vertex):
		# find existing vertex
		if not Vertex.Position[0] in This.VertexDict:
			This.VertexDict[Vertex.Position[0]] = []
		Bucket = This.VertexDict[Vertex.Position[0]]
		for i in range(0, len(Bucket)):
			if Bucket[i].Compare(Vertex):
				return Bucket[i].Index
		# add new vertex
		Vertex.Index = len(This.VertexList)
		This.VertexList.append(Vertex)
		This.VertexDict[Vertex.Position[0]].append(Vertex)
		return Vertex.Index

class CBone:
	def __init__(This):
		This.Index = 0
		This.Parent = -1
		This.Position = [0.0, 0.0, 0.0]
		This.HasData = 0
		This.Flags = 0
		This.SubmeshId = 0
		This.Unknown = [ 0, 0 ]

class CAttachment:
	def __init__(This):
		This.ID = 0
		This.Parent = -1
		This.Position = [0.0, 0.0, 0.0]
		This.Scale = 1.0

class CCamera:
	def __init__(This):
		This.ID = 0
		This.HasData = False
		This.Type = 0
		This.FieldOfView = 0.7
		This.ClipFar = 100.0
		This.ClipNear = 0.5
		This.Position = [0.0, 0.0, 0.0]
		This.Target = [0.0, 0.0, 0.0]
