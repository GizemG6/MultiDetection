import cv2
import main
import socket

cap=cv2.VideoCapture(0)
mycascade = cv2.CascadeClassifier('cascade/cascade.xml')

#connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 1234

s.connect((host, port))

font1=cv2.FONT_HERSHEY_SIMPLEX

while True:

    ret,frame=cap.read()
    frame=cv2.flip(frame,1)
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    pencils=mycascade.detectMultiScale(gray,1.3,7)

    for (x,y,w,h) in pencils:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        img_with_rect = cv2.putText(img = frame,text = 'SHOW TV',org = (x,y),fontFace = font1,fontScale = 1,color = (255,0,0), thickness = cv2.LINE_4)

        #send "Successful" once to server
        if main.pencils.any() == True :
            message = "Successful"
            s.send(message.encode('utf-8'))
            s.close()

    cv2.imshow("detectionShow",frame)

    if cv2.waitKey(100) & 0xff == ord('q') :
        break

cap.release()
cv2.destroyAllWindows()