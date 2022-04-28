from visual import *
import argparse
import quadFit
import temp1
from PIL import Image
import pyscreenshot as ImageGrab
from subprocess import call

rlist = []
xlist = []
ylist = []
zlist = []
bouncing_pt = []
frames_list = []
batsman_mid_list = []

SHOW_3D = False
SHOW_LABELS = True
AFTER_BOUNCE_LINEAR = False

FPS = 120.0

START_RADIUS = 0.0
END_RADIUS = 0.0

START_RADIUS = 13.5
END_RADIUS = 5.5
WICKET_RADIUS = 5






PITCH_WIDTH = 305.0
PITCH_LENGTH = 2012.0
PITCH_THICKNESS = 10
CREASE_LENGTH = 122
XWASTE = 405.4

WICKET_HEIGHT = 71.1
WICKET_WIDTH = 22.86
STUMP_WIDTH = 4.5

WIDE_WIDTH = 264
LINE_WIDTH = 5

BATSMAN_HEIGHT = 160
BATSMAN_WIDTH = 90

BALL_RADIUS = 3.6

FY = 1520.0


SCALE = [1, 0.5, PITCH_LENGTH - (2*CREASE_LENGTH)]


bouncing_pt_idx = -1






with open('coordinates_171638.txt') as coord_file:  



    for i,row in enumerate(coord_file):
        x,y,r,frame_no,is_bouncing_pt,r_new,y_new,batsman_xmid,batsman_ymid = row.split()
        r_new = float(r_new)
        x = ((float(x)-XWASTE)*305/500)-152
        y = (720.0-float(y_new))*SCALE[1]
        bouncing_pt.append(int(is_bouncing_pt))
        if int(is_bouncing_pt) == 1:
            bouncing_pt_idx = i
        
        xlist.append(x)
        ylist.append(y)
        frames_list.append(float(frame_no))
        
        
        
        rlist.append(r_new)

        batsman_mid_list.append((float(batsman_xmid), float(batsman_ymid)))

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file", default=0)
args = vars(ap.parse_args())
flag = int(args["video"])
if flag == 1:
    END_RADIUS = 5.2
    WICKET_RADIUS = 4.8
elif flag == 2:
    END_RADIUS = 6.5
    WICKET_RADIUS = 6
elif flag == 3:
    END_RADIUS = 4.5
    WICKET_RADIUS = 4
elif flag == 4:
    END_RADIUS = 5.8
    WICKET_RADIUS = 5.3
elif flag == 5:
    END_RADIUS = 6.4
    WICKET_RADIUS = 5.8

for i,radius in enumerate(rlist):   
    z = abs((START_RADIUS-radius)/(START_RADIUS-END_RADIUS))
    zlist.append(z*SCALE[2])

def getBatsmanHeight():
    yavg = 0.0
    for (x,y) in batsman_mid_list:
        if y == -1:
            continue
        yavg += y
    yavg = float(yavg)/len(batsman_mid_list)
    

    yavg = (720.0-float(yavg))*SCALE[1]
    

    height = yavg*FY/(FY + (PITCH_LENGTH/2-122))
    

    return height*2*0.73

BATSMAN_HEIGHT = getBatsmanHeight()
print "Batsman's height: "+str(BATSMAN_HEIGHT)


coord_file.close()


scene1 = display(title="HawkEye View", width=1280, height=720, range=800, background=(0.2,0.2,0.2), center=(0,30,30))
if SHOW_3D:
    scene1.stereo = 'redblue'
scene1.forward = (-1,-0.05,0.02)


floor = box(pos=(0,0,0), size=(PITCH_LENGTH*1.2,PITCH_THICKNESS*1.2,PITCH_WIDTH), material=materials.unshaded, color=(0.97,0.94,0.6))
floor_outer = box(pos=(0,0,0), size=(PITCH_LENGTH*1.25,PITCH_THICKNESS,PITCH_WIDTH*2), material=materials.unshaded, color=(0.2,0.7,0.27))
floor_impact = box(pos=(0,0,0), size=(PITCH_LENGTH,PITCH_THICKNESS*1.3,WICKET_WIDTH), material=materials.unshaded, color=(0.63,0.57,0.93), opacity=0.8)


