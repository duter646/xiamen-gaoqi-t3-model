"""Marked west void boundary: opaque wall, solid left bay, open right bay."""
# Join the end wall and the domestic bank's existing west isolation return.
wall('Interior_DomesticMarkedBoundary',(X0,30.1),(-56,30.1),F3,3,WHITE)
# The remaining span sits along the void edge; turn toward the screening-bank
# enclosure, not through the existing post-screening passage at x=-25.
wall('Interior_DomesticMarkedBoundary',(-56,30.1),(-32.3,30.1),F3,3,WHITE)
# Recess the final return at the bank's public side, keeping the authorised exit.
# Two-storey void perimeter guards at 2F are on the retained floor side.
for a,b in [((-83.97,6.3,15.43),(92.59,6.3,15.43)),((-83.97,6.3,29.61),(92.59,6.3,29.61)),((-83.97,6.3,15.43),(-83.97,6.3,29.61)),((92.59,6.3,15.43),(92.59,6.3,29.61))]:
    rail('Interior_SecondFloorLongVoidGuards',a,b)
(ROOT/'void21-register.json').write_text(json.dumps(dict(solid_upper_bay=[-83.8653,-67.6301,15.5323,29.0652],extended_upper_void=[-66.0066,-32.4588,17.6047,29.5],second_floor_open_strip=[-83.8653,92.4926,15.5323,29.5],arrival_upper_landings=[[-49.2,F3,20.5271],[23.1,F3,20.5271]],wall_z=30.1,dimensions='user-marked topology; exact dimensions estimated'),indent=2),encoding='utf-8')
