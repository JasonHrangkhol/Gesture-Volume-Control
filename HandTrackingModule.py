import cv2 as cv
import mediapipe as mp
import time

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

class handDetector():

    def __init__(self):
        pass
    
    def find_hands(self,img,draw=True):

        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:  
                if draw:      
                    mpDraw.draw_landmarks(img, hand, mpHands.HAND_CONNECTIONS)

        return img


    def find_position(self,img, draw = False, hand_indx = 0):
        
        landmark_list = []
        xList = []
        yList = []
        positions = []
        
        if self.results.multi_hand_landmarks:

            hand = self.results.multi_hand_landmarks[hand_indx]
                
            for (id, landmark) in enumerate(hand.landmark):

                height, width, channel = img.shape
                x, y = int(landmark.x * width), int(landmark.y * height)
                xList.append(x)
                yList.append(y)
                landmark_list.append([id, x, y])

                if draw:
                    cv.circle(img, (x, y), 7, (255, 0, 255), cv.FILLED)
            
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            
            positions = xmin, ymin, xmax, ymax
 
            if draw:
                cv.rectangle(img, (positions[0] - 20, positions[1] - 20),
                (positions[2] + 20, positions[3] + 20), (0, 255, 0), 2)
    
        return landmark_list,positions

def main():
        
    cap = cv.VideoCapture(0)
    last_time = 0
    detector = handDetector()

    while True:

        isTrue,frame = cap.read()

        if isTrue:

            frame = detector.find_hands(frame)
            landmark_list = detector.find_position(frame,False)

            current_time = time.time()
            fps = 1/(current_time-last_time)
            last_time = current_time

            cv.putText(frame, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
            
            cv.imshow("Video",frame)

            if cv.waitKey(25)==ord('q'):
                break
        else:
            break

    cap.release()
    cv.destroyAllWindows()

if __name__=="__main__":
    main()