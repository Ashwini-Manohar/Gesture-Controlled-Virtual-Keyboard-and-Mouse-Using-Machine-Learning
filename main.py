import cv2
import pyautogui
import mouse
import time
import numpy as np
from HTM import HandDetector
import os

cap = cv2.VideoCapture(0)
cap.set(4, 1080)
cap.set(6, 720)

detector = HandDetector(detectionCon=0.8)

############
k1=['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=']
sk1=['!','@','#','$','%','^','&','*','(',')','_','+']

k2=["\t",'q','w','e','r','t','y','u','i','o','p','[',']',"\ "]
sk2=["\t",'Q',"W","E","R","T","Y","U","I","O","P","{","}","|"]

k3=['a','s','d','f','g','h','j','k','l',';',"'"]
sk3=["A","S","D","F","G","H","J","K","L",":",'"']

k4=['z','x','c','v','b','n','m',',','.','/']
sk4=['Z','X','C','V','B','N','M','<','>','?']
arrow=['left','up','down','right']

Folder="keyboard keys"
myList=os.listdir(Folder)
overlayls=[]
for imPath in myList:
    image=cv2.imread(f'{Folder}/{imPath}')
    overlayls.append(image)
shift=False
caps=False
controll=False

###########

def Distance(x1,y1,x2,y2):
    x1=int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    length=int(((((x2-x1)**2)+((y2-y1)**2))**0.5))
    return length

def cornerRect(img, loc, l=30, t=5, rt=1,
               colorR=(255, 0, 255), colorC=(0, 255, 0)):

    x, y, w, h = loc
    x1, y1 = x + w, y + h
    if rt != 0:
        cv2.rectangle(img, loc, colorR, rt)
    # Top Left  x,y
    cv2.line(img, (x, y), (x + l, y), colorC, t)
    cv2.line(img, (x, y), (x, y + l), colorC, t)
    # Top Right  x1,y
    cv2.line(img, (x1, y), (x1 - l, y), colorC, t)
    cv2.line(img, (x1, y), (x1, y + l), colorC, t)
    # Bottom Left  x,y1
    cv2.line(img, (x, y1), (x + l, y1), colorC, t)
    cv2.line(img, (x, y1), (x, y1 - l), colorC, t)
    # Bottom Right  x1,y1
    cv2.line(img, (x1, y1), (x1 - l, y1), colorC, t)
    cv2.line(img, (x1, y1), (x1, y1 - l), colorC, t)

    return img


############
############
wCam, hCam = 640, 480
frameR = 90
smoothening = 10


pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
wScr, hScr = 1400,780
drag=True
drag_from_X,drag_from_Y=0,0
drag_to_X,drag_to_Y=0,0
destination=False

############




