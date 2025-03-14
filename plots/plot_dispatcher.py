import importlib


def dispatch_plot(plot_type, data, **kwargs):
    print(f"plot_type:{plot_type}, data:{data}")
    try:
        # 动态导入对应的绘图模块
        module = importlib.import_module(f"plots.{plot_type}.plot")
        # 调用模块中的 plot 函数
        module.plot(data, **kwargs)
    except ModuleNotFoundError:
        raise ValueError(f"Unsupported plot type: {plot_type}")
    except AttributeError:
        raise ValueError(f"Module plot.{plot_type} does not have a plot function")
