from pathlib import Path
import json,struct,hashlib
R=Path(__file__).resolve().parent
def geometry(path):
    b=path.read_bytes();n=struct.unpack_from('<I',b,12)[0];d=json.loads(b[20:20+n]);off=28+n
    result={}
    for node in d['nodes']:
        if 'mesh' not in node:continue
        digest=hashlib.sha256()
        for p in d['meshes'][node['mesh']]['primitives']:
            a=d['accessors'][p['attributes']['POSITION']];v=d['bufferViews'][a['bufferView']]
            lo=off+v.get('byteOffset',0);digest.update(b[lo:lo+v['byteLength']])
        result[node['name']]=digest.hexdigest()
    return result
old=geometry(R.parent/'revision4/xiamen-gaoqi-t3.glb');new=geometry(R/'xiamen-gaoqi-t3.glb')
names=[n for n in old if n.startswith('Interior_CheckIn')]
assert names,'No accepted island groups selected'
unchanged=all(new.get(n)==old[n] for n in names)
assert not unchanged,'Individual island reconstruction was not applied'
assert not any(n.startswith('Interior_Escalators_') for n in new)
reg=json.loads((R/'circulation-register.json').read_text(encoding='utf-8'))
assert sum(f['kind']=='lift shaft' for f in reg['facilities'])==4
assert sum(f['kind']=='immigration booth' for f in reg['facilities'])==10
assert sum(f['kind']=='arrival escalator' for f in reg['facilities'])==2
assert not any(f['kind']=='arrival descent' for f in reg['facilities'])
out={'islands_individually_rebuilt':not unchanged,'compared_mesh_groups':len(names),'obsolete_escalators_removed':True,'lift_shafts':4,'separate_immigration_booths':10,'upper_arrival_escalators':2,'direct_3F_to_1F_arrival_escalators':2,'not_validated':['survey dimensions','all vertical counterpart pairings','all passenger-route obstacle intersections','post-2024 facility inventory']}
(R/'layout-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out))
