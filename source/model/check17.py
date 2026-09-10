from pathlib import Path
import struct,json,numpy as np
R=Path(__file__).parent
b=(R/'xiamen-gaoqi-t3.glb').read_bytes();n=struct.unpack_from('<I',b,12)[0];doc=json.loads(b[20:20+n]);off=n+28
def points(prefix):
 result=[]
 for node in doc['nodes']:
  if not node['name'].startswith(prefix+'_'):continue
  p=doc['meshes'][node['mesh']]['primitives'][0];a=doc['accessors'][p['attributes']['POSITION']];v=doc['bufferViews'][a['bufferView']]
  result.append(np.frombuffer(b,dtype='<f4',count=a['count']*3,offset=off+v.get('byteOffset',0)).reshape(-1,3))
 return np.concatenate(result) if result else np.empty((0,3))
assert not len(points('Roof_InternalCurvedHaunches'))
supports=points('Roof_InternalTriangleSupports');assert len(supports)==9*21*3*36
roof=json.loads((R/'roof16-register.json').read_text());tiers=roof['tiers']
assert len(tiers['1'])==6 and len(tiers['-1'])==3
for side,width in [('1',58),('-1',26)]:
 spans=[(t[1]-t[0])*width/54 for t in tiers[side]][1:]
 assert np.allclose(spans,10.5)
 drops=-np.diff([t[2] for t in tiers[side]])
 assert np.all(drops>0) and not np.allclose(drops,drops[0])
 assert np.all(np.diff(drops)<0)
assert np.allclose([t[2] for t in tiers['-1']],[t[2] for t in tiers['1'][:3]])
assert len(points('Roof_SolidEaveConcourseClosure'))>0
top=points('Roof_MainSheet');bottom=points('Roof_MainSoffit')
assert np.allclose(np.unique(top[:,1])-np.unique(bottom[:,1]),.22,atol=1e-4)
curves=points('Roof_ContinuousCurvedRibs');bearings=points('Roof_CurveConcourseBearing')
for x in np.arange(-104.5,147.6,12):
 tip=curves[(abs(curves[:,0]-x)<.51)&(curves[:,2]<5.6)]
 assert len(tip)>0 and abs(tip[:,1].min()-18.02)<1e-4
 bearing=bearings[abs(bearings[:,0]-x)<.53];assert len(bearing)>0 and bearing[:,1].min()<=18.01
columns=json.loads((R/'column-connections.json').read_text());assert max(c['max_gap_m'] for c in columns)<1e-5
signs=json.loads((R/'sign-mount-audit.json').read_text());assert not signs['unmounted']
result=dict(passed=True,landside_drops=5,airside_drops=2,terrace_pitch_m=10.5,drops_m={side:(-np.diff([t[2] for t in tt])).tolist() for side,tt in tiers.items()},triangular_supports=189,curved_ribs_land_on_corridor=True,column_connections=len(columns),mounted_signs=signs['mounted'],dimensions='estimated from images; not measured')
(R/'validation20.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result))
