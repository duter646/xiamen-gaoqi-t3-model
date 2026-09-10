"""Trace visible top-face outlines; icons and circulation fills are not walls."""
specs={
 'D-SH01':[(420,631),(476,598),(550,617),(550,631),(536,638),(483,623),(447,651)],
 'D-SH02':[(444,657),(479,639),(528,644),(539,654),(538,666),(500,683),(444,677)],
 'D-SH03':[(378,813),(441,776),(395,747),(395,729),(565,666),(605,666),(630,683),(478,773)],
 'D-CF01':[(305,785),(340,768),(361,771),(360,784),(331,801),(307,797)],
 'I-SH01':[(1141,104),(1180,82),(1246,116),(1244,132),(1199,153),(1159,132)]
}
inventory=[]
caps=[]
def triangulate_polygon(poly):
    cross=lambda a,b:float(a[0]*b[1]-a[1]*b[0])
    indices=list(range(len(poly)))
    if sum(cross(poly[i],poly[(i+1)%len(poly)]) for i in indices)<0:indices.reverse()
    triangles=[]
    while len(indices)>3:
        for k,b in enumerate(indices):
            a=indices[k-1];c=indices[(k+1)%len(indices)]
            if cross(poly[b]-poly[a],poly[c]-poly[b])<=1e-8:continue
            def inside(p):return all(cross(v-u,p-u)>=-1e-8 for u,v in [(poly[a],poly[b]),(poly[b],poly[c]),(poly[c],poly[a])])
            if any(inside(poly[j]) for j in indices if j not in [a,b,c]):continue
            triangles.append((a,b,c));indices.pop(k);break
        else:raise ValueError('Invalid traced facility polygon')
    return triangles+[tuple(indices)]
for id,pixels in specs.items():
    rec=next(r for r in records if r['id']==id);cx,y,cz=rec['position'];width,depth=rec['footprint_estimated']
    cz+=dict({'D-SH01':2.0,'D-SH02':1.2,'D-SH03':-1.4,'I-SH01':1.2}).get(id,0)
    vertices=np.array(pixels,dtype=float)/2
    local=(np.linalg.inv(np.array([[2.39,2.35],[-1.42,1.4]]))@vertices.T).T
    local-=(local.min(axis=0)+local.max(axis=0))/2
    # Keep the existing building anchor; no surveyed metric scale in the diagram.
    local*=np.array([width,depth])/np.ptp(local,axis=0)
    poly=local+[cx,cz]
    caps.append((id,poly,triangulate_polygon(poly)))
    name='Interior_Circulation_'+id
    for key in list(groups):
        if key[0]==name:del groups[key]
    # Locate the frontage edge facing the public forecourt; split it for a door.
    front=max(range(len(poly)),key=lambda i:(poly[i,1]+poly[(i+1)%len(poly),1])/2)
    for i,a in enumerate(poly):
        b=poly[(i+1)%len(poly)];v=b-a;length=np.linalg.norm(v)
        if i==front and length>2.3:
            u=v/length;mid=(a+b)/2
            for aa,bb in [(a,mid-u*.95),(mid+u*.95,b)]:wall(name,aa,bb,F3,2.9)
            wall(name,mid-u*.95,mid+u*.95,F3+2.25,.65,WOOD)
            label(name,'咖啡' if id=='D-CF01' else '商店',id,((a[0]+b[0])/2,F3+2.65,(a[1]+b[1])/2+.12),min(3.5,length),.45)
        else:wall(name,a,b,F3,2.9)
    # A thin floor contour makes the traced recesses reviewable in plan view.
    for a,b in zip(poly,np.roll(poly,-1,axis=0)):beam('Interior_FacilityFootprintEdges',WOOD,(a[0],F3+.03,a[1]),(b[0],F3+.03,b[1]),.08,.035)
    inventory.append(dict(id=id,status='visible outline individually traced; metric scale and hidden edges estimated',source='facility-reference.png; crop x910 y630, scale2',source_pixels=pixels,world_outline_xz=poly.tolist(),front_edge=front))

# Remove oversized rectangular caps left by the previous generic room generator.
for key,data in list(groups.items()):
    if key[0]=='Roof_LocalShopCeilings':del groups[key]
for id,poly,tri in caps:mesh('Roof_TracedFacilityCeiling_'+id,CEILING,[(x,F3+2.98,z) for x,z in poly],tri)

# Complete the inventory without falsely marking obscured footprints verified.
for r in register:
    if r.get('type') in ['shop','cafe','lounge','dutyfree','toilet']:
        inventory.append(dict(id=r['id'],status='functional anchor checked; full wall outline obscured or absent in guide, not verified',position_xz=[r['x'],r['z']]))
for r in footprints:inventory.append(dict(id='island-'+r['id'],status='counter outline traced; rear construction partly inferred',source_pixels=r['source_polygon_crop_pixels']))
for r in arrival_inventory:
    if r.get('type')=='service room':inventory.append(dict(id=r['id'],status='approximate guide-based service outline; exact footprint not verified',outline=r['outline']))
(ROOT/'facility-footprint-audit.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'footprint-column-audit.json').write_text(json.dumps(column_hits(),indent=2),encoding='utf-8')
