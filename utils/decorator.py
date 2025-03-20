import functools
import matplotlib.pyplot as plt
import time
import logging


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
    一个用于记录函数调用信息的日志装饰器。

    功能:
    - 记录函数的名称
    - 记录函数的参数
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

        return result

    return wrapper


def kwargs_dict(param_map):
    """
    一个用于动态扩展参数映射表并准备可选参数的装饰器。

    参数:
    param_map : 参数映射表，字典类型，键为命令行参数名，值为kwargs字典中的键名

    返回:
    decorator : 装饰器函数
    """
    param_map = {
        'color': 'color',
        'linestyle': 'linestyle',
        'marker': 'marker',
        'bins': 'bins',
        'preview': 'preview',
        'regression': 'regression',
        'annotate': 'annotate'
    }

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 假设args的第一个参数是解析后的命令行参数对象
            args_obj = args[0] if args else None

            # 准备可选参数
            kwargs_dict = {}
            for arg_name, kwarg_name in param_map.items():
                value = getattr(args_obj, arg_name, None)
                if value is not None:
                    kwargs_dict[kwarg_name] = value
                else:
                    kwargs_dict[kwarg_name] = None

            # 将准备好的kwargs字典传递给原始函数
            result = func(*args, **kwargs_dict)

            return result

        return wrapper

    return decorator
