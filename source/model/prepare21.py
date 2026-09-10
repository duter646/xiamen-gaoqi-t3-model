from pathlib import Path
p=Path(__file__).parent
f=p/'circulation_detail.py';s=f.read_text(encoding='utf-8')
s=s.replace("x,z=project(p);g='Interior_Circulation_'+id", "x,z=project(p)\n    if id=='L3-E04':x,z=-49.2,20.527083645069553\n    if id=='L3-E05':x,z=23.1,20.527083645069553\n    g='Interior_Circulation_'+id")
s=s.replace("holes.append((75,87,24,33))", """# User: west small bay is solid; the next void extends left to the up escalator.
holes=[h for h in holes if not (-84<h[0]<-83 and -68<h[1]<-67)]
holes=[(-66.00658386951966,h[1],h[2],h[3]) if -56<h[0]<-54 and -33<h[1]<-32 else h for h in holes]
holes.append((75,87,24,33))
# The marked long 2F strip is entirely open, including below 3F landing bridges.
lower_holes.append((-83.86532994164293,92.4925931467904,15.532320814005676,29.5))""")
f.write_text(s,encoding='utf-8')
f=p/'arrivals_detail.py';s=f.read_text(encoding='utf-8').replace("(X0,28),(X1,28),F2,F3-F2-.2", "(X0,29.65),(X1,29.65),F2,F3-F2-.2")
s=s.replace("wall('Interior_ArrivalGallerySeparation',(45,12.8),(45,28),F2,F3-F2-.2)","# No intermediate partition across the two-storey void.")
s=s.replace("for a,b in [(12,14.1),(17.9,76)]:", "arrival_z=20.527083645069553\nfor a,b in [(12,arrival_z-1.85),(arrival_z+1.85,76)]:")
s=s.replace("for a,b in [((30,14.1),(54,14.1)),((30,17.9),(54,17.9)),((30,14.1),(30,17.9))]:", "for a,b in [((22.4,arrival_z-1.85),(48,arrival_z-1.85)),((22.4,arrival_z+1.85),(48,arrival_z+1.85)),((22.4,arrival_z-1.85),(22.4,arrival_z+1.85))]:")
f.write_text(s,encoding='utf-8')
f=p/'interior_detail.py';s=f.read_text(encoding='utf-8').replace("exec(compile((ROOT/'sign_mounts.py')", "exec(compile((ROOT/'void21.py').read_text(encoding='utf-8'),str(ROOT/'void21.py'),'exec'))\nexec(compile((ROOT/'sign_mounts.py')");f.write_text(s,encoding='utf-8')
for name in ['index.html','review.html','render13.cjs','render_roof16.cjs']:
 f=p/name;s=f.read_text(encoding='utf-8').replace('revision20/','revision21/').replace('修订版 20','修订版 21').replace('两侧同高 / 加强弧度 / 实心檐口','挑空对齐 / 到达扶梯 / 安检隔离');f.write_text(s,encoding='utf-8')
