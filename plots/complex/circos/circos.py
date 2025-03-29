from circos import Circos
import numpy as np
import pandas as pd
from scanpy.plotting import scatter

# 设置随机种子以确保结果可重复
np.random.seed(123)

# 生成PPI数据
num_proteins = 20  # 蛋白数量
proteins = [f"Protein_{i+1}" for i in range(num_proteins)]

# 生成相互作用数据
num_interactions = 50  # 相互作用数量
interactions = []
for _ in range(num_interactions):
    prot1, prot2 = np.random.choice(proteins, 2, replace=False)
    interactions.append((prot1, prot2))

# 转换为DataFrame
interactions_df = pd.DataFrame(interactions, columns=["Protein1", "Protein2"])

# 初始化Circos图
circos = Circos(
    figure_kwargs={'figsize': (10, 10)},
    start=0,
    end=num_proteins,
    padding=2,
    labels=True,
    ticks=False
)

# 添加蛋白质扇区
for i, protein in enumerate(proteins):
    circos.add_sector(
        start=i,
        end=i + 1,
        label=protein,
        label_position='start',
        label_orientation='horizontal',
        label_size=10,
        label_color='black',
        label_weight='bold'
    )

# 添加相互作用连接
for _, interaction in interactions_df.iterrows():
    prot1_idx = proteins.index(interaction['Protein1'])
    prot2_idx = proteins.index(interaction['Protein2'])
    circos.add_link(
        start1=prot1_idx,
        end1=prot1_idx + 1,
        start2=prot2_idx,
        end2=prot2_idx + 1,
        color='skyblue',
        alpha=0.5,
        lw=0.5
    )

# 绘制Circos图
circos.plot()
plt.show()