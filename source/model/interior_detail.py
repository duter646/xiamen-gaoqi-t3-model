"""Layout follows user diagram; visible construction details follow source photos.
Executed in the model builder namespace, before GLB serialization.
All numeric offsets remain estimates, listed in interior-register.json.
"""
for key in list(groups):
    n=key[0]
    if n.startswith(('Interior_CheckIn','Interior_Shops','Interior_Seating','Interior_GateDesks','Interior_GateSigns','Interior_GateReaders','Interior_SecurityQueues','Interior_SecurityLanes','Interior_SecuritySigns','Interior_ConcourseLights','Interior_Escalators')):
        del groups[key]

TAUPE=material('Photo reference warm grey counter panels',[.47,.46,.39],.15,.48)
WOOD=material('Photo reference shop wood',[.35,.17,.075],0,.55)
UPHOLSTERY=material('Photo reference tan seats',[.48,.29,.16],0,.52)
WHITE_TILE=material('Light polished stone',[.62,.61,.53],.10,.32)
TEXT_MAT=material('Location-specific bilingual signs',[1,1,1],0,.45,emission=[.2,.2,.2])
materials[TEXT_MAT]['extensions']={'KHR_materials_unlit':{}}
materials[TEXT_MAT]['doubleSided']=False
text_items=[];text_lookup={};register=[]

def label(g,cn,en,c,w=3.0,h=.7,axis='x',color=(13,26,29)):
    key=(cn,en,color)
    if key not in text_lookup:text_lookup[key]=len(text_items);text_items.append(key)
    i=text_lookup[key];col=i%4;row=i//4
    x,y,z=c
    if axis=='x':
        box(g,DARK,c,(w+.04,h+.04,.10))
        vv=[(x-w/2,y-h/2,z+.06),(x+w/2,y-h/2,z+.06),(x+w/2,y+h/2,z+.06),(x-w/2,y+h/2,z+.06)]
    else:
        box(g,DARK,c,(.10,h+.04,w+.04))
        vv=[(x+.06,y-h/2,z+w/2),(x+.06,y-h/2,z-w/2),(x+.06,y+h/2,z-w/2),(x+.06,y+h/2,z+w/2)]
    uv=[(col/4,(row+1)/64),((col+1)/4,(row+1)/64),((col+1)/4,row/64),(col/4,row/64)]
    mesh(g,TEXT_MAT,vv,[(0,1,2),(0,2,3)],uv)
    back=np.array([vv[1],vv[0],vv[3],vv[2]])
    back[:,2 if axis=='x' else 0]-=.12
    mesh(g,TEXT_MAT,back,[(0,1,2),(0,2,3)],uv)

def queue(x,z,y=F2,width=10,depth=7):
    for j in range(4):
        zz=z+j*depth/3
        for xx in [x-width/2,x+width/2]:
            rod('Interior_QueuePosts',FRAME,(xx,y,zz),(xx,y+.9,zz),.032,8)
            rod('Interior_QueuePosts',DARK,(xx,y+.01,zz),(xx,y+.045,zz),.16,12)
        # Alternate end gaps form one serpentine route rather than closed pens.
        a=x-width/2+(1.1 if j%2 else 0);b=x+width/2-(0 if j%2 else 1.1)
        beam('Interior_QueueBelts',BELT,(a,y+.81,zz),(b,y+.81,zz),.035,.065)

def counter(x,z,letter,number,side,selfbag=False):
    g='Interior_CheckIn_'+letter
    box(g,TAUPE,(x,F2+.49,z),(.95,.98,1.20))
    box(g,STONE,(x,F2+1.02,z),(1.16,.10,1.35))
    box(g,DARK,(x-side*.7,F2+.34,z+1.1),(2.5,.13,.68))
    for t in np.arange(-1,1.1,.15):box(g,FRAME,(x-side*.7+t,F2+.416,z+1.1),(.025,.025,.65))
    box(g,DARK,(x+side*.07,F2+1.14,z),(.24,.24,.15))
    box(g,SCREEN,(x+side*.1,F2+1.37,z),(.05,.38,.43))
    label(g,letter+f'{number:02d}','BAG DROP' if selfbag else 'CHECK-IN',(x,F2+2.62,z),1.55,.64,'z')
    if selfbag:
        box(g,WHITE,(x+side*.65,F2+.8,z),(.32,1.6,.52))
        box(g,SCREEN,(x+side*.83,F2+1.23,z),(.03,.48,.40))

