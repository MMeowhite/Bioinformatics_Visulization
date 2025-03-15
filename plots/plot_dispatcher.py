import importlib


def dispatch_plot(args, data, **kwargs):
    print(f"plot_type:{args.type}, data:{data}")
    try:
        # 动态导入对应的绘图模块
        print(f"you are trying to import plots.{args.type}.plot file")
        module = importlib.import_module(f"plots.{args.type}.plot")
        # 调用模块中的 plot 函数
        module.plot(args, data, **kwargs)
    except ModuleNotFoundError:
        raise ValueError(f"Unsupported plot type: {args.type}")
    except AttributeError:
        raise ValueError(f"Module plots.{args.type} does not have a plot function")
