import os
import json
from subprocess import Popen,PIPE
api_key="PxcWNl91AtsF51DiaeUhNYZXS18vu6_3"
api_secret="HHWh27sBEcjzm4Nta4ZEIMisjLhRX5vA"
outer_id="0x024"
path='./data/log'

def detect(image_file,return_landmark=0):
    result=Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/detect" -F \
        "api_key={api_key}" -F \
        "api_secret={api_secret}" -F \
        "image_file=@{image_file}" -F \
        "return_attributes=gender,age,smiling,glass,headpose,facequality,blur" -F \
        "return_landmark={return_landmark}"'
        .format(api_key=api_key,api_secret=api_secret,image_file=image_file,return_landmark=return_landmark),shell=True,stdout=PIPE)
    wait=""
    result=(result.stdout.read())
    with open("{path}/detect.json".format(path=path),"w+") as f:
        f.write(result)
    with open("{path}/detect.json".format(path=path)) as f:
        result=json.load(f)
    os.remove('{path}/detect.json'.format(path=path))
    return result

# if __name__ == '__main__':
#   result=detect(image_file="../data/wenzhang.jpg",return_landmark=1)
#   print result



def compareTtoT(face_token_1,face_token_2):
    result=Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/compare" -F \
        "api_key={api_key}" -F \
        "api_secret={api_secret}" -F \
        "face_token1={face_token_1}" -F \
        "face_token2={face_token_2}"'
        .format(api_key=api_key,api_secret=api_secret,face_token_1=face_token_1,face_token_2=face_token_2),shell=True,stdout=PIPE)  
    wait="" 
    result=(result.stdout.read())
    with open("{path}/compare.json".format(path=path),"w+") as f:   
        f.write(result)
    with open("{path}/compare.json".format(path=path)) as f:
        result=json.load(f)
    os.remove('{path}/compare.json'.format(path=path))
    return result 



# if __name__ == '__main__':
#   result=compareTtoT(face_token_1='6635c06a425fc964ae5d14a959f3331e',face_token_2='abaab7aeefb818ad0f766ed3cc5d799b')
#   confidence=result["confidence"]
#   print"confidence:{}".format(confidence)


def compareItoT(image_file,face_token):
    result=Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/compare" -F \
        "api_key={api_key}" -F \
        "api_secret={api_secret}" -F \
        "image_file1=@{image_file}" -F \
        "face_token2={face_token}"'
        .format(api_key=api_key,api_secret=api_secret,image_file=image_file,face_token=face_token),shell=True,stdout=PIPE)  
    wait="" 
    result=(result.stdout.read())
    with open("{path}/compare.json".format(path=path),"w+") as f:   
        f.write(result)
    with open("{path}/compare.json".format(path=path)) as f:
        result=json.load(f)
    os.remove('{path}/compare.json'.format(path=path))
    return result 


# if __name__ == '__main__':
#   result=compareItoT(image_file='../data/wenzhang.jpg',face_token='abaab7aeefb818ad0f766ed3cc5d799b')
#   confidence=result["confidence"]
#   print"confidence:{}".format(confidence)


def searchTtoI(face_token,return_result_count=1):
    result=Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/search" -F \
        "api_key={api_key}" -F \
        "api_secret={api_secret}" -F \
        "face_token={face_token}" -F \
        "outer_id={outer_id}" -F \
        "return_result_count={return_result_count}"'
        .format(api_key=api_key,api_secret=api_secret,face_token=face_token,outer_id=outer_id,return_result_count=return_result_count),shell=True,stdout=PIPE)  
    wait="" 
    result=(result.stdout.read())
    with open("{path}/search.json".format(path=path),"w+") as f:
        f.write(result)
    with open("{path}/search.json".format(path=path)) as  f:
        result=json.load(f)
    os.remove('{path}/search.json'.format(path=path))
    return result

# if __name__ == '__main__':
#   result=searchTtoI(face_token="f298edb8c094c5ac2883413320d8ef7f")
#   print result



def searchItoI(image_file,return_result_count=1):
    result=Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/search" -F \
        "api_key={api_key}" -F \
        "api_secret={api_secret}" -F \
        "image_file=@{image_file}" -F \
        "outer_id={outer_id}" -F \
        "return_result_count=1" -F \
        "return_result_count={return_result_count}"'
        .format(api_key=api_key,api_secret=api_secret,image_file=image_file,outer_id=outer_id,return_result_count=return_result_count),shell=True,stdout=PIPE)  
    wait="" 
    result=(result.stdout.read())
    with open("{path}/search.json".format(path=path),"w+") as f:
        f.write(result)
    with open("{path}/search.json".format(path=path)) as  f:
        result=json.load(f)
    os.remove('{path}/search.json'.format(path=path))
    return result

# if __name__ == '__main__':
#     result=searchItoI(image_file="../data/temp/75.pgm")
#     print result






