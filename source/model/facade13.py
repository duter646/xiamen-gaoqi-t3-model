"""Photograph-circled cornices, canopy ties and lettering proportions."""
# Remove the old diagonal face headers that crossed behind the stepped cornices.
for key in list(groups):
    if key[0]=='Facade_EndSteppedHeaders':del groups[key]
# End elevation is a stepped screen. Cut surplus gable glazing/fins above each tier.
face_groups={'Facade_EndGlazing','Facade_EndConcreteFins','Facade_EndVerticalMullions','Facade_EndTransoms'}
for ex in [X0,X1]:
    for side in [-1,1]:
        for d0,d1,h in [(0,8,32.5),(8,26,23.5),(26,54,17.4)]:
            za,zb=sorted([roof_z(d0,side),roof_z(d1,side)])
            subtract_box(face_groups,np.array([ex-1,h+.29,za]),np.array([ex+1,44,zb]))
            face=ex+(-.78 if ex==X0 else .78)
            # Boxed projecting fascia with a narrow shadow recess underneath.
            box('Facade_SteppedFasciaReturns',WHITE,(face,h,(za+zb)/2),(1.5,.62,zb-za+.5))
            box('Facade_CorniceShadowReveals',STONE,(face,h-.33,(za+zb)/2),(1.2,.055,zb-za))
            for zz in [za,zb]:box('Facade_CorniceEndCaps',WHITE,(face,h,zz),(1.5,.62,.20))

# Canopy panels were emitted once after the final bay, creating an unsupported wing.
subtract_box({'Roof_Canopy'},np.array([X1+.01,0,90]),np.array([X1+30,40,112]))
subtract_box({'Roof_Canopy'},np.array([X0-30,0,90]),np.array([X0-.01,40,112]))
for key in list(groups):
    if key[0]=='Roof_CanopyCables':del groups[key]
for cx in np.arange(X0,X1+.1,12):
    # Cable stays lie in the cross-section of each mast, as visible in the photo.
    for end in [(cx,13.12,106.8),(cx,17.55,96.0)]:
        rod('Roof_CanopyCables',FRAME,(cx,25.6,102),end,.035,8)
    rod('Roof_CanopyMastTips',WHITE,(cx,26,102),(cx,26.8,102),.09,8)
box('Roof_CanopyFrontFascia',WHITE,(C,12.75,107),(252,.60,.25))
for ex in [X0,X1]:box('Roof_CanopyEndFascia',WHITE,(ex,12.6,101.5),(.25,.60,11))
# Added facade detail must keep the established west escalator door clear.
stair_z=west['position'][2]
subtract_box({'Facade_SteppedFasciaReturns','Facade_CorniceShadowReveals','Facade_CorniceEndCaps'},np.array([X0-2,F3-.02,stair_z-2]),np.array([X0+2,F3+3.1,stair_z+2]))
subtract_box({'Facade_RecessedEndEnclosure'},np.array([X0-2,F3-.02,stair_z-2]),np.array([X0+2,F3+3.1,stair_z+2]))
letter_bounds={}
for (name,mat),data in groups.items():
    if name not in ['Exterior_XiamenRaisedLetters','Exterior_EnglishRaisedLetters']:continue
    vv=np.concatenate(data['v']);letter_bounds[name]=dict(min=vv.min(0).tolist(),max=vv.max(0).tolist(),size=np.ptp(vv,axis=0).tolist())
(ROOT/'exterior13-register.json').write_text(json.dumps(dict(english='XIAMEN AIRPORT',chinese='厦门',letter_bounds=letter_bounds,canopy_x_range=[X0,X1],changes=['removed diagonal end-face headers','stepped boxed cornice ends','trimmed final canopy bay','cross-section canopy cable stays'],evidence='user supplied marked photograph; dimensions estimated'),ensure_ascii=False,indent=2),encoding='utf-8')
