 # -*- coding:utf-8 -*-

import os
import cv2
import sys
import random
import time
from facepp import BodyAPI
from facepp import FaceAPI
from facepp import DBConnect

reload(sys)
sys.setdefaultencoding('utf8')
conn = DBConnect.dbconnect()
cur = conn.cursor()


def update(dir,topdown=True):
	global filelist
	global fileLists
	with open('./data/log/piclist.log','r') as f:
		content=f.read()
		fileList = [] 
	for root, dirs, files in os.walk(dir, topdown):
		i=0
		for PicName in (sorted(files))[::-1]:
			fileList.append(os.path.join(root,PicName))
			fileLists=fileList[i]
			filelist=fileLists.split('/')[3].split('.')[0]
			print filelist
			if filelist not in content:
				with open ("./data/log/piclist.log","a") as f:
						f.write(filelist)
						f.write("\n")
				checkface_online(fileList[i])

			if filelist in content:
				break
				# checkface(fileList[i])
			i=i+1
def detailface(face_token):
	cur.execute("select * from face_data where face_token='%s'"%face_token)
	line=cur.fetchone()
	ID,name,gender=line[0],line[1],line[2]
	detail=[ID,name,gender]
	return detail


def checkface_offline(filename):
	face_cascade = cv2.CascadeClassifier('./data/cascades/haarcascade_frontalface_alt.xml')
	img = cv2.imread(filename)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces=face_cascade.detectMultiScale(gray, 1.3, 5)
	ft=cv2.freetype.createFreeType2()
	ft.loadFontData(fontFileName='./data/font/simhei.ttf',id =0)
	for (x,y,w,h) in faces:
		img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),3)
		f = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
		name=filelist+(str(random.randint(0,99)))
		print name
		cv2.imwrite('./img/face/{}.jpg'.format(name),f)
		result=FaceAPI.searchItoI(image_file='./img/face/{}.jpg'.format(name))
		confidence=result["results"][0]["confidence"]
		if len(result)==3:
			checkbody_n('./img/shutter/{}.jpg'.format(filelist))
		if confidence >= 80.00:
			face_token=result["results"][0]["face_token"]
			detail=detailface(face_token)
			cur.execute("insert into io_data values('%s',%s,'%s','%s','%s','%s','%s')"%(filelist,detail[0],detail[1],confidence,detail[2],face_token,fileLists))
			conn.commit()
			# checkbody_y('./img/shutter/{}.jpg'.format(filelist))

			ft.putText(img=img,text=detail[1], org=(x, y - 10), fontHeight=30,line_type=cv2.LINE_AA, color=(0,255,165), thickness=1, bottomLeftOrigin=True)
		else:
			print"Unknow face"
			face_token=result["results"][0]["face_token"]
			detail=detailface(face_token)

			random_ID=random.randint(100000000000,100000999999)

			cv2.putText(img,"Unknow", (x, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,225), 2)
			cur.execute("insert into io_data values('%s',%s,'None','%s','%s','%s','%s')"%(filelist,random_ID,confidence,detail[2],face_token,fileLists))
			conn.commit()
	cv2.imwrite('./img/shutter/{}.jpg'.format(filelist),img)
def checkface_online(filename):
	i=0
	img = cv2.imread(filename)
	result_d=FaceAPI.detect(image_file=filename)
	time.sleep(2)
	if len(result_d)==3:
		print result_d
	if len(result_d)>3:
		for i in range(0,len(result_d["faces"])):
			face_token=result_d["faces"][i]["face_token"]
			gender=result_d["faces"][i]["attributes"]["gender"]["value"]
			age=result_d["faces"][i]["attributes"]["age"]["value"]
			face_rectangle=result_d["faces"][i]["face_rectangle"]
			x=face_rectangle["left"]
			y=face_rectangle["top"]
			w=face_rectangle["width"]
			h=face_rectangle["height"]
			img=cv2.rectangle(img,(x,y),(x+w,y+h),(0,225,225),2)
			# cv2.imwrite('./img/shutter/{}.jpg'.format(filelist),img)
			result_s=FaceAPI.searchTtoI(face_token=face_token)
			time.sleep(1)
			# print result_s
			if len(result_s)==3:
				print "result_s==3"
				if i==0:
					checkbody_n('./img/shutter/{}.jpg'.format(filelist))

			if len(result_s)>3:
				face_token=result_s["results"][0]["face_token"]
				confidence=result_s["results"][0]["confidence"]


				if confidence >= 80.00:
					detail=detailface(face_token)
					cur.execute("insert into io_data values('%s',%s,'%s','%s','%s','%s','%s')"%(filelist,detail[0],detail[1],confidence,gender,face_token,fileLists))
					conn.commit()
					ft=cv2.freetype.createFreeType2()
					ft.loadFontData(fontFileName='./data/font/simhei.ttf',id =0)
					ft.putText(img=img,text=detail[1], org=(x, y - 10), fontHeight=30,line_type=cv2.LINE_AA, color=(0,255,165), thickness=1, bottomLeftOrigin=True)
					cv2.imwrite('./img/shutter/{}.jpg'.format(filelist),img)
					if i==1:
						checkbody_y('./img/shutter/{}.jpg'.format(filelist),face_token)
				else:
					print"Unknow face"
					face_token=result_s["results"][0]["face_token"]
					confidence=result_s["results"][0]["confidence"]
					# random_ID=random.randint(100000000000,100000999999)
					cv2.putText(img,"Unknow", (x, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,225), 2)
					cur.execute("insert into io_data values('%s','None','None','%s','%s','%s','%s')"%(filelist,confidence,gender,face_token,fileLists))
					conn.commit()	
					cv2.imwrite('./img/shutter/{}.jpg'.format(filelist),img)
					if i==1:
						checkbody_n('./img/shutter/{}.jpg'.format(filelist))


			i=i+1










