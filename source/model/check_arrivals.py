from pathlib import Path
import json,struct,numpy as np
R=Path(__file__).resolve().parent
b=(R/'xiamen-gaoqi-t3.glb').read_bytes();n=struct.unpack_from('<I',b,12)[0];d=json.loads(b[20:20+n]);offset=28+n
meshes=[]
for node in d['nodes']:
    name=node['name']
    if name.startswith(('Audit_','Site_','Exterior_')):continue
    p=d['meshes'][node['mesh']]['primitives'][0];a=d['accessors'][p['attributes']['POSITION']];v=d['bufferViews'][a['bufferView']]
    t=np.frombuffer(b,dtype='<f4',count=a['count']*3,offset=offset+v.get('byteOffset',0)).reshape(-1,3,3).astype(float)
    meshes.append((name,t,t.min(axis=1),t.max(axis=1)))
def intersects(t,o,end):
    direction=end-o;length=np.linalg.norm(direction)
    if length<1e-6:return False
    direction/=length;e1=t[:,1]-t[:,0];e2=t[:,2]-t[:,0];p=np.cross(direction,e2);det=np.einsum('ij,ij->i',e1,p)
    valid=abs(det)>1e-8
    if not valid.any():return False
    e1=e1[valid];e2=e2[valid];p=p[valid];inv=1/det[valid];q=o-t[valid,0]
    u=np.einsum('ij,ij->i',q,p)*inv;cross=np.cross(q,e1);v=np.einsum('j,ij->i',direction,cross)*inv;dist=np.einsum('ij,ij->i',e2,cross)*inv
    return bool(((u>=-1e-6)&(v>=-1e-6)&(u+v<=1.000001)&(dist>1e-5)&(dist<length-1e-5)).any())
def hits(o,end):
    out=[];low=np.minimum(o,end);high=np.maximum(o,end)
    for name,t,lo,hi in meshes:
        selected=np.all(hi>=low,axis=1)&np.all(lo<=high,axis=1)
        if selected.any() and intersects(t[selected],o,end):out.append(name)
    return out
inv=json.loads((R/'arrival-inventory.json').read_text(encoding='utf-8'));reg=json.loads((R/'circulation-register.json').read_text(encoding='utf-8'))
stairs=inv['stairs']
assert {s['id'] for s in stairs}=={'L3-E04','L3-E05'},'Only the two diagram arrival escalator groups are allowed'
results=[]
for stair in stairs:
    upper=np.array(stair['position']);lower=np.array(stair['lower_landing']);conflicts=[]
    assert abs(upper[2]-lower[2])<.01 and abs(upper[0]-lower[0])>20
    assert abs(lower[1]-.3)<.01 and abs(upper[1]-12.1)<.01
    for side in [-.72,.72]:
        for height in [.30,1.0,1.7]:
            for name in hits(lower+[0,height,side],upper+[0,height,side]):conflicts.append(dict(test='continuous inclined ray',mesh=name))
    for u in np.linspace(0,1,45):
        point=lower*(1-u)+upper*u
        for side in [-.72,.72]:
            o=point+[0,.18,side];end=point+[0,1.85,side]
            for name in hits(o,end):conflicts.append(dict(t=round(float(u),3),mesh=name))
    results.append(dict(id=stair['id'],headroom_passed=not conflicts,collisions=conflicts))
out={'carousels':len([r for r in inv['facilities'] if r['type']=='baggage carousel']),'stairs':results,'scope':'Actual GLB vertical headroom samples along both treads; east-west direction; not full passenger routing certification.'}
(R/'arrival-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
assert out['carousels']==10
assert all(r['headroom_passed'] for r in results)
