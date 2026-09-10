from pathlib import Path
R=Path(__file__).resolve().parent
for name in ['review.html','CHANGES.md','check_revision.py','check_interior.py']:
    p=R/name;s=p.read_text(encoding='utf-8')
    s=s.replace('3 组上层直达 1F','2 组上层直达 1F').replace('已建三组到达','图示国内、国际两组到达')
    s=s.replace("'upper_arrival_escalators':3","'upper_arrival_escalators':2").replace("'direct_3F_to_1F_arrival_escalators':3","'direct_3F_to_1F_arrival_escalators':2")
    s=s.replace("'arrival_bridge_entries':3","'arrival_bridge_entries':2").replace("'arrival_entry_clearance_rays':24","'arrival_entry_clearance_rays':16")
    p.write_text(s,encoding='utf-8')
p=R/'CHANGES.md';s=p.read_text(encoding='utf-8');s=s.replace('约 1.2 m','约 1.2–2.0 m');s+='\n已删除无图示依据的第三组到达扶梯，同时撤掉其楼板开洞、连接平台及附属栏杆；检查断言只允许国内、国际两组。\n';p.write_text(s,encoding='utf-8')
