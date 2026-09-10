"""Additional photo-supported exterior details; numeric sizes are estimates."""
en=json.loads((ROOT/'english-mesh.json').read_text(encoding='utf-8'))
vv=np.array(en['vertices'],float);xx=vv[:,0].copy();yy=vv[:,1].copy();sc=2.2/np.ptp(yy)
vv[:,0]=C-(xx-(xx.min()+xx.max())/2)*sc;vv[:,1]=21.5+(yy.max()-yy)*sc;vv[:,2]=-13.45+vv[:,2]
mesh('Exterior_EnglishRaisedLetters',FRAME,vv,en['faces'])

# Roof fields in photographs are muted grey; structural ribs remain warm white.
ROOF_SHEET=material('Grey roof sheet between white ribs',[1,1,1],.22,.83)
rng=np.random.default_rng(61);gy,gx=np.mgrid[:512,:512]
variation=3*np.sin(gx/54)+2*np.cos(gy/91)+rng.normal(0,1.7,(512,512))
arr=np.clip(np.array([142,145,134])[None,None,:]+variation[:,:,None],0,255).astype('uint8')
arr[:,::32]=[121,126,118]
Image.fromarray(arr).save(ROOT/'roof-sheet.png');texture_images.append(ROOT/'roof-sheet.png')
materials[ROOF_SHEET]['pbrMetallicRoughness']['baseColorTexture']={'index':len(texture_images)}
for key in list(groups):
    if key[0]=='Roof_MainShell' and key[1]==CEILING:
        data=groups.pop(key);groups[('Roof_MainSheet',ROOF_SHEET)]=data
        for i,v in enumerate(data['v']):data['uv'][i]=v[:,[0,2]]/12
        # Preserve a separate light interior soffit, below the exterior sheet.
        for v,f,uv in zip(data['v'],data['f'],data['uv']):
            offset=int(f.min());mesh('Roof_MainSoffit',CEILING,v-[0,.12,0],f-offset,uv)

# Keep structural columns below their own stepped roof bay.
for (name,mat),data in groups.items():
    if name!='Structure_Columns':continue
    for v in data['v']:
        z=float((v[:,2].min()+v[:,2].max())/2);side=-1 if z<RIDGE_Z else 1
        distance=abs(z-RIDGE_Z)*54/(26 if side<0 else 58)
        h=36.8-distance*4.3/8 if distance<8 else (27.8-(distance-8)*4.3/18 if distance<26 else 19.5-(distance-26)*2.1/28)
        v[:,1]=np.minimum(v[:,1],h-.22)

# Horizontal cladding joints bracket the portholes, visible in manufacturer photos.
for side in [-1,1]:
    spans=[(-384,383)] if side<0 else [(-384,X0),(X1,383)]
    for a,b in spans:
        for y in [12.7,16.9]:beam('Exterior_ConcourseHorizontalSeams',DARK,(a,y,side*12.52),(b,y,side*12.52),.018,.024)
    for x in np.arange(-375,380,18):
        if side>0 and X0<x<X1:continue
        box('Exterior_ConcourseFloodlights',DARK,(x,18.34,side*11.1),(.40,.32,.35))
        box('Exterior_ConcourseFloodlights',LIGHT,(x,18.35,side*11.3),(.30,.20,.025))
