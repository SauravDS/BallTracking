
from __future__ import division
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time
import detector
import linReg
import quadFit
import warnings
import math
from imutils.object_detection import non_max_suppression
from imutils import paths

DEBUG_VISUALIZE = True

Textlines = []

warnings.filterwarnings("ignore")

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file", required=True)
ap.add_argument("-a", "--attack", help="specify bowling attack - 1 for Spin bowling and 0 for Fast", default=2)
ap.add_argument("-s", "--sliding", help="Show sliding", default=0)
ap.add_argument("-f", "--first", help="First frame", default=0)
ap.add_argument("-l", "--last", help="Last frame", default=1000)
args = vars(ap.parse_args())
camera = cv2.VideoCapture(args["video"])
bowling_attack = int(args["attack"])
show_slide = int(args["sliding"])
arg_first_frame = int(args["first"])
arg_last_frame = int(args["last"])

SKIP = 45

if bowling_attack:
    SKIP = 65


DURATION = 50


if bowling_attack:
    DURATION = 80

rejected_radius = []

def findRadius(frame, window_x, window_y, frame_no):

    """Function to find radius of the detected ball"""

    
    THRESHOLD_brightness = 75
    MAX_INTENSITY = 255
    MIN_INTENSITY = 0

    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(2,2))
    frame = clahe.apply(frame)

    blurredFrame = cv2.GaussianBlur(frame,(5,5),0)
    

    height, width = blurredFrame.shape[:2]
    frame_center_x = width/2
    frame_center_y = height/2

    
    avg_color_frame = float(np.sum(blurredFrame))/float(width*height)

    
    avg_color_ball = 0.0
    for dx in range(1,6):
        for dy in range(1,6):
            avg_color_ball += blurredFrame[frame_center_y+dy][frame_center_x+dx]
    avg_color_ball /= 25.0

    
    returnVal = True

    
    if avg_color_ball > 120.0:
        THRESHOLD_brightness = 100.0
        returnVal = False
    elif avg_color_ball > 100.0:
        THRESHOLD_brightness = 95.0
    elif avg_color_ball > 80.0:
        THRESHOLD_brightness = min(90.0,avg_color_ball)
    elif avg_color_ball < 65.0:
        THRESHOLD_brightness = 65.0
    else:
        THRESHOLD_brightness = 75.0

    if avg_color_frame - avg_color_ball < 20:
        
        returnVal = False

    for i in range(len(blurredFrame)):
        for j in range(len(blurredFrame[0])):
            if(blurredFrame[i][j]<THRESHOLD_brightness):
                blurredFrame[i][j]=MAX_INTENSITY
            else:
                blurredFrame[i][j]=MIN_INTENSITY
    

    _,contours,_ = cv2.findContours(blurredFrame,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(blurredFrame, contours, -1, (255,0,0), 1)
    

    centre_X = 0
    centre_Y = 0
    radius = 0
    min_diff = 100000
    
    for contour in contours:
        (x,y),r = cv2.minEnclosingCircle(contour)
        diff = abs(x-25)+abs(y-25)
        if diff < min_diff:
            if r < 1:
                
                continue
            
            centre_X = x
            centre_Y = y
            radius = r
            min_diff = diff
        elif diff == min_diff:
            if r > radius:
                centre_X = x
                centre_Y = y
                radius = r
    if min_diff > 20:
        
        returnVal = False

    if radius < 3.0:
        
        returnVal = False

    if len(contours) == 0:
        return False

    circleIndex = 0
    for i,j in enumerate(contours):
        if(len(j)>len(contours[circleIndex])):
            circleIndex = i;
                
    
    (centre_X,centre_Y),radius = cv2.minEnclosingCircle(contours[circleIndex])
    cv2.circle(frame,(int(centre_X),int(centre_Y)), int(radius), (255,0,0), 2)

    if returnVal == False:
        rejected_radius.append((int(window_x+centre_X), int(window_y+centre_Y)))
        return False

    if DEBUG_VISUALIZE:
       cv2.imshow("Best Fit Circle",frame)
    Textlines.append((window_x+centre_X, window_y+centre_Y, radius, frame_no,0))

    return True

frame_no = 1
initial_frame = 0

if bowling_attack < 2:
    
    y_start = 360
    y_end = 720
    x_start = 0
    x_end = 1080 
        
    (grabbed1, prev) = camera.read()
    while True:
        """
            Captures the frame in which bowler starts to bowl
        """
        
        (grabbed1, frame1) = camera.read()
        frame_no += 1
        if not grabbed1:
            print "Unable to grab frame: "+str(frame_no)
            break

        gray1 = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        final1 = gray1[y_start: y_end, x_start: x_end]
        final2 = gray2[y_start: y_end, x_start: x_end]
        difference = cv2.absdiff(final1, final2)
        retval, threshold = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)
        prev = frame1
        
        
        white = cv2.countNonZero(threshold)

        
        
        white_percentage = 0.02
        lower_height = 360
        lower_width = 1080

        if white > (white_percentage * lower_width * lower_height):
            
        
            
            for i in range(0,SKIP):
                (grabbed1, frame1) = camera.read()

            initial_frame = frame_no + SKIP
            frame_no = frame_no + SKIP
            break

