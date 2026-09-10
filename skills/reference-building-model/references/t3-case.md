# 高崎 T3 个案约束与查找入口

只在继续本项目时使用。这是用户确认历史及资源索引；图纸并非实测竣工图，数值和推断须结合当前文件重新核对，不复制成所有航站楼的模板。

## 已确认的主要语义

- 以 2024 年改造后状态为目标，GLB 用于近距离展示，包含主要室内空间。
- 1F 到达、2F 值机与出发公共空间、3F 安检及主要候机相关空间；值机岛上方不铺满 3F，2F 到达扶梯所在长条挑空与上方对应。
- 国内、国际到达下行扶梯各一组，东西向直通 1F；不能增加第三组或错误停靠 2F。国际到达必须接国际侧。
- 国内国际登机廊隔离位于 8、9 号登机口之间；不能用不存在的一整面墙切断安检后的候机长廊。
- 国际出发必须先边检、再安检、再候机；公共侧商店只向未安检一侧开口，其他侧承担隔离。
- 用户最后确认的局部商店为三角形，墙与店顶均随三角轮廓；旧斜玻璃不能留在店内穿模。
- 屋顶是一套屋面；内部支撑是三角直杆，外部梁为弧线。端面台阶水平步长大致等距，不代表高差相等。陆侧与停机坪侧低檐同高，端部与登机廊屋顶的连接及局部实心构造须按实拍。
- 机场牌子为“厦门 / XIAMEN AIRPORT”，使用用户提供图时保持比例、透明区域及支撑关系。
- 用户要求同一入口原位更新，不增加修订目录，不在界面写“最终版”和无关解释。

## 本工作区的项目索引

先在当前工作区查找 `xiamen-t3-model/`，不要假设固定绝对路径。若 skill 随项目存放在 `xiamen-t3-model/skills/reference-building-model/`，项目根目录位于 skill 上两级；独立安装后则按当前任务的项目目录定位。

- `source/model/build_revision.py`：现有模型构建入口。
- `source/model/facility-reference.png`、`diagram-trace.json`、`map-geometry.json`：结构与坐标相关输入。
- `source/model/shop_boundary.py`：三角商店、公共侧入口、国际栏杆修正。
- `source/model/check_shop_access.py`：公共区进店、禁止穿店绕过安检。
- `source/model/check_security_all_geometry.py`：安检设备出口路径。
- `source/model/check_order12.py`、`check_zone22.py`、`check_arrivals.py`：手续顺序、分区与到达净空。
- `source/build_routes.py`：依据网格生成四类路线。
- `tests/shop-boundary.cjs`、`tests/viewer.cjs`：近景与界面检查。
- `references/`、`archive/iterations/revision2/references/`：参考来源；其他历史图也保留在归档里。

这些是遗留实现，不是推荐从零架构。它们曾使用共享作用域和硬编码坐标；新项目应采用独立参数与模块。执行旧检查前确认绑定的是当前产物，不能直接相信历史报告。
