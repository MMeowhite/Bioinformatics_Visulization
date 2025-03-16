import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress


def plot(data, title='Multi Class Scatter Plot', x_label='X Axis Label',
         y_label='Y Axis Label', categories=None, sizes=100,
         category_colors=None, legend=True, legend_loc='upper right',
         legend_position=(1.05, 1), regression=False, **kwargs):

    print(f"data: {data}")
    x = np.array(data["X"])
    y = np.array(data["Y"])
    print(f"x: {x}, y: {y}")
    fig, ax = plt.subplots(figsize=(10, 8))

    if categories is None:
        colors = "blue"
        scatter = ax.scatter(x, y, c=colors, s=sizes)
    else:
        # 根据类别生成颜色
        if category_colors is None:
            unique_categories = np.unique(categories)
            category_colors = plt.cm.tab10(np.linspace(0, 1, len(unique_categories)))
            category_colors = {category: color for category, color in zip(unique_categories, category_colors)}

        colors = [category_colors[category] for category in categories]
        scatter = ax.scatter(x, y, c=colors, s=sizes)

        if legend:
            category_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=category_colors[category], markersize=10, label=category)
                                for category in np.unique(categories)]
            ax.legend(handles=category_handles, title='Categories', loc=legend_loc, bbox_to_anchor=legend_position)

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    if regression:
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        line_x = np.linspace(min(x), max(x), 100)
        line_y = slope * line_x + intercept
        ax.plot(line_x, line_y, color='gray', linestyle='--')
        equation_text = f'y = {slope:.2f}x + {intercept:.2f}'
        r_squared_text = f'R² = {r_value**2:.2f}'
        combined_text = f'{equation_text}\n{r_squared_text}'
        ax.text(1.01, 0.8, combined_text, transform=ax.transAxes, verticalalignment='top', horizontalalignment='left', color='black', fontsize=12)

    plt.savefig('scatter.png')