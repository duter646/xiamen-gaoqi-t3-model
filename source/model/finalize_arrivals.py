from pathlib import Path
R=Path(__file__).resolve().parent
(R/'CHANGES.md').write_text('''# 第 8 版：到达层、楼层连接与隔断

## 已完成

- 一层新增国内 1–6、国际 7–10 号行李转盘，分别设置长度；依据照片制作圆角回转带、斜面胶带和不锈钢围边。
- 补国际入境边检、海关、国内与国际行李厅隔离、接机出口、公共接机通廊、服务柜台、不同轮廓的卫生间及餐饮房间、行李车、方柱包覆、低吊顶和方形灯具。
- 二层补封闭到达通道及四组通往一层的东西向扶梯；与值机大厅以不透明墙分开。公共电梯及扶梯与到达受控通道区分。
- 三层两组原有到达扶梯改为东西向，调整连接平台避免压住梯段；补国际侧上层连接。国际侧新增连接的精确井道位置为推定。
- 安检出口保留取包、横向通行和进入所属候机廊的路线；国内隔断回折移到到达连接桥外侧。
- 国内、国际上层隔断绕开中庭，改用透明玻璃分段；二层值机区补分区隔断，保留入口侧公共横向通廊。
- 洞口栏杆按实际楼板与开洞边界重新生成，去掉重叠、悬空及挡住梯段入口的旧栏杆。
- 恢复原柱径，柱顶逐顶点贴合屋盖底面。隐藏屋顶或剖切时柱顶仍会露出，这是查看方式。
- A–G 岛分别调整长宽；F、G 加入不对称短边和后侧回折。导览图中的蓝色通行地面未做成柜台实体。柜台数量、回折的施工细节和遮挡部分仍为推定。

## 验证范围

- security-exit-validation.json：25 条安检出口路线，多高度射线与楼板采样。
- arrival-validation.json：四组二层至一层、三组上层至二层到达扶梯，沿双侧踏步采样净空并检查东西向方向。
- interior-validation.json：连接桥入口及转向梯段的通路、电梯楼板开洞。
- guard-support-validation.json：新建三层洞口栏杆逐段检查楼板支撑。
- column-connections.json：主楼柱顶与屋盖底面连接。
- corridor-validation.json：国内、国际各自候机廊通行与跨区隔离。
- validation-report.json、browser-validation.json：GLB 结构与浏览器加载。

这些检查不等于全建筑无穿模或所有客流已完全复原。

## 依据和限制

1. [机场官方历史到达图](https://xiamenairport.com.cn/images/lkzn/4hjldt2-big.jpg)：楼层、转盘编号、联检及接机区关系。本地原图 ../revision2/references/official-arrival-map.jpg。
2. [Tyg728，T3 行李提取厅，2017-07-23](https://commons.wikimedia.org/wiki/File:Xiamen_Gaoqi_International_Airport_Terminal_3_Baggage_Claim_Hall_20170723.jpg)，CC BY-SA 4.0。本地 arrival-photo.jpg 为未修改参考照片，用于结构与材料观察，未作为模型纹理。
3. [国航厦门机场指南](https://webresource.airchina.com.cn/zh-CN/content/travel_info/preparing/conditions/destination/china/xmn/)：国际到达的检疫、边检、行李、海关及到达大厅流程。
4. 用户提供的出发结构图及此前保存的值机、候机廊实拍。

仍待核实：2024 年后到达层完整现状清单、精确隔断线位、扶梯井对应关系、测绘尺寸、全部房间门洞及陈设。国际侧新增上层连接未获精确图纸确认。此模型不能声称与现实每一处细节一致。
''',encoding='utf-8')
p=R/'review.html';s=p.read_text(encoding='utf-8')
s=s.replace('第 8 版 · 安检后能够进入所属候机区','第 8 版 · 到达层、楼层连接与隔断')
s=s.replace('index.html?view=exit','index.html?view=arrival')
s=s.replace('<aside><h2','''<aside><p>新增一层行李提取、联检和接机空间，以及二层封闭到达通道。</p>
<button onclick="viewer.contentWindow.setView('arrival')">到达行李厅</button>
<button onclick="viewer.contentWindow.setView('arrivalplan')">到达层平面</button>
<button onclick="viewer.contentWindow.setView('arrivalstairs')">到达扶梯连接</button>
<button onclick="viewer.contentWindow.setView('checkinplan')">值机岛与分区</button>
<p><a href="index.html?view=arrival">全屏浏览</a></p><h2''')
s=s.replace('</small></aside>','''</small><p>到达梯段检查：7 组双侧踏步净空。具体井道位置及部分隔断线位仍为推定，详见报告。</p>
<details><summary>到达参考图</summary><a href="../revision2/references/official-arrival-map.jpg" target="_blank"><img style="width:100%" src="../revision2/references/official-arrival-map.jpg"></a><a href="arrival-photo.jpg" target="_blank"><img style="width:100%" src="arrival-photo.jpg"></a><small>实拍：Tyg728 / CC BY-SA 4.0，出处见报告。</small></details></aside>''')
p.write_text(s,encoding='utf-8')
