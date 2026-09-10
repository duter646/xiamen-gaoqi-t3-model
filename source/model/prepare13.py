from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'fixes.py';s=p.read_text(encoding='utf-8').replace('scale=7.0/','scale=5.2/').replace('C+34.5','C+15').replace('C-34.5','C-15').replace('27.0+(yy.max()-yy)*scale','25.0+(yy.max()-yy)*scale').replace('center-4.3','center-3.2').replace('center+4.3','center+3.2').replace('(x,35,z)','(x,30.8,z)').replace('np.arange(18,35,3)','np.arange(18,28,3)').replace('[19,23,27,31,35]','[19,23,27,30.8]').replace('(x,33,-10.3)','(x,29.5,-10.3)').replace('C-43','C-19').replace('C+43','C+19').replace('height_m=7','height_m=5.2');p.write_text(s,encoding='utf-8')
p=R/'exterior_detail.py';s=p.read_text(encoding='utf-8').replace('sc=2.35/','sc=2.2/').replace('vv[:,1]=22+','vv[:,1]=21.5+');p.write_text(s,encoding='utf-8')
p=R/'interior_detail.py';s=p.read_text(encoding='utf-8');anchor="exec(compile((ROOT/'sign_mounts.py').read_text(encoding='utf-8'),str(ROOT/'sign_mounts.py'),'exec'))";s=s.replace(anchor,anchor+"\nexec(compile((ROOT/'facade13.py').read_text(encoding='utf-8'),str(ROOT/'facade13.py'),'exec'))");p.write_text(s,encoding='utf-8')
for name in ['index.html','render11.cjs','check_ui11.cjs']:
 p=R/name;s=p.read_text(encoding='utf-8').replace('revision12','revision13').replace('修订版 12','修订版 13').replace('边检隔离边界 / 顺序检查 / 指示牌安装','阶梯侧立面 / 雨棚收口 / 厦门机场标识');p.write_text(s,encoding='utf-8')
