"""Replace guessed circulation with explicitly traced diagram anchors.
Diagram units are approximate; equipment sizes remain modelling estimates.
"""
trace=json.loads((ROOT/'diagram-trace.json').read_text(encoding='utf-8'))
def project(p):
    a=p[0]-228;b=p[1]-1358;det=2.39*1.4+1.42*2.35
    return np.array([-384+(1.4*a-2.35*b)/det,-12.5+(1.42*a+2.39*b)/det])

# Remove superseded geometry, including queues formerly put across both halls.
prefixes=('Structure_ThirdFloor','Interior_GalleryRails','Interior_Escalators',
 'Interior_Security','Interior_Scanner','Interior_ScreeningBoundary',
 'Interior_DomesticInternationalBoundary','Interior_GalleryBalustrade')
for key in list(groups):
    if key[0].startswith(prefixes):del groups[key]
# Old security queues used the same group names as the accepted island queues.
# Remove only vertices at the upper level, preserving the lower islands verbatim.
for key,data in list(groups.items()):
    if key[0] in ('Interior_QueuePosts','Interior_QueueBelts'):
        keep=[i for i,v in enumerate(data['v']) if np.min(v[:,1])<F3-.1]
        for field in data:
            if isinstance(data[field],list):data[field]=[data[field][i] for i in keep]

records=[];holes=[];lower_holes=[]
def record(id,kind,xyz,**more):
    records.append(dict(id=id,kind=kind,position=[float(v) for v in xyz],dimensions_verified=False,**more))

def stair(id,p,run=11.0,base=F2,top=F3,arrival=False):
    x,z=project(p)
    if id=='L3-E04':x,z=-49.2,20.527083645069553
    if id=='L3-E05':x,z=23.1,20.527083645069553
    g='Interior_Circulation_'+id
    # Source point is the drawn landing, deliberately separate from floating icon.
    width=2.8
    a=np.array([x,base,z+run]);b=np.array([x,top,z])
    for off in [-.72,.72]:
        aa=a+[off,0,0];bb=b+[off,0,0]
        beam(g,DARK,aa-[0,.28,0],bb-[0,.28,0],1.36,.5)
        step_count=max(36,int(np.ceil(run/.30))+1)
        for t in np.linspace(0,1,step_count):
            v=aa*(1-t)+bb*t
            box(g,FRAME,v,(1.08,.09,run/(step_count-1)+.02))
            box(g,YELLOW,v+[0,.051,0],(1.05,.012,.025))
        for side in [-.62,.62]:
            beam(g,GLASS,aa+[side,.45,0],bb+[side,.45,0],.06,.85)
            rod(g,DARK,aa+[side,.92,0],bb+[side,.92,0],.045,8)
    holes.append((x-width/2-.25,x+width/2+.25,z+.4,z+run+.5))
    for side in [-1,1]:rail(g,(x+side*1.7,top,z+.6),(x+side*1.7,top,z+run+.6))
    label(g,'到达下行' if arrival else '楼层连接',id,(x,top+2.4,z-1.2),3.6,.62)
    if id in ['L3-E01','L3-E03','L3-E06'] or arrival:
        direction=-1 if id=='L3-E01' else 1
        for (name,mat),data in groups.items():
            if name!=g:continue
            for vertices in data['v']:
                ox=vertices[:,0].copy()-x;oz=vertices[:,2].copy()-z
                vertices[:,0]=x+direction*oz;vertices[:,2]=z-direction*ox
        holes[-1]=(min(x+direction*.4,x+direction*(run+.5)),max(x+direction*.4,x+direction*(run+.5)),z-width/2-.25,z+width/2+.25)
        a=np.array([x+direction*run,base,z])
        if arrival and base<1 and top==F3:
            # Close the upper floor above the lower portion once headroom permits.
            holes[-1]=(x+.2,x+4.6,z-width/2-.25,z+width/2+.25)
    record(id,'arrival escalator' if arrival else 'floor connection',b,landing_pixel=p,lower_landing=a.tolist(),pairing='upper landing source-traced; run and lower endpoint estimated')

