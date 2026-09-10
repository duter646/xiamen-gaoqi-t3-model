from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'circulation_detail.py';s=p.read_text(encoding='utf-8').replace("    if id=='SEC-I-05':z+=1.25", "    if id in ['SEC-D-07','SEC-D-09']:x-=1.0\n    if id=='SEC-I-05':z+=1.25");p.write_text(s,encoding='utf-8')
p=R/'fixes.py';s=p.read_text(encoding='utf-8').replace('for offset in [-1.3,3.9]:partition','for offset in ([-1.3,3.9] if rec is lanes[-1] else [-1.3]):partition').replace('for dist in [0,2.5,5]:','for dist in [0,5]:');p.write_text(s,encoding='utf-8')
p=R/'interior_detail.py';s=p.read_text(encoding='utf-8').replace('assert len(text_items)<=256',"exec(compile((ROOT/'zone_separation.py').read_text(encoding='utf-8'),str(ROOT/'zone_separation.py'),'exec'))\nassert len(text_items)<=256");p.write_text(s,encoding='utf-8')
