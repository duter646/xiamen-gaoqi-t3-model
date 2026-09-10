"""Reference-constrained T3 revision. Run with numpy/Pillow, dimensions in metres.
Plan coordinates: OSM; vertical dimensions/window modules: photo estimates.
Read EVIDENCE.md before treating this as an as-built reconstruction.
"""
from pathlib import Path
SOURCE=Path(__file__).resolve().parent/'geometry_source.py'
original=SOURCE.read_text(encoding='utf-8')
# Reuse only the geometry/material utilities, never the v1 building.
exec(compile(original.split('# Site and frontage.')[0],str(SOURCE),'exec'))
mapping=json.loads((ROOT/'map-geometry.json').read_text(encoding='utf-8'))
METAL=material('Satin silver honeycomb cladding',[.56,.59,.58],.72,.34)
PUNCHED_GLASS=material('Dark reflective clerestory glazing',[.06,.095,.105],.35,.23)
TAN=material('West hall terracotta seating',[.52,.28,.18],.05,.6)
SEC_FLOOR=material('Security dark grey tile',[.19,.205,.20],.2,.3)
LIME=material('Airport lime wayfinding',[.30,.52,.065],0,.65)
RED=material('Airport red lettering',[.6,.025,.025],.12,.4)
materials[WHITE]['pbrMetallicRoughness'].update(baseColorFactor=[.83,.83,.74,1],metallicFactor=.08,roughnessFactor=.65)
materials[GLASS]['pbrMetallicRoughness']['baseColorFactor']=[.18,.30,.32,.52]
X0,X1=-104.5,147.5
C=(X0+X1)/2
F2,F3=6.3,12.1
FG=F3  # Airline Level 3 diagram: gate concourse belongs to the security level.
RIDGE_Z=38.0
def roof_z(d,side):return RIDGE_Z+side*d*(26 if side<0 else 58)/54
def roof_y(y,d,side):return y

def beam(g,m,a,b,w,h):
    a=np.array(a,float);b=np.array(b,float);d=b-a;d/=np.linalg.norm(d)
    helper=np.array([0,1,0]) if abs(d[1])<.95 else np.array([0,0,1])
    u=np.cross(d,helper);u/=np.linalg.norm(u);v=np.cross(u,d)
    pts=[p+sx*w/2*u+sy*h/2*v for p in [a,b] for sx,sy in [(-1,-1),(1,-1),(1,1),(-1,1)]]
    mesh(g,m,pts,BOX_F)

def curved_rib(x,side):
    # Continuous cubic curve: steep drop at the ridge, flattening toward the eave.
    # Photo-constrained, not a claim that the original member is a circular arc.
    control=np.array([[0,40.3],[12,26.0],[30,21.0],[54,17.8]])
    pts=[];normals=[]
    for t in np.linspace(0,1,65):
        p=(1-t)**3*control[0]+3*(1-t)**2*t*control[1]+3*(1-t)*t*t*control[2]+t**3*control[3]
        d=3*(1-t)**2*(control[1]-control[0])+6*(1-t)*t*(control[2]-control[1])+3*t*t*(control[3]-control[2])
        normal=np.array([-d[1],d[0]])/np.linalg.norm(d)
        pts.append(p);normals.append(normal)
    vv=[]
    for p,n in zip(pts,normals):
        for dx,dy in [(-.40,-.56),(.40,-.56),(.40,.56),(-.40,.56)]:
            q=p+n*dy;vv.append((x+dx,roof_y(q[1],q[0],side),roof_z(q[0],side)))
    ff=[]
    for j in range(64):
        for k in range(4):
            a=4*j+k;b=4*j+(k+1)%4;c=b+4;d=a+4
            ff.extend([(a,b,c),(a,c,d)])
    ff.extend([(0,2,1),(0,3,2),(256,257,258),(256,258,259)])
    mesh('Roof_ContinuousCurvedRibs',WHITE,vv,ff)
    # A second shallow edge defines the visible concrete member's arris.
    for face in [-.405,.405]:
        path('Roof_RibEdge',STONE,[(x+face,roof_y(p[1]+n[1]*.54,p[0]+n[0]*.54,side),roof_z(p[0]+n[0]*.54,side)) for p,n in zip(pts,normals)],.022,5)

