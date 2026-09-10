"""Cast nine longitudinal clearance rays through actual exported triangles."""
exec((__import__('pathlib').Path(__file__).parent/'check_fixes.py').read_text(encoding='utf-8'))
collisions=[]
rays=[(y,z) for y in [12.35,13.1,13.85] for z in [4.9,5.5,6.1]]
for node in d['nodes']:
    name=node['name']
    if not name.startswith(('Interior_','Structure_','Facade_')):continue
    vv=positions(node);lo=vv.min(axis=0);hi=vv.max(axis=0)
    if hi[1]<12.35 or lo[1]>13.85 or hi[2]<4.9 or lo[2]>6.1:continue
    t=vv.reshape(-1,3,3)
    for y,z in rays:
        a=t[:,0];u=t[:,1]-a;v=t[:,2]-a
        den=u[:,1]*v[:,2]-u[:,2]*v[:,1];good=np.abs(den)>1e-9
        aa=a[good];uu=u[good];v0=v[good];de=den[good]
        s=((y-aa[:,1])*v0[:,2]-(z-aa[:,2])*v0[:,1])/de
        q=(uu[:,1]*(z-aa[:,2])-uu[:,2]*(y-aa[:,1]))/de
        x=aa[:,0]+s*uu[:,0]+q*v0[:,0]
        hit=(s>=0)&(q>=0)&(s+q<=1)&(x>-377)&(x<377)
        if hit.any():collisions.append(dict(mesh=name,ray_yz=[y,z],x=np.round(x[hit],3).tolist()[:8]))
zone=[h for h in collisions if h['mesh'].startswith('Interior_ZoneSeparation')]
unexpected=[h for h in collisions if not h['mesh'].startswith('Interior_ZoneSeparation')]
assert len({tuple(h['ray_yz']) for h in zone})==9, 'Domestic/international separation has an unintended opening'
out={'zones_checked_x':[[-377,74],[76,377]],'clearance_strip_z':[4.9,6.1],'unexpected_collisions':unexpected,'separation_blocks_all_nine_cross_zone_rays':True,'passed':not unexpected,'scope':'Domestic and international circulation are separate. Cross-zone passage is intentionally blocked.'}
(R/'corridor-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False));assert not unexpected
