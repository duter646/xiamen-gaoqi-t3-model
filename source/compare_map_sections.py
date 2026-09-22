"""Reproducible guide overlays from the delivered GLB, without rebuilding it."""
from pathlib import Path
import base64
import hashlib
import html
import json
import struct
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source/model'))
from guide_registration import CHECKIN, CHECKIN_WORLD, CHECKIN_PIXELS
OUT = ROOT / 'assets' / 'map-sections'
OUT.mkdir(parents=True, exist_ok=True)
raw = (ROOT / 'assets/xiamen-gaoqi-t3.glb').read_bytes()
size = struct.unpack_from('<I', raw, 12)[0]
doc = json.loads(raw[20:20 + size])
binary = 28 + size


def accessor(index):
    a = doc['accessors'][index]
    v = doc['bufferViews'][a['bufferView']]
    dtype = {5126: '<f4', 5125: '<u4', 5123: '<u2', 5121: 'u1'}[a['componentType']]
    count = {'SCALAR': 1, 'VEC3': 3}[a['type']]
    offset = binary + v.get('byteOffset', 0) + a.get('byteOffset', 0)
    return np.ndarray((a['count'], count), dtype=dtype, buffer=raw, offset=offset,
                      strides=(v.get('byteStride', np.dtype(dtype).itemsize * count), np.dtype(dtype).itemsize)).copy()


meshes = []
for node in doc['nodes']:
    if 'mesh' not in node:
        continue
    # The current exporter writes world-space, untransformed triangles.
    assert not any(k in node for k in ('matrix', 'translation', 'rotation', 'scale', 'children'))
    name = node['name']
    if name.startswith(('Site_', 'Audit_')):
        continue
    for primitive in doc['meshes'][node['mesh']]['primitives']:
        assert primitive.get('mode', 4) == 4
        vertices = accessor(primitive['attributes']['POSITION'])
        indices = accessor(primitive['indices']).ravel() if 'indices' in primitive else np.arange(len(vertices))
        triangles = vertices[indices].reshape(-1, 3, 3).astype(float)
        assert np.isfinite(triangles).all()
        meshes.append((name, triangles, triangles[:, :, 1].min(1), triangles[:, :, 1].max(1)))


def slice_mesh(triangles, lo, hi, height):
    tri = triangles[(lo < height) & (hi > height)]
    segments = []
    for a, b, c in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
        # Select the vertex on the opposite side of the plane from the other two.
        yes = ((tri[:, a, 1] < height) != (tri[:, b, 1] < height)) & ((tri[:, a, 1] < height) != (tri[:, c, 1] < height))
        t = tri[yes]
        if not len(t):
            continue
        ends = []
        for other in (b, c):
            fraction = (height - t[:, a, 1]) / (t[:, other, 1] - t[:, a, 1])
            ends.append((t[:, a] + fraction[:, None] * (t[:, other] - t[:, a]))[:, [0, 2]])
        segments.extend(np.stack(ends, axis=1))
    return np.asarray(segments).reshape(-1, 2, 2)


lower_matrix = CHECKIN
upper_matrix = np.array([[2.39, 2.35, 228 + 2.39 * 384 + 2.35 * 12.5],
                         [-1.42, 1.4, 1358 - 1.42 * 384 + 1.4 * 12.5]])
arrival_world = np.array([[-86.5, 52, 1], [129.5, 52, 1], [-86.5, 61, 1]])
arrival_pixels = np.array([[646, 1019], [1200, 706], [673.5, 1035.5]])
arrival_matrix = np.linalg.solve(arrival_world, arrival_pixels).T
configs = [
    dict(id='arrival', title='1F 到达层', image='official-arrival-map.jpg', base=.3, matrix=arrival_matrix,
         crop=[310, 510, 1580, 1240], note='以 1、10 号行李转盘中心和 1 号转盘长轴端点作临时配准；其余转盘按图定位并留出柱体间隙。重投影残差仅说明拟合结果，不能验证实际尺寸。'),
    dict(id='checkin', title='2F 值机层', image='official-departure-map.jpg', base=6.3, matrix=lower_matrix,
         crop=[830, 990, 1900, 1640], note='以值机大厅四个楼板边界角点单独配准；不复用上层图的比例。导览图边缘有变形，角点拟合约 9.5 像素残差；设施轮廓参与建模后不再是独立验证。'),
    dict(id='departure', title='上层安检与候机', image='official-departure-map.jpg', base=12.1, matrix=upper_matrix,
         crop=[150, 240, 2170, 1420], note='沿用候机层既有斜投影变换。官方图为展开示意，模型称 3F；局部拉伸及年代差异需单独核查。'),
]
colors = {'low': '#ffd166', 'walls': '#ff537e'}
font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 24)
report = {'model_sha256': hashlib.sha256(raw).hexdigest(), 'method': 'actual GLB triangle-plane intersections; no model mutations',
          'limitations': ['Guide is not a surveyed plan', 'No dimensional or collision pass asserted', 'No camera refitting per component'], 'views': []}
