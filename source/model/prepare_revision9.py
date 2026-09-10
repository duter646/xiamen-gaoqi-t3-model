from pathlib import Path
R=Path(__file__).resolve().parent
for p in [R/'index.html',R/'render_check.cjs',R/'check_review.cjs']:
    s=p.read_text(encoding='utf-8').replace('revision8','revision9').replace('修订版 8','修订版 9');p.write_text(s,encoding='utf-8')
p=R/'build_revision.py';s=p.read_text(encoding='utf-8')
s=s.replace("        for x in np.arange(X0+1.5,X1,3):wallhole('Roof_Clerestory',WHITE,x,(lo+hi)/2,z,3,hi-lo,ww,hh)\n        for y in [lo,hi]:box('Roof_ClerestoryBands',WHITE,(C,y,z),(252,.5,.5))",'''        # Interior connection openings remain visible with the roof enabled.
        openings=[(-48.5,-38),(-29.5,-20.5),(26,35),(105.5,114.5),(129.5,138.5)] if side==-1 and dist==54 else []
        for x in np.arange(X0+1.5,X1,3):
            if any(a<x+1.5 and b>x-1.5 for a,b in openings):
                box('Facade_ConcourseConnectionHeaders',WHITE,(x,(F3+3.1+hi)/2,z),(3,hi-F3-3.1,.22))
            else:wallhole('Roof_Clerestory',WHITE,x,(lo+hi)/2,z,3,hi-lo,ww,hh)
        for y in [lo,hi]:
            if y==lo and openings:
                # Snap band gaps to the same complete facade modules.
                modules=[x for x in np.arange(X0+1.5,X1,3) if not any(a<x+1.5 and b>x-1.5 for a,b in openings)]
                for x in modules:box('Roof_ClerestoryBands',WHITE,(x,y,z),(3,.5,.5))
            else:box('Roof_ClerestoryBands',WHITE,(C,y,z),(252,.5,.5))''')
p.write_text(s,encoding='utf-8')
p=R/'circulation_detail.py';s=p.read_text(encoding='utf-8')
s=s.replace("stair(id,p,arrival=True)","stair(id,p,run=22,base=.3,arrival=True)")
s=s.replace("],arrival=True)\nrecords[-1]['pairing']", "],run=22,base=.3,arrival=True)\nrecords[-1]['pairing']")
a=s.index('# Arrival-only east-west descents');b=s.index('# Atrium openings',a)
s=s[:a]+'''# Direct 3F-to-1F arrival escalators: 2F contains a shaft opening, no transfer landing.
arrival_descents=[r for r in records if r['kind']=='arrival escalator']
for r in arrival_descents:
    x,top,z=r['position'];end=r['lower_landing'][0]
    lower_holes.append((x+.2,end+.5,z-1.7,z+1.7))

'''+s[b:]
p.write_text(s,encoding='utf-8')
p=R/'check_arrivals.py';s=p.read_text(encoding='utf-8').replace("stairs=inv['stairs']+[r for r in reg['facilities'] if r['kind']=='arrival escalator']","stairs=inv['stairs']")
s=s.replace("assert abs(upper[2]-lower[2])<.01 and abs(upper[0]-lower[0])>5","assert abs(upper[2]-lower[2])<.01 and abs(upper[0]-lower[0])>20\n    assert abs(lower[1]-.3)<.01 and abs(upper[1]-12.1)<.01")
p.write_text(s,encoding='utf-8')
p=R/'check_security_exits.py';s=p.read_text(encoding='utf-8').replace("('Interior_','Structure_','Facade_')","('Interior_','Structure_','Facade_','Roof_')");p.write_text(s,encoding='utf-8')
p=R/'check_revision.py';s=p.read_text(encoding='utf-8').replace("assert sum(f['kind']=='arrival descent' for f in reg['facilities'])==4","assert not any(f['kind']=='arrival descent' for f in reg['facilities'])").replace("'arrival_descents_to_1F':4","'direct_3F_to_1F_arrival_escalators':3")
p.write_text(s,encoding='utf-8')
