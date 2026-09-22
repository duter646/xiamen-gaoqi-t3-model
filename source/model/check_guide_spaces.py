"""Map-based commercial access, void support and controlled-area separation."""
from pathlib import Path
R=Path(__file__).resolve().parent
exec((R/'check_order12.py').read_text(encoding='utf-8').split('start=[86.5')[0])
space=json.loads((R/'guide-spaces.json').read_text(encoding='utf-8'))
reg=json.loads((R/'circulation-register.json').read_text(encoding='utf-8'))['facilities']
seals=[]
for bank in ['SEC-D','SEC-I']:
    lanes=[r for r in reg if r['kind']=='security lane' and r['id'].startswith(bank)]
    a=np.array(lanes[0]['position'])[[0,2]];b=np.array(lanes[-1]['position'])[[0,2]];v=(b-a)/np.linalg.norm(b-a)
    seals.append(((a-v*2.2).tolist(),(b+v*4.6).tolist()))


def inside(p,poly):
    answer=False
    for a,b in zip(poly,np.roll(poly,-1,axis=0)):
        if (a[1]>p[1])!=(b[1]>p[1]) and p[0]<(b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0]:answer=not answer
    return answer


shop_checks=[];errors=[]
for shop in space['shops']:
    poly=np.array(shop['outline_xz']);a,b=np.array(shop['door_xz']);mid=(a+b)/2;v=(b-a)/np.linalg.norm(b-a);normal=np.array([-v[1],v[0]])
    if not inside(mid+normal*.7,poly):normal=-normal
    target=(mid+normal*.7).tolist()
    start=[-66,34.2] if shop['id'].startswith('D-') else [115,55]
    gate=[-60,5.5] if shop['id'].startswith('D-') else [134,5.5]
    access=reachable(start,target);bypass=reachable(target,gate,seals)
    result=dict(id=shop['id'],target=target,public_or_post_border_access=access['reachable'],bypasses_sealed_security=bypass['reachable'])
    shop_checks.append(result)
    if not access['reachable'] or bypass['reachable']:errors.append(result)
    for a,b in zip(poly,np.roll(poly,-1,axis=0)):
        for t in [.15,.5,.85]:
            x,z=a*(1-t)+b*t
            supports=hits(np.array([x,12.18,z]),np.array([x,11.55,z]))
            if not any(n.startswith('Structure_') for n in supports):errors.append(dict(id=shop['id'],unsupported_wall=[float(x),float(z)]))
void_checks=[]
for x,z in [(-76,22),(-40,24),(40,24)]:
    names=hits(np.array([x,12.2,z]),np.array([x,11.6,z]))
    void_checks.append(dict(point=[x,z],floor_present=any(n.startswith('Structure_ThirdFloor') for n in names)))
if any(c['floor_present'] for c in void_checks):errors.append({'void_checks':void_checks})
out=dict(shops=shop_checks,upper_voids=void_checks,errors=errors,scope='actual GLB slices: shop doorway access, sealed-security bypass, shop-wall support, three guide void centres')
(R/'guide-spaces-validation.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2));assert not errors
