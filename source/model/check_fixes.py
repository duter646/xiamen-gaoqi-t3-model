from pathlib import Path
import json,struct,numpy as np
R=Path(__file__).resolve().parent
b=(R/'xiamen-gaoqi-t3.glb').read_bytes();n=struct.unpack_from('<I',b,12)[0];d=json.loads(b[20:20+n]);off=28+n
def positions(node):
    a=d['accessors'][d['meshes'][node['mesh']]['primitives'][0]['attributes']['POSITION']];v=d['bufferViews'][a['bufferView']]
    return np.frombuffer(b,dtype='<f4',count=a['count']*3,offset=off+v.get('byteOffset',0)).reshape(-1,3)
ads=[positions(o) for o in d['nodes'] if o['name'].startswith('Interior_GalleryDisplay')]
assert ads
admax=max(float(a[:,1].max()) for a in ads);assert admax<11.7
reg=json.loads((R/'circulation-register.json').read_text(encoding='utf-8'))
stairs={}
for f in reg['facilities']:
    if f['id'] not in ['L3-E03','L3-E06']:continue
    a=np.array(f['position']);b0=np.array(f['lower_landing']);assert abs(a[2]-b0[2])<.001;assert abs(a[0]-b0[0])>10
    assert b0[0]>a[0], 'Upper landing must be west of lower landing'
    stairs[f['id']]={'axis':'X / east-west','upper':a.tolist(),'lower':b0.tolist()}
assert len(stairs)==2
assert not any(o['name'].startswith('Exterior_AirportName') for o in d['nodes'])
assert any(o['name'].startswith('Exterior_XiamenRaisedLetters') for o in d['nodes'])
ribs=np.concatenate([positions(o) for o in d['nodes'] if o['name'].startswith('Roof_ContinuousCurvedRibs')])
ends=[]
for z in [12,96]:
    vs=ribs[np.abs(ribs[:,2]-z)<.6];ends.append(float(vs[:,1].mean()))
assert abs(ends[0]-ends[1])<.15  # finite surface band samples vary with horizontal span
out={'gallery_ad_top_y':admax,'slab_underside_y':11.9,'clearance_m':11.9-admax,'stairs':stairs,'obsolete_airport_name_removed':True,'roof_eave_heights_symmetric':True,'security_frosted_partition_meshes':sum(o['name'].startswith('Interior_SecurityIsolation') for o in d['nodes']),'limitations':'Geometric regression checks, not as-built layout certification.'}
(R/'fix-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=False))