if bowling_attack == 2:
    
    for i in range(0,arg_first_frame-1):
        (grabbed1, frame1) = camera.read()

    initial_frame = arg_first_frame
    frame_no = arg_first_frame

y_start = 150
y_end = 720
x_start = 150
x_end = 900
 
step_size = (10, 10)
threshold = 0.7

ball_detection = []

current_ballPos = (0,0)
            
while True:
    """
        Loop until ball gets detected
    """

    (grabbed1, frame1) = camera.read()

    if not grabbed1:
        print "Unable to grab frame: "+str(frame_no)
        break

    gray_image_1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    crop_img = gray_image_1[y_start: y_end, x_start: x_end]
    current_ballPos_temp = (0,0)

    
    current_ballPos_temp = detector.find(crop_img, step_size, threshold,gray_image_1,x_start,y_start,x_end, y_end)
    
    
    if(not(current_ballPos_temp[0] == 0 and current_ballPos_temp[1] == 0)):
        
        current_ballPos = (current_ballPos_temp[0] + x_start, current_ballPos_temp[1] + y_start)
        
        break


step_size = (3, 3)
threshold = 0.2

stop_search = 0


hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


batsman_mid = {}

batsman_first_detection = True
batsman_area = ()
      
while True:
    """
        Windowing technique, search around the ball detected in previous frame
    """

    (grabbed1, frame1) = camera.read()
    frame_no += 1
    if not grabbed1:
        print "Unable to grab frame: "+str(frame_no)
        break

    if frame_no > initial_frame + DURATION:
        break

    if frame_no > arg_last_frame:
        break

    
    last_frame = frame1
    gray_image_1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    img_copy = gray_image_1.copy()
    img_copy_1 = gray_image_1.copy()

    x1 = current_ballPos[0] - 50        
    x2 = current_ballPos[0] + 200
    y1 = current_ballPos[1] - 150
    y2 = current_ballPos[1] + 100

    
    if x1 < 0:
        x1 = 0
    if x2 > frame1.shape[1]:
        x2 = frame1.shape[1]
    if y1 < 0:
        y1 = 0
    if y2 > frame1.shape[0]:
        y2 = frame1.shape[0]

    
    crop_img = gray_image_1[y1: y2, x1: x2]
    
    print "Analyzing frame: "+str(frame_no)
    
    current_ballPos_temp = detector.find(crop_img, step_size,threshold,img_copy_1,x1,y1,x2,y2,show_slide)
    
    
    if(current_ballPos_temp[0] == 0 and current_ballPos_temp[1] == 0):
        stop_search = stop_search + 1
        if stop_search == 5:
            break
        continue
    
    stop_search = 0
    
    
    current_ballPos = (x1 + current_ballPos_temp[0], y1 + current_ballPos_temp[1])
    
    img_ball = img_copy[current_ballPos[1]: current_ballPos[1] + 50, current_ballPos[0]: current_ballPos[0] + 50]
    
    
    found = findRadius(img_ball, current_ballPos[0], current_ballPos[1], frame_no)

    if found:
        ball_detection.append(current_ballPos)



