import numpy as np

from vtk import *
from numpy import array


def Mat2PointSet(Mat):
    mat_size = Mat.shape
    points = []
    for i in range (mat_size[0]):
        for j in range (mat_size[1]):
            for k in range (mat_size[2]):
                if mat_size[0]==168:
                    p=[4.07283*i+1.36719*4, 4.07283*j+1.36719*4, 3*k]
                if mat_size[0]==512:
                    p=[1.36719*i, 1.36719*j, 3*k]
                if Mat[i,j,k]!=0:
                    points.append(p)
    return points

def PointsetToPolydata(PointSet):
    size = len(PointSet)
    points = vtk.vtkPoints()
    vertices = vtk.vtkCellArray()
    for i in range (size):
        p = PointSet[i]
        points.InsertNextPoint(p)
    
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    vertexFilter = vtkVertexGlyphFilter()
    vertexFilter.AddInputData(polydata)
    vertexFilter.Update()

    polydata2 = vtk.vtkPolyData()
    polydata2.ShallowCopy(vertexFilter.GetOutput())
    return polydata2

def PointSetToCTMat(data,CT_size):
    l=len(data)

    result =np.zeros(CT_size)
    for i in range(l):
        pos = data[i]
        posx = np.around(pos[0]/1.36719)
        posy = np.around(pos[1]/1.36719)
        posz = np.around(pos[2]/3)
        result[posx,posy,posz] = 1
    
    return result

def PointSetToPETMat(data,PET_size):
    l=len(data)

    result =np.zeros(PET_size)
    for i in range(l):
        pos = data[i]
        posx = np.around(pos[0]/4.07283)
        posy = np.around(pos[1]/4.07283)
        posz = np.around(pos[2]/3)
        result[posx,posy,posz] = 1
    
    return result
def PolydataToPointset(ploydata):
    NumberOfPoints = ploydata.GetNumberOfPoints()
    pointset = []
    
    for i in range(NumberOfPoints):
        p=[0,0,0]
        ploydata.GetPoint(i,p)
        pointset.append(p)
    return pointset
def PolydataToCellList(ploydata):
    NumberOfPoints = ploydata.GetNumberOfPoints()
    pointset = []
    
    for i in range(NumberOfPoints):
        p=[0,0,0]
        ploydata.GetPoint(i,p)
        pointset.append(p)
    return pointset

def SavePointSet2VtkImage(PointSet, fileDes):
    size = len(PointSet)
    points = vtk.vtkPoints()
    for i in range (size):
        p = PointSet[i]
        points.InsertNextPoint(p)
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)

    vertexFilter = vtkVertexGlyphFilter()
    vertexFilter.AddInputData(polydata)
    vertexFilter.Update()
#~ 
    polydata2 = vtk.vtkPolyData()
    polydata2.ShallowCopy(vertexFilter.GetOutput())
    
    writer = vtkXMLPolyDataWriter()
    writer.SetFileName(fileDes)
    writer.SetInputData(polydata2)
    writer.Write()
    return
    
def SavePointSet2PLYImage(PointSet, fileDes):
    size = len(PointSet)
    points = vtk.vtkPoints()
    vertices = vtk.vtkCellArray()
    for i in range (size):
        p = PointSet[i]
        points.InsertNextPoint(p)
    
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)

    vertexFilter = vtkVertexGlyphFilter()
    vertexFilter.AddInputData(polydata)
    vertexFilter.Update()
#~ 
    polydata2 = vtk.vtkPolyData()
    polydata2.ShallowCopy(vertexFilter.GetOutput())
    
    writer = vtkPLYWriter()
    writer.SetFileName(fileDes)
    writer.SetInputData(polydata2)
    writer.Write()
    return

def LoadPLYAsPointset(filename):
    reader = vtk.vtkPLYReader()
    reader.SetFileName(filename)
    reader.Update()
    polydata = vtkPolyData()
    polydata = reader.GetOutput()
    NumberOfPoints = polydata.GetNumberOfPoints()
    pointset = []
    
    for i in range(NumberOfPoints):
        p=[0,0,0]
        polydata.GetPoint(i,p)
        pointset.append(p)
    return pointset


    
