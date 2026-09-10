from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'build_revision.py';s=p.read_text(encoding='utf-8').replace('return y+(FG-F2)*d/54 if side<0 else y','return y')
s=s.replace('revision 5, traced circulation study','revision 6, security partitions and exterior fixes')
p.write_text(s,encoding='utf-8')
p=R/'interior_detail.py';s=p.read_text(encoding='utf-8').replace('(x,F3-.05,62.13)','(x,F3-1.12,62.13)')
s=s.replace('assert len(text_items)<=256',"exec(compile((ROOT/'fixes.py').read_text(encoding='utf-8'),str(ROOT/'fixes.py'),'exec'))\nassert len(text_items)<=256")
p.write_text(s,encoding='utf-8')
p=R/'circulation_detail.py';s=p.read_text(encoding='utf-8')
# Transform every primitive belonging to the specified stair, including railing
# and its label, then rotate its opening and recorded lower landing consistently.
needle="    record(id,'arrival escalator' if arrival else 'floor connection',b,landing_pixel=p,lower_landing=a.tolist(),pairing='upper landing source-traced; run and lower endpoint estimated')"
replacement="""    if id in ['L3-E03','L3-E06']:
        direction=-1 if id=='L3-E03' else 1
        for (name,mat),data in groups.items():
            if name!=g:continue
            for vertices in data['v']:
                ox=vertices[:,0].copy()-x;oz=vertices[:,2].copy()-z
                vertices[:,0]=x+direction*oz;vertices[:,2]=z-direction*ox
        holes[-1]=(min(x+direction*.4,x+direction*(run+.5)),max(x+direction*.4,x+direction*(run+.5)),z-width/2-.25,z+width/2+.25)
        a=np.array([x+direction*run,base,z])
    record(id,'arrival escalator' if arrival else 'floor connection',b,landing_pixel=p,lower_landing=a.tolist(),pairing='upper landing source-traced; run and lower endpoint estimated')"""
assert needle in s;s=s.replace(needle,replacement);p.write_text(s,encoding='utf-8')
p=R/'index.html';s=p.read_text(encoding='utf-8').replace('修订版 5','修订版 6').replace('扶梯分流 / 独立边检 / 转向安检','安检隔断 / 东西向扶梯 / 厦门立体字 / 侧立面')
s=s.replace('<button data-view="upperplan">','<button data-view="end">侧立面</button><button data-view="letters">厦门立牌</button><button data-view="isolation">安检隔断</button><button data-view="stairs">东西向扶梯</button><button data-view="upperplan">')
s=s.replace('const views={','const views={end:[[-230,54,53],[-90,23,53]],letters:[[22,26,-85],[22,22,-12]],isolation:[[-20,14,51],[-20,14,37]],stairs:[[-86,26,55],[-68,10,32]],')
s=s.replace("['cutaway','levels','checkinplan','upperplan']","['cutaway','levels','checkinplan','upperplan','stairs']")
s=s.replace('href="./audit.html"','href="./CHANGES.md"').replace('逐项核对原图与设施编号','本轮修改与验证')
p.write_text(s,encoding='utf-8')
