from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'circulation_detail.py';s=p.read_text(encoding='utf-8').replace("F3,X0,X1,12,96,holes)","F3,X0,X1,12,68,holes)");p.write_text(s,encoding='utf-8')
p=R/'international_flow.py';s=p.read_text(encoding='utf-8')
s=s.replace('((78,34),(101,34)),((101,34),(101,40)),((101,40),(82,40)),((78,34),(78,64)),((82,40),(82,64))','((84,34),(101,34)),((101,34),(101,40)),((101,40),(90,40)),((84,34),(84,64)),((90,40),(90,64))')
s=s.replace('(80,F3+2.6,63.8)','(87,F3+2.6,63.8)').replace('(78,82,','(84,90,').replace('if a<82 and b>78','if a<90 and b>84')
s=s.replace('[[88.2879,36.5349],[80,36.5349],[80,65],[106,65]]','[[88.2879,36.5349],[86.5,36.5349],[86.5,65],[105.2,65]]').replace('[[106,65],[105.2,60],[105.2,56],[123,56],[125.2,48]]','[[105.2,65],[105.2,60],[105.2,54],[125.2,54],[125.2,48]]')
# Remove booths enclosed inside the public approach instead of letting them obstruct it.
s=s.replace("gaps=[", "for r in booths:\n    if 83<r['position'][0]<91:\n        for key in list(groups):\n            if key[0]=='Interior_Circulation_IMM-I-'+r['id'].split('-')[-1].zfill(2):del groups[key]\ngaps=[")
p.write_text(s,encoding='utf-8')
p=R/'interior_detail.py';s=p.read_text(encoding='utf-8');anchor="exec(compile((ROOT/'west_stair_fix.py').read_text(encoding='utf-8'),str(ROOT/'west_stair_fix.py'),'exec'))";s=s.replace(anchor,anchor+"\nexec(compile((ROOT/'envelope11.py').read_text(encoding='utf-8'),str(ROOT/'envelope11.py'),'exec'))");p.write_text(s,encoding='utf-8')
for name in ['index.html','render10.cjs','review.html']:
 p=R/name;s=p.read_text(encoding='utf-8').replace('revision10','revision11').replace('修订版 10','修订版 11').replace('修订版10','修订版11');p.write_text(s,encoding='utf-8')
