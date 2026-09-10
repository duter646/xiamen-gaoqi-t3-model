"""Connect signs to modelled trusses/ceilings, using actual triangle intersections."""
mount_targets=[]
for (name,mat),data in groups.items():
    if not name.startswith(('Roof_','Structure_','Interior_CheckInTruss_')):continue
    if any(s in name for s in ['Light','Grid','Sign','Hanger']):continue
    vv=np.concatenate(data['v']);ff=np.concatenate(data['f']);tri=vv[ff]
    mount_targets.append((name,tri,tri.min(axis=1),tri.max(axis=1)))

def overhead(x,y,z):
    found=[]
    for name,tri,lo,hi in mount_targets:
        mask=(lo[:,0]<=x+1e-6)&(hi[:,0]>=x-1e-6)&(lo[:,2]<=z+1e-6)&(hi[:,2]>=z-1e-6)&(hi[:,1]>=y)
        t=tri[mask]
        if not len(t):continue
        a=t[:,0];b=t[:,1]-a;c=t[:,2]-a;det=b[:,0]*c[:,2]-b[:,2]*c[:,0]
        safe=np.where(abs(det)>1e-9,det,1)
        u=((x-a[:,0])*c[:,2]-(z-a[:,2])*c[:,0])/safe
        v=(b[:,0]*(z-a[:,2])-b[:,2]*(x-a[:,0]))/safe
        yy=a[:,1]+u*b[:,1]+v*c[:,1]
        ok=(abs(det)>1e-9)&(u>=-1e-6)&(v>=-1e-6)&(u+v<=1.000001)&(yy>=y-.001)
        if ok.any():found.append((float(yy[ok].min()),name))
    return min(found) if found else None

signs=[]
for (name,mat),data in list(groups.items()):
    if mat not in {TEXT_MAT,WEST_SIGN}:continue
    # label emits a front and back quad; use the front of each pair only.
    for vv in data['v'][::2 if mat==TEXT_MAT else 1]:
        if len(vv)!=4:continue
        c=vv.mean(axis=0);span=np.ptp(vv,axis=0);axis=0 if span[0]>span[2] else 2
        c[2 if axis==0 else 0]-=.06
        signs.append((name,c,float(span[axis]),float(span[1]),axis))
mount_report=[]
for index,(name,c,width,height,axis) in enumerate(signs):
    top=c[1]+height/2+.02
    # Labels flush on lift front panels are surface mounted; add short brackets.
    if 'Circulation_L' in name and '-L0' in name:
        for side in [-1,1]:
            p=c.copy();p[axis]+=side*width*.3
            end=p.copy();end[2 if axis==0 else 0]-=.12
            rod('Interior_SignWallBrackets',FRAME,p,end,.025,6)
        mount_report.append(dict(group=name,center=c.tolist(),type='shaft panel brackets'))
        continue
    anchors=[]
    for side in [-1,1]:
        p=c.copy();p[axis]+=side*width*.30;p[1]=top
        hit=overhead(*p)
        if hit:
            roof,name_target=hit
            rod('Interior_SignSuspension',FRAME,p,[p[0],roof+.012,p[2]],.018,8)
            box('Interior_SignCeilingMountPlates',FRAME,(p[0],roof-.014,p[2]),(.12,.028,.12))
            anchors.append(dict(start=p.tolist(),end=[float(p[0]),roof,float(p[2])],target=name_target))
        else:
            # End-of-concourse / projecting stair landing: floor-fixed sign stand.
            supports=[]
            for target,tri,lo,hi in mount_targets:
                if not target.startswith('Structure_'):continue
                mask=(lo[:,0]<=p[0])&(hi[:,0]>=p[0])&(lo[:,2]<=p[2])&(hi[:,2]>=p[2])&(hi[:,1]<c[1]-height/2)
                if mask.any():supports.append((float(hi[mask,1].max()),target))
            if supports:
                base,target=max(supports)
                rod('Interior_SignFloorPosts',FRAME,(p[0],base,p[2]),(p[0],top,p[2]),.032,8)
                box('Interior_SignFloorFeet',FRAME,(p[0],base+.025,p[2]),(.22,.05,.22))
                anchors.append(dict(start=p.tolist(),end=[float(p[0]),base,float(p[2])],target=target))
    mount_report.append(dict(group=name,center=c.tolist(),type='truss or ceiling suspension',anchors=anchors))
unmounted=[r for r in mount_report if r['type']!='shaft panel brackets' and len(r['anchors'])!=2]
(ROOT/'sign-mount-audit.json').write_text(json.dumps(dict(signs=len(signs),mounted=len(signs)-len(unmounted),unmounted=unmounted,mounts=mount_report),ensure_ascii=False,indent=2),encoding='utf-8')
