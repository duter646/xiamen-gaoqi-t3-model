from pathlib import Path
R=Path(__file__).resolve().parent
exec((R/'check_arrivals.py').read_text(encoding='utf-8').split('inv=json.loads')[0])
reg=json.loads((R/'revision11-register.json').read_text(encoding='utf-8'));failures=[]
for door in reg['west_gate_doors']:
 for dx in [-.85,0,.85]:
  for h in [.5,1.7,2.3]:
   a=np.array([door['x']+dx,.28+h,door['z']-1]);b=a+[0,0,2]
   found=hits(a,b)
   if found:failures.append(dict(gate=door['number'],height=h,meshes=found))
# Verify the removed front upper slab across a grid, independent of camera visibility.
void_fail=[]
for x in np.linspace(-102,145,24):
 for z in [69,75,85,94]:
  found=[name for name in hits(np.array([x,11.6,z]),np.array([x,12.4,z])) if name.startswith('Structure_ThirdFloor')]
  if found:void_fail.append([float(x),z])
wall_gaps=[]
for x in np.linspace(-103,146,30):
 for y in [1.,4.,6.]:
  found=hits(np.array([x,y,11.6]),np.array([x,y,12.4]))
  if not any(name.startswith('Facade_ArrivalApronWall') for name in found):wall_gaps.append([float(x),y])
out=dict(gates=4,gate_collisions=failures,upper_void_floor_hits=void_fail,arrival_wall_gaps=wall_gaps)
(R/'revision11-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=False));assert not failures and not void_fail and not wall_gaps
