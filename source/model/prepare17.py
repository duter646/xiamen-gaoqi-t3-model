from pathlib import Path
p=Path(__file__).parent
f=p/'roof16.py';s=f.read_text(encoding='utf-8')
s=s.replace('roof16_tiers=[(0,8,32.5),(8,26,23.5),(26,54,17.4)]',"roof17_tiers={1:[(0,8,32.5),(8,16,27.8),(16,24,23.5),(24,32,20.3),(32,40,18.1),(40,54,16.6)],-1:[(0,8,32.5),(8,26,27.8),(26,54,23.5)]}\nroof16_tiers=roof17_tiers")
s=s.replace("'Roof_Ventilators'}", "'Roof_Ventilators','Roof_Clerestory','Roof_ClerestoryBands','Roof_MassiveRibs'}")
s=s.replace('for d0,d1,h in roof16_tiers:', 'for d0,d1,h in roof17_tiers[side]:')
a=s.index('    # Solid riser');b=s.index('    for xx in np.arange(X0+3',a)
s=s[:a]+'''    # Every riser belongs to the same stepped roof section.
    tiers=roof17_tiers[side]
    for upper,lower in zip(tiers,tiers[1:]):
        zz=roof_z(upper[1],side);lo=lower[2];hi=upper[2]
        for xx in np.arange(X0+1.5,X1,3):
            wallhole('Roof_Clerestory',WHITE,xx,(lo+hi)/2,zz,3,hi-lo,1.85,max(.6,hi-lo-.7))
        for yy in [lo,hi]:box('Roof_ClerestoryBands',WHITE,(C,yy,zz),(X1-X0,.24,.3))
    if side==1:
        for xx in np.arange(X0+1.5,X1,3):wallhole('Roof_Clerestory',WHITE,xx,(12.8+16.6)/2,96,3,3.8,1.85,3.1)
''' +s[b:]
s += "\nexec(compile((ROOT/'curve17.py').read_text(encoding='utf-8'),str(ROOT/'curve17.py'),'exec'))\n"
f.write_text(s,encoding='utf-8')
f=p/'interior_detail.py';s=f.read_text(encoding='utf-8');s=s.replace('assert len(text_items)<=256',"exec(compile((ROOT/'facade17.py').read_text(encoding='utf-8'),str(ROOT/'facade17.py'),'exec'))\nassert len(text_items)<=256");f.write_text(s,encoding='utf-8')
for name in ['index.html','review.html','render13.cjs','render_roof16.cjs']:
 f=p/name;s=f.read_text(encoding='utf-8').replace('revision16/','revision17/').replace('修订版 16','修订版 17').replace('单层阶梯屋面 / 内部弧形支撑','非对称阶梯 / 弧梁连接通道屋顶');f.write_text(s,encoding='utf-8')
