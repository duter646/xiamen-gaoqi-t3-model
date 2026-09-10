from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'circulation_detail.py';s=p.read_text(encoding='utf-8')
s=s.replace("pp[:,1].min(),pp[:,1].max());holes.append(h)","pp[:,1].min(),min(pp[:,1].max(),29.5));holes.append(h)")
assert 'min(pp[:,1].max(),29.5)' in s
p.write_text(s,encoding='utf-8')
p=R/'interior_detail.py';s=p.read_text(encoding='utf-8').replace('assert len(text_items)<=256',"exec(compile((ROOT/'exit_routes.py').read_text(encoding='utf-8'),str(ROOT/'exit_routes.py'),'exec'))\nassert len(text_items)<=256");p.write_text(s,encoding='utf-8')
p=R/'index.html';s=p.read_text(encoding='utf-8').replace('修订版 7','修订版 8').replace('室内结构检查 / 碰撞修复 / 实拍色彩','安检出口 / 取包通道 / 候机廊连接').replace('显示图示动线（待校验）','显示安检出口检查路线');s=s.replace('const views={','const views={exit:[[3,33,53],[-5,12.1,30]],');s=s.replace('<button data-view="corridor">','<button data-view="exit">安检后通路</button><button data-view="corridor">');s=s.replace("'upperplan','stairs']","'upperplan','stairs','exit']");p.write_text(s,encoding='utf-8')
for name in ['render_check.cjs','check_review.cjs']:
    p=R/name;s=p.read_text(encoding='utf-8').replace('/revision7/','/revision8/');p.write_text(s,encoding='utf-8')
