import cv2
import main
import socket
import mysql.connector
import numpy as np

#db connection
mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

#execute hdmi query
mycursor = mydb.cursor()
mycursor.execute("select query")
result = mycursor.fetchone()

cap=cv2.VideoCapture(0)
mycascade = cv2.CascadeClassifier('cascade/cascade.xml')

#connection
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = ''
# port = 1234
#
# s.connect((host, port))

#detect colors-red,white,gray
class ColorDetect():

    _, frame = cap.read()
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)

    white_lower = np.array([0, 0, 0], np.uint8)
    white_upper = np.array([0, 0, 255], np.uint8)

    gray_lower = np.array([0, 0, 0], np.uint8)
    gray_upper = np.array([255, 10, 255], np.uint8)

    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    white_mask = cv2.inRange(hsvFrame, white_lower, white_upper)

    gray_mask = cv2.inRange(hsvFrame, gray_lower, gray_upper)

    kernel = np.ones((5, 5), "uint8")

    red_mask = cv2.dilate(red_mask, kernel)
    res_red = cv2.bitwise_and(frame, frame, mask=red_mask)

    white_mask = cv2.dilate(white_mask, kernel)
    res_white = cv2.bitwise_and(frame, frame, mask=white_mask)

    gray_mask = cv2.dilate(gray_mask, kernel)
    res_gray = cv2.bitwise_and(frame, frame, mask=gray_mask)

font1=cv2.FONT_HERSHEY_SIMPLEX

while True:

    ret,frame=cap.read()
    frame=cv2.flip(frame,1)
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    pencils=mycascade.detectMultiScale(gray,1.3,7)

    #red
    contours, hierarchy = cv2.findContours(ColorDetect().red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours) :
        area = cv2.contourArea(contour)
        if (area > 300) :
            if result == (1, ) :
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, "Red", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
                mycursor.execute("update query")
                updateResult = mycursor.fetchone()
                mydb.commit()


    #white
    contours, hierarchy = cv2.findContours(ColorDetect().white_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours) :
        area = cv2.contourArea(contour)
        if (area > 300) :
            if result == (1, ) :
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, "White", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
                mycursor.execute("update query")
                updateResult = mycursor.fetchone()
                mydb.commit()

    #gray
    contours, hierarchy = cv2.findContours(ColorDetect().gray_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours) :
        area = cv2.contourArea(contour)
        if (area > 300) :
            if result == (1, ) :
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 10, 255), 2)
                cv2.putText(frame, "Gray", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 10, 255), 2)
                mycursor.execute("update pasadvanced.grayresult set grayresult='gri'")
                updateResult = mycursor.fetchone()
                mydb.commit()

    #show tv
    for (x,y,w,h) in pencils:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        img_with_rect = cv2.putText(img = frame,text = 'SHOW TV',org = (x,y),fontFace = font1,fontScale = 1,color = (255,0,0), thickness = cv2.LINE_4)

        #update
        if main.pencils.any() & result == 1 :
            mycursor.execute("update pasadvanced.hdmiresult set hdmi1Result='change'")
            updateResult = mycursor.fetchone()
            mydb.commit()

        #send "Successful" once to server
        # if main.pencils.any() == True :
        #     message = "Successful"
        #     s.send(message.encode('utf-8'))
        #     s.close()

    cv2.imshow("detectionShow",frame)

    if cv2.waitKey(100) & 0xff == ord('q') :
        cap.release()
        cv2.destroyAllWindows()
        break

