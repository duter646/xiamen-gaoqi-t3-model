"""Vertical sections of the delivered mesh for shaft and void review."""
from pathlib import Path
import hashlib,json,struct
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
raw=(ROOT/'assets/xiamen-gaoqi-t3.glb').read_bytes();n=struct.unpack_from('<I',raw,12)[0];doc=json.loads(raw[20:20+n])
meshes=[]
for node in doc['nodes']:
    name=node['name']
    if name.startswith(('Site_','Audit_','Exterior_')):continue
    for p in doc['meshes'][node['mesh']]['primitives']:
        a=doc['accessors'][p['attributes']['POSITION']];v=doc['bufferViews'][a['bufferView']]
        tri=np.frombuffer(raw,dtype='<f4',count=a['count']*3,offset=n+28+v.get('byteOffset',0)).reshape(-1,3,3)
        meshes.append((name,tri,tri[:,:,0].min(1),tri[:,:,0].max(1)))
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',22)
small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',16)
canvas=Image.new('RGB',(1500,1500),'#101820');heading=ImageDraw.Draw(canvas)
heading.text((26,12),'T3 · 电梯与挑空模型纵剖',font=font,fill='white')
heading.text((26,50),'黄色：楼板、支撑和屋面截线    青色：井道、墙体及设施截线    坐标单位：模型米',font=small,fill='#bacbdb')
lifts={r['id']:r for r in json.loads((ROOT/'source/model/circulation-register.json').read_text(encoding='utf-8'))['facilities'] if r['kind']=='lift shaft'}
views=[('西侧上层电梯',lifts['L2-L01']['position'][0],-6,16,-.3,18),('东侧上层电梯',lifts['L3-L02']['position'][0],-4,16,-.3,18),('西侧前部电梯',lifts['L2-L02']['position'][0],84,95,-.3,11),('东侧前部电梯',lifts['L2-L04']['position'][0],84,95,-.3,11),('西侧小挑空',-76,10,70,-.3,18),('主挑空及下层到达廊',40,10,70,-.3,18)]
for i,(title,x,z0,z1,y0,y1) in enumerate(views):
    tile=Image.new('RGB',(710,440),'#172733');d=ImageDraw.Draw(tile)
    d.text((16,8),title+f'  x={x:g}',font=font,fill='white')
    def project(p):return (45+(p[0]-z0)/(z1-z0)*640,400-(p[1]-y0)/(y1-y0)*340)
    for y,label in [(.3,'1F'),(6.3,'2F'),(12.1,'上层')]:
        if not y0<y<y1:continue
        py=project([z0,y])[1];d.line((45,py,688,py),fill='#385064',width=1);d.text((3,py-18),label,font=small,fill='#c5d4df')
    for name,tri,lo,hi in meshes:
        tri=tri[(lo<x)&(hi>x)]
        if not len(tri):continue
        color='#ffd166' if name.startswith(('Structure_','Roof_')) else '#66e0e6'
        for a,b,c in [(0,1,2),(1,2,0),(2,0,1)]:
            t=tri[((tri[:,a,0]<x)!=(tri[:,b,0]<x))&((tri[:,a,0]<x)!=(tri[:,c,0]<x))]
            if not len(t):continue
            ends=[]
            for other in [b,c]:
                f=(x-t[:,a,0])/(t[:,other,0]-t[:,a,0]);ends.append((t[:,a]+f[:,None]*(t[:,other]-t[:,a]))[:,[2,1]])
            for aa,bb in zip(*ends):
                if max(aa[0],bb[0])<z0 or min(aa[0],bb[0])>z1 or max(aa[1],bb[1])<y0 or min(aa[1],bb[1])>y1:continue
                d.line((project(aa),project(bb)),fill=color,width=2)
    # Overlay plot margins so outside geometry cannot obscure the title or ticks.
    d.rectangle((0,0,710,40),fill='#172733');d.text((16,8),title+f'  x={x:g}',font=font,fill='white')
    d.text((45,414),f'z={z0:g} → {z1:g}',font=small,fill='#bacbdb')
    canvas.paste(tile,(25+(i%2)*740,95+(i//2)*455))
heading.text((26,1470),'SHA-256 '+hashlib.sha256(raw).hexdigest(),font=small,fill='#bacbdb')
out=ROOT/'assets/map-sections/vertical-sections.png';canvas.save(out)
print(out)