# Four upper public-side connections are independently visible in the diagram.
for id,p in [('L3-E01',[979,1024]),('L3-E02',[1088,1058]),('L3-E03',[1093,969]),('L3-E06',[1472,756])]:
    stair(id,p,run=22,base=.28) if id=='L3-E01' else stair(id,p)
for id,p in [('L3-E04',[1124,918]),('L3-E05',[1286,809])]:stair(id,p,run=22,base=.3,arrival=True)

def lift(id,x,z,base,top):
    g='Interior_Circulation_'+id;h=top-base+3.0
    for dx in [-1.35,1.35]:box(g,WHITE,(x+dx,base+h/2,z),(.18,h,2.9))
    box(g,WHITE,(x,base+h/2,z-1.4),(2.8,h,.18))
    for yy in [base,top]:
        for dx in [-.57,.57]:box(g,FRAME,(x+dx,yy+1.08,z+1.41),(1.10,2.16,.08))
        box(g,WHITE,(x,yy+2.6,z+1.41),(2.7,.75,.2))
        box(g,SCREEN,(x+.98,yy+1.25,z+1.55),(.13,.24,.05))
        label(g,'电梯',id,(x,yy+2.6,z+1.56),2.4,.45)
    if top==F3:holes.append((x-1.5,x+1.5,z-1.5,z+1.5))
    else:lower_holes.append((x-1.5,x+1.5,z-1.5,z+1.5))
    box(g,WHITE,(x,top+3.08,z),(2.9,.16,3.0))
    record(id,'lift shaft',[x,base,z],upper_level=top)

# Lower front-side lifts connect to arrivals below; no diagram basis for taking
# those shafts through the upper public forecourt. Keep that distinction explicit.
for id,x,z,base,top in [('L2-L01',-78,-2.5,F2,F3),('L3-L02',114,1.7,F2,F3),('L2-L02',-70,88,.3,F2),('L2-L04',94,88,.3,F2)]:lift(id,x,z,base,top)
# Front lower-hall escalators descend toward the arrivals level, not to security.
for id,x,z in [('L2-E02',-56,84),('L2-E04',106,83)]:
    # Convert world upper landing back to source coordinates for the shared helper.
    p=[228+2.39*(x+384)+2.35*(z+12.5),1358-1.42*(x+384)+1.4*(z+12.5)]
    stair(id,p,run=10,base=.3,top=F2);lower_holes.append(holes.pop())

# Direct 3F-to-1F arrival escalators: 2F contains a shaft opening, no transfer landing.
arrival_descents=[r for r in records if r['kind']=='arrival escalator']
for r in arrival_descents:
    x,top,z=r['position'];end=r['lower_landing'][0]
    lower_holes.append((x+.2,end+.5,z-1.7,z+1.7))

# Atrium openings traced from the black polygons, rather than v4's uniform slots.
# Axis-aligned extent is an approximation to the oblique guide's drawn footprint.
for ps in [[(1012,971),(1050,948),(1081,967),(1043,990)],[(1085,933),(1139,901),(1169,919),(1115,951)],[(1175,878),(1435,722),(1473,745),(1213,901)]]:
    pp=np.array([project(p) for p in ps]);h=(pp[:,0].min(),pp[:,0].max(),pp[:,1].min(),min(pp[:,1].max(),29.5));holes.append(h)
    for z in h[2:]:rail('Interior_AtriumGuardrails',(h[0],F3,z),(h[1],F3,z))
    for x in h[:2]:rail('Interior_AtriumGuardrails',(x,F3,h[2]),(x,F3,h[3]))

