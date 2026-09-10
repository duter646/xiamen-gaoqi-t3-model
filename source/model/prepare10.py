from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'build_revision.py';s=p.read_text(encoding='utf-8');s=s.replace("        z=roof_z(dist,side);lo=roof_y(lo,dist,side);hi=roof_y(hi,dist,side)","        if side==-1 and dist==54:continue  # no wall between hall and gate concourse\n        z=roof_z(dist,side);lo=roof_y(lo,dist,side);hi=roof_y(hi,dist,side)")
p.write_text(s,encoding='utf-8')
p=R/'interior_detail.py';s=p.read_text(encoding='utf-8').replace('assert len(text_items)<=256',"exec(compile((ROOT/'doors_and_sides.py').read_text(encoding='utf-8'),str(ROOT/'doors_and_sides.py'),'exec'))\nassert len(text_items)<=256");p.write_text(s,encoding='utf-8')
for file in ['index.html','review.html','render_check.cjs']:
    p=R/file;s=p.read_text(encoding='utf-8').replace('revision9','revision10').replace('修订版 9','修订版 10').replace('第 9 版','第 10 版');p.write_text(s,encoding='utf-8')
p=R/'index.html';s=p.read_text(encoding='utf-8')
s=s.replace('<div class="label">模型图层</div>', '<div class="label">独立展示楼层</div><div class="views"><button data-floor="all" class="active">全部楼层</button><button data-floor="1">只看 1F</button><button data-floor="2">只看 2F</button><button data-floor="3">只看 3F</button></div><div class="label">模型图层</div>')
s=s.replace("let current='overall';","let current='overall';let selectedFloor='all';")
s=s.replace("window.setView=(name)=>{current=name;", "window.setView=(name)=>{selectedFloor='all';document.querySelectorAll('[data-floor]').forEach(e=>e.classList.toggle('active',e.dataset.floor==='all'));current=name;")
needle="document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>window.setView(b.dataset.view));"
s=s.replace(needle,'''window.setFloor=(floor)=>{
 selectedFloor=String(floor);current='floor'+floor;
 const bands={'1':[-.15,5.75,.3],'2':[5.85,11.65,6.3],'3':[11.65,50,12.1]};
 if(floor==='all'){window.setView('overall');return;}
 const [low,high,y]=bands[selectedFloor];
 renderer.clippingPlanes=[new THREE.Plane(new THREE.Vector3(0,1,0),-low),new THREE.Plane(new THREE.Vector3(0,-1,0),high)];
 camera.position.set(22,y+200,66);controls.target.set(22,y,65.99);
 document.querySelector('#roof').checked=false;document.querySelector('#rotate').checked=false;controls.autoRotate=false;
 layers();controls.update();document.querySelectorAll('[data-floor]').forEach(e=>e.classList.toggle('active',e.dataset.floor===selectedFloor));
 document.querySelectorAll('[data-view]').forEach(e=>e.classList.remove('active'));
};document.querySelectorAll('[data-floor]').forEach(b=>b.onclick=()=>window.setFloor(b.dataset.floor));
'''+needle)
p.write_text(s,encoding='utf-8')
