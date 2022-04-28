from visual import *
import quadFit
import temp1

rlist = []
xlist = []
ylist = []
zlist = []
bouncing_pt = []
START_RADIUS = 0.0
END_RADIUS = 0.0

PITCH_WIDTH = 305.0
PITCH_LENGTH = 2012.0
PITCH_THICKNESS = 10
CREASE_LENGTH = 122
XWASTE = 405.4

WICKET_HEIGHT = 71.1
WICKET_WIDTH = 22.86
STUMP_WIDTH = 4.5

FY = 1120.0

SCALE = [1, 0.5, PITCH_LENGTH - (2*CREASE_LENGTH)]

with open('coordinates.txt') as coord_file:


    for i,row in enumerate(coord_file):
        x,y,r,frame_no,is_bouncing_pt,r_new,y_new= row.split()
        r_new = float(r_new)
        x = ((float(x)-XWASTE)*305/500)-152
        y = (720.0-float(y_new))*SCALE[1]
        bouncing_pt.append(int(is_bouncing_pt))
        
        xlist.append(x)
        ylist.append(y)
        if i == 0:
            START_RADIUS = r_new
        END_RADIUS = r_new
        rlist.append(r_new)


START_RADIUS = 16
END_RADIUS = 3.0

for i,radius in enumerate(rlist):   
    z = (START_RADIUS-radius)/(START_RADIUS-END_RADIUS)
    zlist.append(z*SCALE[2])
    


scene1 = display(title="Automated Cricket Umpiring - HawkEye", width=1280, height=720, range=10, background=(0.2,0.2,0.2), center=(0,30,30))

floor = box(pos=(0,0,0), size=(PITCH_LENGTH*1.2,PITCH_THICKNESS*1.2,PITCH_WIDTH), material=materials.unshaded, color=(0.97,0.94,0.6))
floor_outer = box(pos=(0,0,0), size=(PITCH_LENGTH*1.25,PITCH_THICKNESS,PITCH_WIDTH*2), material=materials.unshaded, color=(0.2,0.7,0.27))
floor_impact = box(pos=(0,0,0), size=(PITCH_LENGTH,PITCH_THICKNESS*1.3,WICKET_WIDTH), material=materials.unshaded, color=(0.63,0.57,0.93), opacity=0.8)


batting_wicket1 = box(pos=(PITCH_LENGTH/2,WICKET_HEIGHT/2,-(WICKET_WIDTH/2-STUMP_WIDTH/2)), size=(5,71.1,STUMP_WIDTH), color=color.white)
batting_wicket2 = box(pos=(PITCH_LENGTH/2,WICKET_HEIGHT/2,0), size=(5,71.1,STUMP_WIDTH), color=color.white)
batting_wicket3 = box(pos=(PITCH_LENGTH/2,WICKET_HEIGHT/2,(WICKET_WIDTH/2-STUMP_WIDTH/2)), size=(5,71.1,STUMP_WIDTH), color=color.white)
line1 = box(pos=(PITCH_LENGTH/2,PITCH_THICKNESS/2,0), size=(10,5,264), color=color.white)
line2 = box(pos=(PITCH_LENGTH/2,PITCH_THICKNESS/2,132), size=(244,5,10), color=color.white)
line3 = box(pos=(PITCH_LENGTH/2,PITCH_THICKNESS/2,-132), size=(244,5,10), color=color.white)
line4 = box(pos=(PITCH_LENGTH/2-122,PITCH_THICKNESS/2,0), size=(10,5,366), color=color.white)


bowling_wicket1 = box(pos=(-PITCH_LENGTH/2,WICKET_HEIGHT/2,-(WICKET_WIDTH/2-STUMP_WIDTH/2)), size=(5,71.1,STUMP_WIDTH), color=color.white)
bowling_wicket2 = box(pos=(-PITCH_LENGTH/2,WICKET_HEIGHT/2,0), size=(5,71.1,STUMP_WIDTH), color=color.white)
bowling_wicket3 = box(pos=(-PITCH_LENGTH/2,WICKET_HEIGHT/2,(WICKET_WIDTH/2-STUMP_WIDTH/2)), size=(5,71.1,STUMP_WIDTH), color=color.white)
line1 = box(pos=(-PITCH_LENGTH/2,PITCH_THICKNESS/2,0), size=(10,5,264), color=color.white)
line2 = box(pos=(-PITCH_LENGTH/2,PITCH_THICKNESS/2,132), size=(244,5,10), color=color.white)
line3 = box(pos=(-PITCH_LENGTH/2,PITCH_THICKNESS/2,-132), size=(244,5,10), color=color.white)
line4 = box(pos=(-PITCH_LENGTH/2+122,PITCH_THICKNESS/2,0), size=(10,5,366), color=color.white)

balls = []
FX = 250

yp = ylist[0]*FY/(FY+zlist[0])

zp = xlist[0]*zlist[0]/(FX+zlist[0])


coords_3d = []








for i in range(1,len(xlist)):
    

    
    
    coords_3d.append((zlist[i-1]-((PITCH_LENGTH-2*CREASE_LENGTH)/2), yp, zp,1,bouncing_pt[i-1]))
    
    
    
    
    
    
    
    
    
    
    
    yp = ylist[i]*FY/(FY+zlist[i])
    zp = xlist[i]*zlist[i]/(FX+zlist[i])
    
    
    
    
    
    
    
    
    
    

    
    
coords_3d.append((zlist[i-1]-((PITCH_LENGTH-2*CREASE_LENGTH)/2), yp, zp,1,bouncing_pt[i-1]))


quadraticReg = quadFit.quadraticRegression(coords_3d)
linearReg = temp1.quadraticRegression(coords_3d)
for idx in range(1,10):
    coords_3d.append(((coords_3d[i-1][0] + idx*30),0,0,0,0))


for idx in range(1,i+1):
    

    
    if coords_3d[idx-1][0] > -400:
        balls.append(sphere(pos=(coords_3d[idx-1][0],quadraticReg[idx-1], linearReg[idx-1]), radius=6, color=(0.52,0.15,0.19)))
        
for idx in range(i+1, len(coords_3d) + 1):
    

    
    if coords_3d[idx-1][0] > -400:
        balls.append(sphere(pos=(coords_3d[idx-1][0],quadraticReg[idx-1], linearReg[idx-1]), radius=6, color=color.blue))
        



coord_file.close()