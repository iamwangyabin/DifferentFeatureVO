import numpy as np 
import cv2

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

from visual_odometry import PinholeCamera, VisualOdometry
data['desc']
# # TUM fr1
# # fx	fy		cx		cy		d0		d1		d2		d3		d4
# # 517.3	516.5	318.6	255.3	0.2624	-0.9531	-0.0054	0.0026	1.1633
# # fx	fy		cx		cy		k1		k2		p1		p2		k3

def showGroundtruth():
	f = open("./Data/groundtruth.txt")
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

def getImageLists():
	imgList=[]
	f = open("./Data/rgb.txt")
	for line in f:
		if line[0] == '#':
			continue
		data = line.split()
		imgList.append(data[1])
	return imgList

def getVO(data_path,rgb_txt):
	cam = PinholeCamera(640.0, 480.0, 517.3, 516.5, 318.6, 255.3, 0.2624, -0.9531, -0.0054, 0.0026, 1.1633)
	vo = VisualOdometry(cam)
	imgList = getImageLists()
	traj = np.zeros((400,400,3), dtype=np.uint8)

	for img_id in range(len(imgList)):
		img = cv2.imread('./Data/'+imgList[img_id], 0)
		vo.update(img, img_id)

		cur_t = vo.cur_t
		if(img_id > 2):
			x, y, z = cur_t[0], cur_t[1], cur_t[2]
		else:
			x, y, z = 0., 0., 0.
		draw_x, draw_y = int(x)+290, int(z)+90
		true_x, true_y = int(vo.trueX)+290, int(vo.trueZ)+90

		cv2.circle(traj, (draw_x,draw_y), 1, (img_id*255/4540,255-img_id*255/4540,0), 1)
		cv2.circle(traj, (true_x,true_y), 1, (0,0,255), 2)
		cv2.rectangle(traj, (10, 20), (600, 60), (0,0,0), -1)
		text = "Coordinates: x=%2fm y=%2fm z=%2fm"%(x,y,z)
		cv2.putText(traj, text, (20,40), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, 8)

		cv2.imshow('Road facing camera', img)
		cv2.imshow('Trajectory', traj)
		cv2.waitKey(1)

	cv2.imwrite('map.png', traj)


if __name__ == "__main__":
	getVO("","")

import os

imgList = getImageLists()

def getKptsDescs(feat_path, img_path):
	path = img_path.split('/')
	npz_path = feat_path + path[1] + '.npz'
	data = np.load(npz_path)
	des = data['descs']
	kpt = data['kpts']
	return kpt, des

def drawMatchLine(imgList):
	root_dir = './Data/'
	# 读入图片    
	Img1 = cv2.imread(root_dir + imgList[0])
	Img2 = cv2.imread(root_dir + imgList[1])
	feat_path = './Data/rgb_feats/'
	k1, d1 = getKptsDescs(feat_path, imgList[0])
	k2, d2 = getKptsDescs(feat_path, imgList[1])
	# BFMatcher
	FLANN_INDEX_KDTREE = 0
	index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
	search_params = dict(checks=50)
	flann = cv2.FlannBasedMatcher(index_params,search_params)
	matchers = flann.knnMatch(d1,d2,k=2)
    # 相似列表
	Match = []
	for m,n in matchers:
		if m.distance <  0.50*n.distance:
			Match.append(m)
	# 查看两张图片的宽及高
	height1 , width1 = Img1.shape[:2]
	height2 , width2 = Img2.shape[:2]
	# 像素调整
	vis = np.zeros((max(height1, height2), width1 + width2, 3), np.uint8)
	vis[:height1, :width1] = Img1
	vis[:height2, width1:width1 + width2] = Img2
	p1 = [kpp.queryIdx for kpp in Match[:20]]
	p2 = [kpp.trainIdx for kpp in Match[:20]]
	post1 = np.int32([k1[pp] for pp in p1])
	post2 = np.int32([k2[pp] for pp in p2]) + (width1, 0)
	for (x1, y1), (x2, y2) in zip(post1, post2):
		cv2.line(vis, (x1, y1), (x2, y2), (0,0,255))
	cv2.namedWindow("match",cv2.WINDOW_NORMAL)
	cv2.imshow("match", vis)    
	cv2.waitKey(0)
	cv2.destroyAllWindows()

drawMatchLine(imgList)