views = []
for cfg in configs:
    matrix = cfg['matrix']
    source = ROOT / 'references' / cfg['image']
    im = Image.open(source).convert('RGB')
    width, height = im.size
    svg_groups = []
    raster = Image.blend(im, Image.new('RGB', im.size, '#111923'), .18)
    draw = ImageDraw.Draw(raster)
    inventory = []
    for category, offset in [('low', .55), ('walls', 1.5)]:
        cut = cfg['base'] + offset
        paths = []
        total = 0
        for name, tri, lo, hi in meshes:
            segments = slice_mesh(tri, lo, hi, cut)
            if not len(segments):
                continue
            projected = segments @ matrix[:, :2].T + matrix[:, 2]
            total += len(projected)
            inventory.append(dict(mesh=name, section=category, segments=len(projected)))
            d = ' '.join(f'M{a[0]:.2f},{a[1]:.2f}L{b[0]:.2f},{b[1]:.2f}' for a, b in projected)
            paths.append(f'<path d="{d}"><title>{html.escape(name)}</title></path>')
            for line in projected:
                draw.line([tuple(line[0]), tuple(line[1])], fill=colors[category], width=2)
        assert total > 100, (cfg['id'], category, total)
        svg_groups.append(f'<g class="{category}" fill="none" stroke="{colors[category]}" stroke-width="1.25" stroke-linecap="round">' + ''.join(paths) + '</g>')
    data = base64.b64encode(source.read_bytes()).decode()
    viewbox = ' '.join(map(str, [cfg['crop'][0], cfg['crop'][1], cfg['crop'][2]-cfg['crop'][0], cfg['crop'][3]-cfg['crop'][1]]))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" role="img" aria-label="{cfg["title"]}地图与模型切片叠图"><image class="map" width="{width}" height="{height}" href="data:image/jpeg;base64,{data}"/>' + ''.join(svg_groups) + '</svg>'
    (OUT / (cfg['id'] + '.svg')).write_text(svg, encoding='utf-8')
    crop = raster.crop(tuple(cfg['crop']))
    canvas = Image.new('RGB', (crop.width, crop.height + 90), '#111923')
    canvas.paste(crop, (0, 90))
    label = ImageDraw.Draw(canvas)
    label.text((18, 8), cfg['title'] + ' · 当前 GLB 与官方导览图叠加', font=font, fill='white')
    label.text((18, 46), '黄色：楼面 +0.55m 切片    粉色：楼面 +1.50m 切片', font=font, fill='#ffd166')
    canvas.save(OUT / (cfg['id'] + '.png'))
    views.append(f'<section id="{cfg["id"]}" class="view"><h2>{cfg["title"]}</h2><p>{cfg["note"]}</p><div class="viewport">{svg}</div></section>')
    report['views'].append(dict(id=cfg['id'], source=cfg['image'], source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        transform_xz_to_pixels=matrix.tolist(), slice_heights=[cfg['base']+.55, cfg['base']+1.5], crop=cfg['crop'], note=cfg['note'], inventory=inventory))

# Fitted carousel centres: this is a reprojection check, not independent evidence.
observations = {2: [711, 979], 3: [781, 944], 4: [833, 906], 5: [894, 867], 6: [956, 831], 7: [986, 791], 8: [1080, 769], 9: [1142, 736]}
checks = []
for number, observed in observations.items():
    points = []
    for name, tri, lo, hi in meshes:
        if name.startswith(f'Interior_ArrivalCarousel_{number}_'):
            body=tri[(hi<1.5)&(lo>.4)]
            if len(body):
                points.extend(body[:,:,[0,2]].reshape(-1,2))
    pts = np.asarray(points)
    centre = (pts.min(0) + pts.max(0)) / 2
    projected = arrival_matrix[:, :2] @ centre + arrival_matrix[:, 2]
    checks.append(dict(id=number, mesh_center_xz=centre.tolist(), guide_pixel=observed, projected_pixel=projected.tolist(), residual_pixels=float(np.linalg.norm(projected-observed))))
