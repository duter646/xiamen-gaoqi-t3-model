"""Check actual mesh sections for fixture/column surface intersections."""
from pathlib import Path
import json
import struct
import sys
import numpy as np

R=Path(__file__).resolve().parent
raw=Path(sys.argv[1]).read_bytes() if len(sys.argv)>1 else (R/'xiamen-gaoqi-t3.glb').read_bytes()
n=struct.unpack_from('<I',raw,12)[0]
doc=json.loads(raw[20:20+n])


def segments(tri,h):
    tri=tri[(tri[:,:,1].min(1)<h)&(tri[:,:,1].max(1)>h)]
    out=[]
    for a,b,c in [(0,1,2),(1,2,0),(2,0,1)]:
        t=tri[((tri[:,a,1]<h)!=(tri[:,b,1]<h))&((tri[:,a,1]<h)!=(tri[:,c,1]<h))]
        if not len(t):continue
        ends=[]
        for j in [b,c]:
            f=(h-t[:,a,1])/(t[:,j,1]-t[:,a,1])
            ends.append((t[:,a]+f[:,None]*(t[:,j]-t[:,a]))[:,[0,2]])
        out.extend(np.stack(ends,axis=1))
    return np.asarray(out).reshape(-1,2,2)


selected=[]
for node in doc['nodes']:
    name=node['name']
    is_column=name.startswith(('Structure_Columns_','Interior_ArrivalColumnWrap_','Interior_ConcourseColumns_'))
    is_fixture=name.startswith(('Interior_CheckIn_','Interior_CheckInReturn_','Interior_IslandSpines_','Interior_ArrivalCarousel_','Interior_Circulation_D-SH','Interior_Circulation_D-CF','Interior_Circulation_I-SH','Interior_Circulation_SEC-','Interior_Circulation_L2-L','Interior_Circulation_L3-L'))
    if not (is_column or is_fixture):continue
    for p in doc['meshes'][node['mesh']]['primitives']:
        a=doc['accessors'][p['attributes']['POSITION']];v=doc['bufferViews'][a['bufferView']]
        t=np.frombuffer(raw,dtype='<f4',count=a['count']*3,offset=n+28+v.get('byteOffset',0)+a.get('byteOffset',0)).reshape(-1,3,3)
        selected.append((name,is_column,t))


def cross(a,b):return a[...,0]*b[...,1]-a[...,1]*b[...,0]


issues=[]
for h in [.70,1.00,6.85,7.30,12.65,13.60,14.50]:
    columns=[(name,segments(t,h)) for name,col,t in selected if col]
    for name,col,t in selected:
        if col:continue
        lines=segments(t,h)
        for colname,cs in columns:
            if not len(cs) or not len(lines):continue
            for a,b in lines:
                candidate=cs[np.all(cs.max(1)>=np.minimum(a,b),1)&np.all(cs.min(1)<=np.maximum(a,b),1)]
                if not len(candidate):continue
                c=candidate[:,0];d=candidate[:,1]
                det=cross(b-a,d-c);valid=abs(det)>1e-9
                u=cross(c-a,d-c)/np.where(valid,det,1)
                v=cross(c-a,b-a)/np.where(valid,det,1)
                hit=valid&(u>1e-5)&(u<1-1e-5)&(v>1e-5)&(v<1-1e-5)
                if hit.any():
                    point=a+u[hit][0]*(b-a)
                    issues.append(dict(fixture=name,column=colname,height=h,point=point.tolist()))
                    break
report={'issues':issues,'heights':[.70,1.00,6.85,7.30,12.65,13.60,14.50],'scope':'actual triangle-section segment crossings: counters, belts, guide shops, security equipment against main and concourse columns; not building-wide collision certification'}
(R/'guide-fixtures-validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
assert not issues
