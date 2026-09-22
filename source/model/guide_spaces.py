"""Canonical guide-based shop shells; obsolete guessed shells are removed."""
from guide_registration import SHOP_TOPS,shop_model_outline,UPPER

for key in list(groups):
    name=key[0]
    if name.startswith(('Roof_TracedFacilityCeiling_','Interior_FacilityFootprintEdges')) or name in {'Interior_Circulation_'+id for id in SHOP_TOPS}:
        del groups[key]

shop_inventory=[]
for id in SHOP_TOPS:
    poly=shop_model_outline(id)
    # A door on the public face, never in the two controlled D-SH01 sides.
    front={'D-SH01':9,'D-SH02':3,'D-SH03':2,'D-CF01':0,'I-SH01':2}[id]
    name='Interior_Circulation_'+id
    doors=[]
    for index,a in enumerate(poly):
        b=poly[(index+1)%len(poly)]
        if index==front:
            tangent=(b-a)/np.linalg.norm(b-a);mid=(a+b)/2;half=min(.95,np.linalg.norm(b-a)/2-.25)
            left=mid-half*tangent;right=mid+half*tangent
            wall(name,a,left,F3,2.9);wall(name,right,b,F3,2.9)
            wall(name,left,right,F3+2.25,.65,WOOD)
            doors=[left.tolist(),right.tolist()]
        else:wall(name,a,b,F3,2.9)
    triangles=triangulate_polygon(poly)
    vertices=[(x,F3+2.9,z) for x,z in poly]+[(x,F3+3.02,z) for x,z in poly]
    count=len(poly);faces=[(c,b,a) for a,b,c in triangles]+[(a+count,b+count,c+count) for a,b,c in triangles]
    for a in range(count):
        b=(a+1)%count;faces.extend([(a,b,b+count),(a,b+count,a+count)])
    mesh('Roof_TracedFacilityCeiling_'+id,CEILING,vertices,faces)
    rec=next(r for r in records if r['id']==id);center=poly.mean(0)
    rec['position']=[float(center[0]),F3,float(center[1])];rec['footprint_estimated']=np.ptp(poly,axis=0).tolist()
    rec['outline_xz']=poly.tolist();rec['door_xz']=doors
    shop_inventory.append(dict(id=id,outline_xz=poly.tolist(),door_xz=doors,source_crop_pixels=SHOP_TOPS[id],base_offset_source_pixels=[0,6],height=2.9,roof_top=F3+3.02))

# The two upper shafts open onto the controlled arrival gallery at 2F. Their
# old isolated landing pads stopped short of that gallery by roughly ten metres.
for key in list(groups):
    if key[0] in {'Structure_LowerLiftLanding','Interior_LowerLiftLandingRails'}:del groups[key]
for rec in [r for r in records if r['kind']=='lift shaft' and r['upper_level']==F3]:
    x,base,z=rec['position'];near=z+1.5;far=12.3
    box('Structure_LowerLiftLanding',FLOOR,(x,F2-.2,(near+far)/2),(3.5,.4,far-near))
    for side in [-1,1]:wall('Interior_LowerLiftLobbyWalls',(x+side*1.75,near),(x+side*1.75,far),F2,3.0)
    box('Roof_LowerLiftLobbies',CEILING,(x,F2+3.08,(near+far)/2),(3.66,.16,far-near))
    rec['lower_lobby']={'start':[x,F2,near],'end':[x,F2,far],'controlled_gallery':True}
wall('Interior_ArrivalGallerySeparation',(20.2,12),(20.2,29.65),F2,F3-F2-.3,ARR_GLASS)


def finish_guide_connections():
    # Run after the original builder raises its concourse support ribs.
    for rec in [r for r in records if r['kind']=='lift shaft' and r['upper_level']==F3]:
        x,_,z=rec['position']
        subtract_box({'Structure_ConcourseBase'},np.array([x-1.55,F2-.01,z-1.7]),np.array([x+1.55,F3,12.4]))
        subtract_box({'Structure_Level2_AirsideBoundary'},np.array([x-1.5,F2-.01,12.0]),np.array([x+1.5,F2+2.8,13.0]))
        box('Structure_LiftGalleryThreshold',FLOOR,(x,F2-.06,12.5),(3.0,.12,1.0))
        for side in [-1,1]:
            box('Structure_LiftLobbySupportPosts',STONE,(x+side*1.75,(.3+F3-.4)/2,z+1.4),(.4,F3-.7,.4))
        box('Structure_LiftLobbySupportHeader',STONE,(x,F3-.3,z+1.4),(3.9,.6,.4))

(ROOT/'guide-spaces.json').write_text(json.dumps(dict(shops=shop_inventory,upper_openings=holes,lower_openings=lower_holes,
    limitations=['Guide blue top faces lowered by observed drawing side thickness (6 original pixels).','Long upper void edge limited to z=31.7 within diagram-edge uncertainty, retaining the post-security passage.','Door width, wall height and concealed faces estimated.']),ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'circulation-register.json').write_text(json.dumps(dict(facilities=records,floor_openings=holes),ensure_ascii=False,indent=2),encoding='utf-8')
old_inventory=json.loads((ROOT/'facility-footprint-audit.json').read_text(encoding='utf-8'))
updated=[]
for item in old_inventory:
    if item.get('id') not in SHOP_TOPS:updated.append(item)
for item in shop_inventory:
    updated.append(dict(id=item['id'],source='facility-reference.png; crop x910 y630, scale2',source_pixels=item['source_crop_pixels'],base_offset_source_pixels=[0,6],world_outline_xz=item['outline_xz'],door_xz=item['door_xz'],status='guide base outline, with documented column/boundary clearance; dimensions estimated'))
(ROOT/'facility-footprint-audit.json').write_text(json.dumps(updated,ensure_ascii=False,indent=2),encoding='utf-8')
