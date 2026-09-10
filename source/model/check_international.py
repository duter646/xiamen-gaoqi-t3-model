from pathlib import Path
R=Path(__file__).resolve().parent
exec((R/'check_arrivals.py').read_text(encoding='utf-8').split("inv=json.loads")[0])
flow=json.loads((R/'international-flow.json').read_text(encoding='utf-8'))
results=[]
for key in ['public_stair_to_border','border_to_security']:
    problems=[]
    for a,b in zip(flow[key],flow[key][1:]):
        a=np.array([a[0],0,a[1]],float);b=np.array([b[0],0,b[1]],float)
        v=b-a;normal=np.array([-v[2],0,v[0]])/np.linalg.norm(v)
        for lateral in [-.34,0,.34]:
            for height in [12.3,13,13.8]:
                start=a+normal*lateral+[0,height,0];end=b+normal*lateral+[0,height,0]
                found=hits(start,end)
                if found:problems.append(dict(segment=[a.tolist(),b.tolist()],meshes=found))
    results.append(dict(stage=key,passed=not problems,collisions=problems))
a,b=flow['forbidden_shortcut'];blocked=hits(np.array([a[0],13.2,a[1]]),np.array([b[0],13.2,b[1]]))
out=dict(stages=results,bypass_blocked_by=blocked,scope='Actual geometry checks for stair approach, immigration aperture and screening approach; direct bypass ray must be blocked')
(R/'international-flow-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=False))
assert all(r['passed'] for r in results) and blocked