def wallhole(g,m,x,y,z,pitch,height,width,wh,octagon=True):
    # A through-aperture with a thick reveal. Glass occupies the aperture only.
    n=8 if octagon else 40
    angles=np.linspace(0,2*math.pi,n,endpoint=False)+(math.pi/8 if octagon else 0)
    if octagon:
        w,h,c=width/2,wh/2,width*.20
        inner=np.array([(w,h-c),(w-c,h),(-w+c,h),(-w,h-c),(-w,-h+c),(-w+c,-h),(w-c,-h),(w,-h+c)])
    else:inner=np.array([(width/2*math.cos(t),wh/2*math.sin(t)) for t in angles])
    outer=[]
    for xx,yy in inner:
        scale=min(pitch/2/max(abs(xx),1e-8),height/2/max(abs(yy),1e-8));outer.append((xx*scale,yy*scale))
    # Add rectangle corner vertices explicitly: no gaps between modules.
    for i in range(n):
        j=(i+1)%n; a=inner[i];b=inner[j];oa=outer[i];ob=outer[j]
        poly=[a,b,ob]
        for corner in [(pitch/2,height/2),(-pitch/2,height/2),(-pitch/2,-height/2),(pitch/2,-height/2)]:
            t0=math.atan2(oa[1],oa[0]);t1=math.atan2(ob[1],ob[0]);tc=math.atan2(corner[1],corner[0]);span=(t1-t0)%(2*math.pi)
            if 1e-6<(tc-t0)%(2*math.pi)<span-1e-6:poly.append(corner)
        poly.append(oa)
        vv=[(x+p[0],y+p[1],z) for p in poly]
        mesh(g,m,vv,[(0,k,k+1) for k in range(1,len(vv)-1)])
        mesh(g,STONE,[(x+a[0],y+a[1],z),(x+b[0],y+b[1],z),(x+b[0],y+b[1],z-.25),(x+a[0],y+a[1],z-.25)],[(0,1,2),(0,2,3)])
    vv=[(x+p[0],y+p[1],z-.13) for p in inner]
    mesh(g,PUNCHED_GLASS if octagon else GLASS,vv,[(0,k,k+1) for k in range(1,n-1)])
    for a,b in zip(inner,np.roll(inner,-1,axis=0)):
        beam(g,FRAME,(x+a[0],y+a[1],z+.02),(x+b[0],y+b[1],z+.02),.07,.07)
    box(g,FRAME,(x,y-(wh*.05 if octagon else .1),z+.03),(width,.055,.07))
    if not octagon:box(g,FRAME,(x,y-wh/4-.05,z+.03),(.055,wh/2-.1,.07))

def roofstrip(z0,y0,z1,y1):
    g='Roof_MainShell'
    for x in np.arange(X0,X1,3):
        mesh(g,CEILING,[(x,y0,z0),(min(x+3,X1),y0,z0),(min(x+3,X1),y1,z1),(x,y1,z1)],[(0,1,2),(0,2,3)])
        beam(g,FRAME,(x,y0+.03,z0),(x,y1+.03,z1),.035,.035)

def curtain(g,x0,x1,z,y0,y1):
    box(g,GLASS,((x0+x1)/2,(y0+y1)/2,z),(x1-x0,y1-y0,.1))
    for x in np.arange(x0,x1+.01,3):box(g,WHITE,(x,(y0+y1)/2,z),(.12,y1-y0,.18))
    for y in np.arange(y0,y1,.95):box(g,FRAME,((x0+x1)/2,y,z),(x1-x0,.065,.16))

def escalator(x,z0,z1,y0,y1):
    g='Interior_Escalators'
    for dx in [-1.15,1.15]:
        a=np.array([x+dx,y0,z0]);b=np.array([x+dx,y1,z1])
        beam(g,DARK,a-[0,.25,0],b-[0,.25,0],1.85,.65)
        for t in np.linspace(0,1,38):
            p=a*(1-t)+b*t;box(g,FRAME,p,(1.25,.10,abs(z1-z0)/37+.04))
            box(g,YELLOW,p+[0,.055,.06],(1.2,.015,.04))
        for side in [-.8,.8]:
            beam(g,GLASS,a+[side,.45,0],b+[side,.45,0],.08,.9)
            rod(g,DARK,a+[side,.95,0],b+[side,.95,0],.07,8)

