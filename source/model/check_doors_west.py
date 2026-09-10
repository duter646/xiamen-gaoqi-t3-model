from pathlib import Path
R=Path(__file__).resolve().parent
exec((R/'check_arrivals.py').read_text(encoding='utf-8').split('inv=json.loads')[0])
doors=json.loads((R/'door-register.json').read_text(encoding='utf-8'));problems=[]
for door in doors['street_doors']:
    for dx in [-1.2,0,1.2]:
        for dy in [.5,1.7]:
            x=door['x']+dx;y=door['bottom']+dy
            found=hits(np.array([x,y,94.5]),np.array([x,y,97.0]))
            if found:problems.append(dict(door=door['number'],level=door['level'],hits=found))
west=json.loads((R/'west-stair-register.json').read_text());a=np.array(west['lower']);b=np.array(west['upper'])
for side in [-.72,.72]:
    for height in [.3,1.0,1.7]:
        found=hits(a+[0,height,side],b+[0,height,side])
        if found:problems.append(dict(west_stair=found))
for dy in [.5,1.7]:
    found=hits(np.array([-106,12.1+dy,b[2]]),np.array([-103,12.1+dy,b[2]]))
    if found:problems.append(dict(west_door=found))
out=dict(street_doors=len(doors['street_doors']),west_lower_y=float(a[1]),failures=problems)
(R/'door-west-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=False));assert not problems
