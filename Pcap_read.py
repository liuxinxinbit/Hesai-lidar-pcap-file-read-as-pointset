#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import struct
import numpy as np
from numpy import binary_repr
import matplotlib.pyplot as plt
import math
from LxxIO import SavePointSet2PLYImage
from scipy.signal.signaltools import medfilt
from scipy.ndimage.morphology import distance_transform_edt


def PcapFileReadAsPointset(filename):
    fpcap = open(filename,'rb')
    string_data = fpcap.read()
    file_read_index=0
    #pcap文件包头解析
    pcap_header = {}
    pcap_header['magic_number'] = string_data[0:4]
#     if string_data[0:4]==b'\xd4\xc3\xb2\xa1':
#         print('字节读取:交换顺序')
#     elif string_data[0:4]==b'\xa1\xb2\xc3\xd4':
#         print('字节读取:顺序')
#     else:
#         print('字节读取:未知顺序')     
    pcap_header['version_major'] = struct.unpack('H', bytes(string_data[4:6]))[0]
    pcap_header['version_minor'] = struct.unpack('H', bytes(string_data[6:8]))[0]
    pcap_header['thiszone'] = struct.unpack('I', bytes(string_data[8:12]))[0]
    pcap_header['sigfigs'] = struct.unpack('I', bytes(string_data[12:16]))[0]
    pcap_header['snaplen'] = struct.unpack('I', bytes(string_data[16:20]))[0]
    pcap_header['linktype'] = struct.unpack('I', bytes(string_data[20:24]))[0]
#     print(pcap_header)
    Pandar40_Wire_angular_distribution = np.double(np.loadtxt("Pandar40_Wire_angular_distribution.csv", dtype=np.str, delimiter=","))
    packet_num = 0
    pcap_packet_header = {}
    pcap_packet_data=[]
    file_read_index +=24
    while(file_read_index<len(string_data)):
        pcap_packet_header['GMTtime:']=struct.unpack('I', bytes(string_data[file_read_index:file_read_index+4]))[0]
        pcap_packet_header['MicroTime:']=struct.unpack('I', bytes(string_data[file_read_index+4:file_read_index+8]))[0]
        pcap_packet_header['caplen:']=struct.unpack('I', bytes(string_data[file_read_index+8:file_read_index+12]))[0]
        pcap_packet_header['len:']=struct.unpack('I', bytes(string_data[file_read_index+12:file_read_index+16]))[0]
        file_read_index+=16
#         print(pcap_packet_header)

        ip_packet_header={}
        ip_packet_header['Ethernet_II_MAC_Destination']=string_data[file_read_index:file_read_index+6]
        ip_packet_header['Ethernet_II_MAC_Src']=string_data[file_read_index+6:file_read_index+12]
        ip_packet_header['Ethernet_Packet_Type']=struct.unpack('H', bytes(string_data[file_read_index+12:file_read_index+14]))[0]
        ip_packet_header['Internet_Protocol']=string_data[file_read_index+14:file_read_index+34]
        ip_packet_header['UDP_Protocol']=string_data[file_read_index+34:file_read_index+38]
        ip_packet_header['UDP_Protocol_Length']=struct.unpack('H', bytes(string_data[file_read_index+38:file_read_index+40]))[0]
        ip_packet_header['UDP_Protocol_Correct']=struct.unpack('H', bytes(string_data[file_read_index+40:file_read_index+42]))[0]

        file_read_index+=42
        block_index=1
        FE=struct.unpack('H', bytes(string_data[file_read_index+block_index*124:file_read_index+block_index*124+2]))
        Azimuth=struct.unpack('H', string_data[file_read_index+block_index*124+2:file_read_index+block_index*124+4])[0]/100
        for Channel_index in range(40):
            Channel_Distance=string_data[file_read_index+block_index*124+Channel_index*3+4:file_read_index+block_index*124+Channel_index*3+2+4]
            Channel_Distance = struct.unpack('H',bytes(Channel_Distance))[0]
            Channel_Distance = int(np.flip(binary_repr(Channel_Distance)),2)
            Channel_Distance=np.double(Channel_Distance*4)/1000
            Channel_Reflectivity=struct.unpack('B', string_data[file_read_index+block_index*124+Channel_index*3+2+4:file_read_index+block_index*124+Channel_index*3+3+4])[0]
            Channel_Azimuth=Azimuth+Pandar40_Wire_angular_distribution[Channel_index,1]
            Channel_Elevation=Pandar40_Wire_angular_distribution[Channel_index,2]
            Channel_Polar_coordinates=[Channel_Azimuth,Channel_Elevation,Channel_Distance,Channel_Reflectivity]
            pcap_packet_data.append(Channel_Polar_coordinates)
 
        file_read_index+=1240
        Additional_information={}
        Additional_information['Reserved_nothing']=string_data[file_read_index:file_read_index+8]
        Additional_information['motor_speed']=struct.unpack('H', bytes(string_data[file_read_index+8:file_read_index+10]))[0]
        Additional_information['Timestamp']=struct.unpack('I', bytes(string_data[file_read_index+10:file_read_index+14]))[0]
        Additional_information['Echo_information']=string_data[file_read_index+14:file_read_index+15]
        Additional_information['Factory']=string_data[file_read_index+15:file_read_index+16]
        file_read_index += 16
        packet_num+=1
    fpcap.close() 
    return np.array(pcap_packet_data)
