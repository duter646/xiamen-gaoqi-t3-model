"""Confirmed separator topology; numerical placement remains estimated."""
for a,b in [((75,40.15),(84.15,40.15)),((84.15,40.15),(84.15,33.6)),((84.15,33.6),(111,33.6))]:
    wall('Interior_InternationalPurpleBoundary',a,b,F3,3,ARR_GLASS)
    length=np.linalg.norm(np.array(b)-a)
    for t in np.linspace(0,1,max(2,int(length/2.4)+1)):
        p=np.array(a)*(1-t)+np.array(b)*t
        rod('Interior_InternationalBoundaryPosts',FRAME,(p[0],F3,p[1]),(p[0],F3+3,p[1]),.035,8)
booths=[r for r in records if r['kind']=='immigration booth'];gaps=[]
# Close the north end of the post-border waiting strip against the screening bank.
# Without this return, passengers could walk round the first security lane.
wall('Interior_PostBorderNorthReturn',(111,12),(111,33.6),F3,3,ARR_GLASS)
wall('Interior_PostBorderNorthReturn',(111,12),(128.93,12),F3,3,ARR_GLASS)
for i,r in enumerate(booths):
    old=np.array(r['position']);new=np.array([111,F3,35.5+3*i])
    group='Interior_Circulation_IMM-I-'+str(i+1).zfill(2)
    for (name,mat),data in groups.items():
        if name!=group:continue
        for v in data['v']:
            dx=v[:,0]-old[0];dz=v[:,2]-old[2]
            v[:,0]=new[0]-dz;v[:,2]=new[2]+dx
    r['position']=new.tolist()
    a=new[2]+.85;b=new[2]+2.25;gaps.append((a,b,r['id']))
    for zz in [a,b]:box('Interior_ImmigrationPassageReaders',FRAME,(111,F3+.5,zz),(.4,1,.16))
cursor=33.6
for a,b,_ in gaps:
    wall('Interior_ImmigrationControlledBoundary',(111,cursor),(111,a),F3,3,ARR_GLASS);cursor=b
wall('Interior_ImmigrationControlledBoundary',(111,cursor),(111,68),F3,3,ARR_GLASS)
label('Interior_InternationalFlowSigns','边防检查 → 安全检查','IMMIGRATION THEN SECURITY',(110.6,F3+2.7,55.5),5,.65,'z')
flow=dict(status='User-confirmed separator topology; dimensions estimated',public_stair_to_border=[[88.2879,36.5349],[86.5,36.5349],[86.5,65],[107,65],[107,55]],border_to_security=[[107,55],[111,55],[115,55],[125.2,55],[125.2,48]],controlled_apertures=gaps,forbidden_shortcut=[[88.2879,36.5349],[100,30]])
(ROOT/'international-flow.json').write_text(json.dumps(flow,ensure_ascii=False,indent=2),encoding='utf-8')
