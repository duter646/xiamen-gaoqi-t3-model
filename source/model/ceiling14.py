"""Horizontal suspended ceilings below each roof terrace, independent of weather roof."""
flat_ceiling_report=[]
for (name,mat),data in groups.items():
    if name!='Roof_MainSoffit':continue
    for v in data['v']:
        y=float(v[:,1].min());v[:,1]=y
        flat_ceiling_report.append(dict(y=y,z_min=float(v[:,2].min()),z_max=float(v[:,2].max())))
(ROOT/'flat-ceiling-register.json').write_text(json.dumps(flat_ceiling_report,indent=2),encoding='utf-8')