batting_wicket1 = box(pos=(PITCH_LENGTH/2,WICKET_HEIGHT/2,-(WICKET_WIDTH/2-STUMP_WIDTH/2)), size=(5,WICKET_HEIGHT,STUMP_WIDTH), color=color.white)
batting_wicket2 = box(pos=(PITCH_LENGTH/2,WICKET_HEIGHT/2,0), size=(5,WICKET_HEIGHT,STUMP_WIDTH), color=color.white)
batting_wicket3 = box(pos=(PITCH_LENGTH/2,WICKET_HEIGHT/2,(WICKET_WIDTH/2-STUMP_WIDTH/2)), size=(5,WICKET_HEIGHT,STUMP_WIDTH), color=color.white)
line1 = box(pos=(PITCH_LENGTH/2,PITCH_THICKNESS/2,0), size=(LINE_WIDTH,5,WIDE_WIDTH), color=color.white)
line2 = box(pos=(PITCH_LENGTH/2,PITCH_THICKNESS/2,132), size=(244,5,LINE_WIDTH), color=color.white)
line3 = box(pos=(PITCH_LENGTH/2,PITCH_THICKNESS/2,-132), size=(244,5,LINE_WIDTH), color=color.white)
line4 = box(pos=(PITCH_LENGTH/2-122,PITCH_THICKNESS/2,0), size=(LINE_WIDTH,5,366), color=color.white)


bowling_wicket1 = box(pos=(-PITCH_LENGTH/2,WICKET_HEIGHT/2,-(WICKET_WIDTH/2-STUMP_WIDTH/2)), size=(5,WICKET_HEIGHT,STUMP_WIDTH), color=color.white)
bowling_wicket2 = box(pos=(-PITCH_LENGTH/2,WICKET_HEIGHT/2,0), size=(5,WICKET_HEIGHT,STUMP_WIDTH), color=color.white)
bowling_wicket3 = box(pos=(-PITCH_LENGTH/2,WICKET_HEIGHT/2,(WICKET_WIDTH/2-STUMP_WIDTH/2)), size=(5,WICKET_HEIGHT,STUMP_WIDTH), color=color.white)
line1 = box(pos=(-PITCH_LENGTH/2,PITCH_THICKNESS/2,0), size=(LINE_WIDTH,5,WIDE_WIDTH), color=color.white)
line2 = box(pos=(-PITCH_LENGTH/2,PITCH_THICKNESS/2,132), size=(244,5,LINE_WIDTH), color=color.white)
line3 = box(pos=(-PITCH_LENGTH/2,PITCH_THICKNESS/2,-132), size=(244,5,LINE_WIDTH), color=color.white)
line4 = box(pos=(-PITCH_LENGTH/2+122,PITCH_THICKNESS/2,0), size=(LINE_WIDTH,5,366), color=color.white)









balls = []
FX = 350

yp = ylist[0]*FY/(FY+zlist[0])

zp = xlist[0]*zlist[0]/(FX+zlist[0])




coords_3d = []




num_detected_points = len(xlist)
for i in range(len(xlist)):
    

    yp = ylist[i]*FY/(FY+zlist[i])
    zp = xlist[i]*zlist[i]/(FX+zlist[i])

    
    
    coords_3d.append((zlist[i]-((PITCH_LENGTH-2*CREASE_LENGTH)/2), yp, zp,1,bouncing_pt[i]))

    
    
    
    
    
    
    
    
    
    
    

quadraticReg = quadFit.quadraticRegression(coords_3d, after_bounce_linear = AFTER_BOUNCE_LINEAR)
linearReg = temp1.quadraticRegression(coords_3d)


for idx in range(1,300):
    coords_3d.append(((coords_3d[num_detected_points-1][0] + idx),0,0,0,0))




final_coords_3d = []


fnum = 0


for idx in range(num_detected_points):
    rate(50)
    final_coords_3d.append((coords_3d[idx][0],quadraticReg[idx], linearReg[idx]))
    
    if coords_3d[idx][0] > -400:
        balls.append(sphere(pos=(coords_3d[idx][0],quadraticReg[idx], linearReg[idx]), radius=BALL_RADIUS, color=(0.52,0.15,0.19)))
        
        
        if idx > 0:
            displacement = (final_coords_3d[idx][0]-final_coords_3d[idx-1][0], final_coords_3d[idx][1]-final_coords_3d[idx-1][1], final_coords_3d[idx][2]-final_coords_3d[idx-1][2])
            cylinder(pos=(final_coords_3d[idx-1][0], final_coords_3d[idx-1][1], final_coords_3d[idx-1][2]), axis=displacement, radius=BALL_RADIUS, color=(0.52,0.15,0.19), opacity=0.3)
    if fnum < 900:
        im = ImageGrab.grab((0,40,1280,760))
        num = '00'+repr(fnum)
        print "Saving num: "+str(num[-3:])
        im.save('video/img-'+num[-3:]+'.png')
        fnum += 1

