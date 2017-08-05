import cv2
import time

def cam(i):

	bs = cv2.createBackgroundSubtractorKNN(detectShadows = True)
	camera = cv2.VideoCapture(i)

	while True:
		ret, frame = camera.read()
		fgmask = bs.apply(frame)
		# img = frame
		th = cv2.threshold(fgmask.copy(), 244, 255, cv2.THRESH_BINARY)[1]
		th = cv2.erode(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)), iterations = 2)
		dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8,3)), iterations = 2)
		image, contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		for c in contours:
			if cv2.contourArea(c) > 1000:
				(x,y,w,h) = cv2.boundingRect(c)
				# cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 255, 0), 2)
				cv2.imwrite('./img/shutter/{}.jpg'.format(time.strftime('%Y%m%d%H%M%S')), frame)

		cv2.imshow("detection", frame)
		k = cv2.waitKey(30) & 0xff
		if k == 27:
			break

	camera.release()
	cv2.destroyAllWindows()
if __name__ == '__main__':
	cam(0)