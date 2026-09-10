from pathlib import Path
R=Path(__file__).parent
exec((R/'check_order12.py').read_text(encoding='utf-8').split('start=[86.5')[0])
reg=json.loads((R/'circulation-register.json').read_text(encoding='utf-8'))['facilities']
sealed=[]
for bank in ['SEC-D','SEC-I']:
 lanes=[r for r in reg if r['kind']=='security lane' and r['id'].startswith(bank)]
 a=np.array(lanes[0]['position'])[[0,2]];b=np.array(lanes[-1]['position'])[[0,2]];v=(b-a)/np.linalg.norm(b-a)
 sealed.append(((a-2.2*v).tolist(),(b+4.6*v).tolist()))
arrival=[21.75,20.5]
international=reachable([81.5,5.5],arrival,sealed)
domestic=reachable([5.75,5.5],arrival,sealed)
out=dict(international_gate9_to_arrival=international['reachable'],domestic_gate8_to_arrival=domestic['reachable'],divider_x=20.2,gate8_x=5.7304,gate9_x=81.4633,scope='3F controlled areas with security banks sealed to exclude reverse traversal through public halls')
(R/'zone22-validation.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out))
assert international['reachable'] and not domestic['reachable']
