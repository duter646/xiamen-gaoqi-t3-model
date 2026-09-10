"""Remove physical glazing and roof obstructions on the west descent."""
west=next(r for r in records if r['id']=='L3-E01')
x,y,z=west['position']
def clip_polygon(poly,axis,bound,less):
    out=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        ina=a[axis]<=bound if less else a[axis]>=bound
        inb=b[axis]<=bound if less else b[axis]>=bound
        if ina:out.append(a)
        if ina!=inb:
            t=(bound-a[axis])/(b[axis]-a[axis]);out.append(a+(b-a)*t)
    return out
def subtract_box(groupnames,lo,hi):
    for key,data in list(groups.items()):
        if key[0] not in groupnames:continue
        old=groups.pop(key);offset=0
        for vv,ff,uv in zip(old['v'],old['f'],old['uv']):
            ff=ff-offset;offset+=len(vv)
            if (vv.max(axis=0)<lo).any() or (vv.min(axis=0)>hi).any():mesh(*key,vv,ff,uv);continue
            for f in ff:
                pending=[np.concatenate([vv[i],uv[i]]) for i in f];outside=[]
                for axis in range(3):
                    for bound,inside_less in [(lo[axis],False),(hi[axis],True)]:
                        if not pending:break
                        part=clip_polygon(pending,axis,bound,not inside_less)
                        if len(part)>=3:outside.append(part)
                        pending=clip_polygon(pending,axis,bound,inside_less)
                for part in outside:
                    array=np.array(part);mesh(*key,array[:,:3],[(0,i,i+1) for i in range(1,len(part)-1)],array[:,3:])

subtract_box({'Facade_EndGlazing','Facade_EndGrid'},np.array([X0-.5,F3-.02,z-2]),np.array([X0+.5,F3+3.1,z+2]))
for door in doors:
    subtract_box({'Facade_StonePiers'},np.array([door['x']-2.1,door['bottom'],95]),np.array([door['x']+2.1,door['top'],97]))
for key in list(groups):
    if key[0]=='Roof_West2024':del groups[key]
floor_with_holes('Roof_West2024',7.325,wx-50.5,wx+50.5,wz-13.5,wz+13.5,[(x-14,x+2,z-2,z+2)],WHITE)
for zz in [z-2,z+2]:box('Facade_WestStairDoorFrame',FRAME,(X0,F3+1.5,zz),(.22,3,.12))
box('Facade_WestStairDoorFrame',FRAME,(X0,F3+3.05,z),(.22,.12,4.1))
# Landing across the short gap between end facade and the west connection slab.
box('Structure_WestStairDoorThreshold',FLOOR,(X0,F3-.1,z),(1.0,.2,4))
(ROOT/'west-stair-register.json').write_text(json.dumps(dict(upper=west['position'],lower=west['lower_landing'],main_hall_door=dict(x=X0,z=z,width=4,height=3.1),note='Continuous west descent to the existing indicative annex floor; no new arrival escalator group'),indent=2),encoding='utf-8')
