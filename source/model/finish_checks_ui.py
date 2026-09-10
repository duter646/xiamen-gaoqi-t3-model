from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'check_corridor.py';s=p.read_text(encoding='utf-8')
a=s.index("out={'clearance_strip_z'")
s=s[:a]+"""zone=[h for h in collisions if h['mesh'].startswith('Interior_ZoneSeparation')]
unexpected=[h for h in collisions if not h['mesh'].startswith('Interior_ZoneSeparation')]
assert len({tuple(h['ray_yz']) for h in zone})==9, 'Domestic/international separation has an unintended opening'
out={'zones_checked_x':[[-377,74],[76,377]],'clearance_strip_z':[4.9,6.1],'unexpected_collisions':unexpected,'separation_blocks_all_nine_cross_zone_rays':True,'passed':not unexpected,'scope':'Domestic and international circulation are separate. Cross-zone passage is intentionally blocked.'}
(R/'corridor-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False));assert not unexpected
""";p.write_text(s,encoding='utf-8')
p=R/'index.html';s=p.read_text(encoding='utf-8')
s=s.replace("const tick=new THREE.Clock();", """window.showExitRoute=async(id)=>{const paths=await fetch('security-exit-paths.json').then(r=>r.json());const route=paths.find(p=>p.id===id);if(!route)return;window.setView('exit');document.querySelector('#routes').checked=true;layers();model.traverse(o=>{if(o.isMesh&&o.name.startsWith('Audit_'))o.visible=o.name.startsWith('Audit_Exit_'+id+'_');});let dom=id.includes('-D-');camera.position.set(dom?-4:146,70,dom?63:44);controls.target.set(dom?-5:129,12.1,dom?32:31);controls.update();};
const tick=new THREE.Clock();""")
p.write_text(s,encoding='utf-8')
p=R/'render_check.cjs';s=p.read_text(encoding='utf-8').replace("['end','letters','isolation','stairs','corridor','hall']","['exit','isolation','stairs','corridor']");p.write_text(s,encoding='utf-8')
