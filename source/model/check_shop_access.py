from pathlib import Path
R=Path(__file__).parent
exec((R/'check21.py').read_text(encoding='utf-8'))
shop=json.loads((R/'triangular-shop.json').read_text(encoding='utf-8'))
inside=np.mean(shop['outline_xz'],axis=0).tolist()
result=dict(public_to_shop=reachable(start,inside,seal)['reachable'],shop_to_gates_when_security_sealed=reachable(inside,gate,seal)['reachable'],shop_to_gates_via_security=reachable(inside,gate)['reachable'])
(R/'shop-access-validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result))
assert result['public_to_shop'] and result['shop_to_gates_via_security']
assert not result['shop_to_gates_when_security_sealed']