for idx in range(num_detected_points, len(coords_3d)):
    final_coords_3d.append((coords_3d[idx][0],quadraticReg[idx], linearReg[idx]))


STEP_SIZE = 20
for idx in range(num_detected_points, len(coords_3d),20):
    rate(50)
    
    if coords_3d[idx][0] <= PITCH_LENGTH*1.2/2:
        balls.append(sphere(pos=(coords_3d[idx][0],quadraticReg[idx], linearReg[idx]), radius=BALL_RADIUS, color=color.blue, opacity=0.8))
        
        
        if idx-STEP_SIZE > 0 and idx > num_detected_points:
            displacement = (final_coords_3d[idx][0]-final_coords_3d[idx-STEP_SIZE][0], final_coords_3d[idx][1]-final_coords_3d[idx-STEP_SIZE][1], final_coords_3d[idx][2]-final_coords_3d[idx-STEP_SIZE][2])
            cylinder(pos=(final_coords_3d[idx-STEP_SIZE][0], final_coords_3d[idx-STEP_SIZE][1], final_coords_3d[idx-STEP_SIZE][2]), axis=displacement, radius=BALL_RADIUS, color=color.blue, opacity=0.3)
    if fnum < 900:
        im = ImageGrab.grab((0,40,1280,760))
        num = '00'+repr(fnum)
        print "Saving num: "+str(num[-3:])
        im.save('video/img-'+num[-3:]+'.png')
        fnum += 1


speed_list = []

average_speed = 0.0

average_length = 0


for idx in range(num_detected_points):
    if idx == 0:
        speed_list.append(0)
    else:
        displacement = vector(final_coords_3d[idx][0]-final_coords_3d[idx-1][0], final_coords_3d[idx][1]-final_coords_3d[idx-1][1], final_coords_3d[idx][2]-final_coords_3d[idx-1][2])
        time = float(frames_list[idx]-frames_list[idx-1])/FPS
        speed = (mag(displacement)/time)*3.6/100
        speed_list.append(speed)
        if idx >= bouncing_pt_idx or bouncing_pt_idx == 0:
            average_speed += speed
            average_length += 1

    
    
    
    
    
    

average_speed = average_speed*0.9/(average_length)

print "Speed of delivery: {:.3f} km/h".format(average_speed)


""" Umpiring decisions below """

def get_nearest_ball_params(near_crease=False):
    """
        Returns the index of the ball closest to wicket, absolute difference in position
        of nearest ball, and index of the last ball just before the wicket
    """
    near_wicket_idx = 0
    before_wicket_idx = num_detected_points-1
    min_diff = 1000000

    
    dist = PITCH_LENGTH/2
    if near_crease:
        dist = PITCH_LENGTH/2-122

    for i in range(len(final_coords_3d)):
        diff = abs(dist-final_coords_3d[i][0])
        if diff < min_diff:
            min_diff = diff
            near_wicket_idx = i
        if dist-final_coords_3d[i][0] < 0 and before_wicket_idx == num_detected_points-1:
            before_wicket_idx = i-1
    return near_wicket_idx, min_diff, before_wicket_idx

def get_nearest_ball_coords(idx, min_diff, before_wicket_idx, near_crease=False):
    """
        Returns the y and z coordinates of the ball closest to the wicket
    """

    
    dist = PITCH_LENGTH/2
    if near_crease:
        dist = PITCH_LENGTH/2-122

    
    if abs(min_diff) <= 1:
        y = final_coords_3d[idx][1]
        z = final_coords_3d[idx][2]
        return y, z
    else:
        
        y2 = final_coords_3d[before_wicket_idx+1][1]
        y1 = final_coords_3d[before_wicket_idx][1]
        z2 = final_coords_3d[before_wicket_idx+1][2]
        z1 = final_coords_3d[before_wicket_idx][2]
        x2 = final_coords_3d[before_wicket_idx+1][0]
        x1 = final_coords_3d[before_wicket_idx][0]

        slopey = (y2-y1)/(x2-x1)
        slopez = (z2-z1)/(x2-x1)
        ynew = y1 + slopey*(dist-x1)
        znew = z1 + slopez*(dist-x1)

        

        return ynew, znew


decision = {}


