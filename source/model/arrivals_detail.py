"""1F arrivals, separate 2F arrival passage, and supported floor boundaries.
Evidence: official-arrival-map.jpg; Tyg728's 2017 baggage-hall photograph.
The guide establishes topology, not surveyed dimensions or current tenant names.
"""
F1=.3
ARR_TILE=material('Arrival polished warm granite',[.55,.54,.48],.12,.26)
ARR_BELT=material('Arrival black rubber slats',[.045,.05,.048],.15,.45)
ARR_GLASS=material('Arrival clear framed partitions',[.70,.79,.77],0,.18,.32)
arrival_inventory=[]

def wall(g,a,b,base,height,mat=WHITE):
    beam(g,mat,(a[0],base+height/2,a[1]),(b[0],base+height/2,b[1]),.16,height)

# Public check-in halls: partition only the controlled side, keeping the shared
# entrance circulation strip open as drawn. Transparent upper panels soften it.
wall('Interior_CheckInZoneSeparation',(20,28),(20,86),F2,.85)
wall('Interior_CheckInZoneSeparation',(20,28),(20,86),F2+.85,3.55,ARR_GLASS)
for z in np.arange(28,87,2.4):wall('Interior_CheckInZoneFrames',(20,z),(20,z+.02),F2,4.4,FRAME)
label('Interior_CheckInZoneSign','国内值机','DOMESTIC CHECK-IN',(17,F2+3.5,84),4,.65)
label('Interior_CheckInZoneSign','国际值机','INTERNATIONAL CHECK-IN',(24,F2+3.5,84),4,.65)

# Enclosed arrival gallery behind the check-in hall: passengers descending to
# baggage reclaim are screened from the public check-in room by an opaque wall.
wall('Interior_ArrivalGalleryEnclosure',(X0,29.65),(X1,29.65),F2,F3-F2-.2)
# No intermediate partition across the two-storey void.
floor_with_holes('Roof_ArrivalGalleryCeiling',F3-.25,X0,X1,12.8,27.8,holes,CEILING)
for x in np.arange(-98,146,6):
    if not any(a-1<x<b+1 and c-1<20<d+1 for a,b,c,d in holes):box('Roof_ArrivalGalleryLights',LIGHT,(x,F3-.38,20),(1.2,.04,.6))

# 1F main slab and ceiling have openings aligned to the actual stair runs.
for key in list(groups):
    if key[0]=='Structure_GroundSlab':del groups[key]
box('Structure_ArrivalFloor',ARR_TILE,(C,F1-.2,54),(252,.4,84))
floor_with_holes('Roof_ArrivalCeiling',5.45,X0,X1,12,96,lower_holes,CEILING)
for x in np.arange(-101,146,3):
    for z in np.arange(15,94,3):
        if any(a-.8<x<b+.8 and c-.8<z<d+.8 for a,b,c,d in lower_holes):continue
        box('Roof_ArrivalPanelLights',LIGHT,(x,5.02,z),(.85,.035,.85))
        if int((x+101)/3)%3==0:box('Roof_ArrivalVentGrilles',DARK,(x+1.1,5.01,z),(.38,.025,.38))
for x in np.arange(-103,147,3):box('Interior_ArrivalFloorInlay',DARK,(x,F1+.008,54),(.055,.012,84))
for z in np.arange(12,96,3):box('Interior_ArrivalFloorInlay',DARK,(C,F1+.008,z),(252,.012,.055))

# Domestic and international baggage rooms have separate exits to a shared
# public reception hall. Entry control precedes international baggage reclaim.
arrival_z=20.527083645069553
for a,b in [(12,arrival_z-1.85),(arrival_z+1.85,76)]:wall('Interior_ArrivalZoneBoundary',(45,a),(45,b),F1,4.7)
# The direct international descent passes through this boundary above its base;
# wrap the shaft instead of putting a wall through the moving tread.
for a,b in [((22.4,arrival_z-1.85),(48,arrival_z-1.85)),((22.4,arrival_z+1.85),(48,arrival_z+1.85)),((22.4,arrival_z-1.85),(22.4,arrival_z+1.85))]:
    wall('Interior_InternationalArrivalShaft',a,b,F1,5.7)
