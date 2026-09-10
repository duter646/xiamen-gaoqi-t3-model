"""Primitive-level audit: distinguish collisions from merely shared group bounds."""
def bounds(v):return np.min(v,axis=0),np.max(v,axis=0)
def column_hits():
    cols=[]
    for (g,m),a in groups.items():
        if g not in ['Structure_Columns','Interior_ConcourseColumns']:continue
        for v in a['v']:
            lo,hi=bounds(v);cols.append(((lo+hi)/2,(hi[0]-lo[0])/2,lo[1],hi[1]))
    hits=[]
    for (g,m),a in groups.items():
        if not g.startswith(('Interior_Facility_','Interior_Circulation_D-SH','Interior_Circulation_D-CF','Interior_Circulation_I-SH','Interior_Circulation_SEC-')):continue
        for i,v in enumerate(a['v']):
            if len(v)!=8:continue
            lo,hi=bounds(v)
            for c,r,y0,y1 in cols:
                if min(hi[1],y1)-max(lo[1],y0)<.06:continue
                nearest=np.maximum(lo[[0,2]],np.minimum(c[[0,2]],hi[[0,2]]))
                if np.linalg.norm(nearest-c[[0,2]])<r-.03:
                    hits.append(dict(group=g,material=m,primitive=i,column=c[[0,2]].tolist(),box=[lo.tolist(),hi.tolist()]));break
    return hits
audit_before=column_hits()
(ROOT/'audit-initial.json').write_text(json.dumps(dict(column_fixture_intersections=audit_before),indent=2),encoding='utf-8')
print('Fixture/column overlaps:',len(audit_before))
