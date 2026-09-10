from pathlib import Path
R=Path(__file__).resolve().parent
exec((R/'check_arrivals.py').read_text(encoding='utf-8').split('inv=json.loads')[0])
reg=json.loads((R/'circulation-register.json').read_text(encoding='utf-8'))['facilities'];stair=next(r for r in reg if r['id']=='L3-E06')
a=np.array(stair['lower_landing']);b=np.array(stair['position']);issues=[]
for side in [-.72,.72]:
 for height in [.3,1,1.7]:
  h=hits(a+[0,height,side],b+[0,height,side])
  if h:issues.append(dict(stair=h))
for x in [90,94,97]:
 for z in [35.4,36.5,37.7]:
  h=hits(np.array([x,6.0,z]),np.array([x,6.5,z]))
  if any(n.startswith(('Structure_DepartureFloor','Roof_ArrivalCeiling')) for n in h):issues.append(dict(lower_void=[x,z],hits=h))
landing=hits(a+[0,-.35,0],a+[0,.015,0])
if not any(n.startswith('Structure_DepartureFloor') for n in landing):issues.append(dict(missing_lower_landing=True))
ceilings=json.loads((R/'flat-ceiling-register.json').read_text());out=dict(international_stair_and_lower_void_issues=issues,flat_ceiling_panels=len(ceilings),sign_source='unchanged RGBA user image, not stretched')
(R/'revision14-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=False));assert not issues
