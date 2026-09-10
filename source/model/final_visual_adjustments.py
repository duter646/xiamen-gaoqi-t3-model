from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'interior_detail.py';s=p.read_text(encoding='utf-8').replace('(x,F3-1.12,62.13)','(x,F3-1.82,62.13)');p.write_text(s,encoding='utf-8')
p=R/'index.html';s=p.read_text(encoding='utf-8').replace('0xe9f4ff,0xa7b4ac,1.65','0xf4f3ed,0xb8afa2,1.65').replace("new THREE.Color(0x889b9c)","new THREE.Color(0xa5a59e)").replace('0xdbe8ef','0xe8e7df').replace('0xe2e9e8','0xe7e4db').replace('0x829aa2','0x999992');p.write_text(s,encoding='utf-8')
p=R/'CHANGES.md';s=p.read_text(encoding='utf-8').replace('距楼板底 0.275 m','距楼板底约 0.975 m，且低于邻近吊顶约 0.315 m');s=s.replace('未用全局色调覆盖替代材质修改。','同时将预览环境光改为较中性的色温，减少绿灰反射偏色。');p.write_text(s,encoding='utf-8')
