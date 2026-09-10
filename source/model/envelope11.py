"""User photo corrections: void over check-in, lower envelope, gate apertures."""
for key in list(groups):
    if key[0] in {'Roof_CheckInCeiling','Roof_CheckInDownlights','Roof_CheckInAirGrilles'}:del groups[key]
# Lights now attach to the actual roof soffit instead of the deleted low ceiling.
for lx in np.arange(X0+6,X1,12):
    for lz in [74,86]:
        ly=soffit_height(lx,lz)
        rod('Roof_CheckInHighLightSupports',FRAME,(lx,ly,lz),(lx,ly-.6,lz),.025,6)
        disc('Roof_CheckInHighLights',LIGHT,(lx,ly-.62,lz),.20,normal=(0,-1,0),n=12)
# July 2025 D7/D8 photograph confirms a local suspended ceiling, not a 3F slab.
box('Roof_InternationalDIslandSuspendedCeiling',CEILING,(42,10.95,76),(11,.08,18))
for xx in [37,47]:
    for zz in [68,84]:
        rod('Roof_InternationalDIslandCeilingHangers',FRAME,(xx,11,zz),(xx,soffit_height(xx,zz),zz),.025,6)
for zz in [70,75,80]:disc('Roof_InternationalDIslandCeilingLights',LIGHT,(42,10.89,zz),.15,normal=(0,-1,0),n=12)
# The guide's grey forecourt is not an upper slab. Trim its attached partition too.
subtract_box({'Interior_ZoneSeparation'},np.array([X0-1,F3-.1,68]),np.array([X1+1,30,100]))
rail('Interior_CheckInVoidEdge',(X0,F3,67.85),(X1,F3,67.85))
beam('Interior_CheckInVoidEdgeGlass',ARR_GLASS,(X0,F3+.55,67.85),(X1,F3+.55,67.85),.055,.95)

# The apron-facing wall of the baggage hall was absent, in addition to the ends.
box('Facade_ArrivalApronWall',WHITE,(C,3.3,12),(252,6,.3))
for x in np.arange(X0+3,X1,6):
    box('Facade_ArrivalApronPilasters',STONE,(x,3.3,11.78),(.5,6,.22))

# Open four existing gate positions. Desks sit beside, never inside the aperture.
gate_doors=[]
for key,data in groups.items():
    if key[0]=='Unverified_West2024GateSigns':
        for v in data['v']:v[:,1]+=.85
for j,(gx,gz) in enumerate([(wx-30,wz-13),(wx+30,wz-13),(wx-30,wz+13),(wx+30,wz+13)]):
    gate_doors.append(dict(number=[22,23,25,26][j],x=gx,z=gz,width=2.6,bottom=.28,top=3.08))
    subtract_box({'Unverified_West2024Glazing'},np.array([gx-1.3,.27,gz-.5]),np.array([gx+1.3,3.08,gz+.5]))
    for key,data in groups.items():
        if key[0]!='Unverified_West2024GateDesks':continue
        for v in data['v']:
            if abs(v[:,0].mean()-gx)<.1 and abs(v[:,2].mean()-gz)<.5:v[:,0]+=2.8
    for dx in [-1.35,1.35]:box('Unverified_West2024DoorFrames',FRAME,(gx+dx,1.68,gz),(.1,2.8,.16))
    box('Unverified_West2024DoorFrames',FRAME,(gx,3.14,gz),(2.8,.12,.16))
    box('Unverified_West2024GateThresholds',FLOOR,(gx,.18,gz),(2.6,.2,1.4))
    for dx in [-2.05,2.05]:box('Unverified_West2024OpenGateLeaves',GLASS,(gx+dx,1.65,gz+.19),(1.3,2.7,.06))

# Photo: narrow cream horizontal blades and projecting stepped cornices.
# Recessed glazing remains the weather envelope; blade dimensions are estimates.
LOUVER=material('Warm ivory exterior louvers',[.82,.79,.65],.13,.57)
for ex in [X0,X1]:
    face=ex+(-.48 if ex==X0 else .48)
    for side in [-1,1]:
        for d0,d1,h in [(0,8,32.5),(8,26,23.5),(26,54,17.4)]:
            za,zb=sorted([roof_z(d0,side),roof_z(d1,side)])
            for yy in np.arange(6.65,h-.3,.43):
                beam('Facade_SteppedLouvers',LOUVER,(face,yy,za),(face,yy,zb),.22,.10)
            box('Facade_SteppedCornice',WHITE,(face,h,(za+zb)/2),(.95,.58,zb-za+.55))
            for zz in np.arange(za,zb+.01,2.8):box('Facade_SteppedMullions',WHITE,(face-.04,(F2+h)/2,zz),(.27,h-F2,.17))
# Keep the actual west access aperture open through the newly added facade detail.
stair_z=west['position'][2]
subtract_box({'Facade_SteppedLouvers','Facade_SteppedMullions','Facade_SteppedCornice'},np.array([X0-1,F3-.02,stair_z-2]),np.array([X0+1,F3+3.1,stair_z+2]))
(ROOT/'revision11-register.json').write_text(json.dumps(dict(west_gate_doors=gate_doors,checkin_void={'z_min':68,'z_max':96,'upper_floor_removed':True},arrival_apron_wall={'z':12,'bottom':.3,'top':6.3},facade='Photo-based louver rhythm and stepped projecting cornices; dimensions estimated'),ensure_ascii=False,indent=2),encoding='utf-8')
