from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'interior_detail.py';s=p.read_text(encoding='utf-8');s=s.replace('assert len(text_items)<=256',"exec(compile((ROOT/'exterior_detail.py').read_text(encoding='utf-8'),str(ROOT/'exterior_detail.py'),'exec'))\nassert len(text_items)<=256");p.write_text(s,encoding='utf-8')
p=R/'build_revision.py';s=p.read_text(encoding='utf-8').replace('4.5,4.2,2.95,2.95,False','4.5,4.2,3.4,3.4,False');p.write_text(s,encoding='utf-8')
p=R/'index.html';s=p.read_text(encoding='utf-8').replace('letters:[[22,26,-85],[22,22,-12]]','letters:[[22,31,-150],[22,27,-12]]');s=s.replace('<button data-view="upperplan">','<button data-view="corridor">长廊通行</button><button data-view="upperplan">');s=s.replace('const views={','const views={corridor:[[30,13.8,5.5],[110,13.8,5.5]],');p.write_text(s,encoding='utf-8')