def check_lbw():
    """
        Checks if the ball delivery would result in lbw
    """
    near_wicket_idx, min_diff, before_wicket_idx = get_nearest_ball_params()

    

    
    
    if bouncing_pt_idx != -1 and final_coords_3d[bouncing_pt_idx][2] <= WICKET_WIDTH/2:
        if final_coords_3d[bouncing_pt_idx][2] >= -WICKET_WIDTH/2:
            decision['pitching'] = "INSIDE"
            print "PITCHING: INSIDE IMACT ZONE"
        else:
            decision['pitching'] = "OUTSIDE OFF"
            print "PITCHING: OUTSIDE OFF"
        
        if final_coords_3d[num_detected_points-1][2] >= -(WICKET_WIDTH/2+BALL_RADIUS) and final_coords_3d[num_detected_points-1][2] <= (WICKET_WIDTH/2+BALL_RADIUS):
            decision['impact'] = "IN-LINE"
            print "IMPACT: IN-LINE"
            return check_nearest_coord(near_wicket_idx, min_diff, before_wicket_idx)
        else:
            decision['impact'] = "OUTSIDE"
            print "IMPACT: OUTSIDE"
            return False
    
    elif bouncing_pt_idx == -1:
        decision['pitching'] = "DID NOT BOUNCE"
        print "PITCHING: DID NOT BOUNCE"
        if final_coords_3d[num_detected_points-1][2] >= -(WICKET_WIDTH/2+BALL_RADIUS) and final_coords_3d[num_detected_points-1][2] <= (WICKET_WIDTH/2+BALL_RADIUS):
            decision['impact'] = "IN-LINE"
            print "IMPACT: IN-LINE"
            return check_nearest_coord(near_wicket_idx, min_diff, before_wicket_idx)
        else:
            decision['impact'] = "OUTSIDE"
            print "IMPACT: OUTSIDE"
            return False
    
    else:
        decision['pitching'] = "OUTSIDE LEG"
        decision['impact'] = "OUTSIDE"
        print "PITCHING: OUTSIDE LEG"
        return False

def check_nearest_coord(idx, min_diff, before_wicket_idx):
    """
        Checks if the ball hits the wicket
    """
    
    y, z = get_nearest_ball_coords(idx, min_diff, before_wicket_idx)

    if y <= (WICKET_HEIGHT+BALL_RADIUS) and z >= -(WICKET_WIDTH/2+BALL_RADIUS) and z <= WICKET_WIDTH/2+BALL_RADIUS:
        return True
    else:
        return False

if check_lbw():
    decision['lbw'] = "OUT"
    decision['wickets'] = "HITTING"
    print "WICKETS: HITTING"
    
else:
    decision['lbw'] = "NOT OUT"
    decision['wickets'] = "NOT HITTING"
    print "WICKETS: NOT HITTING"
    


def check_wide():
    """
        Checks if the ball delivery would result in wide decision
    """
    
    near_wicket_idx, min_diff, before_wicket_idx = get_nearest_ball_params(near_crease=True)
    y, z = get_nearest_ball_coords(near_wicket_idx, min_diff, before_wicket_idx, near_crease=True)

    
    
    

    
    if y >= BATSMAN_HEIGHT:
        return True

    if z <= -(WIDE_WIDTH/2-LINE_WIDTH-BALL_RADIUS) or z >= (WICKET_WIDTH+BALL_RADIUS):
        return True
    else:
        return False

if check_wide():
    print "\nWIDE DECISION: WIDE"
    decision['wide'] = "WIDE"
else:
    print "\nWIDE DECISION: NOT WIDE"
    decision['wide'] = "NOT WIDE"


def check_bouncer():
    """
        Checks if the ball delivery would result in bouncer
    """
    
    near_wicket_idx, min_diff, before_wicket_idx = get_nearest_ball_params(near_crease=True)
    y, z = get_nearest_ball_coords(near_wicket_idx, min_diff, before_wicket_idx, near_crease=True)

    
    
    

    
    if bouncing_pt_idx == -1:
        return False

    if (y > BATSMAN_HEIGHT*0.92):
        return True
    else:
        return False

if check_bouncer():
    decision['bouncer'] = "BOUNCER"
    print "\nBOUNCER DECISION: BOUNCER"
else:
    decision['bouncer'] = "NOT A BOUNCER"
    print "\nBOUNCER DECISION: NOT A BOUNCER"



def check_noball():
    """
        Checks if the ball delivery would result in a no-ball
    """
    
    near_wicket_idx, min_diff, before_wicket_idx = get_nearest_ball_params(near_crease=True)
    y, z = get_nearest_ball_coords(near_wicket_idx, min_diff, before_wicket_idx, near_crease=True)

    
    if bouncing_pt_idx != -1:
        return False

    
    if bouncing_pt_idx == num_detected_points-1:
        return False

    if (y >= BATSMAN_HEIGHT*0.62):
        return True
    else:
        return False

if check_noball():
    decision['noball'] = "NO BALL"
    print "\nNO BALL DECISION: NO BALL"
