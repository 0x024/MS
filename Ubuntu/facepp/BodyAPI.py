 # -*- coding:utf-8 -*-

import os
import json
import cv2
from subprocess import Popen,PIPE
api_key="PxcWNl91AtsF51DiaeUhNYZXS18vu6_3"
api_secret="HHWh27sBEcjzm4Nta4ZEIMisjLhRX5vA"
outer_id="0x024"
path='./data/log'

def detect(image_file):
    result=Popen('curl -X POST "https://api-cn.faceplusplus.com/humanbodypp/beta/detect" -F \
        "api_key={api_key}" -F \
        "api_secret={api_secret}" -F \
        "image_file=@{image_file}" -F \
        "return_attributes=gender,cloth_color" '
        .format(api_key=api_key,api_secret=api_secret,image_file=image_file),shell=True,stdout=PIPE)
    wait=""
    result=(result.stdout.read())
    with open("{path}/detect.json".format(path=path),"w+") as f:
        f.write(result)
    with open("{path}/detect.json".format(path=path)) as f:
        result=json.load(f)
    os.remove('{path}/detect.json'.format(path=path))
    return result

# if __name__ == '__main__':
  # img=cv2.imread("20170720226458.jpg")
  # result=detect(image_file="20170720226458.jpg")
  # print result["humanbodies"]
  # ft=cv2.freetype.createFreeType2()
  # ft.loadFontData(fontFileName='../data/font/simhei.ttf',id =0)
  # for i in range(0,len(result["humanbodies"])):
  #   humanbody_rectangle=result["humanbodies"][i]["humanbody_rectangle"]
  #   x=humanbody_rectangle["left"]
  #   y=humanbody_rectangle["top"]
  #   w=humanbody_rectangle["width"]
  #   h=humanbody_rectangle["height"]
  #   z=str(i)
  #   img=cv2.rectangle(img,(x,y),(x+w,y+h),(0,225,225),2)
  #   cv2.putText(img, z, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 100)

  #   cv2.imwrite("1.png",img)
  #   gender=result["humanbodies"][i]["attributes"]["gender"]["value"]
  #   print gender