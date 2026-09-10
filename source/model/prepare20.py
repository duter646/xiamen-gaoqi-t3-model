from pathlib import Path
p=Path(__file__).parent
f=p/'roof16.py';s=f.read_text(encoding='utf-8');a=s.index('photo_rows=');b=s.index('for side,width,distances',a)
s=s[:a]+'''# Shared elevations on both sides. Larger near-ridge drops and progressively
# smaller outer drops produce the more pronounced curved silhouette requested.
photo_heights=np.array([32.5,25.8,21.8,19.2,17.5,16.5],float)
'''+s[b:]
a=s.index('# Independently match');b=s.index('roof16_tiers=roof17_tiers',a);s=s[:a]+s[b:];f.write_text(s,encoding='utf-8')
f=p/'check17.py';s=f.read_text(encoding='utf-8').replace('validation19.json','validation20.json');s=s.replace("top=points('Roof_MainSheet')", "assert np.allclose([t[2] for t in tiers['-1']],[t[2] for t in tiers['1'][:3]])\nassert len(points('Roof_SolidEaveConcourseClosure'))>0\ntop=points('Roof_MainSheet')");f.write_text(s,encoding='utf-8')
for name in ['index.html','review.html','render13.cjs','render_roof16.cjs']:
 f=p/name;s=f.read_text(encoding='utf-8').replace('revision19/','revision20/').replace('修订版 19','修订版 20').replace('停机坪侧檐口 / 通道屋顶衔接','两侧同高 / 加强弧度 / 实心檐口');f.write_text(s,encoding='utf-8')
(p/'CHANGES.md').write_text('修订版 20\n\n撤销停机坪侧独立标高：两侧对应三档保持同高，同时调整共享高度轮廓，加强靠近屋脊的弯曲，向外檐逐步放缓。水平步长不变。\n\n檐口至登机通道屋顶之间补成闭合实心体，沿弧梁下缘封闭顶部与两端，底部连接通道屋顶。内部仍为三角形支撑。标高与构件尺寸为照片估算。\n',encoding='utf-8')