def floor_with_holes(g,y,xmin,xmax,zmin,zmax,cutouts,mat=SEC_FLOOR):
    xs=sorted(set([xmin,xmax]+[max(xmin,min(xmax,v)) for h in cutouts for v in h[:2]]))
    zs=sorted(set([zmin,zmax]+[max(zmin,min(zmax,v)) for h in cutouts for v in h[2:]]))
    for a,b in zip(xs,xs[1:]):
        for c,d in zip(zs,zs[1:]):
            x=(a+b)/2;z=(c+d)/2
            if b-a<.01 or d-c<.01 or any(h[0]<x<h[1] and h[2]<z<h[3] for h in cutouts):continue
            box(g,mat,(x,y-.20,z),(b-a,.4,d-c))

# User: west small bay is solid; the next void extends left to the up escalator.
holes=[h for h in holes if not (-84<h[0]<-83 and -68<h[1]<-67)]
holes=[(-66.00658386951966,h[1],h[2],h[3]) if -56<h[0]<-54 and -33<h[1]<-32 else h for h in holes]
holes.append((75,87,24,33))
# The marked long 2F strip is entirely open, including below 3F landing bridges.
lower_holes.append((-83.86532994164293,92.4925931467904,15.532320814005676,29.5))
# Lower-level opening below the public international stair; retain its east landing.
lower_holes.append((88.4,98.7,34.9,38.2))
floor_with_holes('Structure_ThirdFloor_Level3',F3,X0,X1,12,68,holes)
# West-side landing projects beyond the nominal rectangular main hall.
floor_with_holes('Structure_WestConnectionLanding',F3,-114,X0,12,42,holes)
floor_with_holes('Structure_WestConnectionLandingLower',F2,-114,X0,12,42,[])
for key in list(groups):
    if key[0] in ('Structure_DepartureFloor_Level2','Interior_FloorGrid'):del groups[key]
floor_with_holes('Structure_DepartureFloor_Level2',F2,X0,X1,12,96,lower_holes,FLOOR)
# Shafts on the narrow concourse need real slab openings as well.
for key in list(groups):
    if key[0]=='Structure_ConcourseFloor_Level3':del groups[key]
floor_with_holes('Structure_ConcourseFloor_Level3',F3,-384,382,-12.5,12.5,holes)
# Arrival stairs are drawn at the end of fingers projecting into the atrium.
# A shaft opening alone would leave those top landings unsupported.
for rec in records:
    if rec['kind']!='arrival escalator':continue
    x,y,z=rec['position'];g='Structure_ArrivalLanding_'+rec['id']
    box(g,SEC_FLOOR,(x-1.425,F3-.2,(11.8+z)/2),(3.15,.4,z-11.8+3.3))
    for side in [-1,1]:rail('Interior_ArrivalBridgeRails',(x+side*1.7,F3,12),(x+side*1.7,F3,z))

def screening_lane(id,x,z,angle=0):
    if id in ['SEC-D-07','SEC-D-09']:x-=1.0
    if id=='SEC-I-05':z+=1.25  # keep portal clear of the structural column
    g='Interior_Circulation_'+id;start={k:len(d['v']) for k,d in groups.items()}
    for dx in [-.57,.57]:box(g,WHITE,(x+dx,F3+1.12,z),(.14,2.24,.42))
    box(g,WHITE,(x,F3+2.28,z),(1.3,.17,.42))
    for dx in [-.58,.58]:box(g,TAUPE,(x+2+dx,F3+.98,z),(.16,1.05,1.6))
    box(g,TAUPE,(x+2,F3+1.54,z),(1.3,.18,1.6))
    box(g,DARK,(x+2,F3+.4,z),(1.3,.7,1.6))
    for dz in [-1.55,1.55]:
        box(g,FRAME,(x+2,F3+.68,z+dz),(1.16,.15,1.7))
        for dd in np.arange(-.7,.75,.15):rod(g,FRAME,(x+1.47,F3+.79,z+dz+dd),(x+2.53,F3+.79,z+dz+dd),.045,8)
    if angle:
        for key,d in groups.items():
            if key[0]!=g:continue
            for v in d['v'][start.get(key,0):]:
                xx=v[:,0]-x;zz=v[:,2]-z;v[:,0]=x+xx*np.cos(angle)-zz*np.sin(angle);v[:,2]=z+xx*np.sin(angle)+zz*np.cos(angle)
    record(id,'security lane',[x,F3,z],bank='international' if angle else 'domestic')