def seats(x,z,y=F2,mat=SEAT,count=5):
    g='Interior_Seating'
    box(g,FRAME,(x,y+.34,z),(count*.62,.09,.12))
    for dx in [-count*.23,count*.23]:
        rod(g,FRAME,(x+dx,y+.04,z-.28),(x+dx,y+.36,z),.035,8)
        rod(g,FRAME,(x+dx,y+.04,z+.28),(x+dx,y+.36,z),.035,8)
    for j in range(count):
        xx=x+(j-(count-1)/2)*.62
        profile=[(.25,.48),(.12,.44),(-.13,.44),(-.25,.5),(-.28,.66),(-.34,.92),(-.39,1.03)]
        vv=[(xx+dx,y+yy,z+zz) for zz,yy in profile for dx in [-.275,.275]]
        mesh(g,mat,vv,[(2*k,2*k+1,2*k+3) for k in range(6)]+[(2*k,2*k+3,2*k+2) for k in range(6)])
        for dx in [-.275,.275]:path(g,FRAME,[(xx+dx,y+yy,z+zz) for zz,yy in profile],.015,5)
        for dx in [-.3,.3]:rod(g,FRAME,(xx+dx,y+.57,z+.12),(xx+dx,y+.72,z-.22),.025,6)

# The apron is context only; streets/landscape are deliberately plain.
box('Site_Apron',CONCRETE,(0,-.45,-62),(960,.65,150))
box('Site_Landside',ROAD,(C,-.45,124),(470,.65,52))
box('Structure_GroundSlab',STONE,(C,-.1,42),(252,.3,108))
box('Structure_DepartureFloor_Level2',FLOOR,(C,F2-.22,54),(252,.44,84))
box('Structure_ConcourseFloor_Level3',FLOOR,(-1,FG-.22,0),(767,.44,25))
for x in np.arange(X0+6,X1,12):
    for z in [18,42,66,90]:
        rod('Structure_Columns',WHITE,(x,0,z),(x,19 if z in [18,90] else 25,z),.53,14)
        rod('Interior_ColumnBases',FRAME,(x,F2,z),(x,F2+.9,z),.56,14)
        rod('Interior_ColumnVents',DARK,(x,F2+2.35,z),(x,F2+2.65,z),.545,14)
    box('Interior_FloorGrid',TRIM,(x,F2+.012,54),(.045,.02,84))
for z in np.arange(12,96,6):box('Interior_FloorGrid',TRIM,(C,F2+.012,z),(252,.02,.045))

# Stepped terraces: ridge shifted toward apron as in the supplied aerial view. Heights are photo estimates.
profile=[(0,36.8),(8,32.5),(8,27.8),(26,23.5),(26,19.5),(54,17.4),(54,12.8)]
for side in [-1,1]:
    for d0,y0,d1,y1 in [(0,36.8,8,32.5),(8,27.8,26,23.5),(26,19.5,54,17.4)]:
        roofstrip(roof_z(d0,side),roof_y(y0,d0,side),roof_z(d1,side),roof_y(y1,d1,side))
    for dist,lo,hi,ww,hh in [(8,27.8,32.5,1.85,3.7),(26,19.5,23.5,1.85,3.0),(54,12.8,17.4,1.85,3.5)]:
        if side==-1 and dist==54:continue  # no wall between hall and gate concourse
        z=roof_z(dist,side);lo=roof_y(lo,dist,side);hi=roof_y(hi,dist,side)
        # Interior connection openings remain visible with the roof enabled.
        openings=[(-48.5,-38),(-29.5,-20.5),(26,35),(105.5,114.5),(129.5,138.5)] if side==-1 and dist==54 else []
        for x in np.arange(X0+1.5,X1,3):
            if any(a<x+1.5 and b>x-1.5 for a,b in openings):
                box('Facade_ConcourseConnectionHeaders',WHITE,(x,(F3+3.1+hi)/2,z),(3,hi-F3-3.1,.22))
            else:wallhole('Roof_Clerestory',WHITE,x,(lo+hi)/2,z,3,hi-lo,ww,hh)
        for y in [lo,hi]:
            if y==lo and openings:
                # Snap band gaps to the same complete facade modules.
                modules=[x for x in np.arange(X0+1.5,X1,3) if not any(a<x+1.5 and b>x-1.5 for a,b in openings)]
                for x in modules:box('Roof_ClerestoryBands',WHITE,(x,y,z),(3,.5,.5))
            else:box('Roof_ClerestoryBands',WHITE,(C,y,z),(252,.5,.5))
    for x in np.arange(X0,X1+.1,12):
        curved_rib(x,side)
        for dist,lo,hi in [(8,27.8,32.5),(26,19.5,23.5)]:
            beam('Roof_MassiveRibs',WHITE,(x,roof_y(lo,dist,side),roof_z(dist,side)),(x,roof_y(hi+.4,dist,side),roof_z(dist,side)),.65,.7)
    for x in np.arange(X0+3,X1,6):
        vy=roof_y(33.1,7,side);vz=roof_z(7,side)
        rod('Roof_Ventilators',DARK,(x,vy,vz),(x,vy+.5,vz),.42,12)
        rod('Roof_Ventilators',WHITE,(x,vy+.5,vz),(x,vy+.67,vz),.75,18)