# Individual cyan counter footprints traced from the supplied guide, not its blue circulation floor.
# Pixel coordinates refer to islands-reference.png (2x crop of the original).
from guide_registration import CHECKIN, unproject

island_specs=[
 ('A',-74,74,[(138,859),(182,834),(257,878),(213,903)],False),
 ('B',-42,74,[(290,774),(327,752),(442,819),(404,842)],False),
 ('C',-10,74,[(452,673),(481,656),(558,701),(528,718)],False),
 ('D',42,75,[(615,531),(658,506),(735,551),(692,576)],False),
 ('E',70,73,[(867,390),(911,364),(986,407),(943,433)],False),
 ('F',98,73,[(1008,227),(1045,205),(1194,291),(1158,313)],True),
 ('G',126,69,[(1098,141),(1128,124),(1360,257),(1330,275)],True),
]
footprints=[]
islands=[]
for letter,x,z,pixels,has_return in island_specs:
    source=np.array(pixels,dtype=float)/2+[1080,1020]
    outline=unproject(source,CHECKIN)
    x,z=outline.mean(axis=0)
    local=outline-[x,z]
    # Small clearances within the guide corner-fit uncertainty, shared by all children.
    x += {'D':1.4,'F':-1.4}.get(letter,0)
    width=float(np.ptp(local[:,0]));length=float(np.ptp(local[:,1]))
    islands.append((letter,x,z,length))
    # Separate baggage spines leave the staff aisle open; F/G have a rear return.
    half=max(2.4,width/2-.55)
    for side in [-1,1]:
        side_length=length*(.58 if has_return and side==1 else 1)
        start=z-length/2 if not (has_return and side==1) else z+length/2-side_length
        end=start+side_length
        box('Interior_IslandSpines_'+letter,DARK,(x+side*(half-.6),F2+.16,(start+end)/2),(1.0,.32,side_length))
        n=max(4,int(side_length/2.4))
        for j,zz in enumerate(np.linspace(start+1,end-1,n)):
            counter(x+side*half,zz,letter,j+1+(n if side>0 else 0),side,letter=='C')
        for dx,dy in [(-.45,0),(.45,0),(0,.65)]:
            rod('Interior_CheckInTruss_'+letter,FRAME,(x+side*half+dx,F2+3.10+dy,start),(x+side*half+dx,F2+3.10+dy,end),.035,8)
        for zz in np.arange(start,end-1.4,1.4):
            for dx in [-.45,.45]:rod('Interior_CheckInTruss_'+letter,FRAME,(x+side*half+dx,F2+3.1,zz),(x+side*half,F2+3.75,zz+1.4),.022,6)
        for zz in [start,end]:rod('Interior_CheckInTruss_'+letter,FRAME,(x+side*half,F2,zz),(x+side*half,F2+3.75,zz),.045,8)
        queue(x+side*(half+4.5),start+2,F2,4.5,min(10,side_length-3))
    if has_return:
        box('Interior_CheckInReturn_'+letter,TAUPE,(x,F2+.52,z+length/2),(half*2,1.04,.65))
        box('Interior_CheckInReturn_'+letter,STONE,(x,F2+1.08,z+length/2),(half*2+.16,.08,.78))
    label('Interior_IslandLetters',letter+'  值机区','CHECK-IN',(x,F2+4.15,z+length/2),3,1)
    footprints.append(dict(id=letter,source_polygon_crop_pixels=pixels,source_relative_outline=local.tolist(),width_m=width,length_m=length,center_xz=[x,z],rear_return=has_return,status='guide proportions; counter count, rear equipment and hidden edges inferred'))
    register.append({'id':'island-'+letter,'type':'check-in island','x':x,'z':z,'level':2,'layout_source':'individually traced cyan footprint; blue passenger floor excluded','detail_source':'B island photos; equipment elsewhere inferred','exact_counter_count_verified':False})
(ROOT/'island-footprints.json').write_text(json.dumps(footprints,ensure_ascii=False,indent=2),encoding='utf-8')

# Soffit, mezzanine face, vents and advertisements visible behind B13–B20 in 2024.
for x in [-23.5,84.5]:
    escalator(x,78,62,F2,F3)
    register.append({'id':f'escalator-{x}','type':'paired escalators','level':[2,3],'x':x,'z':[78,62],'note':'placed in inter-island aisles; endpoints estimated, avoid counters and columns'})
