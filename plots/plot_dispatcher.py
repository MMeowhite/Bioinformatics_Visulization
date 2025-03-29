import importlib
import logging
from utils.decorator import log


@log
def dispatch_plot(args, data, file_extension):
    logger = logging.getLogger(__name__)
    try:
        # 动态导入对应的绘图模块
        if args.type in ["bar", "box", "heatmap", "histogram", "line", "network", "pie", "scatter", "volcano"]:
            logger.info(f"you are trying to import plots.{args.type}.plot file")
            logger.info(f"you are trying to import plots.{args.type}.data_processing file")
            module_plot = importlib.import_module(f"plots.{args.type}.plot")
            module_data_processing = importlib.import_module(f"plots.{args.type}.data_processing")
        else:
            logger.info(f"you are trying to import plots.complex.{args.type}.plot file")
            logger.info(f"you are trying to import plots.complex.{args.type}.data_processing file")
            module_plot = importlib.import_module(f"plots.complex.{args.type}.plot")
            module_data_processing = importlib.import_module(f"plots.complex.{args.type}.data_processing")

        # 调用module_data_processing模块中的 data_processing 函数
        args, data = module_data_processing.data_processing(args, data)

        # 调用module_plot的 plot 函数
        module_plot.plot(args, data)
    except ModuleNotFoundError as e:
        logger.error(f"Unsupported plot type: {args.type}")
        logger.error(f"Error: {str(e)}")
        print(f"Error: {str(e)}")