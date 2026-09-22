"""Border bank moved to the user's marked front return; old bank becomes wall."""
for a,b in [((75,33.2),(111,33.2)),((111,12),(111,63)),((111,12),(128.93,12))]:
    wall('Interior_InternationalPurpleBoundary',a,b,F3,3,ARR_GLASS)
booths=[r for r in records if r['kind']=='immigration booth'];gaps=[]
for i,r in enumerate(booths):
    old=np.array(r['position']);source=project([1451+(1563-1451)*i/9,834+(767-834)*i/9]);new=np.array([source[0],F3,60.0])
    name_target='Interior_Circulation_IMM-I-'+str(i+1).zfill(2)
    for (name,mat),data in groups.items():
        if name==name_target:
            for v in data['v']:v+=new-old
    r['position']=new.tolist()
    a=new[0]+.85;b=new[0]+2.05;gaps.append((a,b,r['id']))
    for xx in [a,b]:box('Interior_ImmigrationPassageReaders',FRAME,(xx,F3+.5,60),(.16,1,.4))
cursor=75+(60-48)*(45-75)/(65-48)
for a,b,_ in gaps:
    wall('Interior_ImmigrationControlledBoundary',(cursor,60),(a,60),F3,3,ARR_GLASS);cursor=b
wall('Interior_ImmigrationControlledBoundary',(cursor,60),(111,60),F3,3,ARR_GLASS)
wall('Interior_InternationalOuterWall',(147.35,12),(147.35,68),F3,3,WHITE)
label('Interior_InternationalFlowSigns','边防检查','IMMIGRATION',(94,F3+2.7,62.7),5,.65)
flow=dict(status='User marked front border bank and outer wall; dimensions estimated',public_stair_to_border=[[88.2879,36.5349],[86.5,36.5349],[86.5,60],[85.1,60],[85.1,61]],border_to_security=[[85.1,61],[85.1,65],[115,65],[115,55],[125.2,55],[125.2,48]],controlled_apertures=gaps,forbidden_shortcut=[[88.2879,36.5349],[100,30]])
(ROOT/'international-flow.json').write_text(json.dumps(flow,ensure_ascii=False,indent=2),encoding='utf-8')
