"""Bounded fixes requested by the user: screening, signs, lettering and end frame."""
FROSTED=material('Security frosted pale aqua glass',[.57,.73,.70],0,.93,.88)
END_GLASS=material('Side elevation muted grey glazing',[.33,.39,.36],.18,.52)

def partition(a,b,g='Interior_SecurityIsolation',height=2.55):
    a=np.array(a,float);b=np.array(b,float)
    if np.linalg.norm(b-a)<.04:return
    beam(g,FROSTED,(a[0],F3+height/2,a[1]),(b[0],F3+height/2,b[1]),.12,height)
    n=max(1,int(np.ceil(np.linalg.norm(b-a)/2.4)))
    for t in np.linspace(0,1,n+1):
        p=a*(1-t)+b*t;beam(g,FRAME,(p[0],F3,p[1]),(p[0],F3+height+.04,p[1]),.075,.075)
    beam(g,FRAME,(a[0],F3+.1,a[1]),(b[0],F3+.1,b[1]),.15,.20)

# Continuous boundary with only passenger and scanner apertures left open.
bank_records=[]
for bank in ['D','I']:
    lanes=[r for r in records if r['id'].startswith('SEC-'+bank+'-')]
    origin=np.array(lanes[0]['position'])[ [0,2] ]
    tangent=np.array(lanes[-1]['position'])[ [0,2] ]-origin;tangent/=np.linalg.norm(tangent)
    normal=np.array([-tangent[1],tangent[0]])
    total=np.dot(np.array(lanes[-1]['position'])[[0,2]]-origin,tangent)
    gaps=[]
    for rec in lanes:
        p=np.array(rec['position'])[[0,2]];t=float(np.dot(p-origin,tangent))
        gaps.extend([(t-.64,t+.64),(t+1.32,t+2.68)])
        # Each screening lane has a tall translucent side screen, as in the photo.
        for offset in ([-1.3,3.9] if rec is lanes[-1] else [-1.3]):partition(p+tangent*offset-normal*2.5,p+tangent*offset+normal*3.0)
        q=p+normal*5.5
        for off in [-1.05,1.05]:
            for dist in [0,5]:
                r=q+tangent*off+normal*dist
                rod('Interior_SecurityQueue',FRAME,(r[0],F3,r[1]),(r[0],F3+.95,r[1]),.035,8)
                rod('Interior_SecurityQueue',DARK,(r[0],F3+.02,r[1]),(r[0],F3+.06,r[1]),.17,12)
            p0=q+tangent*off;p1=p0+normal*5
            beam('Interior_SecurityQueue',BELT,(p0[0],F3+.86,p0[1]),(p1[0],F3+.86,p1[1]),.045,.075)
    cursor=-2.2
    for lo,hi in sorted(gaps):
        if lo>cursor:partition(origin+tangent*cursor,origin+tangent*lo)
        cursor=max(cursor,hi)
    partition(origin+tangent*cursor,origin+tangent*(total+4.6))
    bank_records.append(dict(bank=bank,lanes=len(lanes),pedestrian_aperture_m=1.28,scanner_aperture_m=1.36,partition_height_m=2.55))

# Connect the bank boundaries to the concourse edge and exterior enclosure.
d0=np.array([r for r in records if r['id']=='SEC-D-01'][0]['position'])[[0,2]]
d1=np.array([r for r in records if r['id']=='SEC-D-18'][0]['position'])[[0,2]]
partition(d0+[-2.2,0],[-56,30.3]);partition([-56,30.3],[-56,16]);partition([-56,16],[-45.5,16]);partition([-45.5,16],[-45.5,12])
partition(d1+[4.6,0],[75,34])
i0=np.array([r for r in records if r['id']=='SEC-I-01'][0]['position'])[[0,2]]
i1=np.array([r for r in records if r['id']=='SEC-I-07'][0]['position'])[[0,2]]
partition(i0+[0,-2.2],[i0[0],12]);partition(i1+[0,4.6],[147.5,i1[1]+4.6])

# Replace the long textured board with extruded, un-stretched KaiTi characters.
for key in list(groups):
    if key[0] in ['Exterior_AirportName','Exterior_LetterSupports']:del groups[key]