def SavePointSet2Mesh(PointSet, fileDes,polydata):
    polydata_refer = polydata
    size = len(PointSet)
    points = vtk.vtkPoints()
    for i in range (size):
        p = PointSet[i]
        points.InsertNextPoint(p)
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetPolys ( polydata_refer.GetPolys() )
    #~ vertexFilter = vtkVertexGlyphFilter()
    #~ vertexFilter.SetInputConnection(polydata.GetProducerPort())
    #~ vertexFilter.Update()

    #~ polydata2 = vtk.vtkPolyData()
    #~ polydata2.ShallowCopy(vertexFilter.GetOutput())
    
    writer = vtkXMLPolyDataWriter()
    writer.SetFileName(fileDes)
    writer.SetInputData(polydata)
    writer.Write()

def PointSet2Mesh(PointSet,filename):
    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(filename)
    reader.Update()
    polydata_refer = vtk.vtkPolyData()
    polydata_refer = reader.GetOutput()
    size = len(PointSet)
    points = vtk.vtkPoints()
    vertices = vtk.vtkCellArray()
    for i in range (size):
        p = PointSet[i]
        points.InsertNextPoint(p)
    
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetPolys ( polydata_refer.GetPolys() )

    return polydata
def PointSet2Meshfrompolydata(PointSet,polydata_refer):
    size = len(PointSet)
    points = vtk.vtkPoints()
    vertices = vtk.vtkCellArray()
    for i in range (size):
        p = PointSet[i]
        points.InsertNextPoint(p)
    
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetPolys ( polydata_refer.GetPolys() )

    return polydata
# def SaveMat2ItkImage(Mat, fileDes):
#     mat_size = Mat.shape
#     pixelType = itk.UC
#     ImageType = itk.Image[pixelType, 3]
#     image = ImageType.New()
#     start=[0,0,0]
#     size=[mat_size[0],mat_size[1],mat_size[2]]
#     region = itk.ImageRegion._3(start,size)
#     space=[1,1,1]
#     if mat_size[0]==168:
#         space=[4.07283, 4.07283, 3]
#     if mat_size[0]==512:
#         space=[1.36719, 1.36719, 3]
#     image.SetRegions(region)
#     image.SetSpacing(space)
#     image.Allocate()
#     image.FillBuffer(0) 
#     for i in range (mat_size[0]):
#         for j in range (mat_size[1]):
#             for k in range (mat_size[2]):
#                 pixelIndex = [i,j,k]
#                 if Mat[i,j,k]!=0:
#                     image.SetPixel(pixelIndex, 1)
#     writerType = itk.ImageFileWriter[ImageType]
#     writer = writerType.New()
#     writer.SetFileName(fileDes)
#     writer.SetInput(image)
#     writer.Update()
#     return



def SavePolydata2VtkImage(Ploydata, fileDes):
    writer = vtkXMLPolyDataWriter()
    writer.SetFileName(fileDes)
    writer.SetInputData(Ploydata)
    writer.Write()
    return
def SavePolydata2PLYImage(Ploydata, fileDes):
    writer = vtkPLYWriter()
    writer.SetFileName(fileDes)
    writer.SetInputData(Ploydata)
    writer.Write()
    return
    
    
def LoadOneMesh_self(filename):
    dimension = 3
    file = open(filename, 'r')
    if dimension == 3: # in 3D case, the first line will be "OFF"
        file.readline()
    size = file.readline()
    size = size.split()
    mesh = [[0]*dimension] * int(size[0])
    triangle = [[0]*dimension] * int(size[1])
    for vertexid in range(int(size[0])):
        curLine = file.readline()
        curLine = curLine.split()
        curLine = map(float, curLine) # cast string to int
        mesh[vertexid] = curLine
    for vertexid in range(int(size[1])):
        triangleLine = file.readline()
        triangleLine = triangleLine.split()
        triangleLine = map(float, triangleLine) # cast string to int
        triangle[vertexid] = triangleLine
    file.close()
    return mesh,triangle
