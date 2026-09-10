"""Actual apertures, not transparent panes placed across entries."""
for key in list(groups):
    if key[0]=='Facade_Entrance':del groups[key]
doors=[]
for y,numbers,centers in [(F1,[11,9,7,5,3,1],[-90,-47,-4,39,82,125]),(F2,[12,10,8,6,4,2],[-90,-47,-4,39,82,125])]:
    for num,x in zip(numbers,centers):doors.append(dict(level=1 if y==F1 else 2,number=num,x=x,bottom=y,top=y+2.8,width=4.2))
xs=sorted(set([X0,X1]+[v for d in doors for v in [d['x']-2.1,d['x']+2.1]]))
ys=sorted(set([.2,12.7]+[v for d in doors for v in [d['bottom'],d['top']]]))
for a,b in zip(xs,xs[1:]):
    for c,d in zip(ys,ys[1:]):
        xx=(a+b)/2;yy=(c+d)/2
        if any(abs(xx-q['x'])<2.1 and q['bottom']<yy<q['top'] for q in doors):continue
        box('Facade_EntranceWithOpenDoors',GLASS,(xx,yy,96),(b-a,d-c,.10))
for door in doors:
    x,y=door['x'],door['bottom']
    for dx in [-2.15,2.15]:box('Facade_OpenEntranceFrames',FRAME,(x+dx,y+1.4,96),(.1,2.8,.18))
    box('Facade_OpenEntranceFrames',FRAME,(x,y+2.85,96),(4.4,.1,.18))
    # Open sliding leaves are parked to the sides of the clear aperture.
    for side in [-1,1]:box('Facade_OpenSlidingLeaves',GLASS,(x+side*3.1,y+1.4,96.2),(1.9,2.75,.06))
    box('Structure_EntranceThresholds',FLOOR,(x,y-.07,96),(4.2,.14,.9))

# Solid 1F end walls; west passage opens toward the adjacent waiting extension.
for x in [X0,X1]:
    spans=[(12,34),(42,96)] if x==X0 else [(12,96)]
    for a,b in spans:box('Facade_ArrivalSideWalls',WHITE,(x,3.3,(a+b)/2),(.3,6.0,b-a))
    if x==X0:box('Facade_WestConnectionLintel',WHITE,(x,4.85,38),(.3,2.9,8))

# Existing west annex end panel also needs the matching clear doorway.
for key,data in list(groups.items()):
    if key[0]!='Unverified_West2024End':continue
    keep=[i for i,v in enumerate(data['v']) if abs(v[:,0].mean()-(wx+50))>.5]
    rebuild_group(key,keep)
for a,b in [(wz-13,34),(42,wz+13)]:box('Unverified_West2024OpenEnd',WHITE,(wx+50,3.5,(a+b)/2),(.35,7,b-a))
box('Unverified_West2024OpenEnd',WHITE,(wx+50,5.2,38),(.35,3.6,8))
box('Structure_WestConnectionThreshold',FLOOR,(-104.75,.18,38),(1.5,.24,8))
(ROOT/'door-register.json').write_text(json.dumps(dict(street_doors=doors,west_connection=dict(x=-104.75,z_range=[34,42],clear_height=3.4),side_walls='1F both ends; west connection retained'),ensure_ascii=False,indent=2),encoding='utf-8')
