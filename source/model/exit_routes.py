"""Explicit paths through EACH scanner portal, pickup area and sterile corridor."""
for key in list(groups):
    if key[0].startswith('Audit_Route_'):del groups[key]
paths=[]
for r in records:
    if r['kind']!='security lane':continue
    x,_,z=r['position'];dom=r['id'].startswith('SEC-D')
    if dom:
        pts=[[x,z+3.7],[x,z],[x,z-3.3],[x+.8,z-3.3],[x+.8,32.9],[-25,32.9],[-25,5.5]]
    else:
        pts=[[x-3.7,z],[x,z],[x+3.3,z],[x+3.3,z+.8],[134,z+.8],[134,5.5]]
    paths.append(dict(id=r['id'],points=pts,level_y=F3,steps=['approach','portal','pickup','post-screening corridor','gate concourse']))
    for a,b in zip(pts,pts[1:]):
        if np.linalg.norm(np.array(a)-b)<.01:continue
        beam('Audit_Exit_'+r['id'],LIME,(a[0],F3+.045,a[1]),(b[0],F3+.045,b[1]),.12,.015)
label('Interior_ExitWayfinding','取行李后前往登机口 →','GATES / AFTER BAG PICKUP',(-24,F3+2.8,32.0),6,.6)
(ROOT/'security-exit-paths.json').write_text(json.dumps(paths,ensure_ascii=False,indent=2),encoding='utf-8')
