from pathlib import Path
import json,heapq,numpy as np
R=Path(__file__).parent/'model'
grid_source=(R/'check_order12.py').read_text(encoding='utf-8').split('start=[86.5')[0]
grids={}
for level,y in [(1,.3),(2,6.3),(3,12.1)]:
 source=grid_source.replace('abs(t[:,:,1]-12.1)','abs(t[:,:,1]-'+str(y)+')').replace('[12.55,13.15,13.75]',str([y+.45,y+1.05,y+1.65])).replace('np.arange(-12,96,step)','np.arange(-12,98,step)')
 ns={'__file__':str(R/'check_order12.py')};exec(source,ns)
 grids[level]=ns

def floor_path(level,a,b):
 g=grids[level];allowed=g['floor']&~g['blocked'];start=g['node'](a);goal=g['node'](b)
 def nearby(n):
  if allowed[n]:return n
  options=[(dr*dr+dc*dc,(n[0]+dr,n[1]+dc)) for dr in range(-5,6) for dc in range(-5,6) if 0<=n[0]+dr<allowed.shape[0] and 0<=n[1]+dc<allowed.shape[1] and allowed[n[0]+dr,n[1]+dc]]
  if not options:raise ValueError(('blocked endpoint',level,a,b,n))
  return min(options)[1]
 start=nearby(start);goal=nearby(goal);queue=[(0,0,start)];cost={start:0};parents={start:None}
 while queue:
  _,c,u=heapq.heappop(queue)
  if c!=cost[u]:continue
  if u==goal:break
  for dr,dc in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
   v=(u[0]+dr,u[1]+dc)
   if not(0<=v[0]<allowed.shape[0] and 0<=v[1]<allowed.shape[1]) or not allowed[v]:continue
   if dr and dc and not(allowed[u[0]+dr,u[1]] and allowed[u[0],u[1]+dc]):continue
   nc=c+(1.41421356 if dr and dc else 1)
   if nc<cost.get(v,1e20):cost[v]=nc;parents[v]=u;heapq.heappush(queue,(nc+np.hypot(v[0]-goal[0],v[1]-goal[1]),nc,v))
 if goal not in parents:raise ValueError(('no route',level,a,b,start,goal))
 path=[];u=goal
 while u is not None:path.append(u);u=parents[u]
 path=path[::-1];simple=[path[0]]
 for i in range(1,len(path)-1):
  if (path[i][0]-path[i-1][0],path[i][1]-path[i-1][1])!=(path[i+1][0]-path[i][0],path[i+1][1]-path[i][1]):simple.append(path[i])
 simple.append(path[-1]);y={1:.3,2:6.3,3:12.1}[level]
 return [[float(g['xs'][c]),y+.18,float(g['zs'][r])] for r,c in simple]

routes=[]
def route(id,label,color,stages):
 points=[];stops=[]
 for item in stages:
  if item[0]=='floor':
   _,lev,a,b,caption=item;segment=floor_path(lev,a,b)
  else:
   _,a,b,caption=item;segment=[[a[0],a[1]+.18,a[2]],[b[0],b[1]+.18,b[2]]]
  points+=segment;stops.append({'label':caption,'position':segment[-1]})
 routes.append(dict(id=id,label=label,color=color,points=points,stops=stops))
route('domestic-departure','国内出发','#168bd2',[
 ('floor',2,[-90,95],[-72,80],'值机'),('floor',2,[-72,80],[-55,32.18],'上行扶梯'),
 ('stair',[-55,6.3,32.18],[-66,12.1,32.18],'3F'),
 ('floor',3,[-67,32.2],[-40.17,42.8],'安检'),('floor',3,[-40.17,42.8],[-40.17,35.7],'安检出口'),
 ('floor',3,[-40.17,35.7],[-60,5.5],'候机'),('floor',3,[-60,5.5],[-60,-10],'登机口')])
route('international-departure','国际出发','#b470e5',[
 ('floor',2,[125,95],[96,77],'值机'),('floor',2,[96,77],[99.3,36.53],'上行扶梯'),
 ('stair',[99.3,6.3,36.53],[88.29,12.1,36.53],'3F'),
 ('floor',3,[86.5,36.5],[85.1,61],'边检'),('floor',3,[85.1,61],[85.1,65],'边检出口'),
 ('floor',3,[85.1,65],[125.2,48],'安检'),('floor',3,[125.2,48],[134,48],'安检出口'),
 ('floor',3,[134,48],[81.5,-10],'登机口')])
route('domestic-arrival','国内到达','#e89828',[
 ('floor',3,[-60,-10],[-49.7,20.53],'到达扶梯'),('stair',[-49.2,12.1,20.53],[-27.2,.3,20.53],'1F'),
 ('floor',1,[-26.5,20.53],[-33,52],'行李提取'),('floor',1,[-33,52],[-48,80],'到达出口'),('floor',1,[-48,80],[-47,95],'离开航站楼')])
route('international-arrival','国际到达','#19a485',[
 ('floor',3,[81.5,-10],[22.5,20.53],'到达扶梯'),('stair',[23.1,12.1,20.53],[45.1,.3,20.53],'1F'),
 ('floor',1,[46,20.53],[102.5,29],'入境边检'),('floor',1,[102.5,29],[102.5,35],'边检出口'),
 ('floor',1,[102.5,35],[87,52],'行李提取'),('floor',1,[87,52],[95,69],'海关'),('floor',1,[95,69],[95,80],'到达出口'),('floor',1,[95,80],[82,95],'离开航站楼')])
out=R.parent.parent/'assets';out.mkdir(parents=True,exist_ok=True)
(out/'routes.json').write_text(json.dumps(routes,ensure_ascii=False),encoding='utf-8')
print([(r['id'],len(r['points'])) for r in routes])