for a,b in [(-104,5),(25,147)]:
    box('Interior_GalleryFascia',WHITE,((a+b)/2,F3-.6,61.85),(b-a,1.2,.32))
    for x in np.arange(a+2,b,3):
        disc('Interior_GalleryVents',DARK,(x,F3-.73,62.04),.14,n=18)
        ring('Interior_GalleryVents',STONE,(x,F3-.73,62.07),.18,.06,n=20)
    for x in np.arange(a+8,b-5,20):
        label('Interior_GalleryDisplay','厦门  XIAMEN','CITY / TRAVEL',(x,F3-1.82,62.13),6.5,1.25,color=(27,99,119))
    rail('Interior_GalleryBalustrade',(a,F3,62),(b,F3,62))
box('Roof_CheckInCeiling',CEILING,(C,F2+5.0,79),(252,.12,32))
for x in np.arange(-98,146,6):
    for z in [68,77,86,92]:
        disc('Roof_CheckInDownlights',LIGHT,(x,F2+4.92,z),.13,normal=(0,-1,0),n=12)
        if z==77:box('Roof_CheckInAirGrilles',DARK,(x,F2+4.91,z+2),(.48,.03,.48))

def travelator(a,b,z):
    g='Interior_MovingWalkways'
    box(g,DARK,((a+b)/2,FG+.09,z),(b-a,.18,1.36))
    for x in np.arange(a,b,.40):box(g,FRAME,(x,FG+.195,z),(.018,.018,1.30))
    for side in [-1,1]:
        beam(g,GLASS,(a,FG+.58,z+side*.77),(b,FG+.58,z+side*.77),.07,.82)
        rod(g,DARK,(a,FG+1.03,z+side*.78),(b,FG+1.03,z+side*.78),.045,8)
        beam(g,FRAME,(a,FG+.17,z+side*.79),(b,FG+.17,z+side*.79),.1,.20)
    for x in [a,b]:box(g,FRAME,(x,FG+.09,z),(1.4,.18,1.8))

# Diagram and corridor photo show paired moving walkways along the round windows.
for a,b in [(-367,-309),(-278,-241),(-216,-187),(-160,-130),(172,189),(218,245),(275,306),(331,357)]:
    for z in [7.3,9.7]:travelator(a,b,z)
    register.append({'id':f'walkway-{a}','type':'paired moving walkway','span':[a,b],'level':3,'source':'user diagram + 2017 corridor photo','exact_endpoints_verified':False})
for x in np.arange(-378,383,12):
    rod('Interior_ConcourseColumns',WHITE,(x,FG,3.9),(x,FG+4.7,3.9),.44,16)
    rod('Interior_ConcourseColumns',FRAME,(x,FG,3.9),(x,FG+.55,3.9),.455,16)
    beam('Roof_ConcourseBeams',WHITE,(x,FG+4.9,-11.8),(x,FG+4.9,11.8),.48,.6)
    for z in [-6,0,5]:disc('Roof_ConcourseDownlights',LIGHT,(x+3,FG+5.38,z),.12,normal=(0,-1,0),n=12)
box('Roof_ConcourseInteriorCeiling',CEILING,(-.5,FG+5.45,0),(767,.10,22.8))

def shop(id,x,z,width,depth,kind='shop'):
    g='Interior_Facility_'+id
    # No invented historic shop branding: physical shop fronts only where indicated.
    box(g,WHITE,(x,FG+1.55,z-depth/2),(width,3.1,.15))
    for dx in [-width/2,width/2]:box(g,WHITE,(x+dx,FG+1.55,z),(.14,3.1,depth))
    box(g,WOOD,(x,FG+2.9,z+depth/2),(width,.5,.20))
    box('Roof_FacilityCeilings',CEILING,(x,FG+3.15,z),(width,.12,depth))
    label(g,{'shop':'商店','cafe':'咖啡','lounge':'候机休息室','dutyfree':'免税商店','toilet':'卫生间'}.get(kind,'服务'),kind.upper(),(x,FG+2.9,z+depth/2+.15),min(width-.2,4),.52)
    if kind in ['shop','dutyfree']:
        for dx in [-width*.3,0,width*.3]:
            box(g,WOOD,(x+dx,FG+.45,z),(width*.25,.9,1.0))
            box(g,GLASS,(x+dx,FG+1.13,z),(width*.24,.48,.95))
            for k in range(4):box(g,TAUPE,(x+dx+(k-1.5)*.22,FG+.97,z),(.15,.18,.2))
    elif kind in ['lounge','cafe']:
        for dx in [-width*.27,width*.27]:
            seats(x+dx,z,FG,UPHOLSTERY,3)
            rod(g,FRAME,(x+dx,FG,z+1.4),(x+dx,FG+.67,z+1.4),.05,8)
            rod(g,WOOD,(x+dx,FG+.67,z+1.4),(x+dx,FG+.72,z+1.4),.55,20)
    register.append({'id':id,'type':kind,'x':x,'z':z,'level':3,'layout_source':'user diagram functional blocks, approximate placement','shop_brand_verified':False})

