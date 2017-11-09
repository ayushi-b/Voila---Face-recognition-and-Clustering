import os
import pandas as pd
import cv2
import face_recognition
import shutil

def is_similar(i,j):
	try:
		imageA = face_recognition.load_image_file(i)
		imageB = face_recognition.load_image_file(j)

		encoding_imageA = face_recognition.face_encodings(imageA)[0]
		encoding_imageB = face_recognition.face_encodings(imageB)[0]

		return face_recognition.compare_faces([encoding_imageA],encoding_imageB)[0]
	except:
		return False
groups = {}	
index = 0
def is_grouped(imageA):
	global groups
	for i in groups:
		for j in groups[i]:
			if is_similar(j,imageA):
				groups[i].append(imageA)
				return True
	return False

def main():
	global groups, index

	image_files = []

	for i in os.listdir('uploads'):
		if "DS_Store" in i : continue
		image_files.append('uploads/{}'.format(i))
	# Making the dataframe
	images = []
	print("Total Images:- ",len(image_files))
	for i in image_files:
		images.append(cv2.imread(i))
	df = pd.DataFrame({'image_data':images,'name':image_files})
	df['sim'] = ""


	# Clustering of data
	for i in range(0,len(image_files)):
		if is_grouped(image_files[i]): continue
		index += 1
		groups[index] = [image_files[i]]

	print(groups)
	print("Total people found:- ", len(groups))
	try:
		os.mkdir('downloads')
	except:
		shutil.rmtree('downloads')
		os.mkdir('downloads')
	for i in groups:
		os.mkdir('downloads/{}'.format(i))
		for j in groups[i]:
			file = j.split('/')[1]
			try:
				os.rename(j,'downloads/{}/{}'.format(i,file))
			except:
				try:
					os.mkdir('downloads/{}'.format(i))
					os.rename(j, 'downloads/{}/{}'.format(i, file))
				except:
					continue


	print("All files moved")
	shutil.make_archive('output', 'zip', 'downloads')
	shutil.rmtree('downloads')
	groups = {}
	index = 0







	