box('Roof_Ridge_BoxWeb',WHITE,(C,40.0,RIDGE_Z),(254,1.8,1.25))
for y in [39.02,40.98]:box('Roof_Ridge_Caps',WHITE,(C,y,RIDGE_Z),(254,.18,1.6))
for side in [-1,1]:
    for x in np.arange(X0+1.5,X1,3):
        box('Roof_Ridge_RecessedPanels',STONE,(x,40,RIDGE_Z+side*.631),(2.87,1.37,.025))
        box('Roof_Ridge_Stiffeners',WHITE,(x+1.5,40,RIDGE_Z+side*.68),(.12,1.75,.13))
for x in np.arange(X0,X1+.1,12):beam('Roof_Ridge',WHITE,(x,36.8,RIDGE_Z),(x,40,RIDGE_Z),.65,.7)

# End walls follow the stepped section, with glazing and substantial mullions.
for x in [X0,X1]:
    for side in [-1,1]:
        pp=[(x,F2,RIDGE_Z),(x,F2,roof_z(54,side))]+[(x,roof_y(y,d,side),roof_z(d,side)) for d,y in reversed(profile)]
        mesh('Facade_EndGlazing',PUNCHED_GLASS,pp,[(0,j,j+1) for j in range(1,len(pp)-1)])
        for d in np.arange(0,55,3):
            height=36.8-d*4.3/8 if d<8 else (27.8-(d-8)*4.3/18 if d<26 else 19.5-(d-26)*2.1/28)
            beam('Facade_EndGrid',WHITE,(x,F2,roof_z(d,side)),(x,roof_y(height,d,side),roof_z(d,side)),.18,.18)
        for y in np.arange(F2,36,2.3):
            for d0,d1,h in [(0,8,32.5),(8,26,23.5),(26,54,17.4)]:
                if y<h:beam('Facade_EndGrid',FRAME,(x,roof_y(y,d0,side),roof_z(d0,side)),(x,roof_y(y,d1,side),roof_z(d1,side)),.1,.1)

# Landside facade, elevated departure road, and the thick suspended canopy.
curtain('Facade_Entrance',X0,X1,96,.2,12.7)
for x in np.arange(X0+1.5,X1,6):
    box('Facade_StonePiers',WHITE,(x,9.3,96.15),(2.0,6,.42))
    for y in [7.7,9.2,10.7]:box('Facade_StonePiers',STONE,(x,y,96.38),(2,.025,.015))
box('Structure_KerbsideDeck',STONE,(C,F2-.5,108),(292,.65,25))
box('Site_DepartureRoad',ROAD,(C,F2-.15,112),(292,.07,13))
for x in np.arange(X0-18,X1+18,6):
    box('Site_RoadLines',WHITE,(x,F2-.105,110),(3,.016,.12))
    box('Site_Bollards',FRAME,(x,F2+.42,101.5),(.12,.9,.12))
for x in np.arange(X0,X1+.1,12):
    beam('Roof_Canopy',WHITE,(x,12.3,96),(x,13.1,107),.52,1.5)
    beam('Roof_Canopy',WHITE,(x,12.5,102),(x,26,102),.25,.25)
    for dx in [-5.7,5.7]:rod('Roof_CanopyCables',FRAME,(x,22.5,102),(x+dx,12.9,105),.025,6)
    box('Roof_Canopy',WHITE,(x+5.8,12.25,101.5),(11.4,.24,11))
