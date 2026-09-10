from pathlib import Path
p=Path(__file__).parent
f=p/'roof16.py';s=f.read_text(encoding='utf-8')
s=s.replace('# About 10.5 m per complete terrace, 3.2 m per drop; the ridge divides\n# the central terrace into 5.5 m landside and 5 m airside halves.', '''# Equal horizontal runs, independently photo-traced elevations.
# Approximate cornice elevations in reference-end-inspect.png, top to bottom.
# Normalize the image differences to the existing overall height range;
# these are proportions from an oblique photo, not measured dimensions.
photo_rows=np.array([50,145,222,280,326,350],float)
photo_heights=32.5-(photo_rows-photo_rows[0])/(photo_rows[-1]-photo_rows[0])*16.0''')
s=s.replace('32.5-3.2*i','float(photo_heights[i])')
f.write_text(s,encoding='utf-8')
f=p/'check17.py';s=f.read_text(encoding='utf-8').replace("assert np.allclose(-np.diff([t[2] for t in tiers[side]]),3.2)","drops=-np.diff([t[2] for t in tiers[side]])\n assert np.all(drops>0) and not np.allclose(drops,drops[0])\n assert np.all(np.diff(drops)<0)")
s=s.replace('drop_m=3.2','drops_m={side:(-np.diff([t[2] for t in tt])).tolist() for side,tt in tiers.items()}').replace('validation17.json','validation18.json');f.write_text(s,encoding='utf-8')
for name in ['index.html','review.html','render13.cjs','render_roof16.cjs']:
 f=p/name;s=f.read_text(encoding='utf-8').replace('revision17/','revision18/').replace('修订版 17','修订版 18').replace('非对称阶梯 / 弧梁连接通道屋顶','等步长 / 按实图调整落差');f.write_text(s,encoding='utf-8')
(p/'CHANGES.md').write_text('修订版 18\n\n撤销统一 3.2 m 落差。保持各档水平步长约 10.5 m；按用户实图檐口高度比例重设各档标高，靠近屋脊落差较大，向檐口逐渐减小。同步更新屋面、窗带、端墙和外部弧梁。内部三角支撑及通道屋顶连接保留。\n\n图片为斜视照片，具体尺寸仍为比例估算。验证见 validation18.json。\n',encoding='utf-8')
