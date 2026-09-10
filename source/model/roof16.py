"""One stepped weather roof with a thin matching underside and internal haunches.
Tier levels and member sizes are photo estimates, not surveyed dimensions.
"""
roof17_tiers={}
# Equal horizontal runs, independently photo-traced elevations.
# Approximate cornice elevations in reference-end-inspect.png, top to bottom.
# Normalize the image differences to the existing overall height range;
# these are proportions from an oblique photo, not measured dimensions.
# Shared elevations on both sides. Larger near-ridge drops and progressively
# smaller outer drops produce the more pronounced curved silhouette requested.
photo_heights=np.array([32.5,25.8,21.8,19.2,17.5,16.5],float)
for side,width,distances in [(1,58,[0,5.5,16,26.5,37,47.5,58]),(-1,26,[0,5,15.5,26])]:
    roof17_tiers[side]=[(a*54/width,b*54/width,float(photo_heights[i])) for i,(a,b) in enumerate(zip(distances,distances[1:]))]
roof16_tiers=roof17_tiers
# Remove both previous roof surfaces and the seams on the old sloping surfaces.
for key in list(groups):
    if key[0] in {'Roof_MainSheet','Roof_MainSoffit','Roof_MainShell','Roof_Ventilators','Roof_Clerestory','Roof_ClerestoryBands','Roof_MassiveRibs'}:
        del groups[key]
roof16_panels=[]
for side in [-1,1]:
    for d0,d1,h in roof17_tiers[side]:
        za,zb=sorted([roof_z(d0,side),roof_z(d1,side)])
        for xx in np.arange(X0,X1,3):
            xb=min(xx+3,X1)
            top=np.array([(xx,h,za),(xb,h,za),(xb,h,zb),(xx,h,zb)])
            mesh('Roof_MainSheet',ROOF_SHEET,top,[(0,2,1),(0,3,2)],top[:,[0,2]]/12)
            bottom=top-[0,.22,0]
            mesh('Roof_MainSoffit',CEILING,bottom,[(0,1,2),(0,2,3)],bottom[:,[0,2]]/12)
            roof16_panels.append(dict(top=h,bottom=h-.22,x=[float(xx),float(xb)],z=[za,zb]))
            beam('Roof_TerraceStandingSeams',FRAME,(xx,h+.018,za),(xx,h+.018,zb),.025,.025)
        for zz in [za,zb]:box('Roof_TerraceEdgeClosure',WHITE,(C,h-.11,zz),(X1-X0,.22,.16))
        for xx in [X0,X1]:box('Roof_TerraceEndClosure',WHITE,(xx,h-.11,(za+zb)/2),(.16,.22,zb-za))
        # Straight top chord, vertical end and straight diagonal form a triangle.
        for xx in np.arange(X0+6,X1,12):
            z_inner=roof_z(d0,side);z_outer=roof_z(d1,side)
            a=(xx,h-.46,z_inner);b=(xx,h-.46,z_outer)
            c=(xx,h-2.95,z_outer)
            for start,end in [(a,b),(b,c),(c,a)]:beam('Roof_InternalTriangleSupports',WHITE,start,end,.46,.44)
    # Every riser belongs to the same stepped roof section.
    tiers=roof17_tiers[side]
    for upper,lower in zip(tiers,tiers[1:]):
        zz=roof_z(upper[1],side);lo=lower[2];hi=upper[2]
        for xx in np.arange(X0+1.5,X1,3):
            wallhole('Roof_Clerestory',WHITE,xx,(lo+hi)/2,zz,3,hi-lo,1.85,max(.6,hi-lo-.7))
        for yy in [lo,hi]:box('Roof_ClerestoryBands',WHITE,(C,yy,zz),(X1-X0,.24,.3))
    if side==1:
        for xx in np.arange(X0+1.5,X1,3):wallhole('Roof_Clerestory',WHITE,xx,(12.8+16.5)/2,96,3,3.7,1.85,3.0)
    for xx in np.arange(X0+3,X1,6):
        zz=roof_z(5,side)
        rod('Roof_Ventilators',DARK,(xx,32.5,zz),(xx,32.95,zz),.42,12)
        rod('Roof_Ventilators',WHITE,(xx,32.95,zz),(xx,33.1,zz),.75,18)
# Ridge posts now start at the actual upper terrace, not at the old phantom roof.
for key in list(groups):
    if key[0]=='Roof_Ridge':del groups[key]
for xx in np.arange(X0,X1+.1,12):beam('Roof_Ridge',WHITE,(xx,32.5,RIDGE_Z),(xx,40,RIDGE_Z),.65,.7)
(ROOT/'roof16-register.json').write_text(json.dumps(dict(panels=roof16_panels,thickness_m=.22,tiers=roof16_tiers,internal_beams='three straight members forming triangular supports',references=['revision2/references/exterior-airside.jpg','revision2/references/exterior-day.jpg','revision2/references/checkin-detail-2017.jpg','revision2/references/walk-2024-20241208071835.jpg'],dimensions='photo estimates'),indent=2),encoding='utf-8')

exec(compile((ROOT/'curve17.py').read_text(encoding='utf-8'),str(ROOT/'curve17.py'),'exec'))
