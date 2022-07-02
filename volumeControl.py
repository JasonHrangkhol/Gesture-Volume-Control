from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import HandTrackingModule as htm
import numpy as np
import cv2 as cv
import math,time

wCam, hCam = 640, 480

capture = cv.VideoCapture(0)
capture.set(3, wCam)
capture.set(4, hCam)
lastTime =0
volumeBar=400
volumePercentage = 0
detector = htm.handDetector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volumeRange = volume.GetVolumeRange()
minVol = volumeRange[0]
maxVol = volumeRange[1]

while True:

    success,frame = capture.read()

    if success:
        
        frame = detector.find_hands(frame, draw = False)
        landmarkList,positions = detector.find_position(frame, draw = False)

        if len(landmarkList) != 0:
           
            area = (positions[2] - positions[0]) * (positions[3] - positions[1]) // 100

            if 450 < area < 2500:
 
                x1, y1 = landmarkList[4][1], landmarkList[4][2]
                x2, y2 = landmarkList[8][1], landmarkList[8][2]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        
                cv.circle(frame, (x1, y1), 10, (255, 0, 255), cv.FILLED)
                cv.circle(frame, (x2, y2), 10, (255, 0, 255), cv.FILLED)
                cv.circle(frame, (cx, cy), 10, (255, 0, 255), cv.FILLED)
                cv.line(frame, (x1, y1), (x2, y2), (270, 255, 150), 3)

                length = math.hypot(x2 - x1, y2 - y1)

                volumeBar = np.interp(length, [50, 250], [400, 150])
                volumePercentage = np.interp(length, [50, 250], [0, 100])

                smoothness = 10
                volumePercentage = smoothness * round(volumePercentage / smoothness)

                volume.SetMasterVolumeLevelScalar(volumePercentage / 100, None)
 
        cv.rectangle(frame, (20,150), (45, 400), (224, 224, 224), 2)
        cv.rectangle(frame, (20, int(volumeBar)), (45, 400), (255, 0, 0), cv.FILLED)
        cv.putText(frame, f'{int(volumePercentage)} %', (20, 140), cv.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 2)            

        currentTime = time.time()
        fps = 1/(currentTime-lastTime)
        lastTime = currentTime

        cv.putText(frame, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
            
        cv.imshow("Video",frame)

        if cv.waitKey(25)==ord('q'):
            break
    else:
        break

capture.release()
cv.destroyAllWindows()