from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'circulation_detail.py';s=p.read_text(encoding='utf-8').replace("direction=-1 if id=='L3-E03' else 1","direction=1")
p.write_text(s,encoding='utf-8')
p=R/'build_revision.py';s=p.read_text(encoding='utf-8').replace('RIDGE_Z=54.0','RIDGE_Z=38.0')
s=s.replace('return RIDGE_Z+side*d*42/54','return RIDGE_Z+side*d*(26 if side<0 else 58)/54')
s=s.replace('# Symmetric stepped terraces around the central ridge.', '# Stepped terraces: ridge shifted toward apron as in the supplied aerial view.')
p.write_text(s,encoding='utf-8')
p=R/'fixes.py';s=p.read_text(encoding='utf-8').replace('partition([75,34],[75,-12.5])','partition([75,34],[75,12.5])')
s=s.replace("lv[:,0]=C-((xx-(xx.min()+xx.max())/2)*scale)","""for mask,center in [(xx<1000,C+34.5),(xx>=1000,C-34.5)]:
    local=xx[mask];lv[mask,0]=center-(local-(local.min()+local.max())/2)*scale""")
s=s.replace('lv[:,1]=19.0+','lv[:,1]=27.0+')
a=s.index('for x in np.linspace(C-width/2');b=s.index('# End wall:',a)
s=s[:a]+"""for center in [C+34.5,C-34.5]:
    for x in [center-4.3,center+4.3]:
        for z in [-12.8,-10.3]:beam('Exterior_XiamenLetterFrame',FRAME,(x,18,z),(x,35,z),.12,.12)
        for y in np.arange(18,35,3):
            beam('Exterior_XiamenLetterFrame',FRAME,(x,y,-12.8),(x,y+3,-10.3),.07,.07)
    for y in [19,23,27,31,35]:
        beam('Exterior_XiamenLetterFrame',FRAME,(center-4.3,y,-12.8),(center+4.3,y,-12.8),.09,.09)
    for x in [center-4.3,center+4.3]:beam('Exterior_XiamenLetterFrame',FRAME,(x,18,-4),(x,33,-10.3),.10,.10)
for y in [20,23]:beam('Exterior_XiamenLetterFrame',FRAME,(C-43,y,-12.7),(C+43,y,-12.7),.1,.12)

"""+s[b:]
p.write_text(s,encoding='utf-8')
