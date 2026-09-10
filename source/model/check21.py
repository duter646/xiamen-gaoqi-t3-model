from pathlib import Path
R=Path(__file__).parent
exec((R/'check_order12.py').read_text(encoding='utf-8').split('start=[86.5')[0])
reg=json.loads((R/'circulation-register.json').read_text(encoding='utf-8'))['facilities']
lanes=[r for r in reg if r['kind']=='security lane' and r['id'].startswith('SEC-D')]
a=np.array(lanes[0]['position'])[[0,2]];b=np.array(lanes[-1]['position'])[[0,2]];t=(b-a)/np.linalg.norm(b-a)
seal=[((a-t*2.2).tolist(),(b+t*4.6).tolist())]
start=[-68,32.2];gate=[-78,5.5]
opened=reachable(start,gate);closed=reachable(start,gate,seal)
filled_closed=reachable(start,[-75,23],seal)
void_nodes=[node([x,z]) for x,z in [(-63,25),(-60,25),(-40,25)]]
assert all(not floor[q] for q in void_nodes)
assert floor[node([-75,23])]
out=dict(open_route_exists=opened['reachable'],sealed_security_reaches_gates=closed['reachable'],sealed_security_reaches_filled_bay=filled_closed['reachable'],path=opened.get('path',[]),scope='3F actual mesh slices, .25m grid and .22m body radius; physical model, not viewer movement enforcement')
(R/'domestic-order21.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='path'}))
assert opened['reachable'] and not closed['reachable'] and not filled_closed['reachable']
