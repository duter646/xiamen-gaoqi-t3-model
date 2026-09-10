"""Separate the public stair approach from the post-immigration screening hall.
The constrained flow is required; precise return-wall coordinates are estimates.
"""
g='Interior_InternationalPreBorderEnclosure'
# Enclose the existing stair upper landing and route it to the public side of
# immigration. There is no opening from this landing into the screening hall.
for a,b in [((84,34),(101,34)),((101,34),(101,40)),((101,40),(90,40)),((84,34),(84,64)),((90,40),(90,64))]:
    wall(g,a,b,F3,3.0,ARR_GLASS)
label(g,'边防检查  ↓','IMMIGRATION FIRST',(87,F3+2.6,63.8),3,.6)
booths=[r for r in records if r['kind']=='immigration booth']
for r in booths:
    if 83<r['position'][0]<91:
        for key in list(groups):
            if key[0]=='Interior_Circulation_IMM-I-'+r['id'].split('-')[-1].zfill(2):del groups[key]
gaps=[(84,90,'public approach corridor')]
for r in booths:
    x,_,z=r['position'];a=x+.85;b=x+2.25
    if a<90 and b>84:continue
    gaps.append((a,b,r['id']))
    for xx in [a,b]:box('Interior_ImmigrationPassageReaders',FRAME,(xx,F3+.5,60),(.16,1,.4))
cursor=53.83
for a,b,id in sorted(gaps):
    if a>cursor:wall('Interior_ImmigrationControlledBoundary',(cursor,60),(a,60),F3,3.0,ARR_GLASS)
    cursor=max(cursor,b)
if cursor<147.5:wall('Interior_ImmigrationControlledBoundary',(cursor,60),(147.5,60),F3,3.0,ARR_GLASS)
label('Interior_InternationalFlowSigns','边防检查 → 安全检查','IMMIGRATION THEN SECURITY',(110,F3+2.6,58.8),6,.65)
flow={'status':'ordered processing represented; exact wall line requires current floor plan','public_stair_to_border':[[88.2879,36.5349],[86.5,36.5349],[86.5,65],[105.2,65]],'border_to_security':[[105.2,65],[105.2,60],[105.2,54],[125.2,54],[125.2,48]],'controlled_apertures':gaps,'forbidden_shortcut':[[88.2879,36.5349],[120,36.5349]]}
(ROOT/'international-flow.json').write_text(json.dumps(flow,ensure_ascii=False,indent=2),encoding='utf-8')

