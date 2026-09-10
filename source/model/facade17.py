"""Use the same asymmetric roof outline for the end wall, fins and cornices."""
obsolete={'Facade_EndGlazing','Facade_EndTransoms','Facade_EndSteppedHeaders','Facade_SteppedLouvers','Facade_SteppedCornice','Facade_SteppedFasciaReturns','Facade_CorniceShadowReveals','Facade_CorniceEndCaps','Facade_PhotoFineMullions','Facade_PhotoPrimaryPiers','Roof_MainConcourseFlashing'}
for key in list(groups):
    if key[0] in obsolete:del groups[key]
for ex in [X0,X1]:
    face=ex+(-.48 if ex==X0 else .48)
    edges={}
    for side in [-1,1]:
        for a,b,h in roof17_tiers[side]:
            za,zb=sorted([roof_z(a,side),roof_z(b,side)])
            box('Facade_EndGlazing',END_GLASS,(ex,(F2+h)/2,(za+zb)/2),(.15,h-F2,zb-za))
            box('Facade_SteppedCornice',WHITE,(face,h,(za+zb)/2),(.95,.42,zb-za+.3))
            for yy in np.arange(F2+.35,h-.3,.43):beam('Facade_SteppedLouvers',LOUVER,(face,yy,za),(face,yy,zb),.22,.10)
            for zz in np.arange(za+.9,zb,.95):box('Facade_PhotoFineMullions',WHITE,(face,(F2+h)/2,zz),(.14,h-F2,.065))
            for zz in [za,zb]:edges[zz]=max(h,edges.get(zz,0))
    for zz,h in edges.items():
        if abs(zz-RIDGE_Z)>.01:box('Facade_PhotoPrimaryPiers',WHITE,(face,(F2+h)/2,zz),(.55,h-F2,.38))
# Close the roof strip above the hall/concourse interface without blocking passage.
edge_height=roof17_tiers[-1][-1][2]
box('Roof_AirsideInterfaceFascia',WHITE,(C,(18.0+edge_height)/2,12),(252,edge_height-18.0,.18))
stair_z=west['position'][2]
subtract_box({'Facade_EndGlazing','Facade_SteppedCornice','Facade_SteppedLouvers','Facade_PhotoFineMullions','Facade_PhotoPrimaryPiers'},np.array([X0-2,F3-.02,stair_z-2]),np.array([X0+2,F3+3.1,stair_z+2]))
(ROOT/'facade17-register.json').write_text(json.dumps(dict(terraces=roof17_tiers,landside_drops=5,airside_drops=2,source='user supplied side elevation photograph; count visible returns, exclude canopy and corridor',dimensions='estimated'),indent=2),encoding='utf-8')