report['arrival_fitted_centres'] = checks
report['arrival_centres_used_for_refinement'] = True
report['checkin_registration_anchors'] = {'world':CHECKIN_WORLD.tolist(),'pixels':CHECKIN_PIXELS.tolist(),'method':'four floor outline corners; least-squares affine; manual diagram reading'}
report['arrival_registration_anchors'] = {'world_xz_homogeneous': arrival_world.tolist(), 'pixels': arrival_pixels.tolist(), 'reading_uncertainty_px': 8, 'scale_is_estimated': True}
(OUT / 'audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
template = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>T3 地图与模型逐层切片</title>
<style>*{box-sizing:border-box}body{margin:0;background:#101820;color:#eef3f8;font:15px/1.65 system-ui,"Microsoft YaHei",sans-serif}header,main{max-width:1440px;margin:auto;padding:22px}h1{margin:0;font-size:28px}h2{font-size:20px;margin:12px 0}p{color:#b9c7d4;margin:8px 0}nav{position:sticky;top:0;z-index:2;background:#182733;padding:12px 22px;display:flex;gap:18px;flex-wrap:wrap;align-items:center}select,button{padding:8px;border:1px solid #536676;background:#243747;color:white;border-radius:5px}label{white-space:nowrap}input{vertical-align:middle}a{color:#9dd6ff}.view{display:none}.view.active{display:block}.viewport{overflow:auto;border:1px solid #405564;background:#211e1f}svg{display:block;width:100%;min-width:650px;height:auto}.map{opacity:.85}td,th{text-align:left;padding:10px;border-bottom:1px solid #3b4d59}table{width:100%;border-collapse:collapse}.hint{border-left:3px solid #ffd166;padding-left:14px}footer{padding:20px;color:#a9b8c4}button{cursor:pointer}</style>
<header><h1>T3 · 地图与模型逐层切片</h1><p>直接读取交付 GLB 的三角网格。黄色为楼面上方 0.55 m，粉色为 1.50 m 的真实水平截线。</p><p class="hint">导览图含错层展开、图标抬升和示意变形；用于发现相对布局问题，像素偏差不等于实际米数。长廊外围廊桥超出地图表现范围仍保留。</p></header>
<nav><select id="floor" aria-label="对比楼层"><option value="arrival">1F 到达层</option><option value="checkin">2F 值机层</option><option value="departure">上层安检与候机</option></select><label><input type="checkbox" id="low" checked> <span style="color:#ffd166">低位设施</span></label><label><input type="checkbox" id="walls" checked> <span style="color:#ff537e">墙体高度</span></label><label>地图透明度 <input id="opacity" type="range" min="0" max="100" value="85"></label><label>放大 <input id="zoom" type="range" min="100" max="250" value="100"></label><button id="reset">复位</button><a href="../index.html">三维模型</a><a href="../assets/map-sections/vertical-sections.png">电梯与挑空纵剖</a></nav>
<main>VIEWS
<h2>部件核对范围</h2><table><tr><th>范围</th><th>对比要点</th><th>核查范围</th></tr><tr><td>1F 行李转盘</td><td>10 组转盘使用各自图上中心；7 号长转盘位于更靠后的位置。</td><td>中心定位已统一；长度、宽度和隐藏构造仍为估计。</td></tr><tr><td>2F A–G 值机岛</td><td>7 个岛的中心和轮廓使用同一大厅配准；柜台、回折、支架和排队设施共享位置。</td><td>柜台与柱体截线检查通过；柜台数量和隐藏后端仍待实测。</td></tr><tr><td>上层商店与挑空</td><td>5 处商业空间按图示底部轮廓生成；三处上层挑空分开布置，下层保留到达廊楼板。</td><td>店面与店顶共用轮廓；入口、墙脚支撑及封闭安检后的禁止绕行检查通过。</td></tr><tr><td>长廊与登机口</td><td>模型外壳和廊桥参考 OSM，图中沿廊位置是示意；整体变形不能单凭导览图改正。</td><td>先核对数量、顺序、连接，再以卫星图和实拍确认尺寸。</td></tr><tr><td>扶梯、电梯与隔墙</td><td>4 个电梯井道、门槛及前室已核查；2 条下层连接廊接入受控到达廊。</td><td>28 条安检出口路径及国内、国际隔离检查通过；详见模型纵剖与核查报告。</td></tr></table><p>配准与每个切片的网格清单见 <a href="../assets/map-sections/audit.json">审计数据</a>。此页对应当前交付模型；未覆盖的实测尺寸、屋面纵剖与设施运营状态保留待核查。</p></main>
<footer>模型 SHA-256：HASH</footer><script>
const $=id=>document.getElementById(id);function update(){document.querySelectorAll('.view').forEach(s=>s.classList.toggle('active',s.id===$('floor').value));document.querySelectorAll('.low').forEach(g=>g.style.display=$('low').checked?'':'none');document.querySelectorAll('.walls').forEach(g=>g.style.display=$('walls').checked?'':'none');document.querySelectorAll('.map').forEach(g=>g.style.opacity=$('opacity').value/100);document.querySelectorAll('svg').forEach(g=>g.style.width=$('zoom').value+'%')}['floor','low','walls','opacity','zoom'].forEach(id=>$(id).addEventListener('input',update));$('reset').onclick=()=>{$('low').checked=$('walls').checked=true;$('opacity').value=85;$('zoom').value=100;update()};update();</script></html>'''
(ROOT / 'tests/map-sections.html').write_text(template.replace('VIEWS', ''.join(views)).replace('HASH', report['model_sha256']), encoding='utf-8')
print(json.dumps({'model_sha256': report['model_sha256'], 'views': len(views), 'fitted_centres': checks}, ensure_ascii=False, indent=2))