def LoadVtpAsPointset(filename):
    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(filename)
    reader.Update()
    polydata = vtkPolyData()
    polydata = reader.GetOutput()
    NumberOfPoints = polydata.GetNumberOfPoints()
    pointset = []
    
    for i in range(NumberOfPoints):
        p=[0,0,0]
        polydata.GetPoint(i,p)
        #~ print i,'****',p
        pointset.append(p)
    return pointset

def LoadVtpAsPolydata(filename):
    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(filename)
    reader.Update()
    polydata = reader.GetOutput()
    return polydata

def LoadPlyAsPolydata(filename):
    reader = vtk.vtkPLYReader()
    reader.SetFileName(filename)
    reader.Update()
    polydata = reader.GetOutput()
    return polydata
    
def LoadObjAsPolydata(filename):
    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(filename)
    reader.Update()
    polydata = reader.GetOutput()
    return polydata
    
def write_mat(filename,mat):
    #~ Write python mat to txt file
    size = mat.shape
    dim = len(size)
    if dim==1:
        file_name = open(filename,'w')
        file_name.write(repr(dim))
        file_name.write('\n')
        file_name.write(repr(size[0]))
        file_name.write(('\n'))
        for i in range(size[0]):
            cell = mat[i]
            cell_str = repr(cell)
            file_name.write(cell_str)
            file_name.write(('\n'))
        file_name.close

    if dim==2:
        file_name = open(filename,'w')
        file_name.write(repr(dim))
        file_name.write(('\n'))
        file_name.write(repr(size[0]))
        file_name.write(('\n'))
        file_name.write(repr(size[1]))
        file_name.write(('\n'))
        for i in range(size[0]):
            for j in range(size[1]):
                cell = mat[i,j]
                cell_str = repr(cell)
                file_name.write(cell_str)
                file_name.write(('\n'))
        file_name.close
    if dim==3:
        file_name = open(filename,'w')
        file_name.write(repr(dim))
        file_name.write(('\n'))
        file_name.write(repr(size[0]))
        file_name.write(('\n'))
        file_name.write(repr(size[1]))
        file_name.write(('\n'))
        file_name.write(repr(size[2]))
        file_name.write(('\n'))
        for i in range(size[0]):
            for j in range(size[1]):
                for k in range(size[2]):
                    cell = mat[i,j,k]
                    cell_str = repr(cell)
                    file_name.write(cell_str)
                    file_name.write(('\n'))
        file_name.close


def read_mat(filename):
    #~ Read python mat from txt file
    file_name = open(filename,'r')
    dim = eval(file_name.readline())
    
    if dim==1:
        size = eval(file_name.readline())
        size_img = [size]
        mat = np.zeros((size))
        for i in range(size):
            mat[i] = eval(file_name.readline())

    if dim==2:
        size_1 = eval(file_name.readline())
        size_2 = eval(file_name.readline())
        size_img = [size_1,size_2]
        mat = np.zeros((size_1,size_2))
        for i in range(size_1):
            for j in range(size_2):
                mat[i,j] = eval(file_name.readline())
    
    if dim==3:
        size_1 = eval(file_name.readline())
        size_2 = eval(file_name.readline())
        size_3 = eval(file_name.readline())
        size_img = [size_1,size_2,size_3]
        mat = np.zeros((size_1,size_2,size_3))
        for i in range(size_1):
            for j in range(size_2):
                for k in range(size_3):
                    mat[i,j,k] = eval(file_name.readline())

    file_name.close
    return mat


def Normal_vector(v1):
    v1= np.array(v1)
    v=array([0,0,0])
    if(np.sqrt(v1[0]**2+v1[1]**2+v1[2]**2)>0):  
        v=v1/np.sqrt(v1[0]**2+v1[1]**2+v1[2]**2)
    return v