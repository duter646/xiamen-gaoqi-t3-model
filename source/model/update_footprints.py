from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'interior_detail.py'
s=p.read_text(encoding='utf-8')
a=s.index('# Seven correctly differentiated')
b=s.index('# Soffit, mezzanine',a)
s=s[:a]+'''# Individual cyan counter footprints traced from the supplied guide, not its blue circulation floor.
# Pixel coordinates refer to islands-reference.png (2x crop of the original).
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
    source=np.array(pixels,dtype=float)/2
    inverse=np.linalg.inv(np.array([[2.39,2.35],[-1.42,1.40]]))
    local=(inverse@source.T).T
    local-=local.mean(axis=0)
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

'''+s[b:]
p.write_text(s,encoding='utf-8')
p=R/'zone_separation.py';s=p.read_text(encoding='utf-8');s=s[:s.index('# Remove free column')]+'''# Fit every top vertex to the actual roof soffit triangles, preserving the original radius.
soffit=[]
for (name,mat),data in groups.items():
    if name!='Roof_MainSoffit':continue
    vv=np.concatenate(data['v']);ff=np.concatenate(data['f'])
    soffit.extend(vv[ff])
rooftri=np.array(soffit)
connections=[]
def soffit_height(x,z):
    hits=[]
    for tri in rooftri:
        a,b,c=tri
        matrix=np.array([[b[0]-a[0],c[0]-a[0]],[b[2]-a[2],c[2]-a[2]]])
        if abs(np.linalg.det(matrix))<1e-8:continue
        u,v=np.linalg.solve(matrix,[x-a[0],z-a[2]])
        if u>=-1e-6 and v>=-1e-6 and u+v<=1.000001:hits.append(a[1]+u*(b[1]-a[1])+v*(c[1]-a[1]))
    if not hits:raise ValueError(('No roof above column',x,z))
    return min(hits)
for (name,mat),data in groups.items():
    if name!='Structure_Columns':continue
    for vertices in data['v']:
        top=vertices[:,1].max();mask=vertices[:,1]>top-1e-5
        for vertex in vertices[mask]:
            pass
        for index in np.flatnonzero(mask):
            vertex=vertices[index];vertex[1]=soffit_height(vertex[0],vertex[2])
        connections.append(dict(center_xz=[float(vertices[:,0].mean()),float(vertices[:,2].mean())],top_vertices=int(mask.sum()),max_gap_m=max(abs(float(v[1])-soffit_height(v[0],v[2])) for v in vertices[mask])))
(ROOT/'column-connections.json').write_text(json.dumps(connections,indent=2),encoding='utf-8')
(ROOT/'zone-boundary.json').write_text(json.dumps(dict(points_xz=boundary,height_m=5.3,status='functional reconstruction; exact historic divider alignment unverified'),ensure_ascii=False,indent=2),encoding='utf-8')
''';s=s.replace("        for vertex in vertices[mask]:\n            pass\n",'');p.write_text(s,encoding='utf-8')
p=R/'check_revision.py';s=p.read_text(encoding='utf-8').replace("assert unchanged,'Accepted check-in island geometry changed'","assert not unchanged,'Individual island reconstruction was not applied'")
s=s.replace("'accepted_checkin_geometry_unchanged':unchanged","'islands_individually_rebuilt':not unchanged")
p.write_text(s,encoding='utf-8')
