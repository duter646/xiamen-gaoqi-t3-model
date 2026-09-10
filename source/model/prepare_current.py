from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'interior_detail.py';s=p.read_text(encoding='utf-8').replace("('gate7-shop',-79,-1,10,4,'shop')","('gate7-shop',-90,-1,10,4,'shop')");s=s.replace('assert len(text_items)<=256',"exec(compile((ROOT/'repair_interior.py').read_text(encoding='utf-8'),str(ROOT/'repair_interior.py'),'exec'))\nassert len(text_items)<=256");p.write_text(s,encoding='utf-8')
p=R/'index.html';s=p.read_text(encoding='utf-8').replace('修订版 6','修订版 7').replace('安检隔断 / 东西向扶梯 / 厦门立体字 / 侧立面','室内结构检查 / 碰撞修复 / 实拍色彩');p.write_text(s,encoding='utf-8')
for name in ['render_check.cjs','check_review.cjs']:
    p=R/name;s=p.read_text(encoding='utf-8').replace('/revision6/','/revision7/');p.write_text(s,encoding='utf-8')
