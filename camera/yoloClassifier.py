from mvnc import mvncapi as mvnc
import os
import cv2
import numpy as np
from datetime import datetime
from skimage.transform import resize

class YoloClassifier:
	def __init__(self, graphFile='graph', verbose=False):
		if verbose:
			mvnc.SetGlobalOption(mvnc.GlobalOption.LOG_LEVEL, 2)
		devices = mvnc.EnumerateDevices()
		if len(devices) == 0:
			raise Exception('No Movidius found!')

		device = mvnc.Device(devices[0])
		try:
			device.OpenDevice()

			rootPath = ('/'.join(os.path.realpath(__file__).split('/')[:-1]))+'/'
			with open(rootPath+graphFile, mode='rb') as f:
				blob = f.read()
			graph = device.AllocateGraph(blob)
			graph.SetGraphOption(mvnc.GraphOption.ITERATIONS, 1)
			self.verbose = verbose
			self.device = device
			self.graph = graph
		except:
			raise Exception('Unable to open device! Maybe re-plug it or reboot and try again... thanks')


	def classify(self, img):
		start = datetime.now()
		if self.verbose:
			print('Classifying image {}'.format(img.shape))
		dim=(448,448)
		im = resize(img.copy()/255.0,dim,1)
		im = im[:,:,(2,1,0)]
		
		end = datetime.now()
		elapsedTime = end-start
		if self.verbose:
			print (' -> Image manipulation took {} ms'.format(elapsedTime.total_seconds()*1000))
		
		strt = datetime.now()
		self.graph.LoadTensor(im.astype(np.float16), 'user object')
		out, userobj = self.graph.GetResult()
		
		end = datetime.now()
		elapsedTime = end-strt
		if self.verbose:
			print (' -> Classification took {} ms'.format(elapsedTime.total_seconds()*1000))
		
		strt = datetime.now()
		results = self.interpret_output(out.astype(np.float32), img.shape[1], img.shape[0]) # fc27 instead of fc12 for yolo_small
		end = datetime.now()
		elapsedTime = end-start
		if self.verbose:
			print (' -> Parsing took {} ms'.format((end-strt).total_seconds()*1000))
			print (' # Total classification took {} ms'.format(elapsedTime.total_seconds()*1000))

		return [elapsedTime.total_seconds()*1000, results]

	def interpret_output(self, output, img_width, img_height):
		classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train","tvmonitor"]
		w_img = img_width
		h_img = img_height
		threshold = 0.2
		iou_threshold = 0.5
		num_class = 20
		num_box = 2
		grid_size = 7
		probs = np.zeros((7,7,2,20))
		class_probs = (np.reshape(output[0:980],(7,7,20)))#.copy()
		#print(class_probs)
		scales = (np.reshape(output[980:1078],(7,7,2)))#.copy()
		#print(scales)
		boxes = (np.reshape(output[1078:],(7,7,2,4)))#.copy()
		offset = np.transpose(np.reshape(np.array([np.arange(7)]*14),(2,7,7)),(1,2,0))
		#boxes.setflags(write=1)
		boxes[:,:,:,0] += offset
		boxes[:,:,:,1] += np.transpose(offset,(1,0,2))
		boxes[:,:,:,0:2] = boxes[:,:,:,0:2] / 7.0
		boxes[:,:,:,2] = np.multiply(boxes[:,:,:,2],boxes[:,:,:,2])
		boxes[:,:,:,3] = np.multiply(boxes[:,:,:,3],boxes[:,:,:,3])

		boxes[:,:,:,0] *= w_img
		boxes[:,:,:,1] *= h_img
		boxes[:,:,:,2] *= w_img
		boxes[:,:,:,3] *= h_img

		for i in range(2):
			for j in range(20):
				probs[:,:,i,j] = np.multiply(class_probs[:,:,j],scales[:,:,i])
		#print (probs)
		filter_mat_probs = np.array(probs>=threshold,dtype='bool')
		filter_mat_boxes = np.nonzero(filter_mat_probs)
		boxes_filtered = boxes[filter_mat_boxes[0],filter_mat_boxes[1],filter_mat_boxes[2]]
		probs_filtered = probs[filter_mat_probs]
		classes_num_filtered = np.argmax(probs,axis=3)[filter_mat_boxes[0],filter_mat_boxes[1],filter_mat_boxes[2]]

		argsort = np.array(np.argsort(probs_filtered))[::-1]
		boxes_filtered = boxes_filtered[argsort]
		probs_filtered = probs_filtered[argsort]
		classes_num_filtered = classes_num_filtered[argsort]

		for i in range(len(boxes_filtered)):
			if probs_filtered[i] == 0 : continue
			for j in range(i+1,len(boxes_filtered)):
				if self.iou(boxes_filtered[i],boxes_filtered[j]) > iou_threshold :
					probs_filtered[j] = 0.0

		filter_iou = np.array(probs_filtered>0.0,dtype='bool')
		boxes_filtered = boxes_filtered[filter_iou]
		probs_filtered = probs_filtered[filter_iou]
		classes_num_filtered = classes_num_filtered[filter_iou]

		result = []
		for i in range(len(boxes_filtered)):
			result.append([classes[classes_num_filtered[i]],boxes_filtered[i][0],boxes_filtered[i][1],boxes_filtered[i][2],boxes_filtered[i][3],probs_filtered[i]])

		return result

	def iou(self, box1, box2):
		tb = min(box1[0]+0.5*box1[2],box2[0]+0.5*box2[2])-max(box1[0]-0.5*box1[2],box2[0]-0.5*box2[2])
		lr = min(box1[1]+0.5*box1[3],box2[1]+0.5*box2[3])-max(box1[1]-0.5*box1[3],box2[1]-0.5*box2[3])
		if tb < 0 or lr < 0 : intersection = 0
		else : intersection =  tb*lr
		return intersection / (box1[2]*box1[3] + box2[2]*box2[3] - intersection)

	def tagImage(self, img, result, maxWidth, maxHeight):
		for el in result[1]:
			x = int(el[1]);
			y = int(el[2]);
			w = int(el[3])//2;
			h = int(el[4])//2;
			xmin = x-w;
			xmax = x+w;
			ymin = y-h;
			ymax = y+h;
			if xmin<0:
				xmin = 0;
			if ymin<0:
				ymin = 0;
			if xmax>maxWidth:
				xmax = maxWidth;
			if ymax>maxHeight:
				ymax = maxHeight;
			cv2.rectangle(img,(xmin,ymin),(xmax,ymax),(0,255,0),2);
			cv2.rectangle(img,(xmin,ymin-20),(xmax,ymin),(125,125,125),-1);
			cv2.putText(img,el[0] + ' : %.2f' % el[5],(xmin+5,ymin-7),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1);

	def close(self):
		self.graph.DeallocateGraph()
		self.device.CloseDevice()