else:
    decision['noball'] = "NOT A NO BALL"
    print "\nNO BALL DECISION: NOT A NO BALL"


decision['lbwheading'] = "LBW DECISION"
decision['wicketsheading'] = "WICKETS"
decision['impactheading'] = "IMPACT"
decision['pitchingheading'] = "PITCHING"
decision['wideheading'] = "WIDE DECISION"
decision['noballheading'] = "NO BALL DECISION"
decision['bouncerheading'] = "BOUNCER DECISION"
decision['speedheading'] = "SPEED"
decision['speed'] = "{:.2f} KM/H".format(average_speed)


max_len = 0
for key in decision:
    if len(decision[key]) > max_len:
        max_len = len(decision[key])
for key in decision:
    val = ''
    for i in range((max_len-len(decision[key]))/2):
        val += ' '
    val += decision[key]
    for i in range((max_len-len(decision[key]))/2):
        val += ' '
    
    if len(val) < max_len:
        val += ' '
    decision[key] = val

TEXT_SIZE = 12
TEXT_FONT = 'sans'


if SHOW_LABELS:
    
    

    display3 = label(pos=(-PITCH_LENGTH*1.5/2,700,-1000), text=decision['wicketsheading'], background=color.blue, opacity=0.4, box=False, height=TEXT_SIZE, font=TEXT_FONT)
    display4 = label(pos=(-PITCH_LENGTH*1.5/2,600,-1000), text=decision['wickets'], background=color.red, opacity=0.4, box=False, height=TEXT_SIZE, font=TEXT_FONT)

    display5 = label(pos=(-PITCH_LENGTH*1.5/2,450,-1000), text=decision['impactheading'], background=color.blue, opacity=0.4, box=False, height=TEXT_SIZE, font=TEXT_FONT)
    display6 = label(pos=(-PITCH_LENGTH*1.5/2,350,-1000), text=decision['impact'], background=color.red, opacity=0.4, box=False, height=TEXT_SIZE, font=TEXT_FONT)

    display7 = label(pos=(-PITCH_LENGTH*1.5/2,200,-1000), text=decision['pitchingheading'], background=color.blue, opacity=0.4, box=False, height=TEXT_SIZE, font=TEXT_FONT)
    display8 = label(pos=(-PITCH_LENGTH*1.5/2,100,-1000), text=decision['pitching'], background=color.red, opacity=0.4, box=False, height=TEXT_SIZE, font=TEXT_FONT)

    display9 = label(pos=(-PITCH_LENGTH*1.5/2,700,1000), text=decision['wideheading'], background=color.blue, opacity=0.4, box=False, height=TEXT_SIZE, font=TEXT_FONT)
    display10 = label(pos=(-PITCH_LENGTH*1.5/2,600,1000), text=decision['wide'], background=color.red, opacity=0.4, box=False, height=TEXT_SIZE, font=TEXT_FONT)

    display11 = label(pos=(-PITCH_LENGTH*1.5/2,450,1000), text=decision['noballheading'], background=color.blue, opacity=0.4, box=False, height=TEXT_SIZE, font=TEXT_FONT)
    display12 = label(pos=(-PITCH_LENGTH*1.5/2,350,1000), text=decision['noball'], background=color.red, opacity=0.4, box=False, height=TEXT_SIZE, font=TEXT_FONT)

    display13 = label(pos=(-PITCH_LENGTH*1.5/2,200,1000), text=decision['bouncerheading'], background=color.blue, opacity=0.4, box=False, height=TEXT_SIZE, font=TEXT_FONT)
    display14 = label(pos=(-PITCH_LENGTH*1.5/2,100,1000), text=decision['bouncer'], background=color.red, opacity=0.4, box=False, height=TEXT_SIZE, font=TEXT_FONT)

    display15 = label(pos=(-PITCH_LENGTH*1.5/2,700,0), text=decision['speedheading'], background=color.blue, opacity=0.4, box=False, height=TEXT_SIZE, font=TEXT_FONT)
    display16 = label(pos=(-PITCH_LENGTH*1.5/2,600,0), text=decision['speed'], background=color.red, opacity=0.4, box=False, height=TEXT_SIZE, font=TEXT_FONT)


im = ImageGrab.grab((0,40,1280,760))
num = '00'+repr(fnum)
print "Saving num: "+str(num[-3:])
im.save('video/img-'+num[-3:]+'.png')
fnum += 1
call("ffmpeg -r 30 -i video/img-%3d.png -vcodec libx264 -vf format=yuv420p -y video/movie.mp4")
print ("\n Movie made: movie.mp4")