def checkbody_y(filename,face_token):
	img = cv2.imread(filename)

	result=BodyAPI.detect(image_file=filename)
	# print result


	for i in range(0,len(result["humanbodies"])):

		humanbody_rectangle=result["humanbodies"][i]["humanbody_rectangle"]
		x=humanbody_rectangle["left"]
		y=humanbody_rectangle["top"]
		w=humanbody_rectangle["width"]
		h=humanbody_rectangle["height"]
		img=cv2.rectangle(img,(x,y),(x+w,y+h),(0,225,225),2)
		cv2.putText(img, "i", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 100)
		detail=detailface(face_token)

		gender=result["humanbodies"][i]["attributes"]["gender"]["value"]
		confidence_gender=result["humanbodies"][i]["attributes"]["gender"]["confidence"]
		confidence_all=result["humanbodies"][i]["confidence"]
		upper_body_cloth_color=result["humanbodies"][i]["attributes"]["upper_body_cloth_color"]
		lower_body_cloth_color=result["humanbodies"][i]["attributes"]["lower_body_cloth_color"]
		confidence_all=result["humanbodies"][i]["confidence"]
		# print gender
		i=i+1
		cv2.imwrite('./img/shutter/{}.jpg'.format(filelist),img)
		# cv2.imshow("canny", img)
		# cv2.waitKey()
		# cv2.destroyAllWindows()
		print "llllllllllllllllllll"
		cur.execute("insert into walk_data values('%s',%s,'%s','%s','%s','%s','%s','%s')"%(filelist,detail[0],detail[1],gender,confidence_gender,\
			upper_body_cloth_color,lower_body_cloth_color,confidence_all))
		conn.commit()

def checkbody_n(filename):
	img = cv2.imread(filename)

	result=BodyAPI.detect(image_file=filename)
	# print result["humanbodies"]
	for i in range(0,len(result["humanbodies"])):
		if len(result)==3:
			break
		if len(result)>3:
			humanbody_rectangle=result["humanbodies"][i]["humanbody_rectangle"]
			x=humanbody_rectangle["left"]
			y=humanbody_rectangle["top"]
			w=humanbody_rectangle["width"]
			h=humanbody_rectangle["height"]
			img=cv2.rectangle(img,(x,y),(x+w,y+h),(0,225,225),2)
			cv2.putText(img, "i", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
			cv2.imwrite('./img/shutter/{}.jpg'.format(filelist),img)
			# cv2.imshow("canny", img)
			# cv2.waitKey()
			# cv2.destroyAllWindows()
			gender=result["humanbodies"][i]["attributes"]["gender"]["value"]
			confidence_gender=result["humanbodies"][i]["attributes"]["gender"]["confidence"]
			confidence_all=result["humanbodies"][i]["confidence"]
			upper_body_cloth_color=result["humanbodies"][i]["attributes"]["upper_body_cloth_color"]
			lower_body_cloth_color=result["humanbodies"][i]["attributes"]["lower_body_cloth_color"]
			confidence_all=result["humanbodies"][i]["confidence"]
			# print gender
			i=i+1
			cur.execute("insert into walk_data values('%s','None','None','%s','%s','%s','%s','%s')"%(filelist,gender,confidence_gender,\
				upper_body_cloth_color,lower_body_cloth_color,confidence_all))
			conn.commit()















if __name__ == '__main__':

	update("./img/shutter")



