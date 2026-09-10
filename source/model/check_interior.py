exec((__import__('pathlib').Path(__file__).parent/'check_fixes.py').read_text(encoding='utf-8'))
reg=json.loads((R/'circulation-register.json').read_text(encoding='utf-8'))
audit=json.loads((R/'interior-audit-report.json').read_text(encoding='utf-8'))
assert not audit['column_fixture_intersections_after']
assert len(audit['arrival_bridge_rail_openings'])==2
def ray_hits(v,axis,start,end,fixed):
    t=v.reshape(-1,3,3);a=t[:,0];u=t[:,1]-a;w=t[:,2]-a;other=[i for i in range(3) if i!=axis];j,k=other
    den=u[:,j]*w[:,k]-u[:,k]*w[:,j];mask=abs(den)>1e-9
    a=a[mask];u=u[mask];w=w[mask];den=den[mask]
    s=((fixed[0]-a[:,j])*w[:,k]-(fixed[1]-a[:,k])*w[:,j])/den
    q=(u[:,j]*(fixed[1]-a[:,k])-u[:,k]*(fixed[0]-a[:,j]))/den
    at=a[:,axis]+s*u[:,axis]+q*w[:,axis]
    return bool(((s>=0)&(q>=0)&(s+q<=1)&(at>start)&(at<end)).any())
blocks=[]
for r in reg['facilities']:
    if r['kind']!='arrival escalator':continue
    x,y,z=r['position']
    for node in d['nodes']:
        if not node['name'].startswith(('Interior_Atrium','Interior_ArrivalBridge','Interior_SecurityIsolation','Interior_SupportedOpening')):continue
        v=positions(node)
        for dx in [-1.9,-1.5,-1.1]:
            for dy in [.5,1.5]:
                if ray_hits(v,2,12.05,z-.1,[x+dx,y+dy]):blocks.append((r['id'],node['name']))
        for dy in [.5,1.5]:
            if ray_hits(v,0,x-1.5,x-.1,[y+dy,z]):blocks.append((r['id'],node['name'],'turn to stair'))
assert not blocks,blocks
slab_hits=[]
for r in reg['facilities']:
    if r['kind']!='lift shaft':continue
    x,base,z=r['position'];level=r['upper_level']
    for node in d['nodes']:
        if not node['name'].startswith(('Structure_DepartureFloor','Structure_ThirdFloor','Structure_ConcourseFloor')):continue
        if ray_hits(positions(node),1,level-.5,level+.1,[x,z]):slab_hits.append((r['id'],node['name']))
assert not slab_hits,slab_hits
out={'fixture_column_collisions_after':0,'arrival_bridge_entries':2,'arrival_entry_clearance_rays':16,'arrival_entry_obstructions':blocks,'lift_top_level_slab_penetrations':slab_hits,'scope':'Bridge centreline is 1.5 m west of the east-west stair upper endpoint; checks approach and right-angle landing turn. Not building-wide collision certification.'}
(R/'interior-validation.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out))