def facesetcreate():
    result=Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/faceset/create" -F \
        "api_key={api_key}" -F \
        "api_secret={api_secret}" -F \
        "outer_id={outer_id}"'
        .format(api_key=api_key,api_secret=api_secret,outer_id=outer_id),shell=True,stdout=PIPE)    
    wait="" 
    result=(result.stdout.read())
    with open("{path}/facesetcreate.json".format(path=path),"w+") as f:
        f.write(result)
    with open("{path}/facesetcreate.json".format(path=path)) as f:
        result=json.load(f)
    os.remove('{path}/facesetcreate.json'.format(path=path))
    return result 


# if __name__ == '__main__':
#   result=facesetcreate()
#   print result




def facesetaddface(face_tokens):
    result=Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/faceset/addface" -F \
        "api_key={api_key}" -F \
        "api_secret={api_secret}" -F \
        "outer_id={outer_id}" -F \
        "face_tokens={face_tokens}"'
        .format(api_key=api_key,api_secret=api_secret,outer_id=outer_id,face_tokens=face_tokens),shell=True,stdout=PIPE)    
    wait="" 
    result=(result.stdout.read())
    with open("{path}/facesetaddfacce.json".format(path=path),"w+") as f:
        f.write(result)
    with open("{path}/facesetaddfacce.json".format(path=path)) as f:
        result=json.load(f)
    os.remove('{path}/facesetaddfacce.json'.format(path=path))
    return result 

# if __name__ == '__main__':
#   result=facesetaddface(face_tokens="cae2e796ad38737a5006fde10b529c32")
#   print result



def facesetremoveface(face_tokens):
    result=Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/faceset/removeface" -F \
        "api_key={api_key}" -F \
        "api_secret={api_secret}" -F \
        "outer_id={outer_id}" -F \
        "face_tokens={face_tokens}"'
        .format(api_key=api_key,api_secret=api_secret,outer_id=outer_id,face_tokens=face_tokens),shell=True,stdout=PIPE)    
    wait="" 
    result=(result.stdout.read())
    with open("{path}//facesetremoveface.json".format(path=path),"w+") as f:
        f.write(result)
    with open("{path}//facesetremoveface.json".format(path=path)) as f:
        result=json.load(f)
    os.remove('{path}/facesetremoveface.json'.format(path=path))
    return result 

# if __name__ == '__main__':
    # result=facesetremoveface(face_tokens="cae2e796ad38737a5006fde10b529c32")
    # print result



def facesetgetdetail():
    result=Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/faceset/getdetail" -F \
        "api_key={api_key}" -F \
        "api_secret={api_secret}" -F \
        "outer_id={outer_id}"'
        .format(api_key=api_key,api_secret=api_secret,outer_id=outer_id),shell=True,stdout=PIPE)    
    wait="" 
    result=(result.stdout.read())
    with open("{path}/facesetgetdetail.json".format(path=path),"w+") as f:
        f.write(result)
    with open("{path}/facesetgetdetail.json".format(path=path)) as f:
        result=json.load(f)
    os.remove('{path}/facesetgetdetail.json'.format(path=path))
    return result 


# if __name__ == '__main__':
#   result=facesetgetdetail()
#   print result

def facesetdelete(check_empty=1):
    global confidence
    result=Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/faceset/delete" -F \
        "api_key={api_key}" -F \
        "api_secret={api_secret}" -F \
        "check_empty={check_empty}" -F \
        "outer_id={outer_id}"'
        .format(api_key=api_key,api_secret=api_secret,check_empty=check_empty,outer_id=outer_id),shell=True,stdout=PIPE)    
    wait="" 
    result=(result.stdout.read())
    with open("{path}/facesetdelete.json".format(path=path),"w+") as f:
        f.write(result)
    with open("{path}/facesetdelete.json".format(path=path)) as f:
        result=json.load(f)
    os.remove('{path}/facesetdelete.json'.format(path=path))
    return result 

# if __name__ == '__main__':
#   result=facesetdelete(check_empty=0)
#   print result


def facesetgetfacesets():
    global confidence
    result=Popen('curl -X POST "https://api-cn.faceplusplus.com/facepp/v3/faceset/getfacesets" -F \
        "api_key={api_key}" -F \
        "api_secret={api_secret}"'
        .format(api_key=api_key,api_secret=api_secret),shell=True,stdout=PIPE)  
    wait="" 
    result=(result.stdout.read())
    with open("{path}/facesetdelete.json".format(path=path),"w+") as f:
        f.write(result)
    with open("{path}/facesetdelete.json".format(path=path)) as f:
        result=json.load(f)
    os.remove('{path}/facesetdelete.json'.format(path=path))
    return result 

# if __name__ == '__main__':
#   result=facesetgetfacesets()
#   print result

















