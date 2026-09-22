"""Shaft enclosure, floor apertures and doorway support in actual exported meshes."""
from pathlib import Path
R=Path(__file__).resolve().parent
exec((R/'check_arrivals.py').read_text(encoding='utf-8').split('inv=json.loads')[0])
reg=json.loads((R/'circulation-register.json').read_text(encoding='utf-8'))['facilities']
failures=[];checks=[]
for lift in [r for r in reg if r['kind']=='lift shaft']:
    x,base,z=lift['position'];top=lift['upper_level'];name='Interior_Circulation_'+lift['id']
    for y in [base,top]:
        approach=hits(np.array([x,y+1,z+1.65]),np.array([x,y+1,z+3.1]))
        if approach:failures.append(dict(id=lift['id'],type='blocked doorway approach',level=y,meshes=approach))
        for dx in [-.8,0,.8]:
            support=hits(np.array([x+dx,y+.08,z+1.43]),np.array([x+dx,y-.25,z+1.43]))
            if not any(q.startswith(('Structure_',name)) for q in support):failures.append(dict(id=lift['id'],type='unsupported doorway threshold',level=y,dx=dx))
            door=hits(np.array([x+dx,y+1,z+1.2]),np.array([x+dx,y+1,z+1.8]))
            if dx and not any(q.startswith(name) for q in door):failures.append(dict(id=lift['id'],type='missing door leaf',level=y,dx=dx))
    for y in [base+3.3,(base+top)/2+1,top+2.8]:
        front=hits(np.array([x,y,z+1.15]),np.array([x,y,z+1.8]))
        if not any(q.startswith(name) for q in front):failures.append(dict(id=lift['id'],type='open shaft front between landings',y=y))
    inside=hits(np.array([x,top-.3,z]),np.array([x,top+.1,z]))
    floor=[q for q in inside if q.startswith(('Structure_DepartureFloor','Structure_ThirdFloor','Structure_ConcourseFloor'))]
    if floor:failures.append(dict(id=lift['id'],type='floor through shaft',meshes=floor))
    obstruction=hits(np.array([x,base+1,z-.6]),np.array([x,base+1,z+.8]))
    if any(q.startswith('Structure_ConcourseBase') for q in obstruction):failures.append(dict(id=lift['id'],type='support rib through shaft'))
    if top==12.1:
        for dy in [.5,1.5]:
            collision=hits(np.array([x,base+dy,z+1.8]),np.array([x,base+dy,14.0]))
            if collision:failures.append(dict(id=lift['id'],type='blocked lower lobby',meshes=collision))
        for zz in np.linspace(z+1.8,12.2,12):
            support=hits(np.array([x,base+.05,zz]),np.array([x,base-.5,zz]))
            if not any(q.startswith('Structure_') for q in support):failures.append(dict(id=lift['id'],type='lower lobby floor gap',z=float(zz)))
    checks.append(dict(id=lift['id'],base=base,top=top))
out=dict(lifts=checks,failures=failures,scope='four modelled shafts; closed door surfaces, front enclosure, threshold support, upper slab openings; car mechanism and surveyed dimensions not assessed')
(R/'lifts-validation.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2));assert not failures
