"""Marked facade changes and unmodified user-supplied transparent sign artwork."""
for a,b in [((88.25,F2,34.75),(98.7,F2,34.75)),((88.25,F2,38.35),(98.7,F2,38.35)),((88.25,F2,34.75),(88.25,F2,38.35))]:
    rail('Interior_InternationalLowerVoidGuards',a,b)
for key in list(groups):
    if key[0] in {'Exterior_XiamenRaisedLetters','Exterior_EnglishRaisedLetters','Exterior_XiamenLetterFrame','Facade_EndConcreteFins','Facade_EndVerticalMullions','Facade_EndPierBases','Facade_SteppedMullions','Roof_CanopyEndFascia'}:del groups[key]
# Original alpha PNG embedded without raster editing or stretching.
texture_images.append(ROOT/'user-airport-sign.png')
PHOTO_SIGN=material('User supplied XIAMEN AIRPORT sign',[1,1,1],0,.7)
materials[PHOTO_SIGN]['pbrMetallicRoughness']['baseColorTexture']={'index':len(texture_images)}
materials[PHOTO_SIGN]['alphaMode']='MASK';materials[PHOTO_SIGN]['alphaCutoff']=.45
materials[PHOTO_SIGN]['extensions']={'KHR_materials_unlit':{}}
width=35.;height=width*759/2072;bottom=18.1
vv=[(C+width/2,bottom,-13.35),(C-width/2,bottom,-13.35),(C-width/2,bottom+height,-13.35),(C+width/2,bottom+height,-13.35)]
mesh('Exterior_UserAirportSign',PHOTO_SIGN,vv,[(0,1,2),(0,2,3)],[(0,1),(1,1),(1,0),(0,0)])
# Narrow back braces support the photographic frame on the existing concourse roof.
for sx in [C-14,C+14]:beam('Exterior_UserSignBackBraces',FRAME,(sx,18.03,-6),(sx,25,-13.3),.10,.10)
for ex in [X0,X1]:
    face=ex+(-.58 if ex==X0 else .58)
    edges={}
    for side in [-1,1]:
        for d0,d1,h in [(0,8,32.5),(8,26,23.5),(26,54,17.4)]:
            za,zb=sorted([roof_z(d0,side),roof_z(d1,side)])
            for zz in [za,zb]:
                if abs(zz-RIDGE_Z)>.01:edges[zz]=max(edges.get(zz,0),h)
            for zz in np.arange(za+.9,zb,.95):
                if abs(zz-RIDGE_Z)<.25:continue
                box('Facade_PhotoFineMullions',WHITE,(face,(F2+h)/2,zz),(.14,h-F2,.065))
    for zz,h in edges.items():box('Facade_PhotoPrimaryPiers',WHITE,(face,(F2+h)/2,zz),(.55,h-F2,.38))
# Inset the canopy by one existing 12 m structural bay at each end.
canopy_names={key[0] for key in groups if key[0].startswith('Roof_Canopy')}
for lo,hi in [(X0-3,X0+12),(X1-12,X1+3)]:
    subtract_box(canopy_names,np.array([lo-.001,0,95]),np.array([hi+.001,40,110]))
for ex in [X0+12,X1-12]:box('Roof_CanopyInsetEndCap',WHITE,(ex,12.6,101.5),(.22,.60,11))
# Weather flashing connects the main low eave to the boarding corridor roof.
mesh('Roof_MainConcourseFlashing',METAL,[(X0,17.43,12.15),(X1,17.43,12.15),(X1,18.015,10.9),(X0,18.015,10.9)],[(0,1,2),(0,2,3)])
stair_z=west['position'][2]
subtract_box({'Facade_PhotoFineMullions','Facade_PhotoPrimaryPiers'},np.array([X0-2,F3-.02,stair_z-2]),np.array([X0+2,F3+3.1,stair_z+2]))
(ROOT/'revision14-register.json').write_text(json.dumps(dict(sign='user-airport-sign.png unchanged, original aspect ratio and alpha',sign_width=width,sign_height=height,canopy_inset=12,roof_connection='flashing between main eave and concourse roof',facade='primary piers separated from fine mullions; prior overlapping fins removed'),ensure_ascii=False,indent=2),encoding='utf-8')
