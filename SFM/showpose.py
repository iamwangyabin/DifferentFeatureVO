import json
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

with open("fr1/reconstruction.json","r", encoding="utf-8") as f:
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

data={}
c=0
for i in cc[c]["shots"]:
    data[i]=cc[c]["shots"][i]["translation"]

data_name=sorted(data.keys())

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
        ax.plot(x,y,z,c='b')
        i+=1
        # # plot text
        # if i %2 == 0:
        #     label = '%s' % (name[i].split('.')[0][-5:])
        #     ax.text(aa[i][0], aa[i][1], aa[i][2], label, color='red')
    ax.set_zlabel('Z')  # 坐标轴
    ax.set_ylabel('Y')
    ax.set_xlabel('X')
    plt.show()


show(data,data_name)
