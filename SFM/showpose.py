import json
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

with open("fr1_LF/reconstruction.json","r", encoding="utf-8") as f:
    cc = json.loads(f.read())

data=[]
name=[]
for c in range(len(cc)):
    for i in cc[c]["shots"]:
        data.append(cc[c]["shots"][i]["translation"])

def show(aa):
    ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
    for i in range(len(aa)):
        # plot point
        ax.scatter(aa[i][0],aa[i][1],aa[i][2], c='y')        # plot line
    ax.set_zlabel('Z')  # 坐标轴
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    plt.show()

show(data)


def show(aa,name):
    ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
    for i in range(len(aa)):
        # plot point
        ax.scatter(aa[i][0],aa[i][1],aa[i][2], c='y')
        # # plot text
        label = '%s' % (name[i])
        ax.text(aa[i][0], aa[i][1], aa[i][2], label, color='red')
    ax.set_zlabel('Z')  # 坐标轴
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    plt.show()




def getReconData(filename):
    with open(filename,"r", encoding="utf-8") as f:
        cc = json.loads(f.read())
    data={}
    for c in range(len(cc)):
        for i in cc[c]["shots"]:
            data[i]=cc[c]["shots"][i]["translation"]
    data_name=sorted(data.keys())
    return data,data_name

dataLF,nameLF=getReconData("fr1_LF/reconstruction.json")
dataSIFT,nameSIFT=getReconData("fr1_sift/reconstruction.json")

def show(data,name):
    ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
    i=0
    for key in name:
        if i==0:
            pre_value=data[key]
            i+=1
            continue
        value=data[key]
        ax.scatter(value[0],value[1],value[2], c='y')
        x=np.array([value[0],pre_value[0]])
        y=np.array([value[1],pre_value[1]])
        z=np.array([value[2],pre_value[2]])
        pre_value = value
        ax.plot(x,y,z,c='b')
        i+=1
        # # plot text
        if i %10 == 0:
            label = '%s' % (key.split('.')[0][-5:])
            ax.text(value[0], value[1], value[2], label, color='red')
    ax.set_zlabel('Z')  # 坐标轴
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    plt.show()


show(data,name)

show(dataSIFT,nameSIFT)



def show(data1,data2,name):
    ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
    i=0
    for key in data1.keys():
        # if i==0:
        #     pre_value1=data1[key]
        #     pre_value2=data2[key]
        #     i+=1
        #     continue
        value=data[key]
        ax.scatter(value[0],value[1],value[2], c='y')
    for key in data2.keys():
        value2=data2[key]
        ax.scatter(value2[0],value2[1],value2[2], c='r')
        # x=np.array([value[0],pre_value[0]])
        # y=np.array([value[1],pre_value[1]])
        # z=np.array([value[2],pre_value[2]])
        # pre_value = value
        # ax.plot(x,y,z,c='b')
        i+=1
        # # plot text
        # if i %10 == 0:
        #     label = '%s' % (key.split('.')[0][-5:])
        #     ax.text(value[0], value[1], value[2], label, color='red')
    ax.set_zlabel('Z')  # 坐标轴
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    plt.show()

show(data,dataSIFT,name)

def showGroundtruth():
    f = open("./groundtruth.txt")
    x = []
    y = []
    z = []
    for line in f:
        if line[0] == '#':
            continue
        data = line.split()
        x.append( float(data[1] ) )
        y.append( float(data[2] ) )
        z.append( float(data[3] ) )
    ax = plt.subplot( 111, projection='3d')
    ax.plot(x,y,z)
    plt.show()

showGroundtruth()



def show(data1,data2,name):
    ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
    x = []
    y = []
    z = []
    for key in name:
        value=data1[key]
        x.append( value[0] )
        y.append( value[1] )
        z.append( value[2] )
    ax.plot(x,y,z)
    f = open("./groundtruth.txt")
    x = []
    y = []
    z = []
    for line in f:
        if line[0] == '#':
            continue
        data = line.split()
        x.append( float(data[1] ) )
        y.append( float(data[2] ) )
        z.append( float(data[3] ) )
    ax.plot(x,y,z)
    ax.set_zlabel('Z')  # 坐标轴
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    plt.show()

show(data,dataSIFT,name)

dataLF,nameLF=getReconData("fr1/reconstruction.json")
show(dataLF,dataSIFT,nameLF)


## name:list
##  从真实值找匹配值，并在找不到的地方放弃
def getGroundAlian(name):
    groundtruth={}
    f = open("./groundtruth.txt")
    for line in f:
        if line[0] == '#':
            continue
        data_ = line.split()
        groundtruth[data_[0][:13]]=[float(data_[1]), float(data_[2]), float(data_[3])]
    valueG={}
    new_name=[]
    for key in name:
        try:
            valueG[key]=groundtruth[key[:13]]
            new_name.append(key)
        except:
            print(key)
    return valueG,new_name

ground,new_name=getGroundAlian(nameLF)

def Change2Point(data,name):
    points=[]
    for i in name:
        point=data[i]
        points.append(point)
    points=np.array(points)
    return points

LFPoints=Change2Point(dataLF,new_name)
GroundPoints=Change2Point(ground,new_name)

import transformations as tf

def align_reconstruction_naive_similarity(X, Xp):
    """Align with GPS and GCP data using direct 3D-3D matches."""
    # Compute similarity Xp = s A X + b
    T = tf.superimposition_matrix(X.T, Xp.T, scale=True)
    A, b = T[:3, :3], T[:3, 3]
    s = np.linalg.det(A)**(1. / 3)
    A /= s
    return s, A, b

s, A, b=align_reconstruction_naive_similarity(LFPoints.T, GroundPoints.T)


new_GroundPoints=s*A.dot(GroundPoints.T).T+b
new_LFPoints=s*A.dot(LFPoints.T).T+b

# just show points get from above
def show(data1,data2):
    ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
    x=data1[:,0]
    y=data1[:,1]
    z=data1[:,2]
    ax.plot(x,y,z,c='b')
    x=data2[:,0]
    y=data2[:,1]
    z=data2[:,2]
    ax.plot(x,y,z,c='r')
    ax.set_zlabel('Z')  # 坐标轴
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    plt.show()

show(new_GroundPoints,LFPoints)

show(new_LFPoints,GroundPoints)
