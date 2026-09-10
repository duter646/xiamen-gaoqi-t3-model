from pathlib import Path
p=Path(__file__).parent
f=p/'curve17.py';s=f.read_text(encoding='utf-8')
a=s.index('    xx=np.array');b=s.index('    dy=np.gradient',a)
s=s[:a]+'''    # One cubic Bezier elevation profile: no tangent resets at tier corners.
    # End meets the corridor obliquely, as photographed; no hooked flat tail.
    if side<0:knots=knots[:-2]+[(32.5,18.67)]
    length=knots[-1][0];top=knots[0][1];end=knots[-1][1]
    q=np.array(knots[1:-1]);t=q[:,0]/length
    basis=np.column_stack([3*(1-t)**2*t,3*(1-t)*t*t])
    rhs=q[:,1]-(1-t)**3*top-t**3*end
    c1,c2=np.linalg.lstsq(basis,rhs,rcond=None)[0]
    def elevation(t):return (1-t)**3*top+3*(1-t)**2*t*c1+3*(1-t)*t*t*c2+t**3*end
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
''' +s[b:]
# Purlins must follow the fitted curve, not the superseded interpolation knots.
s=s.replace("for distance,height in knots[1:-1]:beam", "for distance,_ in knots[1:-1]:\n        height=float(elevation(distance/length)+4*lift*(distance/length)*(1-distance/length))\n        beam")
f.write_text(s,encoding='utf-8')
f=p/'zone_separation.py';s=f.read_text(encoding='utf-8')
s=s.replace('boundary=[[75,-12.5],[75,15.8],[93.3,15.8],[93.3,30.3],[75,30.3],[75,48],[45,65],[45,96]]', '''boundary=[[75,-12.5],[75,9],[20.2,9],[20.2,16.4]]
arrival_boundary=[[23.25,16.4],[75,16.4],[75,15.8],[93.3,15.8],[93.3,30.3],[75,30.3],[75,48],[45,65],[45,96]]
for a,b in zip(arrival_boundary,arrival_boundary[1:]):partition(a,b,'Interior_ZoneSeparation',3.0)''')
f.write_text(s,encoding='utf-8')
for name in ['index.html','review.html','render13.cjs','render_roof16.cjs','render21.cjs']:
 f=p/name;s=f.read_text(encoding='utf-8').replace('revision21/','revision22/').replace('修订版 21','修订版 22').replace('挑空对齐 / 到达扶梯 / 安检隔离','挑空连通 / 到达隔离 / 独立梁脚');f.write_text(s,encoding='utf-8')