for a,b in [(X0,-52),(-44,91),(99,X1)]:wall('Interior_ArrivalPublicBoundary',(a,76),(b,76),F1,4.7,ARR_GLASS)
for x,cn,en in [(-48,'国内到达出口','DOMESTIC ARRIVALS'),(95,'国际到达出口','INTERNATIONAL ARRIVALS')]:
    label('Interior_ArrivalExitSigns',cn,en,(x,3.8,76),7,.8)
    for side in [-1,1]:wall('Interior_ArrivalExitFrames',(x+side*4,76),(x+side*4,79),F1,2.7,FRAME)
    arrival_inventory.append(dict(id=en,type='exit',position=[x,F1,76],clear_width=8))

def capsule(cx,cz,length,r):
    straight=length/2-r
    return np.array([(cx+r*math.cos(t),cz+straight+r*math.sin(t)) for t in np.linspace(0,math.pi,25)]+[(cx+r*math.cos(t),cz-straight+r*math.sin(t)) for t in np.linspace(math.pi,2*math.pi,25)])

def carousel(number,x,z,length):
    outer=capsule(x,z,length,2.9);inner=capsule(x,z,length-2.0,1.9)
    g='Interior_ArrivalCarousel_'+str(number)
    for i in range(len(outer)):
        j=(i+1)%len(outer)
        a,b=outer[i],outer[j];c,d=inner[i],inner[j]
        mesh(g,FRAME,[(a[0],F1+.15,a[1]),(b[0],F1+.15,b[1]),(b[0],F1+.58,b[1]),(a[0],F1+.58,a[1])],[(0,1,2),(0,2,3)])
        mesh(g,ARR_BELT,[(a[0],F1+.59,a[1]),(b[0],F1+.59,b[1]),(d[0],F1+1,d[1]),(c[0],F1+1,c[1])],[(0,1,2),(0,2,3)])
        beam(g,FRAME,(a[0],F1+.605,a[1]),(c[0],F1+1.015,c[1]),.022,.018)
    label(g,str(number)+'  行李提取','BAGGAGE CLAIM',(x,F1+2.8,z+length/2+1),4,.65)
    for dx in [-1.5,1.5]:rod(g,FRAME,(x+dx,F1,z+length/2+1),(x+dx,F1+2.45,z+length/2+1),.03,8)
    arrival_inventory.append(dict(id=number,type='baggage carousel',zone='domestic' if number<=6 else 'international',center=[x,F1,z],length=length,width=5.8,source='1F official guide numbering; photo belt profile; dimensions estimated'))

from guide_registration import ARRIVAL, ARRIVAL_CENTRES, unproject
def clear_carousel_center(center,length):
    # Keep the existing structural grid. Search only within the 8-pixel manual
    # reading uncertainty; the belt annulus must clear the square column wraps.
    columns=np.array([(x,z) for x in np.arange(X0+6,X1,12) for z in [18,42,66,90]])
    candidates=[]
    for dx in np.arange(-3,3.01,.125):
        for dz in np.arange(-3,3.01,.125):
            delta=np.array([dx,dz]);error=np.linalg.norm(ARRIVAL[:,:2]@delta)
            if error>8:continue
            c=center+delta;distance=np.abs(columns-c)
            nearest=np.maximum(distance-[.71,length/2-2.9+.71],0)
            farthest=distance+[.71,.71];farthest[:,1]=np.maximum(farthest[:,1]-(length/2-2.9),0)
            intersects=(np.linalg.norm(nearest,axis=1)<3.05)&(np.linalg.norm(farthest,axis=1)>1.75)
            if not intersects.any():candidates.append((error,dx,dz,c))
    if not candidates:raise ValueError(('No guide-consistent column clearance',center.tolist()))
    return min(candidates,key=lambda r:r[:3])[3]

for n,length in [(1,18),(2,20),(3,22),(4,23),(5,24),(6,25),(7,32),(8,22),(9,23),(10,24)]:
    x,z=clear_carousel_center(unproject(ARRIVAL_CENTRES[n],ARRIVAL),length)
    carousel(n,float(x),float(z),length)

# Immigration upstream of the international carousels; customs at its exit.
for x in [78,85,92,99,106,113,120,127,134]:
    box('Interior_ArrivalImmigration',TAUPE,(x,F1+.55,32),(2.0,1.1,1.25))
    box('Interior_ArrivalImmigration',ARR_GLASS,(x,F1+1.7,32),(2,.9,.055))
    box('Interior_ArrivalImmigration',SCREEN,(x-.5,F1+1.25,32.25),(.45,.35,.06))
