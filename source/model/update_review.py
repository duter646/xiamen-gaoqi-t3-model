from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'review.html';s=p.read_text(encoding='utf-8').replace('第6版','第7版').replace('reference-roof.png','../revision6/reference-roof.png').replace('reference-security.png','../revision6/reference-security.png')
s=s.replace('<button data-key="roof">','<button data-key="palette">室内色彩</button><button data-key="roof">')
s=s.replace('const choices={',"const choices={palette:{title:'暖灰地面、米色顶面与棕绿座椅',image:'../references/check-in.jpg',view:'hall',note:'校正室内材质；修复安检门框与柱子、商店背墙与柱子及商店与电梯/安检设备之间的重叠。补玻璃护栏、登机标牌吊杆、小商店顶面和电梯井顶盖。两处到达桥入口及电梯开洞完成针对性检查。',source:'2024 年 12 月值机大厅实拍；另对照 2024 年候机区和 2017 年长廊照片。'},")
s=s.replace("select('roof');","select('palette');")
p.write_text(s,encoding='utf-8')
