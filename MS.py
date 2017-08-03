 # -*- coding:utf-8 -*-

import os
import cv2
import sys
import time
import thread
import numpy as np
import RPi.GPIO as GPIO
from facepp import BodyAPI
from facepp import FaceAPI
from facepp import DBConnect

reload(sys)
sys.setdefaultencoding('utf8')
conn = DBConnect.dbconnect()
cur = conn.cursor()
os.system(sys.argv[1]) 

def checkdist():
	index=2
	GPIO.output(2,GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(2,GPIO.LOW)
	while not GPIO.input(3):
		pass
	t1 = time.time()
	while GPIO.input(3):
		pass
	t2 = time.time()
	distance=((t2-t1)*340/2)
	if distance>=(index+1) or distance<=(index-1):
		print "Detection of moving objects!"
		camrun()
	return distance

def camrun():
		thread.start_new_thread(cam,(0,))
		# thread.start_new_thread(cam,(1,))
		time.sleep(10)
		print "time up!"

def cam(i):
	t1=int(time.time())
	bs = cv2.createBackgroundSubtractorKNN(detectShadows = True)
	camera = cv2.VideoCapture(i)
	while True:
		ret, frame = camera.read()
		fgmask = bs.apply(frame)
		try:
			th = cv2.threshold(fgmask.copy(), 244, 255, cv2.THRESH_BINARY)[1]
			th = cv2.erode(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)), iterations = 2)
			dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8,3)), iterations = 2)
			image, contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			for c in contours:
				if cv2.contourArea(c) > 1000:
					(x,y,w,h) = cv2.boundingRect(c)
					if i==0:
						cv2.imwrite('./img/shutter/{}.jpg'.format(time.strftime('%Y%m%d%H%M%S'+'_'+str(0))), frame)
					if i==1:
						cv2.imwrite('./img/shutter/{}.jpeg'.format(time.strftime('%Y%m%d%H%M%S'+'_'+str(1))), frame)
			t2=int(time.time())
			if (t2-t1) == 10:
				break
		except AttributeError:
			print "The camera:%s are busy or Not plugged in"%i
			break
	camera.release()
	cv2.destroyAllWindows()

def checkcycle():
	while True:
		print "checking "
		getfilename()
		time.sleep(5)

def testfacepp():
	result=FaceAPI.detect(image_file="./img/shutter/999999999999999.jpg")
	try:
		result=result["faces"]
		access=1
		return access
	except KeyError:
		access=0
		return access

def getfilename():
	global filedate,fileList
	topdown=True
	i=0
	dir="./img/shutter"
	with open('./data/log/piclist.log','r') as f:
		content=f.read()
	fileLists = [] 
	access=testfacepp()
	if access==1:
		for root, dirs, files in os.walk(dir, topdown):
			for PicName in (sorted(files)):
				fileLists.append(os.path.join(root,PicName))
				fileList=fileLists[i]
				filedate=fileList.split('/')[3].split('.')[0]
				if filedate =="999999999999999":
					print"over"
				if filedate not in content:
					print "img:%s  now checking!"%filedate
					checkbody(fileList)
				i=i+1
	if access==0:
		print"due to CONCURRENCY_LIMIT_EXCEEDED We are trying again"		

def checkbody(filename):
	global namei,gender_b,confidence_gender,upper_body_cloth_color,lower_body_cloth_color,confidence_all
	img = cv2.imread(filename)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	print "We are now running the BodyAPI"
	result=BodyAPI.detect(image_file=filename)
	if len(result["humanbodies"])==0:
		print "img:%s no body!"%filedate
		with open ("./data/log/piclist.log","a") as f:
			f.write(filedate)
			f.write("\n")

	if len(result["humanbodies"])>0:
		for i in range(0,len(result["humanbodies"])):

			humanbody_rectangle=result["humanbodies"][i]["humanbody_rectangle"]
			x=humanbody_rectangle["left"]
			y=humanbody_rectangle["top"]
			w=humanbody_rectangle["width"]
			h=humanbody_rectangle["height"]
			gender_b=result["humanbodies"][i]["attributes"]["gender"]["value"]
			confidence_gender=result["humanbodies"][i]["attributes"]["gender"]["confidence"]
			upper_body_cloth_color=result["humanbodies"][i]["attributes"]["upper_body_cloth_color"]
			lower_body_cloth_color=result["humanbodies"][i]["attributes"]["lower_body_cloth_color"]
			confidence_all=result["humanbodies"][i]["confidence"]
			img=cv2.rectangle(img,(x,y),(x+w,y+h),(0,225,225),2)
			f = cv2.resize(gray[y:y+h, x:x+w], (x+w,y+h))
			count=str(i)
			cv2.putText(img, count, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 100)
			namei=filedate+str(i)
			cv2.imwrite("./img/done/{}.jpg".format(namei),f)
			
			try:
				checkface_online("./img/done/{}.jpg".format(namei))
			except KeyError:
				print "lalalalal"

