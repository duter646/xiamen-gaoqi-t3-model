# A continuous passenger separation boundary, without an uncontrolled shortcut
# between domestic and international gates. Bends keep the immigration bank east.
boundary=[[20.2,-12.5],[20.2,16.4]]  # between mapped gates 8 (x=5.73) and 9 (x=81.46)
arrival_boundary=[[23.25,16.4],[75,16.4],[75,15.8],[93.3,15.8],[93.3,30.3],[75,30.3],[75,48],[45,65],[45,96]]
for a,b in zip(arrival_boundary,arrival_boundary[1:]):partition(a,b,'Interior_ZoneSeparation',3.0)
for a,b in zip(boundary,boundary[1:]):partition(a,b,'Interior_ZoneSeparation',3.0)
label('Interior_ZoneSeparationSigns','国内候机区','DOMESTIC GATES',(20.0,F3+2.8,7),4.2,.65,'z')
label('Interior_ZoneSeparationSigns','国际候机区','INTERNATIONAL GATES',(20.4,F3+2.8,7),4.2,.65,'z')
# Fit every top vertex to the actual roof soffit triangles, preserving the original radius.
soffit=[]
for (name,mat),data in groups.items():
    if name!='Roof_MainSoffit':continue
    vv=np.concatenate(data['v']);ff=np.concatenate(data['f'])
    soffit.extend(vv[ff])
rooftri=np.array(soffit)
connections=[]
def soffit_height(x,z):
    a=rooftri[:,0];b=rooftri[:,1]-a;c=rooftri[:,2]-a
    det=b[:,0]*c[:,2]-b[:,2]*c[:,0]
    valid=abs(det)>1e-8;safe=np.where(valid,det,1)
    u=((x-a[:,0])*c[:,2]-(z-a[:,2])*c[:,0])/safe
    v=(b[:,0]*(z-a[:,2])-b[:,2]*(x-a[:,0]))/safe
    hit=valid&(u>=-1e-6)&(v>=-1e-6)&(u+v<=1.000001)
    if not hit.any():raise ValueError(('No roof above column',x,z))
    return float((a[:,1]+u*b[:,1]+v*c[:,1])[hit].min())
for (name,mat),data in groups.items():
    if name!='Structure_Columns':continue
    for vertices in data['v']:
        top=vertices[:,1].max();mask=vertices[:,1]>top-1e-5
        for index in np.flatnonzero(mask):
            vertex=vertices[index];vertex[1]=soffit_height(vertex[0],vertex[2])
        connections.append(dict(center_xz=[float(vertices[:,0].mean()),float(vertices[:,2].mean())],top_vertices=int(mask.sum()),max_gap_m=max(abs(float(v[1])-soffit_height(v[0],v[2])) for v in vertices[mask])))
(ROOT/'column-connections.json').write_text(json.dumps(connections,indent=2),encoding='utf-8')
(ROOT/'zone-boundary.json').write_text(json.dumps(dict(points_xz=boundary,height_m=5.3,status='functional reconstruction; exact historic divider alignment unverified'),ensure_ascii=False,indent=2),encoding='utf-8')
