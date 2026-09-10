from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'index.html';s=p.read_text(encoding='utf-8')
s=s.replace('到达层 / 三层连接 / 洞口隔断修复','登机廊连接 / 直达 1F / 边防后安检')
s=s.replace('const views={','const views={passage:[[-25,13.8,32],[-25,13.8,5]],international:[[116,51,109],[100,12,49]],footprints:[[-66,105,61],[-66,12,60.99]],directarrival:[[-13,13,43],[-33,6,20]],')
s=s.replace('<button data-view="arrivalstairs">到达扶梯连接</button>','<button data-view="directarrival">直达 1F 剖面</button><button data-view="passage">穿过登机廊接口</button><button data-view="international">边防与安检围合</button><button data-view="footprints">商业占地轮廓</button>')
s=s.replace("renderer.clippingPlanes=name==='levels'?", "renderer.clippingPlanes=name==='directarrival'?[new THREE.Plane(new THREE.Vector3(0,0,-1),27.8)]:name==='levels'?")
s=s.replace("'arrivalplan'].includes(name)","'arrivalplan','international','footprints','directarrival'].includes(name)")
s=s.replace('及独立到达通道','及到达扶梯穿层空间')
p.write_text(s,encoding='utf-8')
p=R/'render_check.cjs';s=p.read_text(encoding='utf-8').replace("['arrival','arrivalplan','arrivalstairs','checkinplan','exit','isolation']","['passage','international','directarrival','footprints']")
p.write_text(s,encoding='utf-8')
p=R/'review.html';s=p.read_text(encoding='utf-8').replace('第 8 版 · 到达层、楼层连接与隔断','第 9 版 · 登机廊连接、直达 1F 与国际出发顺序').replace('index.html?view=arrival','index.html?view=passage')
s=s.replace('新增一层行李提取、联检和接机空间，以及二层封闭到达通道。','修复屋顶组内误封闭的登机廊窗墙；到达扶梯改为上层直达 1F，国际出发补边防前后围合。')
s=s.replace("setView('arrivalstairs')","setView('directarrival')").replace('到达扶梯连接','直达 1F 剖面')
s=s.replace('<p id="result">','<button onclick="viewer.contentWindow.setView(\'international\')">国际出发围合</button><button onclick="viewer.contentWindow.setView(\'footprints\')">商业轮廓</button><p id="result">')
s=s.replace('到达梯段检查：7 组双侧踏步净空。','到达梯段检查：3 组上层直达 1F，含连续斜向通行射线。')
s=s.replace('检查每条路线的安检门、取包位置、出口通路及其脚下楼板。','检查包含窗墙、屋顶组在内的建筑构件，覆盖安检门、取包位置、出口通路及楼板。')
p.write_text(s,encoding='utf-8')
(R/'CHANGES.md').write_text('''# 第 9 版

- 定位并修复登机廊接口的实际堵墙：Roof_Clerestory 窗墙和 Roof_ClerestoryBands 横带此前被通行检查漏掉。现在保留窗墙结构、在连接口开出实体通路，检查包含 Roof 组。第 8 版的“25 条路线通过”不能证明开屋顶状态下通行。
- 已建三组到达下行扶梯改为上层直达 1F，取消虚构的二层接续梯段。二层设置穿层开洞和遮挡；按净空恢复梯段上方不必要的开洞，国际到达分界处围合梯井。
- 国际扶梯出口补封闭引导通路，先进入边防前区域，再通过边防通道进入安检前区域。保留国内国际隔离，直接绕过边防的横向路线被围合阻挡。具体墙线仍为推定，不能声称符合实测平面。
- 五处主要商业块按参考图可辨认的折角、斜边和凹口单独重建，并记录源图顶点。为避免与柱子冲突，个别估算位置微调约 1.2 m。新增顶盖随实际多边形轮廓。
- facility-footprint-audit.json 列出设施核对状态；其余被图标遮挡或缺乏清晰墙线的设施不能标为已准确复原。该项核对仍有未确认部分，未用任意凹口冒充真实形状。

## 检查

security-exit-validation.json：包含 Roof 构件的安检至候机廊路径。
international-flow-validation.json：扶梯到边防前、边防到安检前的路径，以及绕过边防的直接通路阻挡检查。
arrival-validation.json：上层直达 1F 的方向、终点、双侧净空采样及连续斜向射线。
footprint-column-audit.json：新商业轮廓与柱子的局部碰撞检查。
guard-support-validation.json：新生成洞口栏杆的落地支撑。
validation-report.json、browser-validation.json：GLB 结构和浏览器加载。

## 参考与限制

以用户提供的出发结构图、机场官方历史到达图及项目已有实拍为依据。facility-reference.png 是出发图局部放大，形状顶点记录与之对应；图纸比例不等于测绘尺寸。

补检资料：[机场商业项目公告](https://xiamenairport.com.cn/gywm/kgdt-open.aspx?id=1507&name=%E9%87%8D%E8%A6%81%E5%85%AC%E5%91%8A)、[T3 国内出发及商业区域照片记录](https://classic-blog.udn.com/visa520infinite/179174837)。这些资料未提供可确认所有商铺完整边界的近期测绘平面。旧照片不代表 2024 年后每家商户现状。

国际出发流程的先后关系已落实；精确井道配对、墙线和全设施占地仍存在估计项，当前版本并非完整实景还原。
''',encoding='utf-8')