def detailface(face_token):
	cur.execute("select * from face_data where face_token='%s'"%face_token)
	line=cur.fetchone()
	ID,name,gender=line[0],line[1],line[2]
	detail=[ID,name,gender]
	return detail



def checkface_online(filename):
	img = cv2.imread(filename)
	print "we are now running the FaceAPI"
	result_d=FaceAPI.detect(image_file=filename)
	if len(result_d["faces"])==0:
		print "img:%s have body,but no faces!"%filedate
		with open ("./data/log/piclist.log","a") as f:
			f.write(filedate)
			f.write("\n")
	if len(result_d["faces"])>0:
		face_token=result_d["faces"][0]["face_token"]
		gender=result_d["faces"][0]["attributes"]["gender"]["value"]
		age=result_d["faces"][0]["attributes"]["age"]["value"]
		face_rectangle=result_d["faces"][0]["face_rectangle"]
		x=face_rectangle["left"]
		y=face_rectangle["top"]
		w=face_rectangle["width"]
		h=face_rectangle["height"]
		img=cv2.rectangle(img,(x,y),(x+w,y+h),(0,225,225),2)
		result_s=FaceAPI.searchTtoI(face_token=face_token)
		if len(result_s)==3:
			print "img:%s maybe  is a stranger"%filedate
			cv2.putText(img,"stranger", (x, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,225), 2)
			cur.execute("insert into io_data values('%s','None','stranger','%s','%s','%s','%s')"\
				%(filedate,confidence,gender,face_token,fileList))
			conn.commit()
			cv2.imwrite('./img/done/{}.jpg'.format(namei),img)
			cur.execute("insert into walk_data values('%s','None','stranger','%s','%s','%s','%s','%s','%s')"\
				%(filedate,gender_b,confidence_gender,\
				upper_body_cloth_color,lower_body_cloth_color,confidence_all,fileList))
			conn.commit()	
			with open ("./data/log/piclist.log","a") as f:
					f.write(filedate)
					f.write("\n")

		if len(result_s)>3:
			face_token=result_s["results"][0]["face_token"]
			confidence=result_s["results"][0]["confidence"]
			if confidence >= 80.00:
				detail=detailface(face_token)
				print "img:%s he's name :%s"%(filedate,detail[1])
				cur.execute("insert into io_data values('%s',%s,'%s','%s','%s','%s','%s')"\
					%(filedate,detail[0],detail[1],confidence,gender,face_token,fileList))
				conn.commit()
				cv2.putText(img,detail[1], (x, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,225), 2)
				cv2.imwrite('./img/done/{}.jpg'.format(namei),img)
				cur.execute("insert into walk_data values('%s',%s,'%s','%s','%s','%s','%s','%s','%s')"\
					%(filedate,detail[0],detail[1],gender_b,confidence_gender,\
					upper_body_cloth_color,lower_body_cloth_color,confidence_all,fileList))
				conn.commit()
				with open ("./data/log/piclist.log","a") as f:
						f.write(filedate)
						f.write("\n")
			else:
				print "img:%s maybe he is a stranger"%filedate
				cv2.putText(img,"stranger", (x, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,225), 2)
				cur.execute("insert into io_data values('%s','None','stranger','%s','%s','%s','%s')"%\
					(filedate,confidence,gender,face_token,fileList))
				conn.commit()	
				cv2.imwrite('./img/done/{}.jpg'.format(namei),img)
				cur.execute("insert into walk_data values('%s','None','stranger','%s','%s','%s','%s','%s','%s')"\
					%(filedate,gender_b,confidence_gender,upper_body_cloth_color,lower_body_cloth_color,confidence_all,fileList))
				conn.commit()
				with open ("./data/log/piclist.log","a") as f:
						f.write(filedate)
						f.write("\n")


if __name__ ==  '__main__':

	if sys.argv[1]=='check':
		checkcycle()
	if  sys.argv[1]== 'camera':
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(2,GPIO.OUT,initial=GPIO.LOW)
		GPIO.setup(3,GPIO.IN)
		while True:
			try:
				while True:
					print 'Distance: %0.2f m' %checkdist()
					time.sleep(0.5)
			except KeyboardInterrupt:
				GPIO.cleanup()


