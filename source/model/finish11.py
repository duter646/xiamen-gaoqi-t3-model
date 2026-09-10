from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'index.html';s=p.read_text(encoding='utf-8')
floors=s[s.index('<div class="label">独立展示楼层'):s.index('<div class="label">模型图层')]
s=s.replace(floors,'').replace('<aside class="panel">','<aside class="panel">'+floors)
s=s.replace('登机廊连接 / 直达 1F / 边防后安检','大厅挑空 / 国际动线 / 外墙与门洞')
s=s.replace('<button data-view="international">边防与安检围合</button>','<button data-view="international">边防与安检围合</button><button onclick="showInternationalRoute()">核对国际动线</button>')
s=s.replace('window.setView=(name)=>{',"window.setView=(name)=>{if(window.internationalOverlay)window.internationalOverlay.visible=false;")
insert="""
window.showInternationalRoute=async()=>{
 window.setView('international');
 if(!window.internationalOverlay){
  const f=await fetch('./international-flow.json').then(r=>r.json());
  const group=new THREE.Group();
  const points=[...f.public_stair_to_border,...f.border_to_security.slice(1)].map(p=>new THREE.Vector3(p[0],12.27,p[1]));
  const mat=new THREE.MeshBasicMaterial({color:0xd65b00});
  for(let i=1;i<points.length;i++){
   const a=points[i-1],b=points[i],delta=b.clone().sub(a),length=delta.length();
   const bar=new THREE.Mesh(new THREE.CylinderGeometry(.14,.14,length,8),mat);bar.position.copy(a).add(b).multiplyScalar(.5);bar.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),delta.clone().normalize());group.add(bar);
   const arrow=new THREE.Mesh(new THREE.ConeGeometry(.6,1.6,12),mat);arrow.position.copy(a).lerp(b,.72);arrow.quaternion.copy(bar.quaternion);group.add(arrow);
  }
  window.internationalOverlay=group;scene.add(group);
 }
 window.internationalOverlay.visible=true;
};
"""
s=s.replace("const tick=new THREE.Clock();",insert+"\nconst tick=new THREE.Clock();")
p.write_text(s,encoding='utf-8')
(R/'review.html').write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=index.html"><title>第11版</title><a href="index.html">打开第11版模型与分层查看</a>',encoding='utf-8')
(R/'CHANGES.md').write_text('''# 第 11 版

- 保留上一轮的整面假墙移除、两组直达 1F 到达扶梯、12 处外门、西侧下行扶梯与独立楼层展示。
- 删除主楼三层临街灰色区域的误建楼板（模型 z=68–96），收回悬空隔断并沿新板边补栏杆。原先平铺到外墙的三层楼板已取消。
- 国际出发重新安排扶梯上口至边防前的折返围合，移除占据公共通道的两处旧边防柜台；通过边防检查开口后进入安检。浏览页新增橙色国际动线核对按钮。
- 补齐 1F 朝停机坪一侧的整段外墙，与先前两端外墙闭合。
- 西侧 22、23、25、26 号登机口设真实门洞；柜台移至一侧，标牌上移，门扇收至两边。
- 按用户侧立面照片增加密排浅色水平百叶、竖向框格和分级挑出檐口；西侧扶梯连接门洞在新增构件中同步开洞。
- 将 1F / 2F / 3F 切换移到侧栏顶部，review 入口直接进入本版 index。

## 验证范围与限制

实际 GLB 几何验证包括四个西侧门洞、12 个主楼外门、西侧下行扶梯净空、两组到达扶梯、25 条安检至登机廊路线、国际路线的通行与直接绕行阻断，以及新补外墙与删除楼板的网格取样。

这是照片和导览图约束下的复原，非测绘模型。三层灰色区域的大块楼板已删除，但原有 F/G 值机岛纵深与上层处理区边缘仍存在投影重叠，需要校准两张分层图的比例和对应位置；不能据此宣称每个值机岛全轮廓上方均已核实无楼板。西侧候机区位置、尺寸仍属示意。外立面照片未提供精确尺寸，百叶间距、檐口尺寸为估计。
''',encoding='utf-8')