for i,x in enumerate(np.linspace(X0+15,X1-15,7)):
    box('Facade_EntranceSigns',LIME,(x,9.5,96.55),(5.6,.7,.12))
    sign('Facade_EntranceSigns',2 if i<3 else 3,(x,9.5,96.65),4.5,.55)

# Capsule section of the long metallic concourse, directly joined to the hall.
bridge_roots=[p[0] for way in mapping['ways'] if way['tags'].get('aeroway')=='jet_bridge' for p in way['points'] if -15<p[1]<-10 and p[0]<383]
for side in [-1,1]:
    z=side*12.5
    for x in np.arange(-382.5,383,4.5):
        if side==1 and X0<x<X1:continue
        nearby=[r for r in bridge_roots if abs(x-r)<4.0] if side==-1 else []
        if nearby:
            r=nearby[0]
            box('Facade_GateDoorHeaders',METAL,(x,10.85,z),(4.5,.5,.15))
            for a,b in [(x-2.25,min(x+2.25,r-1.85)),(max(x-2.25,r+1.85),x+2.25)]:
                if b>a:box('Facade_GateDoorPanels',METAL,((a+b)/2,8.8,z),(b-a,3.6,.15))
            for edge in [r-1.85,r+1.85]:
                if x-2.25<edge<x+2.25:box('Facade_GateDoorFrames',FRAME,(edge,8.5,z),(.12,4.2,.2))
            continue
        wallhole('Facade_ConcoursePortholes',METAL,x,9.0,z,4.5,4.2,3.4,3.4,False)
        box('Facade_CladdingSeams',DARK,(x+2.25,9,z+side*.015),(.018,4.2,.02))
    for t0,t1 in zip(np.linspace(0,math.pi/2,10),np.linspace(0,math.pi/2,10)[1:]):
        for top in [False,True]:
            y0=(11.1+1.05*math.sin(t0)) if top else (6.9-1.05*math.sin(t0))
            y1=(11.1+1.05*math.sin(t1)) if top else (6.9-1.05*math.sin(t1))
            z0=side*(11.45+1.05*math.cos(t0));z1=side*(11.45+1.05*math.cos(t1))
            intervals=[(-384,383)] if side==-1 else [(-384,X0),(X1,383)]
            if side==-1 and not top:
                edges=[-384]+[v for r in sorted(bridge_roots) for v in [r-1.85,r+1.85]]+[383]
                intervals=list(zip(edges[::2],edges[1::2]))
            for a,b in intervals:mesh('Roof_ConcourseCurves' if top else 'Facade_ConcourseCurves',METAL,[(a,y0,z0),(b,y0,z0),(b,y1,z1),(a,y1,z1)],[(0,1,2),(0,2,3)])
box('Roof_Concourse',METAL,(-.5,12.12,0),(767,.18,22.9))
for x in np.arange(-384,384,4.5):
    for z in [-12.5,12.5]:
        if z>0 and X0<x<X1:continue
        path('Facade_CladdingSeams',DARK,[(x,11.1+1.06*math.sin(t),np.sign(z)*(11.45+1.06*math.cos(t))) for t in np.linspace(0,math.pi/2,10)],.014,4)
    box('Interior_ConcourseLights',LIGHT,(x,11.98,1),(1.8,.03,.3))
    for z in [-7,8]:box('Interior_ConcourseFloorGrid',TRIM,(x,FG+.013,z),(.025,.02,3))
for x in [-384,383]:
    if x<0:box('Facade_ConcourseEnds',METAL,(x,9,0),(.12,6.2,25))
    else:
        for z in [-9,11]:box('Facade_ConcourseEnds',METAL,(x,9,z),(.12,6.2,7))
        box('Facade_ConcourseEnds',METAL,(x,11.5,1),(.12,1.2,14))
for x in np.arange(-378,383,18):
    box('Structure_ConcourseBase',STONE,(x,2.8,0),(1.2,5.6,23))

# Mezzanine processing: public guide supplies relationships; exact partitions inferred.
for x0,x1 in [(X0,-76),(5,25),(121,X1)]:
    box('Structure_ThirdFloor_Level3',SEC_FLOOR,((x0+x1)/2,F3-.2,27),(x1-x0,.4,30))
