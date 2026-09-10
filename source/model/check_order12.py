"""Reachability on actual GLB slices, with each control bank virtually sealed."""
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parent
exec((R/'check_arrivals.py').read_text(encoding='utf-8').split('inv=json.loads')[0])
step=.25;xs=np.arange(-114,148,step);zs=np.arange(-12,96,step);shape=(len(zs),len(xs));floor=np.zeros(shape,bool);blocked=np.zeros(shape,bool)
def rectangle(lo,hi):
 ix=np.flatnonzero((xs>=lo[0])&(xs<=hi[0]));iz=np.flatnonzero((zs>=lo[1])&(zs<=hi[1]))
 if not len(ix) or not len(iz):return None
 xx,zz=np.meshgrid(xs[ix],zs[iz]);return ix,iz,xx,zz
def segment(a,b,mask,radius=.22):
 a=np.array(a);b=np.array(b);region=rectangle(np.minimum(a,b)-radius,np.maximum(a,b)+radius)
 if region is None:return
 ix,iz,x,z=region;v=b-a;length=v@v
 t=np.clip(((x-a[0])*v[0]+(z-a[1])*v[1])/max(length,1e-12),0,1)
 inside=(x-a[0]-t*v[0])**2+(z-a[1]-t*v[1])**2<=radius**2
 mask[np.ix_(iz,ix)]|=inside
for name,t,lo,hi in meshes:
 if name.startswith('Interior_Sign') or 'MountPlate' in name:continue
 relevant=(hi[:,0]>=xs[0])&(lo[:,0]<=xs[-1])&(hi[:,2]>=zs[0])&(lo[:,2]<=zs[-1])
 if name.startswith('Structure_'):
  for tri in t[relevant&(abs(t[:,:,1]-12.1).max(axis=1)<.015)]:
   p=tri[:,[0,2]];region=rectangle(p.min(0),p.max(0))
   if region is None:continue
   ix,iz,x,z=region;a=p[0];b=p[1]-a;c=p[2]-a;det=b[0]*c[1]-b[1]*c[0]
   if abs(det)<1e-8:continue
   u=((x-a[0])*c[1]-(z-a[1])*c[0])/det;v=(b[0]*(z-a[1])-b[1]*(x-a[0]))/det
   floor[np.ix_(iz,ix)]|=(u>=-1e-5)&(v>=-1e-5)&(u+v<=1.00001)
 for height in [12.55,13.15,13.75]:
  for tri in t[relevant&(lo[:,1]<height)&(hi[:,1]>height)]:
   crossings=[]
   for a,b in zip(tri,np.roll(tri,-1,axis=0)):
    if (a[1]<=height<b[1]) or (b[1]<=height<a[1]):crossings.append((a+(b-a)*(height-a[1])/(b[1]-a[1]))[[0,2]])
   if len(crossings)==2:segment(*crossings,blocked)
def node(p):return (round((p[1]-zs[0])/step),round((p[0]-xs[0])/step))
def reachable(start,end,extra=[]):
 mask=blocked.copy()
 for a,b in extra:segment(a,b,mask,.35)
 allowed=floor&~mask;s=node(start);e=node(end)
 if not allowed[s] or not allowed[e]:return dict(reachable=False,endpoint_blocked=[not bool(allowed[s]),not bool(allowed[e])])
 seen=np.zeros(shape,bool);seen[s]=True;q=deque([s]);parents={s:None}
 while q:
  r,c=q.popleft()
  if (r,c)==e:
   path=[];cur=e
   while cur is not None:path.append([float(xs[cur[1]]),float(zs[cur[0]])]);cur=parents[cur]
   return dict(reachable=True,path=path[::-1][::4])
  for rr,cc in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
   if 0<=rr<shape[0] and 0<=cc<shape[1] and allowed[rr,cc] and not seen[rr,cc]:seen[rr,cc]=True;q.append((rr,cc));parents[(rr,cc)]=(r,c)
 return dict(reachable=False)
start=[86.5,36.5];post=[115,55];gate=[134,5.5]
reg=json.loads((R/'circulation-register.json').read_text(encoding='utf-8'))
if isinstance(reg,dict):reg=next(v for v in reg.values() if isinstance(v,list) and v and isinstance(v[0],dict) and 'kind' in v[0])
lanes=[r for r in reg if r.get('id','').startswith('SEC-I') and r.get('kind')=='security lane']
sx=float(lanes[0]['position'][0]);zz=[r['position'][2] for r in lanes]
border=[([48.53,63],[111,63])];security=[([sx,min(zz)-2.2],[sx,max(zz)+4.6])]
out=dict(resolution_m=step,body_radius_m=.22,all_open=reachable(start,gate),border_open=reachable(start,post),border_sealed_to_security=reachable(start,post,border),border_sealed_to_gates=reachable(start,gate,border),security_sealed_to_gates=reachable(post,gate,security))
(R/'processing-order-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=False))
assert out['all_open']['reachable'] and out['border_open']['reachable']
assert not any(out[k]['reachable'] for k in ['border_sealed_to_security','border_sealed_to_gates','security_sealed_to_gates'])
