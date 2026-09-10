"""Shop-backed domestic boundary and straight international void edge."""
# The obsolete glass return ran through the domestic stair and its landing.
subtract_box({'Interior_SecurityIsolation'},np.array([-56.18,F3-.01,11.8]),np.array([-45.30,F3+3.2,30.42]))
# Keep the controlled rear boundary; make the public face a recessed shopfront.
# The break follows the stair footprint, leaving both escalator landings clear.
for left,right in [(X0,-72.0)]:
    g='Interior_DomesticBoundaryShops'
    back,front=30.1,34.3
    for x in [left,right]:wall(g,(x,back),(x,front),F3,3,WHITE)
    mid=(left+right)/2
    for a,b in [(left,mid-1.25),(mid+1.25,right)]:
        wall(g,(a,front),(b,front),F3,.55,WOOD)
        wall(g,(a,front),(b,front),F3+.55,1.95,ARR_GLASS)
    wall(g,(left,front),(right,front),F3+2.5,.5,WOOD)
    box('Roof_DomesticBoundaryShops',CEILING,((left+right)/2,F3+3.02,(back+front)/2),(right-left,.12,front-back))
    label(g,'商店','SHOP',(mid,F3+2.75,front+.11),3,.42)
    for x in np.arange(left+1.5,right-1,4):
        box(g,WOOD,(x,F3+.9,back+.55),(2.4,1.8,.7))
        for y in [.4,.95,1.5]:box(g,WHITE,(x,F3+y,back+1),(2.35,.06,.35))
# The marked shop is triangular: its diagonal is the controlled boundary,
# not an independent partition passing through a rectangular storefront.
shop_lane=next(r['position'] for r in records if r['id']=='SEC-D-01')
tip=np.array([-56.0,30.1]);corner=np.array([float(shop_lane[0]-2.2),30.1]);end=np.array([corner[0],float(shop_lane[2])])
subtract_box({'Interior_SecurityIsolation'},np.array([-56.2,F3-.01,29.95]),np.array([corner[0]+.10,F3+3.2,end[1]+.15]))
g='Interior_TriangularBoundaryShop'
shop_mid=(tip+end)/2
shop_tangent=(end-tip)/np.linalg.norm(end-tip)
shop_door_a=shop_mid-shop_tangent
shop_door_b=shop_mid+shop_tangent
for a,b in [(tip,shop_door_a),(shop_door_b,end)]:
    wall(g,a,b,F3,.5,WOOD)
    wall(g,a,b,F3+.5,2,ARR_GLASS)
wall(g,tip,end,F3+2.5,.5,WOOD)
# Existing continuous rear wall supplies the third side at z=30.1.
wall(g,corner,end,F3,3,WHITE)
poly=[tip,corner,end]
mesh('Roof_TriangularBoundaryShop',CEILING,[(x,F3+3,z) for x,z in poly]+[(x,F3+3.12,z) for x,z in poly],[(0,2,1),(3,4,5),(0,1,4),(0,4,3),(1,2,5),(1,5,4),(2,0,3),(2,3,5)])
shop_normal=np.array([-shop_tangent[1],shop_tangent[0]])
label(g+'_Sign','商店','SHOP',(0,F3+2.75,0),3,.42)
for (shop_name,shop_mat),shop_data in groups.items():
    if shop_name==g+'_Sign':
        for shop_vertices in shop_data['v']:
            local=shop_vertices[:,[0,2]].copy()
            shop_vertices[:,[0,2]]=shop_mid+shop_normal*.14+local[:,0,None]*shop_tangent+local[:,1,None]*shop_normal
(ROOT/'triangular-shop.json').write_text(json.dumps(dict(outline_xz=[p.tolist() for p in poly],boundary='east and rear sides closed toward screened area',entrance='unscreened diagonal side, 2m clear',door_xz=[shop_door_a.tolist(),shop_door_b.tolist()]),indent=2),encoding='utf-8')
# The old notch produced a dogleg guard. Fill only its extra 3.5 m recess;
# the principal opening and both international escalators remain unchanged.
box('Structure_InternationalVoidEdgeInfill',FLOOR,(81,F3-.2,31.25),(12,.4,3.5))
subtract_box({'Interior_SupportedOpeningGuards','Interior_SupportedOpeningGlass'},np.array([74.7,F3-.01,29.51]),np.array([87.3,F3+1.3,33.35]))
rail('Interior_InternationalStraightVoidGuard',(75,F3,29.6),(87,F3,29.6))
beam('Interior_InternationalStraightVoidGlass',ARR_GLASS,(75,F3+.55,29.6),(87,F3+.55,29.6),.045,.88)