bouncing_coordinates = (0,0)
idx = 0
bouncing_idx = 0
last_frame1 = last_frame.copy()
for (x, y) in ball_detection:
    
    if y > bouncing_coordinates[1]:
        bouncing_coordinates = (x,y)
        bouncing_idx = idx
    idx = idx + 1
Textlines[bouncing_idx] = (Textlines[bouncing_idx][0], Textlines[bouncing_idx][1], Textlines[bouncing_idx][2], Textlines[bouncing_idx][3], 1)
cv2.rectangle(last_frame, (bouncing_coordinates[0]+23, bouncing_coordinates[1]+23), (bouncing_coordinates[0]+27, bouncing_coordinates[1]+27), (255, 0, 0), thickness=2)

idx = 0
for (x, y) in ball_detection:
    if idx < bouncing_idx:
        cv2.rectangle(last_frame, (x+23, y+23), (x+27, y+27), (0, 0, 0), thickness=2)
    idx = idx + 1    



corrected = []
rejected = []
for i in range(0,bouncing_idx + 2):
    
    if i >= len(ball_detection) or i >= len(Textlines):
        break
    corrected.append((ball_detection[i][0] + 25, ball_detection[i][1] + 25,Textlines[i][2], Textlines[i][3], Textlines[i][4]))

if(len(ball_detection) >= bouncing_idx + 2):
    prev_coord = (ball_detection[bouncing_idx + 1][0] + 25,ball_detection[bouncing_idx + 1][1] + 25,Textlines[bouncing_idx + 1][2], Textlines[bouncing_idx + 1][3], Textlines[bouncing_idx + 1][4])
    
    prev_slope = (prev_coord[1] - (ball_detection[bouncing_idx][1]+ 25) )/(prev_coord[0] - (25+ball_detection[bouncing_idx][0])) 
    for i in range((bouncing_idx+2), len(ball_detection)):
        if i >= len(ball_detection) or i >= len(Textlines):
            break
        current_coord = (ball_detection[i][0]+25,ball_detection[i][1]+25,Textlines[i][2], Textlines[i][3], Textlines[i][4])
        
        if (current_coord[0] - prev_coord[0]) == 0:
            slope = 100000
        else:
            slope = (current_coord[1] - prev_coord[1])/(current_coord[0] - prev_coord[0])
        tn = (slope-prev_slope)/(1.0+(slope*prev_slope))
        angle = math.atan(tn)*180.0/math.pi*(-1)
        distance = ((current_coord[1] - prev_coord[1])*(current_coord[1] - prev_coord[1])) + ((current_coord[0] - prev_coord[0])*(current_coord[0] - prev_coord[0]))
        
        
        
        if angle < 0:
            angle = angle* (-1)
        if angle <= 35 or distance <= 500:
            corrected.append(current_coord)  
            prev_coord = current_coord
            prev_slope = slope
        else:
            rejected.append((current_coord[0],current_coord[1]))      
    
i = 0
for (x,y,_,_,_) in corrected:
    
    cv2.rectangle(last_frame, (x-2, y-2), (x+2, y+2), (0, 255, 0), thickness=2)
    i = i + 1    

for (x,y) in rejected:
    cv2.rectangle(last_frame, (x-2, y-2), (x+2, y+2), (0, 0, 255), thickness=2)

for (x,y) in rejected_radius:
    cv2.rectangle(last_frame, (x-2, y-2), (x+2, y+2), (0, 255, 0), thickness=2)
    

if DEBUG_VISUALIZE:
    cv2.imshow("Ball Path", last_frame)
    cv2.imwrite("path.jpg", last_frame)
    cv2.waitKey(0)

cv2.destroyAllWindows()