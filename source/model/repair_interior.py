"""Repair verified local interference, preserve surveyed/accepted plan anchors."""
def rebuild_group(key,keep):
    old=groups.pop(key);g,m=key
    for i in keep:
        offset=sum(len(v) for v in old['v'][:i])
        mesh(g,m,old['v'][i],old['f'][i]-offset,old['uv'][i])

# Two shop back panels touch columns. Wrap the domestic panel around the column;
# move the international back panel 35 cm away, without moving the shop front.
repairs=[]
for key,data in groups.items():
    if key[0]=='Interior_Circulation_I-SH01':
        for v in data['v']:v[:,0]-=9
for rec in records:
    if rec['id']=='I-SH01':rec['position'][0]-=9
repairs.append('I-SH01 moved 9 m west to clear first international screening lane; inferred footprint')
for key,data in list(groups.items()):
    if key[0] not in ['Interior_Circulation_D-SH02','Interior_Circulation_I-SH01'] or key[1]!=WHITE:continue
    v=data['v'][0];lo,hi=bounds(v);c=(lo+hi)/2
    if key[0].endswith('I-SH01'):
        v[:,2]-=.35;repairs.append('I-SH01 back wall offset -0.35 m');continue
    rebuild_group(key,list(range(1,len(data['v']))))
    xcol=-62.5;z=c[2];y=c[1];h=hi[1]-lo[1]
    for a,b in [(lo[0],xcol-.68),(xcol+.68,hi[0])]:
        if b>a:box(key[0],WHITE,((a+b)/2,y,z),(b-a,h,.15))
    box(key[0],WHITE,(xcol,y,z-.8),(1.36,h,.15))
    for x in [xcol-.68,xcol+.68]:box(key[0],WHITE,(x,y,z-.4),(.15,h,.8))
    repairs.append('D-SH02 back wall wraps structural column')

# Replace uninterrupted atrium rails with rails that leave arrival bridge entries.
for key in list(groups):
    if key[0]=='Interior_AtriumGuardrails':del groups[key]
bridges=[r for r in records if r['kind']=='arrival escalator']
rail_gaps=[]
for h in holes[-3:]:
    for z in h[2:]:
        cuts=[]
        for r in bridges:
            x,_,end=r['position']
            if 12<=z<=end+1.0 and h[0]<x<h[1]:cuts.append((x-1.8,x+1.8));rail_gaps.append(dict(id=r['id'],z=z,x_span=[x-1.8,x+1.8]))
        cursor=h[0]
        for a,b in sorted(cuts):
            if a>cursor:rail('Interior_AtriumGuardrails',(cursor,F3,z),(a,F3,z))
            cursor=b
        if cursor<h[1]:rail('Interior_AtriumGuardrails',(cursor,F3,z),(h[1],F3,z))
    for x in h[:2]:rail('Interior_AtriumGuardrails',(x,F3,h[2]),(x,F3,h[3]))

# Glass infill follows the rebuilt guardrails, including their doorway breaks.
for (name,mat),data in list(groups.items()):
    if name!='Interior_AtriumGuardrails':continue
    for v in data['v']:
        lo,hi=bounds(v)
        if hi[1]-lo[1]>.13 or abs((lo[1]+hi[1])/2-(F3+1.1))>.06:continue
        a=(lo+hi)/2;b=a.copy();axis=0 if hi[0]-lo[0]>hi[2]-lo[2] else 2
        a[axis]=lo[axis]+.06;b[axis]=hi[axis]-.06;a[1]=b[1]=F3+.55
        beam('Interior_AtriumGlass',GLASS,a,b,.045,.88)

# Add omitted lower lift lobbies under the gate corridor; footprint only, no
# invented arrivals circulation beyond the small supporting landing.
for x,z in [(-78,-2.5),(114,1.7)]:
    box('Structure_LowerLiftLanding',FLOOR,(x,F2-.2,z+3.1),(4.0,.4,3.2))
    for side in [-1,1]:rail('Interior_LowerLiftLandingRails',(x+side*2,F2,z+1.5),(x+side*2,F2,z+4.7))

# Cap small source-supported shop rooms: previous walls were left open to the sky.
for rec in records:
    if rec['kind']!='source block':continue
    x,_,z=rec['position'];w,d=rec['footprint_estimated']
    box('Roof_LocalShopCeilings',CEILING,(x,F3+2.98,z),(w,.12,d))

for gate in mapping['gates']:
    if int(gate['tags'].get('ref','0')) not in gate_numbers:continue
    x,_=gate['point']
    for dx in [-1.15,1.15]:rod('Interior_GateSignSuspension',FRAME,(x+dx,FG+3.07,-8),(x+dx,FG+5.38,-8),.016,6)

# Reference palette, applied by material rather than a global lighting tint.
def recolor(m,col,rough=None,metal=None):
    p=materials[m]['pbrMetallicRoughness'];p['baseColorFactor'][:3]=col
    if rough is not None:p['roughnessFactor']=rough
    if metal is not None:p['metallicFactor']=metal
recolor(SEC_FLOOR,[.48,.46,.40],.32,.08)
recolor(SEAT,[.16,.25,.17],.58,.02)
recolor(UPHOLSTERY,[.43,.25,.12],.58,.02)
recolor(TAUPE,[.49,.47,.41],.43,.18)
recolor(WOOD,[.30,.14,.055],.5,.02)
recolor(FRAME,[.67,.69,.67],.26,.7)
recolor(WHITE,[.87,.85,.78],.63,.04)
recolor(CEILING,[.93,.89,.78],.65,.02)
recolor(FROSTED,[.69,.79,.74],.9,0)
# Lower seats keep their photo-referenced brown material; main gate banks mix
# muted leather colours, without changing any seat footprint.
key=('Interior_Seating',SEAT)
if key in groups:
    old=groups.pop(key)
    for i,v in enumerate(old['v']):
        offset=sum(len(q) for q in old['v'][:i]);x=float(np.mean(v[:,0]))
        mat=UPHOLSTERY if int((x+384)/12)%3 else SEAT
        mesh('Interior_Seating',mat,v,old['f'][i]-offset,old['uv'][i])

after=column_hits()
report=dict(column_fixture_intersections_before=audit_before,column_fixture_intersections_after=after,repairs=repairs,arrival_bridge_rail_openings=rail_gaps,lower_lift_slab_openings=lower_holes,dimensions=dict(clear_security_portal_m=1.28,paired_escalator_tread_width_m=1.08,escalator_rise_m=F3-F2,escalator_run_m=11,seat_pitch_m=.62,counter_height_m=1.1),limits=['Only selected box primitives tested against columns, not every mesh pair.','Overall floor heights and as-built equipment dimensions remain unverified.'])
(ROOT/'circulation-register.json').write_text(json.dumps(dict(facilities=records,floor_openings=holes),ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'interior-audit-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
assert not after,'Fixture-column collision remains'
