from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'interior_detail.py';s=p.read_text(encoding='utf-8')
anchor="exec(compile((ROOT/'exterior_detail.py').read_text(encoding='utf-8'),str(ROOT/'exterior_detail.py'),'exec'))"
s=s.replace(anchor,anchor+"\nexec(compile((ROOT/'ceiling14.py').read_text(encoding='utf-8'),str(ROOT/'ceiling14.py'),'exec'))")
anchor="exec(compile((ROOT/'facade13.py').read_text(encoding='utf-8'),str(ROOT/'facade13.py'),'exec'))"
s=s.replace(anchor,anchor+"\nexec(compile((ROOT/'finish_geometry14.py').read_text(encoding='utf-8'),str(ROOT/'finish_geometry14.py'),'exec'))")
s=s.replace("ROOT/'border12.py'","ROOT/'border14.py'");p.write_text(s,encoding='utf-8')
for name in ['index.html','render13.cjs','render11.cjs','check_ui11.cjs']:
 p=R/name;s=p.read_text(encoding='utf-8').replace('revision13','revision14').replace('修订版 13','修订版 14').replace('阶梯侧立面 / 雨棚收口 / 厦门机场标识','边检位置 / 平吊顶 / 实拍机场标识');p.write_text(s,encoding='utf-8')
p=R/'check_order12.py';s=p.read_text(encoding='utf-8').replace('border=[([111,33.6],[111,68])]','border=[([48.53,63],[111,63])]');p.write_text(s,encoding='utf-8')
