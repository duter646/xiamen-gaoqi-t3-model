"""Check every bridge root against the freshly exported triangles, including exterior meshes."""
from pathlib import Path
import json,struct,hashlib,numpy as np
root=Path(__file__).resolve().parent
raw=(root/'xiamen-gaoqi-t3.glb').read_bytes()
n=struct.unpack_from('<I',raw,12)[0];doc=json.loads(raw[20:20+n]);offset=28+n
meshes=[]
for node in doc['nodes']:
    name=node['name']
    if name.startswith(('Audit_','Site_')):continue
    for prim in doc['meshes'][node['mesh']]['primitives']:
        a=doc['accessors'][prim['attributes']['POSITION']];v=doc['bufferViews'][a['bufferView']]
        t=np.frombuffer(raw,dtype='<f4',count=a['count']*3,offset=offset+v.get('byteOffset',0)+a.get('byteOffset',0)).reshape(-1,3,3).astype(float)
        assert np.isfinite(t).all(),name
        meshes.append((name,t,t.min(1),t.max(1)))
def hits(start,end):
    start,end=np.array(start),np.array(end);direction=end-start;length=np.linalg.norm(direction);direction/=length
    found=[]
    for name,t,lo,hi in meshes:
        selected=np.all(hi>=np.minimum(start,end),1)&np.all(lo<=np.maximum(start,end),1)
        q=t[selected]
        if not len(q):continue
        e1=q[:,1]-q[:,0];e2=q[:,2]-q[:,0];p=np.cross(direction,e2);det=(e1*p).sum(1);valid=abs(det)>1e-9
        if not valid.any():continue
        e1,e2,p,inv=e1[valid],e2[valid],p[valid],1/det[valid];s=start-q[valid,0]
        u=(s*p).sum(1)*inv;r=np.cross(s,e1);v=(r*direction).sum(1)*inv;dist=(e2*r).sum(1)*inv
        if ((u>=-1e-6)&(v>=-1e-6)&(u+v<=1.000001)&(dist>1e-5)&(dist<length-1e-5)).any():found.append(name)
    return found
report=json.loads((root/'concourse-repair.json').read_text())
errors=[];checks=[]
for gate in report['portals']:
    x,y,z=gate['root']
    for dx in (-1,0,1):
        for dy in (.4,1.2,2.3):
            collision=hits((x+dx,y+dy,z+1),(x+dx,y+dy,z-1))
            if collision:errors.append({'gate':gate['gate'],'type':'blocked root','offset':[dx,dy],'meshes':collision})
        for dz in (-.5,0,.5):
            if not hits((x+dx,y+.1,z+dz),(x+dx,y-.35,z+dz)):errors.append({'gate':gate['gate'],'type':'floor gap','offset':[dx,dz]})
    checks.append(gate['gate'])
for y in (12.6,14,16):
    for z in (-10,0,13):
        if not hits((420.8,y,z),(422,y,z)):errors.append({'type':'east wall missing','y':y,'z':z})
for x in (-378,-362,-346):
    if not hits((x,13.5,-11),(x,13.5,-14)):errors.append({'type':'west exterior volume not isolated','x':x})
out={'model_sha256':hashlib.sha256(raw).hexdigest(),'gates_checked':checks,'portal_body_samples':len(checks)*9,'portal_support_samples':len(checks)*9,'east_wall_samples':9,'west_isolation_samples':3,'errors':errors}
(root/'concourse-validation.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2));assert not errors
