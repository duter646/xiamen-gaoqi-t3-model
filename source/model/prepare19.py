from pathlib import Path
p=Path(__file__).parent
f=p/'roof16.py';s=f.read_text(encoding='utf-8')
s=s.replace('roof16_tiers=roof17_tiers', '''# Independently match the apron-facing silhouette against the corridor roof.
# Approximate points in the user's 600 px photo: central cornice (423,194),
# inner apron cornice (471,225), outer cornice (520,253), corridor contact (565,266).
# Previous code incorrectly reused landside image heights for this side.
airside_rows=np.array([194,225,253],float)
airside_heights=32.5-(airside_rows-194)/(266-194)*(32.5-18.01)
roof17_tiers[-1]=[(a,b,float(airside_heights[i])) for i,(a,b,h) in enumerate(roof17_tiers[-1])]
roof16_tiers=roof17_tiers''')
f.write_text(s,encoding='utf-8')
f=p/'curve17.py';s=f.read_text(encoding='utf-8').replace('[(38,18.67),(39,18.67)]','[(31.5,18.67),(32.5,18.67)]').replace('(x,18.025,-.5)','(x,18.025,6.0)');f.write_text(s,encoding='utf-8')
f=p/'check17.py';s=f.read_text(encoding='utf-8').replace('(curves[:,2]<-.9)','(curves[:,2]<5.6)').replace('validation18.json','validation19.json');f.write_text(s,encoding='utf-8')
for name in ['index.html','review.html','render13.cjs','render_roof16.cjs']:
 f=p/name;s=f.read_text(encoding='utf-8').replace('revision18/','revision19/').replace('修订版 18','修订版 19').replace('等步长 / 按实图调整落差','停机坪侧檐口 / 通道屋顶衔接');f.write_text(s,encoding='utf-8')
(p/'CHANGES.md').write_text('修订版 19\n\n停机坪侧不再沿用陆侧檐口高度。以照片中最高檐口、停机坪侧两档檐口和通道屋顶接触点，重新估算该侧标高，降低最外档与通道屋顶的高差。缩短外部弧梁在通道屋顶上的延伸，落脚点从通道中部移到靠主楼的一侧。保持水平步长、内部三角支撑及单层屋面。\n\n照片为斜视图，标高仍是估算。检查见 validation19.json。\n',encoding='utf-8')
