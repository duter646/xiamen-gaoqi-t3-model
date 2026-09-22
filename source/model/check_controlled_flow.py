"""Reachability of the current guide layout, including 2F elevator galleries."""
from pathlib import Path
R=Path(__file__).resolve().parent
grid_source=(R/'check_order12.py').read_text(encoding='utf-8').split('start=[86.5')[0]
exec(grid_source)
reg=json.loads((R/'circulation-register.json').read_text(encoding='utf-8'))['facilities']
seals={}
for bank in ['SEC-D','SEC-I']:
    lanes=[r for r in reg if r['kind']=='security lane' and r['id'].startswith(bank)]
    a=np.array(lanes[0]['position'])[[0,2]];b=np.array(lanes[-1]['position'])[[0,2]];v=(b-a)/np.linalg.norm(b-a)
    seals[bank]=[((a-v*2.2).tolist(),(b+v*4.6).tolist())]
border=[([75+(60-48)*(45-75)/(65-48),60],[111,60])]
checks=[]
def check(label,start,end,expected,extra=[]):
    result=reachable(start,end,extra)
    checks.append(dict(label=label,reachable=result['reachable'],expected=expected,passed=result['reachable']==expected))
check('domestic public to gate',[-66,34.2],[-60,5.5],True)
check('domestic security sealed',[-66,34.2],[-60,5.5],False,seals['SEC-D'])
check('international ordered route',[86.5,36.5],[134,5.5],True)
check('border sealed to post-border',[86.5,36.5],[115,55],False,border)
check('border sealed to gates',[86.5,36.5],[134,5.5],False,border)
check('international security sealed',[115,55],[134,5.5],False,seals['SEC-I'])
check('domestic to international gates',[-60,5.5],[81.5,5.5],False,seals['SEC-D']+seals['SEC-I'])
check('international gates to arrival',[81.5,5.5],[21.75,20.5],True,seals['SEC-D']+seals['SEC-I'])
check('domestic gates to international arrival',[5.75,5.5],[21.75,20.5],False,seals['SEC-D']+seals['SEC-I'])
second={ '__file__':str(R/'check_order12.py') }
exec(grid_source.replace('abs(t[:,:,1]-12.1)','abs(t[:,:,1]-6.3)').replace('[12.55,13.15,13.75]','[6.75,7.35,7.95]'),second)
for label,start,end,expected in [
    ('west lift lobby to gallery',[-78,1],[-70,20],True),
    ('east lift lobby to gallery',[114,5],[110,20],True),
    ('arrival gallery to public check-in',[-70,20],[-50,80],False),
    ('domestic to international arrival gallery',[-70,20],[110,20],False)]:
    result=second['reachable'](start,end)
    checks.append(dict(label=label,reachable=result['reachable'],expected=expected,passed=result['reachable']==expected))
out=dict(checks=checks,errors=[r for r in checks if not r['passed']],scope='actual GLB: .25m grid, .22m radius, 3 sampled body heights; virtual control-bank sealing; no elevator car simulation')
(R/'controlled-flow-validation.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2));assert not out['errors']