while True:
    success, img = cap.read()
    img,oldLMlist,MyHandType,myHand = detector.findHands(img)
    lmList=list(oldLMlist)
    if MyHandType=="Right":
        ######
        if len(lmList) != 0:
            x1, y1 = lmList[8][0],lmList[8][1]
            x2, y2 = lmList[12][0],lmList[12][1]

            fingers = detector.fingersUp(myHand)
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                          (255, 0, 255), 2)

            if fingers[1] == 1 and fingers[2] == 0:
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                mouse.move(clocX, clocY)
                cv2.circle(img, (x1, y1), 6, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY

            if fingers[0] == 1 and fingers[1] == 1:

                length = Distance(lmList[3][0], lmList[3][1], lmList[8][0], lmList[8][1])

                if length < 60:
                    cv2.circle(img, (lmList[8][0],lmList[8][1]), 6, (0, 255, 0), cv2.FILLED)

                    mouse.click('left')


            if fingers[1] == 1 and fingers[4] == 1:

                length = Distance(lmList[8][0], lmList[8][1], lmList[20][0], lmList[20][1])

                if length < 40:
                    cv2.circle(img, (lmList[8][0],lmList[8][1]), 6, (0, 255, 0), cv2.FILLED)

                    mouse.click('right')

            if fingers[1] == 1 and fingers[2] == 1:

                length= Distance(lmList[8][0], lmList[8][1], lmList[12][0], lmList[12][1])

                if length < 40:
                    cv2.circle(img, (lmList[8][0], lmList[8][1]), 6, (0, 255, 0), cv2.FILLED)
                    x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                    y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

                    clocX = plocX + (x3 - plocX) / smoothening
                    clocY = plocY + (y3 - plocY) / smoothening

                    mouse.move(clocX, clocY)
                    if drag:
                        drag_from_X, drag_from_Y = clocX, clocY
                        drag = False
                        destination = True
                    plocX, plocY = clocX, clocY

                if destination and length > 40:
                    drag_to_X, drag_to_Y = plocX, plocY
                    mouse.move(drag_from_X, drag_from_Y)
                    mouse.drag(0, 0, drag_to_X - drag_from_X, drag_to_Y - drag_from_Y, absolute=False, duration=0.1)
                    # start (0,0) from current to next (x,y) addtional pixel

                    destination = False
                    drag = True

            if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
                length1=Distance(lmList[8][0], lmList[8][1], lmList[12][0], lmList[12][1])
                length2=Distance(lmList[12][0], lmList[12][1], lmList[16][0], lmList[16][1])
                if length1 < 40 and length2 > 40:
                    mouse.wheel(-1)
                if length1 > 40 and length2 < 40:
                    mouse.wheel(1)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
    ######

    elif MyHandType=="Left":

        for i in range(0, 12):
            img[20:60, 20 + (45 * i):60 + (45 * i)] = overlayls[i]
        img[20:60, 560:620] = overlayls[12]
        for i in range(0, 14):
            img[65:105, 10 + (45 * i):50 + (45 * i)] = overlayls[13 + i]
        if caps:
            img[110:150, 10:70] = overlayls[28]
        else:
            img[110:150, 10:70] = overlayls[27]

        for i in range(0, 11):
            img[110:150, 75 + (45 * i):115 + (45 * i)] = overlayls[29 + i]
        img[110:150, 570:630] = overlayls[40]
        if shift:
            img[155:195, 10:70] = overlayls[42]
            img[155:195, 525:585] = overlayls[42]
        else:
            img[155:195, 10:70] = overlayls[41]
            img[155:195, 525:585] = overlayls[41]
        for i in range(0, 10):
            img[155:195, 75 + (45 * i):115 + (45 * i)] = overlayls[43 + i]
        if controll:
            img[200:240, 10:50] = overlayls[55]
        else:
            img[200:240, 10:50] = overlayls[54]
        img[200:240, 250:370] = overlayls[53]
        for i in range(4):
            img[200:240, 400 + (45 * i):440 + (45 * i)] = overlayls[56 + i]

        if lmList:
            # for 1st line
            for i in range(0, 12):
                x, y = 20 + (45 * i), 20
                w, h = 60 + (45 * i), 60

                if x < lmList[8][0] < w and y < lmList[8][1] < h:
                    cornerRect(img, (20 + (45 * i), 20, 40, 40), 7, 2)
                    length = Distance(lmList[8][0], lmList[8][1], lmList[12][0], lmList[12][1])
                    if length < 40:
                        if shift or caps:
                            pyautogui.press(sk1[i])
                            pyautogui.sleep(0.25)
                            shift = False
                        else:
                            pyautogui.press(k1[i])
                            pyautogui.sleep(0.25)
                        if controll:
                            pyautogui.hotkey("ctrl", k1[i])
                            pyautogui.sleep(0.25)
                            controll = False
            # for BACKSPACE
            if 560 < lmList[8][0] < 620 and 20 < lmList[8][1] < 60:
                cornerRect(img, (560, 20, 60, 40), 7, 2)
                length = Distance(lmList[8][0], lmList[8][1], lmList[12][0], lmList[12][1])
                if length < 40:
                    pyautogui.press("Backspace")
                    pyautogui.sleep(0.25)

            # for 2nd line
            for i in range(0, 14):
                x, y = 10 + (45 * i), 65
                w, h = 50 + (45 * i), 105

                if x < lmList[8][0] < w and y < lmList[8][1] < h:
                    cornerRect(img, (10 + (45 * i), 65, 40, 40), 7, 2)
                    length = Distance(lmList[8][0], lmList[8][1], lmList[12][0], lmList[12][1])
                    if length < 40:
                        if shift:
                            pyautogui.press(sk2[i])
                            pyautogui.sleep(0.25)
                            shift = False
                        else:
                            pyautogui.press(k2[i])
                            pyautogui.sleep(0.25)
                        if controll:
                            pyautogui.hotkey("ctrl", k2[i])
                            pyautogui.sleep(0.25)
                            controll = False

            # for CAPS LOCK
            if 10 < lmList[8][0] < 70 and 110 < lmList[8][1] < 150:
                cornerRect(img, (10, 110, 60, 40), 7, 2)
                length = Distance(lmList[8][0], lmList[8][1], lmList[12][0], lmList[12][1])
                if length < 40:
                    if caps:
                        img[110:150, 10:70] = overlayls[27]
                        caps = False
                        pyautogui.sleep(0.25)
                    else:
                        img[110:150, 10:70] = overlayls[28]
                        caps = True
                        pyautogui.sleep(0.25)

            # for 3th line
            for i in range(0, 11):
                x, y = 75 + (45 * i), 110
                w, h = 115 + (45 * i), 150

                if x < lmList[8][0] < w and y < lmList[8][1] < h:
                    cornerRect(img, (75 + (45 * i), 110, 40, 40), 7, 2)
                    length = Distance(lmList[8][0], lmList[8][1], lmList[12][0], lmList[12][1])
                    if length < 40:
                        if shift or caps:
                            pyautogui.press(sk3[i])
                            pyautogui.sleep(0.25)
                            shift = False
                        else:
                            pyautogui.press(k3[i])
                            pyautogui.sleep(0.25)
                        if controll:
                            pyautogui.hotkey("ctrl", k3[i])
                            pyautogui.sleep(0.25)
                            controll = False
            # for ENTER
            if 570 < lmList[8][0] < 630 and 110 < lmList[8][1] < 150:
                cornerRect(img, (570, 110, 60, 40), 7, 2)
                length = Distance(lmList[8][0], lmList[8][1], lmList[12][0], lmList[12][1])
                if length < 40:
                    pyautogui.press("\n")
                    pyautogui.sleep(0.25)
            # for SHIFT
            if (10 < lmList[8][0] < 70 and 155 < lmList[8][1] < 195) or (
                    525 < lmList[8][0] < 585 and 155 < lmList[8][1] < 195):
                cornerRect(img, (10, 155, 60, 40), 7, 2)
                cornerRect(img, (525, 155, 60, 40), 7, 2)
                length = Distance(lmList[8][0], lmList[8][1], lmList[12][0], lmList[12][1])
                if length < 40:
                    if shift:
                        img[155:195, 10:70] = overlayls[41]
                        img[155:195, 525:585] = overlayls[41]
                        shift = False
                        pyautogui.sleep(0.25)
                    else:
                        img[155:195, 10:70] = overlayls[42]
                        img[155:195, 525:585] = overlayls[42]
                        shift = True
                        pyautogui.sleep(0.25)
            # for 4th line
            for i in range(0, 10):
                x, y = 75 + (45 * i), 155
                w, h = 115 + (45 * i), 195

                if x < lmList[8][0] < w and y < lmList[8][1] < h:
                    cornerRect(img, (75 + (45 * i), 155, 40, 40), 7, 2)
                    length = Distance(lmList[8][0], lmList[8][1], lmList[12][0], lmList[12][1])
                    if length < 40:
                        if shift or caps:
                            pyautogui.press(sk4[i])
                            pyautogui.sleep(0.25)
                            shift = False
                        else:
                            pyautogui.press(k4[i])
                            pyautogui.sleep(0.25)
                        if controll:
                            pyautogui.hotkey("ctrl", k4[i])
                            pyautogui.sleep(0.25)
                            controll = False

            # for SPACE
            if 250 < lmList[8][0] < 370 and 200 < lmList[8][1] < 240:
                cornerRect(img, (250, 200, 120, 40), 7, 2)
                length = Distance(lmList[8][0], lmList[8][1], lmList[12][0], lmList[12][1])
                if length < 40:
                    pyautogui.press("space")
                    pyautogui.sleep(0.25)

            # for controll
            if 10 < lmList[8][0] < 50 and 200 < lmList[8][1] < 240:
                cornerRect(img, (10, 200, 40, 40), 7, 2)
                length = Distance(lmList[8][0], lmList[8][1], lmList[12][0], lmList[12][1])
                if length < 40:
                    if controll:
                        controll = False
                        pyautogui.sleep(0.25)
                    else:
                        controll = True
                        pyautogui.sleep(0.25)

            # for arrows
            for i in range(4):
                x, y = 400 + (45 * i), 200
                w, h = 440 + (45 * i), 240

                if x < lmList[8][0] < w and y < lmList[8][1] < h:
                    cornerRect(img, (400 + (45 * i), 200, 40, 40), 7, 2)
                    length = Distance(lmList[8][0], lmList[8][1], lmList[12][0], lmList[12][1])
                    if length < 40:
                        pyautogui.press(arrow[i])
                        pyautogui.sleep(0.25)

        #####################
    else:
        cv2.putText(img, "To Use Keyborard Place Left Hand", (30,200), cv2.FONT_HERSHEY_PLAIN,
                    2, (0, 0, 255), 5)
        cv2.putText(img, "and for Mouse place Right Hand", (50, 250),
                    cv2.FONT_HERSHEY_PLAIN,
                    2, (0, 0, 255), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
