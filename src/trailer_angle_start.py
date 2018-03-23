import argparse
import rospy
import rosbag
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

class par_rea_plo:
	def __init__(self):
		self.bridge = CvBridge()
		self.bag = []
		self.time = []
		self.angle = []
		self.raw_angle = []

	def plotting(self):
		plt.clf()
		plt.plot(self.time,self.raw_angle-np.mean(self.raw_angle))
		plt.plot(self.time,self.angle)
		plt.xlim([0,self.time[-1]])
		plt.ylim([-2,2])
		plt.xlabel('Time (s)')
		plt.ylabel('Angle (degree)')
		plt.grid(b=True, which='both')
		plt.legend(['raw angle','filtered angle'])
		plt.show()

	def raw_angle_parser(self):
		for msg in self.bag.read_messages(topics=['/urg/trailer_angle']):
			msg_handle = msg.message
			tmp =msg_handle.header.stamp.secs+msg_handle.header.stamp.nsecs/1000000000
			self.time = np.append(self.time, tmp)
			self.raw_angle = np.append(self.raw_angle, np.rad2deg(msg_handle.raw_angle))
			self.angle = np.append(self.angle, np.rad2deg(msg_handle.angle))
		self.time = self.time - self.time[0]
		print('Standard deviation of raw angle',np.std(self.raw_angle))
		print('Standard deviation of filtered angle',np.std(self.angle))
		self.plotting()

	def main(self, args):
		self.bag = rosbag.Bag(args)
		self.raw_angle_parser()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='bag')
	parser.add_argument(
		'bag',
		type=str,
		nargs='?',
		default='/home/yuan/workspace/radar_ana/data/doppler/_30m_v5mph2.bag',
		help='Bag name.'
	)
	args = parser.parse_args()
	arg = vars(args)['bag']
	par_rea_plo().main(arg)