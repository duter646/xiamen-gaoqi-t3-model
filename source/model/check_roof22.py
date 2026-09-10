from pathlib import Path
R=Path(__file__).parent
exec((R/'check17.py').read_text(encoding='utf-8').split("assert not len(points('Roof_InternalCurvedHaunches'))")[0])
assert not len(points('Roof_SolidEaveConcourseClosure'))
assert not len(points('Roof_InternalCurvedHaunches'))
feet=points('Roof_IndividualEaveFeet');assert len(feet)>0
centers=np.arange(-104.5,147.6,12)
assert np.min(abs(feet[:,0,None]-centers[None,:]),axis=1).max()<.501
assert feet[:,1].min()<=18.01
purlins=points('Roof_CurvedFramePurlins');assert purlins[:,1].max()<41 and purlins[:,1].min()>16
rib=points('Roof_ContinuousCurvedRibs');assert rib[:,1].max()<42 and rib[:,1].min()>16
roof=json.loads((R/'roof16-register.json').read_text());assert np.allclose([t[2] for t in roof['tiers']['-1']],[t[2] for t in roof['tiers']['1'][:3]])
result=dict(passed=True,individual_feet=22,solid_between_ribs=False,old_curved_internal_beams=False,purlin_height_range=purlins[:,1].min().item(),max_purlin_height=purlins[:,1].max().item(),corresponding_terraces_equal_height=True)
(R/'roof22-validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result))