letters=json.loads((ROOT/'letter-mesh.json').read_text(encoding='utf-8'))
lv=np.array(letters['vertices'],float);xx=lv[:,0].copy();yy=lv[:,1].copy();scale=5.2/(yy.max()-yy.min())
for mask,center in [(xx<1000,C+15),(xx>=1000,C-15)]:
    local=xx[mask];lv[mask,0]=center-(local-(local.min()+local.max())/2)*scale
lv[:,1]=25.0+(yy.max()-yy)*scale
lv[:,2]=-13.3+lv[:,2]
mesh('Exterior_XiamenRaisedLetters',RED,lv,letters['faces'])
width=float(np.ptp(lv[:,0]))
for center in [C+15,C-15]:
    for x in [center-3.2,center+3.2]:
        for z in [-12.8,-10.3]:beam('Exterior_XiamenLetterFrame',FRAME,(x,18,z),(x,30.8,z),.12,.12)
        for y in np.arange(18,28,3):
            beam('Exterior_XiamenLetterFrame',FRAME,(x,y,-12.8),(x,y+3,-10.3),.07,.07)
    for y in [19,23,27,30.8]:
        beam('Exterior_XiamenLetterFrame',FRAME,(center-3.2,y,-12.8),(center+3.2,y,-12.8),.09,.09)
    for x in [center-3.2,center+3.2]:beam('Exterior_XiamenLetterFrame',FRAME,(x,18,-4),(x,29.5,-10.3),.10,.10)
for y in [20,23]:beam('Exterior_XiamenLetterFrame',FRAME,(C-19,y,-12.7),(C+19,y,-12.7),.1,.12)

# End wall: pale glazing behind strong vertical concrete fins and stepped frames.
for key in list(groups):
    if key[0]=='Facade_EndGlazing':
        groups[(key[0],END_GLASS)]=groups.pop(key)
    elif key[0]=='Facade_EndGrid':del groups[key]
for x in [X0-.18,X1+.18]:
    for side in [-1,1]:
        for dist,height in [(0,36.8),(8,32.5),(26,23.5),(54,17.4)]:
            z=roof_z(dist,side)
            beam('Facade_EndConcreteFins',WHITE,(x,F2,z),(x,height,z),.85,.9)
            box('Facade_EndPierBases',WHITE,(x,F2+.4,z),(1.1,.8,1.4))
        for d0,h0,d1,h1 in [(0,36.8,8,32.5),(8,27.8,26,23.5),(26,19.5,54,17.4)]:
            beam('Facade_EndSteppedHeaders',WHITE,(x,h0,roof_z(d0,side)),(x,h1,roof_z(d1,side)),.75,.65)
            for dist in np.arange(d0+1.1,d1,1.1):
                y=h0+(h1-h0)*(dist-d0)/(d1-d0)
                beam('Facade_EndVerticalMullions',FRAME,(x,F2,roof_z(dist,side)),(x,y,roof_z(dist,side)),.07,.075)
        for y in [F3,18.3]:
            for d0,d1 in [(0,8),(8,26),(26,54)]:
                if y>=17.4 and d0==26:continue
                beam('Facade_EndTransoms',FRAME,(x,y,roof_z(d0,side)),(x,y,roof_z(d1,side)),.07,.07)

# Longitudinal purlins articulate the curved frame seen in the user's aerial photo.
control=np.array([[0,40.3],[12,26.0],[30,21.0],[54,17.8]])
for side in [-1,1]:
    for t in [.23,.43,.63,.82]:
        p=(1-t)**3*control[0]+3*(1-t)**2*t*control[1]+3*(1-t)*t*t*control[2]+t**3*control[3]
        beam('Roof_CurvedFramePurlins',WHITE,(X0,p[1],roof_z(p[0],side)),(X1,p[1],roof_z(p[0],side)),.25,.28)

(ROOT/'fix-register.json').write_text(json.dumps(dict(security=bank_records,airside_lettering=dict(text='厦门',font=letters['font'],geometry='extruded glyph contours',height_m=5.2,nonuniform_scaling=False),gallery_sign_center_y=F3-1.82,roof_airside_artificial_raise_removed_m=FG-F2,checkin_to_security_escalator_axis='east-west / X'),ensure_ascii=False,indent=2),encoding='utf-8')
