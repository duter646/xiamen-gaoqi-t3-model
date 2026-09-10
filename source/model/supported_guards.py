"""Regenerate guards on the union of floor openings, never across an open void."""
rects=[]
for (name,mat),data in groups.items():
    if name.startswith(('Structure_ThirdFloor','Structure_ConcourseFloor','Structure_ArrivalLanding','Structure_WestConnectionLanding')):
        for v in data['v']:
            if abs(v[:,1].max()-F3)<.01:rects.append((v[:,0].min(),v[:,0].max(),v[:,2].min(),v[:,2].max()))
rects=np.array(rects)
def solid(x,z):
    return bool(((rects[:,0]-1e-5<=x)&(rects[:,1]+1e-5>=x)&(rects[:,2]-1e-5<=z)&(rects[:,3]+1e-5>=z)).any())
for key in list(groups):
    if key[0] in ['Interior_AtriumGuardrails','Interior_AtriumGlass','Interior_ArrivalBridgeRails']:del groups[key]
# Remove the helper's untrimmed top rails; the new guards follow actual slabs.
for key,data in list(groups.items()):
    if not key[0].startswith(('Interior_Circulation_L3-E','Interior_Circulation_ARR-UP')):continue
    keep=[]
    for i,v in enumerate(data['v']):
        low,high=v[:,1].min(),v[:,1].max()
        vertical=abs(low-F3)<.01 and abs(high-(F3+1.1))<.01
        horizontal=(high-low<.13 and (abs(v[:,1].mean()-F3-1.1)<.02 or abs(v[:,1].mean()-F3-.45)<.02))
        if not vertical and not horizontal:keep.append(i)
    rebuild_group(key,keep)
segments=[];seen=set()
for hi,h in enumerate(holes):
    if max(h[1]-h[0],h[3]-h[2])<4:continue
    for axis,value,low,high in [(0,h[2],h[0],h[1]),(0,h[3],h[0],h[1]),(2,h[0],h[2],h[3]),(2,h[1],h[2],h[3])]:
        if hi<len(holes)-3 and axis!=(0 if h[1]-h[0]>h[3]-h[2] else 2):continue
        breaks=sorted(set([low,high]+[float(q) for q in rects[:,0:2 if axis==0 else 4].flat if low<q<high])) if axis==0 else sorted(set([low,high]+[float(q) for q in rects[:,2:4].flat if low<q<high]))
        for a,b in zip(breaks,breaks[1:]):
            if b-a<.15:continue
            mid=(a+b)/2
            minus=solid(mid,value-.12) if axis==0 else solid(value-.12,mid)
            plus=solid(mid,value+.12) if axis==0 else solid(value+.12,mid)
            if minus==plus:continue
            v=value+(.10 if plus else -.10)
            start=[a,F3,v] if axis==0 else [v,F3,a]
            end=[b,F3,v] if axis==0 else [v,F3,b]
            key=tuple(round(q,3) for q in start+end)
            if key in seen:continue
            seen.add(key);rail('Interior_SupportedOpeningGuards',start,end)
            beam('Interior_SupportedOpeningGlass',ARR_GLASS,np.array(start)+[0,.55,0],np.array(end)+[0,.55,0],.045,.88)
            segments.append(dict(start=start,end=end))
(ROOT/'supported-guards.json').write_text(json.dumps(segments,indent=2),encoding='utf-8')
unsupported=[]
for i,segment in enumerate(segments):
    a=np.array(segment['start']);b=np.array(segment['end'])
    for t in np.linspace(.01,.99,20):
        p=a*(1-t)+b*t
        if not solid(p[0],p[2]):unsupported.append(i)
assert not unsupported,('Unsupported opening guards',unsupported)
(ROOT/'guard-support-validation.json').write_text(json.dumps(dict(segments=len(segments),samples_per_segment=20,unsupported=unsupported,scope='Regenerated 3F opening guards supported by current floor union'),indent=2),encoding='utf-8')
