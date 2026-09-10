from pathlib import Path
import json,struct,numpy as np
R=Path(__file__).parent
blob=(R/'xiamen-gaoqi-t3.glb').read_bytes();n=struct.unpack_from('<I',blob,12)[0];doc=json.loads(blob[20:20+n]);offset=n+28
def vertices(name):
 out=[]
 for node in doc['nodes']:
  if not (node['name']==name or node['name'].startswith(name+'_')):continue
  for p in doc['meshes'][node['mesh']]['primitives']:
   a=doc['accessors'][p['attributes']['POSITION']];v=doc['bufferViews'][a['bufferView']]
   out.append(np.frombuffer(blob,dtype='<f4',count=a['count']*3,offset=offset+v.get('byteOffset',0)).reshape(-1,3))
 return np.concatenate(out) if out else np.empty((0,3))
top=vertices('Roof_MainSheet');bottom=vertices('Roof_MainSoffit')
assert len(top)>0 and len(top)==len(bottom)
for points,heights in [(top,[17.4,23.5,32.5]),(bottom,[17.18,23.28,32.28])]:
 assert np.allclose(np.unique(points[:,1]),heights,atol=1e-4)
 assert np.max(np.ptp(points.reshape(-1,3,3)[:,:,1],axis=1))<1e-5
assert len(vertices('Facade_RecessedEndEnclosure'))==0
assert len(vertices('Roof_MainShell'))==0
haunch=vertices('Roof_InternalCurvedHaunches')
for d0,d1,h in [(0,8,32.5),(8,26,23.5),(26,54,17.4)]:
 for side,width in [(-1,26),(1,58)]:
  zz=sorted([38+side*d0*width/54,38+side*d1*width/54])
  relevant=haunch[(haunch[:,2]>zz[0]+.2)&(haunch[:,2]<zz[1]-.2)]
  assert len(relevant)>0 and relevant[:,1].max()<=h-.22+1e-4
columns=json.loads((R/'column-connections.json').read_text());assert max(x['max_gap_m'] for x in columns)<1e-5
signs=json.loads((R/'sign-mount-audit.json').read_text());assert not signs['unmounted']
result=dict(roof='one stepped assembly; no sloping second skin',roof_thickness_m=.22,internal_haunches_below_roof=True,columns_connected=len(columns),signs_mounted=signs['mounted'],passed=True)
(R/'roof16-validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result))