def polar2cart(data):
    result=[]
    for point in data:
        angle_A=point[0]*np.pi/180
        angle_E=point[1]*np.pi/180
        x= point[2]*np.cos(angle_E)*np.cos(angle_A)
        y= point[2]*np.cos(angle_E)*np.sin(angle_A)
        z= point[2]*np.sin(angle_E)
        result.append([x,y,z])
    return result
def Radar_data_split(data):
    data_size=data.shape
    frame_size=40*360
    radar_frame_set=[]
    frame_index=0
    while data_size[0]-frame_index>frame_size:
        radar_frame=[]
        for block_index in range(frame_size):
            frame_index+=1
            if data[frame_index,2]>10 and data[frame_index,3]>0:
                radar_frame.append([data[frame_index,0],data[frame_index,1],data[frame_index,2]])
        radar_frame = polar2cart(radar_frame)
        radar_frame_set.append(radar_frame)
    return radar_frame_set

def PointsetTo2DImage(ps):
    result=np.zeros((400,400))
    for point in (ps):
        w=np.int16(np.sqrt(point[0]**2+point[1]**2)*np.sin(np.pi/180)/2+0.5)
        result[np.int16(point[0]+200-w):np.int16(point[0]+200+w),np.int16(point[1])-w+200:np.int16(point[1])+200+w]=255
    return result
    
def GetProjectpoint(center,normal,P):
    D=-(center[0]*normal[0]+center[1]*normal[1]+center[2]*normal[2])
    t=(normal[0]*P[0]+normal[1]*P[1]+normal[2]*P[2]+D)/(normal[0]**2+normal[1]**2+normal[2]**2)
    x=P[0]-normal[0]*t
    y=P[1]-normal[1]*t
    z=P[2]-normal[2]*t
    p=[x,y,z]
    return p
def GetProjectpointset(ps,center=[0,0,0],normal=[0,0,1]):
    result = []
    for point in ps:
        p=GetProjectpoint(center,normal,point)
        result.append(p)
    return result
targetfilepath="test.pcap"
pcap_packet_data = PcapFileReadAsPointset(targetfilepath)
radar_frame_set  = Radar_data_split(pcap_packet_data)

target_radar_frame=GetProjectpointset(radar_frame_set[55])

field_circle=np.ones((360))*199
for point in target_radar_frame:
    d=np.around(np.sqrt(point[0]**2+point[1]**2))
    angle=np.around(np.arctan(point[1]/point[0])/np.pi*180)
    print(angle)
    if angle<0:
        angle=angle+360
    if d<field_circle[np.int16(angle)]:
        field_circle[np.int16(angle)]=d
field_circle = medfilt(field_circle,5)

imagee = PointsetTo2DImage(target_radar_frame)


field=np.zeros((400,400))
for i in range(360):
    x=np.int16(field_circle[i]*np.cos(i*np.pi/180))
    y=np.int16(field_circle[i]*np.sin(i*np.pi/180))
    field[x+200,y+200]=180
field[198:203,198:203]=200
field[200:400,200]=255
plt.imshow(imagee)
plt.imshow(field)
plt.show()
#     SavePointSet2PLYImage(radar_frame,'/home/liuxinxin/ToolKit/result/'+str(frame_index+1)+'.ply')

print ('**************')


