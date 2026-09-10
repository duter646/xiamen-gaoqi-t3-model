from pathlib import Path
R=Path(__file__).parent
exec((R/'check_arrivals.py').read_text(encoding='utf-8').split('inv=json.loads')[0])
failures=[]
for x in np.linspace(-82,91,32):
 for z in [16.2,19,23,28.8]:
  collisions=hits(np.array([x,6.01,z]),np.array([x,6.35,z]))
  floors=[n for n in collisions if n.startswith('Structure_DepartureFloor')]
  if floors:failures.append([x,z,floors])
unsupported=[]
for x,z in [(-83.97,17),(-83.97,28),(92.59,17),(92.59,28),(-70,15.43),(10,15.43),(70,15.43),(-70,29.61),(10,29.61),(70,29.61)]:
 h=hits(np.array([x,6.0,z]),np.array([x,6.32,z]))
 if not any(n.startswith('Structure_DepartureFloor') for n in h):unsupported.append([x,z])
out=dict(second_floor_strip_floor_intrusions=failures,unsupported_guard_samples=unsupported,strip_samples=128)
(R/'void21-validation.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out));assert not failures and not unsupported