# Domestic: long bank parallel to the concourse. International: return bank at
# its east end, after a separate immigration bank. Counts represent drawn symbols.
da=project([1171,942]);db=project([1417,789])
for i,t in enumerate(np.linspace(0,1,18)):
    x,z=da*(1-t)+db*t;screening_lane(f'SEC-D-{i+1:02}',x,z)
ia=project([1530,675]);ib=project([1610,723])
for i,t in enumerate(np.linspace(0,1,7)):
    x,z=ia*(1-t)+ib*t;screening_lane(f'SEC-I-{i+1:02}',x,z,np.pi/2)
ma=project([1451,834]);mb=project([1563,767])
for i,t in enumerate(np.linspace(0,1,10)):
    x,z=ma*(1-t)+mb*t;g=f'Interior_Circulation_IMM-I-{i+1:02}'
    box(g,TAUPE,(x,F3+.6,z),(1.5,1.2,.9));box(g,GLASS,(x,F3+1.65,z),(1.5,.9,.055))
    box(g,SCREEN,(x+.42,F3+1.3,z+.32),(.4,.32,.05));record('IMM-I-'+str(i+1),'immigration booth',[x,F3,z])
for id,p,cn,en in [('SEC-D',[1273,914],'国内安全检查','DOMESTIC SECURITY'),('SEC-I',[1543,723],'国际安全检查','INTERNATIONAL SECURITY'),('IMM-I',[1512,798],'出境边防检查','IMMIGRATION')]:
    x,z=project(p);label('Interior_Circulation_'+id,cn,en,(x,F3+3,z),6,.8)

# Distinct landside commercial blocks flank the domestic vertical connection.
# These footprints use building blocks in the drawing, not the displaced icons.
for id,p,w,d,cn in [('D-SH01',[1100,994],8,4,'商店'),('D-SH02',[1135,977],9,4,'商店'),('D-SH03',[1183,1005],14,5,'商店'),('D-CF01',[1060,1005],7,4,'咖啡'),('I-SH01',[1527,677],10,5,'商店')]:
    x,z=project(p)
    if id=='L3-E04':x,z=-49.2,20.527083645069553
    if id=='L3-E05':x,z=23.1,20.527083645069553
    g='Interior_Circulation_'+id
    box(g,WHITE,(x,F3+1.45,z-d/2),(w,2.9,.15))
    for dx in [-w/2,w/2]:box(g,WHITE,(x+dx,F3+1.45,z),(.15,2.9,d))
    box(g,WOOD,(x,F3+2.7,z+d/2),(w,.45,.15));label(g,cn,id,(x,F3+2.7,z+d/2+.15),min(4,w-.2),.5)
    record(id,'source block',[x,F3,z],footprint_estimated=[w,d])

# Store route lines as an optional audit layer, not physical barriers or navigation.
for rt in trace['routes']:
    col=rt['color'].lstrip('#');mat=material('Audit '+rt['id'],[int(col[i:i+2],16)/255 for i in (0,2,4)],0,.8)
    yy=F3 if rt['level']==3 else F2
    for a,b in zip(rt['estimated_world_xz'],rt['estimated_world_xz'][1:]):
        beam('Audit_Route_'+rt['id'],mat,(a[0],yy+.12,a[1]),(b[0],yy+.12,b[1]),.22,.035)
(ROOT/'circulation-register.json').write_text(json.dumps(dict(facilities=records,floor_openings=holes,limitations=['Guide-symbol positions and footprints are distinct.','Equipment counts, shaft dimensions, lower endpoints and slab heights are not surveyed.','2024 changes not shown on the historical diagram are not verified by this trace.']),ensure_ascii=False,indent=2),encoding='utf-8')
