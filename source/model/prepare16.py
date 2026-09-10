from pathlib import Path
p=Path(__file__).parent
f=p/'interior_detail.py';s=f.read_text(encoding='utf-8').replace('ceiling14.py','roof16.py');f.write_text(s,encoding='utf-8')
f=p/'facade13.py';s=f.read_text(encoding='utf-8')
a=s.index('    # The projecting stepped screen');b=s.index('    for side in [-1,1]:\n        for d0,d1,h',a)
s=s[:a]+s[b:];f.write_text(s,encoding='utf-8')
for name in ['index.html','review.html','render13.cjs','render14.cjs']:
    f=p/name
    if not f.exists():continue
    s=f.read_text(encoding='utf-8').replace('revision14/','revision16/').replace('修订版 14','修订版 16').replace('边检位置 / 平吊顶 / 实拍机场标识','单层阶梯屋面 / 内部弧形支撑')
    f.write_text(s,encoding='utf-8')
(p/'CHANGES.md').write_text('修订版 16：按用户剖面标注和 revision2 内外景修正屋顶。\n\n屋面和下表面采用同一阶梯轮廓，厚度 0.22 米；删除旧斜屋面、分离平吊顶及端部三角形封闭面。补齐窗带下阶梯立面，增加屋面下弧形支撑，柱顶和吊牌重新随实际下表面安装。外部曲梁保留为照片中的外露骨架。尺寸仍为照片估算。\n',encoding='utf-8')
