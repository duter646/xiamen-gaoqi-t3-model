"""Structural checks for the delivered GLB (not the Khronos validator)."""
from pathlib import Path
import struct,json,hashlib
import numpy as np
p=Path(__file__).with_name('xiamen-gaoqi-t3.glb');data=p.read_bytes()
magic,version,total=struct.unpack_from('<III',data)
assert magic==0x46546c67 and version==2 and total==len(data)
jlen,jtype=struct.unpack_from('<II',data,12);assert jtype==0x4e4f534a
d=json.loads(data[20:20+jlen]);bpos=20+jlen;blen,btype=struct.unpack_from('<II',data,bpos)
assert btype==0x004e4942 and bpos+8+blen==total
binary=data[bpos+8:];assert d['buffers'][0]['byteLength']==len(binary)
for v in d['bufferViews']:
    assert v.get('byteOffset',0)%4==0
    assert 0<=v.get('byteOffset',0)<=v.get('byteOffset',0)+v['byteLength']<=len(binary)
for a in d['accessors']:
    v=d['bufferViews'][a['bufferView']];n={'SCALAR':1,'VEC2':2,'VEC3':3}[a['type']]
    assert a['componentType']==5126 and a['count']*n*4==v['byteLength']
    arr=np.frombuffer(binary,dtype='<f4',count=a['count']*n,offset=v.get('byteOffset',0)).reshape(-1,n)
    assert np.isfinite(arr).all()
    if 'min' in a:assert np.allclose(arr.min(0),a['min']) and np.allclose(arr.max(0),a['max'])
for m in d['meshes']:
    for p1 in m['primitives']:
        att=p1['attributes'];count=d['accessors'][att['POSITION']]['count'];assert count%3==0
        assert d['accessors'][att['NORMAL']]['count']==count
        mat=d['materials'][p1['material']]
        if 'baseColorTexture' in mat['pbrMetallicRoughness']:
            assert d['accessors'][att['TEXCOORD_0']]['count']==count
for im in d['images']:
    assert im['mimeType']=='image/png' and 'uri' not in im
    v=d['bufferViews'][im['bufferView']];o=v.get('byteOffset',0);assert binary[o:o+8]==b'\x89PNG\r\n\x1a\n'
report={'format':'GLB 2.0','structural_checks':'passed','meshes':len(d['meshes']),'embedded_textures':len(d['images']),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'notes':'Checks bounds, chunks, finite geometry, matching attribute counts, embedded PNGs. Browser visual checks recorded separately.'}
Path(__file__).with_name('validation-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
