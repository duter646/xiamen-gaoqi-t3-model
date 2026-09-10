from pathlib import Path
import json,struct,numpy as np
R=Path(__file__).resolve().parent
blob=(R/'xiamen-gaoqi-t3.glb').read_bytes();n=struct.unpack_from('<I',blob,12)[0];doc=json.loads(blob[20:20+n]);off=28+n
obstacles=[];floors=[]
for node in doc['nodes']:
    name=node['name'];p=doc['meshes'][node['mesh']]['primitives'][0];a=doc['accessors'][p['attributes']['POSITION']];v=doc['bufferViews'][a['bufferView']]
    tri=np.frombuffer(blob,dtype='<f4',count=a['count']*3,offset=off+v.get('byteOffset',0)).reshape(-1,3,3)
    lo=tri.min(axis=1);hi=tri.max(axis=1)
    if name.startswith(('Structure_ThirdFloor','Structure_ConcourseFloor','Structure_ArrivalLanding')):floors.append(tri)
    if not name.startswith(('Interior_','Structure_','Facade_','Roof_')):continue
    good=(hi[:,1]>12.25)&(lo[:,1]<13.86)&(hi[:,0]>-45)&(lo[:,0]<137)&(hi[:,2]>4)&(lo[:,2]<63)
    if good.any():obstacles.append((name,tri[good].astype(float),lo[good],hi[good]))
floortri=np.concatenate(floors).astype(float)
def hit_segment(tri,origin,direction,length):
    aa=tri[:,0];e1=tri[:,1]-aa;e2=tri[:,2]-aa;p=np.cross(direction,e2);det=np.einsum('ij,ij->i',e1,p)
    valid=np.abs(det)>1e-9
    if not valid.any():return False
    e1=e1[valid];e2=e2[valid];p=p[valid];inv=1/det[valid];tv=origin-aa[valid]
    u=np.einsum('ij,ij->i',tv,p)*inv;q=np.cross(tv,e1);v=np.einsum('j,ij->i',direction,q)*inv;t=np.einsum('ij,ij->i',e2,q)*inv
    return bool(((u>=-1e-7)&(v>=-1e-7)&(u+v<=1+1e-7)&(t>=0)&(t<=length)).any())
def supported(point):
    x,z=point;lo=floortri.min(axis=1);hi=floortri.max(axis=1)
    m=(lo[:,0]<=x)&(hi[:,0]>=x)&(lo[:,2]<=z)&(hi[:,2]>=z)
    return hit_segment(floortri[m],np.array([x,12.2,z]),np.array([0.,-1,0]),.35)
paths=json.loads((R/'security-exit-paths.json').read_text(encoding='utf-8'));results=[]
for path in paths:
    collisions=[];unsupported=[]
    for si,(p0,p1) in enumerate(zip(path['points'],path['points'][1:])):
        a=np.array([p0[0],0,p0[1]],float);b=np.array([p1[0],0,p1[1]],float);length=np.linalg.norm(b-a)
        if length<.01:continue
        direction=(b-a)/length;normal=np.array([-direction[2],0,direction[0]])
        for lateral in [-.34,0,.34]:
            start=a+normal*lateral;end=b+normal*lateral
            for y in [12.3,13.0,13.8]:
                origin=start+[0,y,0];low=np.minimum(start,end)+[0,y-.01,0];high=np.maximum(start,end)+[0,y+.01,0]
                for name,t,lo,hi in obstacles:
                    m=np.all(hi>=low,axis=1)&np.all(lo<=high,axis=1)
                    if m.any() and hit_segment(t[m],origin,direction,length):collisions.append({'segment':si,'mesh':name,'lateral':lateral,'height':y})
            for u in np.linspace(0,1,max(2,int(length/.5)+1)):
                pos=start*(1-u)+end*u
                if not supported(pos[[0,2]]):unsupported.append(np.round(pos[[0,2]],3).tolist())
    results.append(dict(id=path['id'],passed=not collisions and not unsupported,collisions=collisions,unsupported_floor_samples=unsupported))
out=dict(body_width_m=.68,heights_y=[12.3,13.0,13.8],floor_sampling_m=.5,paths=len(results),passed=sum(r['passed'] for r in results),results=results)
(R/'security-all-geometry-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(paths=len(results),passed=out['passed'],failures=[dict(id=r['id'],collisions=r['collisions'][:8],unsupported=r['unsupported_floor_samples'][:3]) for r in results if not r['passed']]),ensure_ascii=False))
assert out['passed']==len(results),'At least one complete screening exit path is blocked'

