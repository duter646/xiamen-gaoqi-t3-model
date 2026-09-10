from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'index.html';s=p.read_text(encoding='utf-8').replace('const views={','const views={voidcheck:[[109,42,51],[90,9,35]],').replace('<button data-view="international">','<button data-view="voidcheck">国际扶梯挑空</button><button data-view="international">').replace("'directarrival'].includes(name)","'directarrival','voidcheck'].includes(name)");p.write_text(s,encoding='utf-8')
(R/'CHANGES.md').write_text('''# 第 14 版

本轮合并用户连续标注的边检、挑空、侧立面和牌子修改。

- 边检柜台从旧纵向排列移到前侧返回位置，原柜台线改为隔离墙，补国际区外侧墙。三层路线依次通过边检、安检、国际候机廊。
- 扶梯旁上层挑空轮廓向图示方向调整，删除原隔断折返，边界沿新的开口外侧连接；二层在梯段下方开洞，保留东端下落平台，并补洞边栏杆。具体坐标为依据图示的建模估计。
- 各阶屋面下方的室内天花板改为水平吊顶；柱顶和标牌吊杆随实际底面重新计算。屋面外部排水坡面与吊顶分别建模。
- 移除叠加的多套粗竖梁，重新区分侧立面主要支柱与细窗框。雨棚两端各缩进一个现有结构跨，约 12 m；增加主楼低檐与登机廊顶的连接收边。
- 机场牌采用用户提供的 2072×759 RGBA 原图，保留比例和透明通道，直接嵌入 GLB；不再使用旧字形。该牌是透明图板配少量背撑，不是每根框架和笔画都独立建模的三维构件。
- 预览新增“国际扶梯挑空”视角。

## 验证

processing-order-validation.json：0.25 m 网格、0.22 m 行人半径的三层几何连通性检查。正常路线可达；虚拟封闭边检后不能进入边检后区域或候机区；封闭安检后不能进入候机区。此检查不覆盖跨楼层逆向行走，预览相机仍为自由观察相机。

revision14-validation.json：国际扶梯两侧连续净空、二层梯段下方洞口及下落平台。

security-exit-validation.json：25 条安检后路线。

door-west-validation.json：12 处外门与西侧扶梯。

sign-mount-audit.json、column-connections.json：牌子支撑和柱顶连接。

validation-report.json、exterior-browser-validation.json、final-browser-validation.json：导出结构与实际渲染。

当前仍非测绘级复原；F/G 岛与三层投影比例、部分设施占地及西侧示意区域仍有待校准。此前道路下方问号的具体含义尚未确认，本轮未重新设计道路。
''',encoding='utf-8')