box('Structure_ThirdFloor_Level3',SEC_FLOOR,(C,F3-.2,52),(252,.4,20))
box('Structure_ThirdFloor_Level3',SEC_FLOOR,(C,F3-.2,20),(252,.4,16))
for a,b in [(-76,5),(25,121)]:
    for x in [a,b]:rail('Interior_GalleryRails',(x,F3,28),(x,F3,42))
    for z in [28,42]:rail('Interior_GalleryRails',(a,F3,z),(b,F3,z))
for x in [-66,111]:escalator(x,78,62,F2,F3)
# No descent from all security exits to the main gate concourse: that was a v2 error.
# Level 2 public hall is enclosed on its airside edge, under the Level 3 circulation.
box('Structure_Level2_AirsideBoundary',WHITE,(C,9.15,12.6),(252,5.7,.35))
# Screening boundary, with openings only at the modelled processing lanes.
for a,b in [(X0,-98),(7,58),(142,X1)]:curtain('Interior_ScreeningBoundary',a,b,46,F3,F3+3)
box('Interior_DomesticInternationalBoundary',GLASS,(35,F3+1.65,22),(.15,3.3,48))
box('Interior_DomesticInternationalBoundary',WHITE,(35,F3+3.3,22),(.2,.16,48))
for x in [-72,-24,28,77,125]:
    for j in range(8):
        xx=x+(j-3.5)*1.8
        box('Interior_CheckIn',BLUE,(xx,F2+.55,82),(1.62,1.1,.85))
        box('Interior_CheckIn',DARK,(xx,F2+.16,79.5),(1.3,.28,3.4))
        box('Interior_CheckIn',SCREEN,(xx,F2+2.8,82),(1.3,.55,.06))
        rod('Interior_CheckIn',FRAME,(xx,F2+1.05,82),(xx,F2+2.55,82),.04,6)
    sign('Interior_CheckInSigns',4 if x<0 else 5,(x,F2+3.9,82),4.5,.7)
for x in np.arange(-93,142,4):
    for z in [50,53,56]:
        rod('Interior_SecurityQueues',FRAME,(x,F3,z),(x,F3+.92,z),.035,6)
        disc('Interior_SecurityQueues',DARK,(x,F3+.04,z),.16,normal=(0,1,0),n=12)
        if x<137:beam('Interior_SecurityQueues',BELT,(x,F3+.85,z),(x+4,F3+.85,z),.03,.07)
for start,end in [(-96,2),(61,137)]:
    for x in np.arange(start,end,5.2):
        for dx in [-.57,.57]:box('Interior_SecurityLanes',WHITE,(x+dx,F3+1.12,46),(.14,2.24,.4))
        box('Interior_SecurityLanes',WHITE,(x,F3+2.3,46),(1.3,.15,.4))
        box('Interior_SecurityLanes',DARK,(x+2.1,F3+.65,45.8),(1.35,1.3,2.0))
        box('Interior_SecurityLanes',FRAME,(x+2.1,F3+.62,48),(1.15,.18,2.5))
        box('Interior_SecurityLanes',FRAME,(x+2.1,F3+.62,43.7),(1.15,.18,2.3))
        box('Interior_SecurityLanes',SCREEN,(x+3,F3+1.3,45.5),(.45,.4,.06))
    sign('Interior_SecuritySigns',6,((start+end)/2,F3+3.1,47.3),5.5,.9)
floor3_rects=[(X0,X1,12,28),(X0,X1,42,62),(X0,-76,28,42),(5,25,28,42),(121,X1,28,42)]
for a,b,c,d in floor3_rects:
    for x in np.arange(a+3,b,3):box('Interior_SecurityTileLines',STONE,(x,F3+.01,(c+d)/2),(.025,.015,d-c))
    for z in np.arange(c+3,d,3):box('Interior_SecurityTileLines',STONE,((a+b)/2,F3+.01,z),(b-a,.015,.025))
# Gallery shop fronts surround the double-height waiting voids.
for x in [-40,45,85]:
    curtain('Interior_Shops',x-10,x+10,62,F3,F3+3)
    sign('Interior_Shops',14,(x,F3+3.3,62.15),3.5,.5)
for x in np.arange(-92,142,9):
    for z in [14,19]:seats(x,z,FG,TAN)

