from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'interior_detail.py';s=p.read_text(encoding='utf-8');anchor="exec(compile((ROOT/'envelope11.py').read_text(encoding='utf-8'),str(ROOT/'envelope11.py'),'exec'))";s=s.replace(anchor,anchor+"\nexec(compile((ROOT/'sign_mounts.py').read_text(encoding='utf-8'),str(ROOT/'sign_mounts.py'),'exec'))");p.write_text(s,encoding='utf-8')
for name in ['index.html','render11.cjs','check_ui11.cjs','render10.cjs']:
 p=R/name;s=p.read_text(encoding='utf-8').replace('revision11','revision12').replace('修订版 11','修订版 12');p.write_text(s,encoding='utf-8')