# Distinct blocks are anchored to gate neighborhoods instead of repeated every bay.
facilities=[('west-lounge1',-325,-1,17,5,'lounge'),('west-lounge2',-265,-1,22,5,'lounge'),('west-cafe',-236,-1,10,4,'cafe'),('gate5-shop',-187,-1,9,4,'shop'),('gate6-lounge',-132,-1,15,5,'lounge'),('gate7-shop',-90,-1,10,4,'shop'),('gate8-shop',-18,-1,12,4,'shop'),('gate9-service',98,-1,12,4,'shop'),('gate10-dutyfree',168,-1,15,5,'dutyfree'),('gate11-dutyfree',225,-1,14,5,'dutyfree'),('gate12-cafe',281,-1,11,4,'cafe'),('gate15-shop',302,-1,9,4,'shop'),('gate16-service',351,-1,10,4,'shop')]
for f in facilities:shop(*f)
for gate in mapping['gates']:
    n=int(gate['tags'].get('ref','0'))
    if n not in gate_numbers:continue
    x,z=gate['point'];z=-8
    box('Interior_GateCounter',TAUPE,(x,FG+.55,z),(2.4,1.1,.8))
    box('Interior_GateCounter',STONE,(x,FG+1.12,z),(2.55,.08,.92))
    label('Interior_GateLocationSigns',f'{n:02d}  登机口',f'GATE {n:02d}',(x,FG+2.7,z),3,.7)
    for dx in [-1.7,1.7]:
        box('Interior_GateReaders',FRAME,(x+dx,FG+.48,z-1.3),(.24,.96,.35))
        box('Interior_GateReaders',SCREEN,(x+dx,FG+1.0,z-1.3),(.20,.08,.28))
    # Keep the continuous landside walkway clear; seats occupy airside gate bays.
    for dx in [-8,-4,4,8]:
        for zz in [-4.7,-2.5]:seats(x+dx,zz,FG,SEAT,4)

# Small service fixtures visible in corridor photographs.
for x in np.arange(wx-44,wx+48,8):
    for z in [wz-8,wz-4,wz+4,wz+8]:seats(x,z,.28,TAN)
for x in [-60,5,55,115]:
    for dx in [-2,0,2]:
        box('Interior_SelfCheckInKiosks',WHITE,(x+dx,F2+.63,91),(.55,1.26,.48))
        box('Interior_SelfCheckInKiosks',SCREEN,(x+dx,F2+1.35,91.1),(.5,.42,.055))
        box('Interior_SelfCheckInKiosks',DARK,(x+dx,F2+.96,91.26),(.28,.035,.035))
# Information desk and baggage wrapping: diagram-supported functions, equipment inferred.
box('Interior_InformationDesk',TAUPE,(10,F2+.52,87),(4.5,1.04,1.2))
label('Interior_InformationDesk','问询服务','INFORMATION',(10,F2+1.7,87.7),3.2,.65)
for x in [-95,138]:
    rod('Interior_BaggageWrapping',FRAME,(x,F2+.08,87),(x,F2+.16,87),.85,24)
    box('Interior_BaggageWrapping',WHITE,(x+1,F2+.85,87),(.35,1.7,.5))
    rod('Interior_BaggageWrapping',FRAME,(x+1,F2+.5,87),(x+1,F2+1.4,87),.14,12)