# Gate positions and bridge polylines come from public OSM data, not uniform spacing.
gate_numbers=[1,2,3,5,6,7,8,9,10,11,12,15,16,17]
for gate in mapping['gates']:
    number=int(gate['tags'].get('ref','0'))
    if number not in gate_numbers:continue
    x,z=gate['point'];i=gate_numbers.index(number)
    box('Interior_GateDesks',BLUE,(x,FG+.55,-8),(2.5,1.1,.8))
    sign('Interior_GateSigns',16+i,(x,FG+2.8,-8),3.0,.75)
    sign('Exterior_GateSigns',16+i,(x,10.4,-12.8),2.9,.65,True)
    for dx in [-11,-7,7,11]:
        for zz in [-4,0,5]:seats(x+dx,zz,FG)
    for dx in [-2.2,2.2]:box('Interior_GateReaders',FRAME,(x+dx,FG+.48,-10),(.3,.96,.4))
for way in mapping['ways']:
    if way['tags'].get('aeroway')!='jet_bridge':continue
    points=way['points'];g='Exterior_JetBridge_'+way['tags'].get('ref','unknown')
    for a,b in zip(points,points[1:]):
        ax,az=a;bx,bz=b
        beam(g,STONE,(ax,6.0,az),(bx,6.0,bz),3.4,.25)
        beam(g,METAL,(ax,9.3,az),(bx,9.3,bz),3.7,.28)
        d=np.array([bx-ax,bz-az]);length=np.linalg.norm(d);normal=np.array([-d[1],d[0]])/length
        for side in [-1,1]:
            off=normal*side*1.65
            beam(g,GLASS,(ax+off[0],7.65,az+off[1]),(bx+off[0],7.65,bz+off[1]),.09,3.1)
            for t in np.linspace(0,1,max(2,int(length/1.8)+1)):
                p=np.array(a)*(1-t)+np.array(b)*t+off
                beam(g,WHITE,(p[0],6.1,p[1]),(p[0],9.25,p[1]),.09,.09)
        for p in [a,b]:rod(g,FRAME,(p[0],.3,p[1]),(p[0],5.9,p[1]),.20,10)
    tip=min(points,key=lambda p:p[1]);box(g,DARK,(tip[0],7.4,tip[1]),(3.8,3.1,2.3))
# Map gate 17 connects through a separate end annex.
box('Structure_Gate17Annex',FLOOR,(402,F2-.2,1),(39,.4,30))
box('Roof_Gate17Annex',WHITE,(402,11,1),(39,.25,30))
curtain('Facade_Gate17Annex',383,421,-14,F2,10.9)
curtain('Facade_Gate17Annex',383,421,16,F2,10.9)

# West extension is a separately flagged indicative component. A current as-built
# plan has not been found; do not pretend the historical museum floorplan is 2024.
wx,wz=-155,38
box('Unverified_West2024Floor',SEC_FLOOR,(wx,.12,wz),(100,.3,26))
box('Roof_West2024',WHITE,(wx,7.2,wz),(101,.25,27))
curtain('Unverified_West2024Glazing',wx-50,wx+50,wz+13,.2,7.1)
curtain('Unverified_West2024Glazing',wx-50,wx+50,wz-13,.2,7.1)
for x in [wx-50,wx+50]:box('Unverified_West2024End',WHITE,(x,3.5,wz),(.35,7,26))
for x in np.arange(wx-44,wx+48,8):
    box('Unverified_West2024Structure',WHITE,(x,3.5,wz),(.4,7,.4))
    for z in [wz-8,wz-4,wz+4,wz+8]:seats(x,z,.28,TAN)
west_atlas=Image.new('RGB',(1024,1024),(20,35,36));west_draw=ImageDraw.Draw(west_atlas)
for j,number in enumerate([22,23,25,26]):
    west_draw.text((25,j*256+25),f'{number}  登机口',font=ImageFont.truetype(fontpath,100),fill=(236,244,219))
    west_draw.text((30,j*256+158),f'GATE {number}',font=ImageFont.truetype(fontpath,48),fill=(236,244,219))
