"""Photo-counted asymmetric terrace envelope and continuous airside landing."""
for key in list(groups):
    if key[0] in {'Roof_ContinuousCurvedRibs','Roof_RibEdge','Roof_CurvedFramePurlins'}:del groups[key]
curve17_report=[]
for side in [-1,1]:
    width=26 if side<0 else 58
    knots=[(0,40.3)]+[(b*width/54,h+.85) for a,b,h in roof17_tiers[side]]
    if side<0:knots += [(31.5,18.67),(32.5,18.67)]
    # One cubic Bezier elevation profile: no tangent resets at tier corners.
    # End meets the corridor obliquely, as photographed; no hooked flat tail.
    if side<0:knots=knots[:-2]+[(32.5,18.67)]
    length=knots[-1][0];top=knots[0][1];end=knots[-1][1]
    q=np.array(knots[1:-1]);t=q[:,0]/length
    basis=np.column_stack([3*(1-t)**2*t,3*(1-t)*t*t])
    rhs=q[:,1]-(1-t)**3*top-t**3*end
    c1,c2=np.linalg.lstsq(basis,rhs,rcond=None)[0]
    def elevation(t,top=top,end=end,c1=c1,c2=c2):return (1-t)**3*top+3*(1-t)**2*t*c1+3*(1-t)*t*t*c2+t**3*end
    # Smooth quadratic lift avoids roof corners without piecewise bends.
    lift=max(0.,float(np.max((q[:,1]-elevation(t))/(4*t*(1-t)))))
    ts=np.linspace(0,1,193)
    sampled=np.column_stack([length*ts,elevation(ts)+4*lift*ts*(1-ts)])
    if side<0:
        part=sampled[sampled[:,0]>=26-1e-6]
        # Separate solid feet only beneath each rib, with open bays between them.
        for cx in np.arange(X0,X1+.1,12):
            solid=[]
            for distance,height in part:
                zz=RIDGE_Z-distance;top_y=max(18.03,height-.45)
                solid.extend([(cx-.5,18.0,zz),(cx+.5,18.0,zz),(cx+.5,top_y,zz),(cx-.5,top_y,zz)])
            faces=[]
            for j in range(len(part)-1):
                for k in range(4):
                    a=4*j+k;b=4*j+(k+1)%4;faces.extend([(a,b,b+4),(a,b+4,a+4)])
            last=4*(len(part)-1)
            faces.extend([(0,2,1),(0,3,2),(last,last+1,last+2),(last,last+2,last+3)])
            mesh('Roof_IndividualEaveFeet',WHITE,solid,faces)
    dy=np.gradient(sampled[:,1],sampled[:,0])
    for x in np.arange(X0,X1+.1,12):
        vv=[]
        for (s,h),m in zip(sampled,dy):
            normal=np.array([1.,-side*m]);normal/=np.linalg.norm(normal)
            for dx,off in [(-.5,-.65),(.5,-.65),(.5,.65),(-.5,.65)]:vv.append((x+dx,h+off*normal[0],RIDGE_Z+side*s+off*normal[1]))
        ff=[]
        for i in range(len(sampled)-1):
            for k in range(4):
                a=4*i+k;b=4*i+(k+1)%4;ff.extend([(a,b,b+4),(a,b+4,a+4)])
        end=4*(len(sampled)-1);ff.extend([(0,2,1),(0,3,2),(end,end+1,end+2),(end,end+2,end+3)])
        mesh('Roof_ContinuousCurvedRibs',WHITE,vv,ff)
        if side<0:box('Roof_CurveConcourseBearing',WHITE,(x,18.025,6.0),(1.05,.05,1.0))
    for distance,_ in knots[1:-1]:
        height=float(elevation(distance/length)+4*lift*(distance/length)*(1-distance/length))
        beam('Roof_CurvedFramePurlins',WHITE,(X0,height,RIDGE_Z+side*distance),(X1,height,RIDGE_Z+side*distance),.22,.24)
    curve17_report.append(dict(side=side,knots=knots,tip_z=RIDGE_Z+side*knots[-1][0],tip_bottom=knots[-1][1]-.65))
(ROOT/'curve17-register.json').write_text(json.dumps(curve17_report,indent=2),encoding='utf-8')