label('Interior_ArrivalImmigrationSign','入境边防检查','IMMIGRATION',(105,3.8,32),7,.75)
for x in [88,102]:
    box('Interior_ArrivalCustoms',TAUPE,(x,F1+.55,70),(2.4,1.1,1.4))
label('Interior_ArrivalCustomsSign','海关检查','CUSTOMS',(95,3.5,70),5,.65)

# Different service-room outlines follow the guide's recesses; frontage doors
# are left open, not filled by the room perimeter.
def service_room(id,poly,cn):
    g='Interior_ArrivalService_'+id
    for a,b in zip(poly,poly[1:]):wall(g,a,b,F1,3.9)
    a,b=poly[-1],poly[0];mid=((a[0]+b[0])/2,(a[1]+b[1])/2)
    label(g,cn,'SERVICE',(mid[0],3.5,mid[1]),min(5,abs(b[0]-a[0])+.5),.65)
    arrival_inventory.append(dict(id=id,type='service room',outline=poly,source='guide topology, estimated dimensions'))
service_room('west-toilet',[(-102,65),(-102,56),(-95,56),(-95,61),(-94,61),(-94,65)],'卫生间')
service_room('west-restaurant',[(-103,92),(-103,80),(-86,80),(-86,85),(-78,85),(-78,92)],'餐饮')
service_room('east-restaurant',[(117,92),(117,86),(126,86),(126,81),(146,81),(146,92)],'餐饮')
service_room('baggage-service',[(-37,74),(-37,68),(-29,68),(-29,71),(-24,71),(-24,74)],'行李查询')
service_room('east-toilet',[(134,79),(134,70),(146,70),(146,79)],'卫生间')
for x,cn in [(-15,'旅游服务'),(9,'问询服务'),(30,'中转服务')]:
    box('Interior_ArrivalPublicDesks',WOOD,(x,F1+.55,80),(5,1.1,1.3))
    label('Interior_ArrivalPublicDesks',cn,'ARRIVAL SERVICES',(x,2.6,80),4,.6)

# Luggage trolleys, square column wraps and low suspended wayfinding from photo.
for x in [-95,-71,-47,-23,1,25,51,75,99,123]:
    for j in range(4):
        xx=x+j*.7;zz=68
        box('Interior_ArrivalTrolleys',FRAME,(xx,F1+.3,zz),(.55,.08,.85))
        for dx in [-.25,.25]:
            rod('Interior_ArrivalTrolleys',FRAME,(xx+dx,F1+.3,zz+.3),(xx+dx,F1+1,zz+.3),.025,6)
        rod('Interior_ArrivalTrolleys',FRAME,(xx-.25,F1+1,zz+.3),(xx+.25,F1+1,zz+.3),.03,8)
        for dx in [-.2,.2]:
            for dz in [-.3,.3]:rod('Interior_ArrivalTrolleys',DARK,(xx+dx-.03,F1+.12,zz+dz),(xx+dx+.03,F1+.12,zz+dz),.10,8)
for x in np.arange(X0+6,X1,12):
    for z in [18,42,66,90]:
        box('Interior_ArrivalColumnWrap',WHITE,(x,2.6,z),(1.12,4.6,1.12))
        box('Interior_ArrivalColumnSkirt',FRAME,(x,.77,z),(1.14,.94,1.14))

# 1F exterior doorway breaks, with circulation space behind them.
for n,x in zip([11,9,7,5,3,1],[-90,-47,-4,39,82,125]):
    label('Interior_ArrivalStreetExit',str(n)+'  出口','EXIT',(x,3.8,95.8),4,.7)
    for dx in [-2.1,2.1]:box('Facade_ArrivalDoorFrames',FRAME,(x+dx,1.7,96),(.12,2.8,.18))
    box('Facade_ArrivalDoorFrames',FRAME,(x,3.12,96),(4.3,.12,.18))

# Keep glass division visually lighter without changing the security screens.
for (name,mat),data in list(groups.items()):
    if name=='Interior_ZoneSeparation' and mat==FROSTED:
        groups.pop((name,mat));groups[(name,ARR_GLASS)]=data

(ROOT/'arrival-inventory.json').write_text(json.dumps(dict(facilities=arrival_inventory,stairs=arrival_descents,limits=['Historical guide inventory; 2024+ changes not fully documented.','Stair orientation is east-west; exact paired shaft coordinates estimated.','Arrival gallery is enclosed from check-in; not a surveyed as-built plan.']),ensure_ascii=False,indent=2),encoding='utf-8')
