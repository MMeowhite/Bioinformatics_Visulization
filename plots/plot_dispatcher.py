import importlib


def dispatch_plot(args, data, **kwargs):
    print(f"plot_type:{args.type},data:\n{data}")
    try:
        # 动态导入对应的绘图模块
        print(f"you are trying to import plots.{args.type}.plot file")
        print(f"you are trying to import plots.{args.type}.data_processing file")
        module_plot = importlib.import_module(f"plots.{args.type}.plot")
        module_data_processing = importlib.import_module(f"plots.{args.type}.data_processing")

        # 调用模块中的 plot 函数
        data, kwargs = module_data_processing.data_processing(args, data, **kwargs)
        module_plot.plot(data, **kwargs)
    except ModuleNotFoundError:
        raise ValueError(f"Unsupported plot type: {args.type}")
    except AttributeError:
        raise ValueError(f"Module plots.{args.type} does not have a plot function")