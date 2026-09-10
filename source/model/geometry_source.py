"""Photo-informed XMN T3 study. Dimensions are estimated, metres, glTF Y-up.
Run with Python + numpy + Pillow. No modelling application is required.
"""
from pathlib import Path
import json, struct, math, io
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
groups = {}
materials = []
def material(name, color, metal=0, rough=.5, alpha=1, emission=None):
    m = {'name':name,'pbrMetallicRoughness':{'baseColorFactor':[*color,alpha], 'metallicFactor':metal,'roughnessFactor':rough},'doubleSided':True}
    if alpha < 1: m['alphaMode']='BLEND'
    if emission: m['emissiveFactor']=emission
    materials.append(m)
    return len(materials)-1
WHITE=material('Warm white aluminium',[.85,.87,.83],.3,.38)
FRAME=material('Pale structural steel',[.69,.73,.72],.55,.3)
STONE=material('Ivory limestone',[.72,.70,.63],0,.7)
DARK=material('Graphite metal',[.055,.07,.08],.45,.32)
GLASS=material('Blue green glazing',[.25,.48,.51],.15,.15,.28)
FLOOR=material('Polished warm terrazzo',[.64,.62,.55],.15,.24)
TRIM=material('Black stone inlay',[.11,.14,.14],.2,.23)
ROAD=material('Asphalt',[.12,.15,.16],0,.95)
CONCRETE=material('Apron concrete',[.48,.51,.50],0,.85)
YELLOW=material('Apron yellow',[.97,.62,.055],0,.8)
BLUE=material('Blue check in counters',[.018,.26,.40],.15,.35)
SEAT=material('Teal seats',[.05,.27,.31],.1,.5)
PURPLE=material('Violet seats',[.30,.14,.31],.1,.5)
BELT=material('Queue belt',[.015,.23,.41],0,.6)
GREEN=material('Landscape foliage',[.14,.31,.18],0,.9)
GREEN2=material('Foliage highlight',[.27,.43,.20],0,.9)
TRUNK=material('Tree trunks',[.27,.21,.13],0,.95)
BRICK=material('Minnan brick',[.43,.20,.13],0,.8)
LIGHT=material('Warm ceiling light',[.96,.9,.68],0,.3,emission=[.8,.72,.45])
SCREEN=material('Screen blue',[.015,.12,.23],.1,.25,emission=[.025,.16,.25])
texture_images=[]
def procedural_texture(mat,name,kind):
    rng=np.random.default_rng(32); size=512
    if kind=='stone':
        noise=rng.normal(0,7,(size,size,1)); base=np.array([193,190,176]); arr=np.clip(base+noise,0,255).astype('uint8')
        for _ in range(5500):
            x,y=rng.integers(0,size,2); arr[y,x]=rng.choice([95,125,220])
    elif kind=='ceiling':
        arr=np.full((size,size,3),221,dtype='uint8');arr[::32,:,:]=166;arr[:,::256,:]=155
    else:
        arr=np.full((size,size,3),[147,79,53],dtype='uint8')
        for y in range(0,size,64):
            arr[y:y+4]=[191,178,147]
            for x in range((y//64%2)*64,size,128):arr[y:y+64,x:x+3]=[191,178,147]
    im=Image.fromarray(arr);p=ROOT/(name+'.png');im.save(p);texture_images.append(p)
    materials[mat]['pbrMetallicRoughness']['baseColorTexture']={'index':len(texture_images)}
    materials[mat]['pbrMetallicRoughness']['baseColorFactor']=[1,1,1,1]
procedural_texture(FLOOR,'terrazzo','stone')
CEILING=material('Linear ceiling panels',[.8,.8,.76],.05,.65)
procedural_texture(CEILING,'ceiling-panels','ceiling')
procedural_texture(BRICK,'minnan-brick','brick')

def mesh(g,m,v,f,uv=None):
    key=(g,m)
    a=groups.setdefault(key, {'v':[],'f':[],'uv':[],'n':0})
    vv=np.asarray(v,dtype=np.float32); ff=np.asarray(f,dtype=np.uint32)
    a['v'].append(vv); a['f'].append(ff+a['n']); a['n']+=len(vv)
    if uv is None:
        if m in [FLOOR,CEILING]:uv=vv[:,[0,2]]/(3 if m==FLOOR else 8)
        elif m==BRICK:uv=vv[:,[0,1]]/3
        else:uv=np.zeros((len(vv),2))
    a['uv'].append(np.asarray(uv,dtype=np.float32))

BOX_F=np.array([[0,2,1],[0,3,2],[4,5,6],[4,6,7],[0,1,5],[0,5,4],[3,7,6],[3,6,2],[0,4,7],[0,7,3],[1,2,6],[1,6,5]])
def box(g,m,c,s):
    v=np.array([[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]],dtype=float)*np.array(s)/2+np.array(c)
    mesh(g,m,v,BOX_F)

def rod(g,m,a,b,r=.12,n=8,r2=None):
    a=np.array(a,float); b=np.array(b,float); d=b-a; length=np.linalg.norm(d)
    if length<1e-6:return
    d/=length; tmp=np.array([0,1,0]) if abs(d[1])<.9 else np.array([1,0,0])
    u=np.cross(d,tmp); u/=np.linalg.norm(u); v=np.cross(d,u)
    pts=[]
    for p,rr in [(a,r),(b,r if r2 is None else r2)]:
        pts.extend(p+rr*(math.cos(t)*u+math.sin(t)*v) for t in np.linspace(0,2*math.pi,n,endpoint=False))
    pts.extend([a,b]); faces=[]
    for i in range(n):
        j=(i+1)%n; faces.extend([(i,j,n+j),(i,n+j,n+i),(2*n,j,i),(2*n+1,n+i,n+j)])
    mesh(g,m,pts,faces)

def path(g,m,pts,r=.1,n=6):
    for a,b in zip(pts,pts[1:]): rod(g,m,a,b,r,n)

def disc(g,m,c,r,normal=(0,0,1),n=40):
    c=np.array(c); d=np.array(normal,float); u=np.array([1.,0,0]) if abs(d[0])<.5 else np.array([0.,0,1])
    v=np.cross(d,u); pts=[c]+[c+r*(u*math.cos(t)+v*math.sin(t)) for t in np.linspace(0,2*math.pi,n,endpoint=False)]
    mesh(g,m,pts,[(0,1+i,1+(i+1)%n) for i in range(n)])

def ring(g,m,c,r,t=.13,n=48,normal=(0,0,1)):
    c=np.array(c); d=np.array(normal,float); u=np.array([1.,0,0]) if abs(d[0])<.5 else np.array([0.,0,1]); v=np.cross(d,u)
    pts=[c+rr*(u*math.cos(a)+v*math.sin(a)) for rr in [r-t,r+t] for a in np.linspace(0,2*math.pi,n,endpoint=False)]
    mesh(g,m,pts,[(i,(i+1)%n,n+(i+1)%n) for i in range(n)]+[(i,n+(i+1)%n,n+i) for i in range(n)])

def window_wall(cx,z,y=12.1,r=2.8,pitch=7.0):
    # Actual aperture geometry: square surround with circular hole, not a decal.
    g='Facade_RoundWindows'; n=48; vv=[]
    for j in range(n):
        t=2*math.pi*j/n; co=math.cos(t); si=math.sin(t)
        rr=min((pitch/2)/max(abs(co),1e-8),3.5/max(abs(si),1e-8))
        vv.extend([(cx+r*co,y+r*si,z),(cx+rr*co,y+rr*si,z)])
    mesh(g,WHITE,vv,[(2*i,2*((i+1)%n),2*((i+1)%n)+1) for i in range(n)]+[(2*i,2*((i+1)%n)+1,2*i+1) for i in range(n)])
    ring(g,FRAME,(cx,y,z+.04),r,.12)
    ring(g,WHITE,(cx,y,z-.09),r+.13,.12)
    disc(g,GLASS,(cx,y,z),r-.10)
    box(g,FRAME,(cx,y-.65,z+.07),(r*2,.085,.11))
    box(g,FRAME,(cx,y,z+.07),(.085,r*2,.11))

# Original bilingual sign atlas. Reference photos are not used as textures.
atlas=Image.new('RGB',(2048,4096),(17,32,41)); draw=ImageDraw.Draw(atlas)
fontpath='C:/Windows/Fonts/msyh.ttc'
labels=[('厦门高崎国际机场','XIAMEN GAOQI INTERNATIONAL AIRPORT'),('T3 航站楼','TERMINAL 3'),('国内出发  ↑','DOMESTIC DEPARTURES'),('国际出发  ↑','INTERNATIONAL DEPARTURES'),('值机区  A · B · C','CHECK-IN'),('值机区  D · E · F · G','CHECK-IN'),('安全检查  ↑','SECURITY CHECK'),('登机口  01 — 17','BOARDING GATES'),('到达出口  →','ARRIVALS / EXIT'),('问询服务  i','INFORMATION'),('头等舱候机室','FIRST CLASS LOUNGE'),('卫生间  →','RESTROOMS'),('出发航班','DEPARTURES'),('厦门航空','XIAMENAIR'),('候机区','WAITING AREA'),('欢迎来到厦门','WELCOME TO XIAMEN')]+[(f'{g:02d}  登机口',f'GATE {g:02d} / BOARDING') for g in [1,2,3,5,6,7,8,9,10,11,12,15,16,17]]
for i,(cn,en) in enumerate(labels):
    y=i*128; draw.rectangle((0,y,2047,y+127),fill=(17,37,48)); draw.rectangle((0,y,12,y+127),fill=(199,177,108))
    draw.text((38,y+8),cn,font=ImageFont.truetype(fontpath,48),fill=(240,241,224))
    draw.text((40,y+76),en,font=ImageFont.truetype(fontpath,24),fill=(175,204,211))
atlas.save(ROOT/'signage-atlas.png')
SIGN=material('Bilingual signage atlas',[1,1,1],0,.5,emission=[.10,.10,.10]); materials[SIGN]['pbrMetallicRoughness']['baseColorTexture']={'index':0}
def sign(g,i,c,w,h,flip=False):
    x,y,z=c; box(g,DARK,(x,y,z),(w+.08,h+.08,.12))
    z+= -.075 if flip else .075
    v=[(x-w/2,y-h/2,z),(x+w/2,y-h/2,z),(x+w/2,y+h/2,z),(x-w/2,y+h/2,z)]
    # Use left half of atlas; enough room for the bilingual label.
    cn,en=labels[i]
    crop=(max(draw.textlength(cn,font=ImageFont.truetype(fontpath,48)),draw.textlength(en,font=ImageFont.truetype(fontpath,24)))+80)/2048
    uv=[(0,(i+1)/32),(crop,(i+1)/32),(crop,i/32),(0,i/32)]
    if flip:uv=[uv[1],uv[0],uv[3],uv[2]]
    mesh(g,SIGN,v,[(0,1,2),(0,2,3)],uv)

def rail(g,a,b,h=1.1):
    a=np.array(a,float);b=np.array(b,float);dist=np.linalg.norm(b-a)
    for t in np.linspace(0,1,max(2,int(dist/2)+1)):
        p=a*(1-t)+b*t; rod(g,FRAME,p,p+[0,h,0],.045,6)
    rod(g,FRAME,a+[0,h,0],b+[0,h,0],.055,8)
    rod(g,FRAME,a+[0,.45,0],b+[0,.45,0],.025,6)

def plant(g,x,y,z,scale=1):
    rod(g,STONE,(x,y,z),(x,y+.65*scale,z),.48*scale,12,r2=.64*scale)
    rod(g,TRUNK,(x,y+.5*scale,z),(x,y+2.2*scale,z),.07*scale,8)
    for j in range(19):
        t=j*2.399; rad=(.35+.35*(j%4)/3)*scale
        stem=np.array([x,y+(.9+j*.065)*scale,z]);tip=stem+np.array([math.cos(t)*rad,.32*scale,math.sin(t)*rad])
        rod(g,TRUNK,stem,tip,.018*scale,5)
        along=np.array([math.cos(t),.3,math.sin(t)]);across=np.array([-math.sin(t),0,math.cos(t)])
        vv=[]
        for k in range(9):
            u=k/8;center=tip+along*u*.58*scale;center[1]+=.12*math.sin(u*math.pi)*scale
            w=.21*math.sin(u*math.pi)*scale
            vv.extend([center-across*w,center+[0,.045*scale,0],center+across*w])
        mesh(g,GREEN if j%3 else GREEN2,vv,[(k*3+a,k*3+a+1,(k+1)*3+a+1) for k in range(8) for a in [0,1]]+[(k*3+a,(k+1)*3+a+1,(k+1)*3+a) for k in range(8) for a in [0,1]])


# Site and frontage.
# Export standard GLB, separate named nodes by architectural group and material.
doc={'asset':{'version':'2.0','generator':'XMN T3 photo-informed procedural architectural study','extras':{'units':'metres','accuracy':'Estimated dimensions and interpretive interiors; not surveyed BIM','references':'See README.md'}},'scene':0,'scenes':[{'name':'Xiamen_Gaoqi_T3','nodes':[]}], 'nodes':[],'meshes':[],'materials':materials,'buffers':[{'byteLength':0}],'bufferViews':[],'accessors':[],'images':[],'textures':[{'source':0,'sampler':0}],'samplers':[{'magFilter':9729,'minFilter':9987,'wrapS':33071,'wrapT':33071}]}
binary=bytearray()
def view(data,target=None):
    while len(binary)%4:binary.append(0)
    i=len(doc['bufferViews']);a={'buffer':0,'byteOffset':len(binary),'byteLength':len(data)}
    if target:a['target']=target
    doc['bufferViews'].append(a);binary.extend(data);return i
def accessor(a,typ,component,target,bounds=False):
    i=len(doc['accessors']);o={'bufferView':view(a.tobytes(),target),'componentType':component,'count':len(a),'type':typ}
    if bounds:o.update(min=a.min(axis=0).tolist(),max=a.max(axis=0).tolist())
    doc['accessors'].append(o);return i
doc['images'].append({'bufferView':view((ROOT/'signage-atlas.png').read_bytes()),'mimeType':'image/png','name':'Original bilingual signage'})
doc['samplers'].append({'magFilter':9729,'minFilter':9987,'wrapS':10497,'wrapT':10497})
for p in texture_images:
    doc['textures'].append({'source':len(doc['images']),'sampler':1})
    doc['images'].append({'bufferView':view(p.read_bytes()),'mimeType':'image/png','name':p.stem})
stats={'triangles':0,'vertices':0,'nodes':0,'groups':[], 'estimated_main_hall_m':[240,96], 'estimated_concourse_length_m':476}
for (g,m),a in groups.items():
    v=np.concatenate(a['v']);f=np.concatenate(a['f']);uv=np.concatenate(a['uv'])
    # Expanded triangles preserve hard architectural edges and correct normals.
    p=v[f].reshape(-1,3);n=np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]])
    norm=np.linalg.norm(n,axis=1);valid=norm>1e-8
    if not np.all(valid):
        f=f[valid];p=v[f].reshape(-1,3);n=n[valid];norm=norm[valid]
    n=np.repeat(n/norm[:,None],3,axis=0).astype('<f4');p=p.astype('<f4')
    attr={'POSITION':accessor(p,'VEC3',5126,34962,True),'NORMAL':accessor(n,'VEC3',5126,34962)}
    if 'baseColorTexture' in materials[m]['pbrMetallicRoughness']:attr['TEXCOORD_0']=accessor(uv[f].reshape(-1,2).astype('<f4'),'VEC2',5126,34962)
    mi=len(doc['meshes']);doc['meshes'].append({'name':g+'_'+materials[m]['name'],'primitives':[{'attributes':attr,'material':m,'mode':4}]})
    ni=len(doc['nodes']);doc['nodes'].append({'name':g+'_'+str(m),'mesh':mi,'extras':{'layer':g}});doc['scenes'][0]['nodes'].append(ni)
    stats['triangles']+=len(f);stats['vertices']+=len(p)
    if g not in stats['groups']:stats['groups'].append(g)
while len(binary)%4:binary.append(0)
doc['buffers'][0]['byteLength']=len(binary)
js=json.dumps(doc,ensure_ascii=False,separators=(',',':')).encode();js+=b' '*((-len(js))%4)
out=struct.pack('<III',0x46546c67,2,12+8+len(js)+8+len(binary))+struct.pack('<II',len(js),0x4e4f534a)+js+struct.pack('<II',len(binary),0x004e4942)+binary
(ROOT/'xiamen-gaoqi-t3.glb').write_bytes(out)
stats.update(nodes=len(doc['nodes']),size_bytes=len(out));(ROOT/'model-stats.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in stats.items() if k!='groups'},indent=2))