west_atlas.save(ROOT/'west-gates.png');texture_images.append(ROOT/'west-gates.png')
WEST_SIGN=material('2024 west gate signage',[1,1,1],0,.6)
materials[WEST_SIGN]['pbrMetallicRoughness']['baseColorTexture']={'index':len(texture_images)}
for j,(x,z) in enumerate([(wx-30,wz-12.8),(wx+30,wz-12.8),(wx-30,wz+12.8),(wx+30,wz+12.8)]):
    box('Unverified_West2024GateDesks',BLUE,(x,.85,z),(2.5,1.1,.8))
    zz=z+.2 if j<2 else z-.2
    mesh('Unverified_West2024GateSigns',WEST_SIGN,[(x-1.5,2.4,zz),(x+1.5,2.4,zz),(x+1.5,3.2,zz),(x-1.5,3.2,zz)],[(0,1,2),(0,2,3)],[(0,(j+1)/4),(1,(j+1)/4),(1,j/4),(0,j/4)])

# Exterior airport lettering is original geometry, placed on an open support frame.
# Separate alpha-cutout texture contains only the airport name, not a copied photo.
im=Image.new('RGBA',(4096,512),(0,0,0,0));dr=ImageDraw.Draw(im)
dr.text((30,0),'厦门高崎国际机场',font=ImageFont.truetype(fontpath,430),fill=(145,10,15,255))
buf=io.BytesIO();im.save(buf,format='PNG');(ROOT/'airport-lettering.png').write_bytes(buf.getvalue())
texture_images.append(ROOT/'airport-lettering.png')
LETTER=material('Red airport name',[1,1,1],.1,.5)
materials[LETTER]['pbrMetallicRoughness']['baseColorTexture']={'index':len(texture_images)}
materials[LETTER]['alphaMode']='MASK';materials[LETTER]['alphaCutoff']=.4
mesh('Exterior_AirportName',LETTER,[(C+85,14,-13.1),(C-85,14,-13.1),(C-85,22,-13.1),(C+85,22,-13.1)],[(0,1,2),(0,2,3)],[(0,1),(1,1),(1,0),(0,0)])
for x in np.arange(C-84,C+85,12):
    for z in [-13,-9]:beam('Exterior_LetterSupports',FRAME,(x,12.2,z),(x,22,z),.10,.10)
    beam('Exterior_LetterSupports',FRAME,(x,12.2,-9),(x,22,-13),.09,.09)

export=original[original.index('# Export standard GLB'):]
exec(compile((ROOT/'interior_detail.py').read_text(encoding='utf-8'),str(ROOT/'interior_detail.py'),'exec'))
lift_groups={'Facade_ConcoursePortholes','Facade_GateDoorHeaders','Facade_GateDoorPanels','Facade_GateDoorFrames','Facade_CladdingSeams','Roof_ConcourseCurves','Facade_ConcourseCurves','Roof_Concourse','Interior_ConcourseLights','Facade_ConcourseEnds','Exterior_GateSigns','Structure_Gate17Annex','Roof_Gate17Annex','Facade_Gate17Annex','Exterior_AirportName','Exterior_LetterSupports'}
for (group,mat),data in groups.items():
    for verts in data['v']:
        if group in lift_groups:verts[:,1]+=FG-F2
        elif group=='Structure_ConcourseBase':verts[:,1]*=(5.6+FG-F2)/5.6
        elif group.startswith('Exterior_JetBridge_'):
            yy=verts[:,1];verts[:,1]+=np.clip((yy-.3)/5.6,0,1)*(FG-F2)
export=export.replace("[240,96]","[252,108]").replace("'estimated_concourse_length_m':476","'mapped_concourse_length_m':767")
export=export.replace('XMN T3 photo-informed procedural architectural study','XMN T3 revision 6, security partitions and exterior fixes')
export=export.replace('See README.md','See EVIDENCE.md; OSM contributors ODbL; heights and detailed interiors estimated')
export=export.replace("binary=bytearray()","doc['extensionsUsed']=['KHR_materials_unlit']\nbinary=bytearray()")
export=export.replace("{'layer':g}","{'layer':g,'evidence':('2024 existence and gate IDs confirmed; spatial placement and layout provisional' if 'West2024' in g else 'OSM plan polyline; height and detail estimated' if 'JetBridge' in g else 'Photo-constrained form; dimensions and interior placement estimated'),'baseline':'post-2024 renovation'}")
exec(compile(export,str(SOURCE),'exec'))
