import plotly.graph_objects as go
import numpy as np
import matplotlib.cm as cm

# 示例数据
nodes = [
    {"name": "A"},
    {"name": "B"},
    {"name": "C"},
    {"name": "D"},
    {"name": "E"}
]

links = [
    {"source": 0, "target": 1, "value": 5},
    {"source": 0, "target": 2, "value": 3},
    {"source": 1, "target": 3, "value": 4},
    {"source": 2, "target": 3, "value": 2},
    {"source": 2, "target": 4, "value": 5},
    {"source": 3, "target": 4, "value": 3}
]

# 生成彩虹色
num_links = len(links)
colors = cm.rainbow(np.linspace(0, 1, num_links))

# 创建桑基图
fig = go.Figure(data=[
    go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=[node["name"] for node in nodes],
            color="black"
        ),
        link=dict(
            source=[link["source"] for link in links],
            target=[link["target"] for link in links],
            value=[link["value"] for link in links],
            color=[f'rgb({int(color[0]*255)}, {int(color[1]*255)}, {int(color[2]*255)})' for color in colors]
        )
    )
])

# 设置图表布局
fig.update_layout(
    title_text="彩虹色桑基图示例",
    font_size=12,
    width=800,
    height=600
)

# 显示图表
fig.show()

# 保存图表
fig.write_image("rainbow_sankey.png", dpi=300)