for x in [-310,-242,-150,-90,190,280,340]:
    rod('Interior_Bins',FRAME,(x,FG,4.3),(x,FG+.84,4.3),.23,18)
    rod('Interior_Bins',DARK,(x,FG+.845,4.3),(x,FG+.87,4.3),.17,18)
for a,b in [(-375,-108),(152,377)]:
    for x in np.arange(a,b,3):box('Interior_ConcourseTileInlay',TRIM,(x,FG+.012,-2),(.06,.018,19))
    for z in [-10,-5,0,4]:box('Interior_ConcourseTileInlay',TRIM,((a+b)/2,FG+.012,z),(b-a,.018,.06))

exec(compile((ROOT/'circulation_detail.py').read_text(encoding='utf-8'),str(ROOT/'circulation_detail.py'),'exec'))
exec(compile((ROOT/'fixes.py').read_text(encoding='utf-8'),str(ROOT/'fixes.py'),'exec'))
exec(compile((ROOT/'exterior_detail.py').read_text(encoding='utf-8'),str(ROOT/'exterior_detail.py'),'exec'))
exec(compile((ROOT/'roof16.py').read_text(encoding='utf-8'),str(ROOT/'roof16.py'),'exec'))
exec(compile((ROOT/'interior_audit.py').read_text(encoding='utf-8'),str(ROOT/'interior_audit.py'),'exec'))
exec(compile((ROOT/'repair_interior.py').read_text(encoding='utf-8'),str(ROOT/'repair_interior.py'),'exec'))
exec(compile((ROOT/'exit_routes.py').read_text(encoding='utf-8'),str(ROOT/'exit_routes.py'),'exec'))
exec(compile((ROOT/'zone_separation.py').read_text(encoding='utf-8'),str(ROOT/'zone_separation.py'),'exec'))
exec(compile((ROOT/'arrivals_detail.py').read_text(encoding='utf-8'),str(ROOT/'arrivals_detail.py'),'exec'))
exec(compile((ROOT/'supported_guards.py').read_text(encoding='utf-8'),str(ROOT/'supported_guards.py'),'exec'))
exec(compile((ROOT/'facility_footprints.py').read_text(encoding='utf-8'),str(ROOT/'facility_footprints.py'),'exec'))
exec(compile((ROOT/'border14.py').read_text(encoding='utf-8'),str(ROOT/'border14.py'),'exec'))
exec(compile((ROOT/'doors_and_sides.py').read_text(encoding='utf-8'),str(ROOT/'doors_and_sides.py'),'exec'))
exec(compile((ROOT/'west_stair_fix.py').read_text(encoding='utf-8'),str(ROOT/'west_stair_fix.py'),'exec'))
exec(compile((ROOT/'envelope11.py').read_text(encoding='utf-8'),str(ROOT/'envelope11.py'),'exec'))
exec(compile((ROOT/'facade13.py').read_text(encoding='utf-8'),str(ROOT/'facade13.py'),'exec'))
exec(compile((ROOT/'finish_geometry14.py').read_text(encoding='utf-8'),str(ROOT/'finish_geometry14.py'),'exec'))
exec(compile((ROOT/'facade17.py').read_text(encoding='utf-8'),str(ROOT/'facade17.py'),'exec'))
exec(compile((ROOT/'guide_spaces.py').read_text(encoding='utf-8'),str(ROOT/'guide_spaces.py'),'exec'))
exec(compile((ROOT/'sign_mounts.py').read_text(encoding='utf-8'),str(ROOT/'sign_mounts.py'),'exec'))
assert len(text_items)<=256
atlas2=Image.new('RGB',(2048,8192),(12,25,28));painter=ImageDraw.Draw(atlas2)
for i,(cn,en,color) in enumerate(text_items):
    xx=(i%4)*512;yy=(i//4)*128
    painter.rectangle((xx,yy,xx+511,yy+127),fill=color)
    painter.text((xx+14,yy+12),cn,font=ImageFont.truetype(fontpath,38),fill=(244,245,224))
    painter.text((xx+15,yy+80),en,font=ImageFont.truetype(fontpath,22),fill=(197,217,208))
atlas2.save(ROOT/'interior-signage.png');texture_images.append(ROOT/'interior-signage.png')
materials[TEXT_MAT]['pbrMetallicRoughness']['baseColorTexture']={'index':len(texture_images)}
(ROOT/'interior-register.json').write_text(json.dumps(register,ensure_ascii=False,indent=2),encoding='utf-8')
