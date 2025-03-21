import importlib
from utils.decorator import log
import logging


@log
def dispatch_plot(args, data, file_extension):
    logger = logging.getLogger(__name__)
    try:
        # 动态导入对应的绘图模块
        logger.info(f"you are trying to import plots.{args.type}.plot file")
        logger.info(f"you are trying to import plots.{args.type}.data_processing file")

        module_plot = importlib.import_module(f"plots.{args.type}.plot")
        module_data_processing = importlib.import_module(f"plots.{args.type}.data_processing")

        # 调用模块中的 plot 函数
        args, data = module_data_processing.data_processing(args, data)

        module_plot.plot(args, data)
    except ModuleNotFoundError:
        raise logger.error(f"Unsupported plot type: {args.type}")