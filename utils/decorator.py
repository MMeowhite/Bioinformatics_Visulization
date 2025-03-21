import functools
import matplotlib.pyplot as plt
import time
import logging
import os

def setting_chart_params(style='seaborn', dpi=300, bbox_inches='tight', show_chart=True, save_path=None):
    """
    一个用于装饰绘图函数的装饰器，可以在绘图前后执行一些通用操作。

    参数:
    style : str
        Matplotlib 的样式主题，默认为 'seaborn'
    dpi : int
        保存图像的分辨率，默认为 300
    bbox_inches : str
        保存图像时的边距设置，默认为 'tight'
    show_chart : bool
        是否显示图表，默认为 True
    save_path : str
        保存图表的路径，如果为 None 则不保存，默认为 None
    """

    def decorator(func):
        """
            一个用于计算函数执行时间的装饰器。

            :parameter
            func : 被装饰的函数。

            :return
            wrapper : 包装后的函数。
            """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 设置 Matplotlib 样式
            plt.style.use(style)

            # 调用原始的绘图函数
            result = func(*args, **kwargs)

            # 添加图例
            plt.legend()

            # 获取图表的标题、xlabel、ylabel
            title = kwargs.get('title', 'Chart')
            xlabel = kwargs.get('xlabel', 'X-axis')
            ylabel = kwargs.get('ylabel', 'Y-axis')

            # 设置图表标题和轴标签
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)

            # 保存图表
            if save_path:
                plt.savefig(save_path, dpi=dpi, bbox_inches=bbox_inches)

            # 显示图表
            if show_chart:
                plt.show()

            # 关闭图表以释放内存
            plt.close()

            return result

        return wrapper

    return decorator


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function '{func.__name__}' completed in {elapsed_time:.4f} seconds")

        return result

    return wrapper


def log(func):
    """
    log decorator to log the function execution, record the name and parametes of the executed function
    """
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('log/bioinformatics_visualization.log'),  # 日志写入文件
            logging.StreamHandler()  # 日志同时输出到控制台
        ]
    )

    logger = logging.getLogger(__name__)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 记录函数调用信息
        logger.info(f"Function '{func.__name__}' called with arguments: args={args}, kwargs={kwargs}")

        # 执行原始函数
        result = func(*args, **kwargs)

        logger.info(f"Function '{func.__name__}' execute done with return value: return={result}")

        return result

    return wrapper