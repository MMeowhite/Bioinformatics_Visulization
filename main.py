from utils.load import *
from utils.decorator import timer, log
from plots.plot_dispatcher import dispatch_plot


@log
@timer
def main():
    # 解析参数
    args = parse_args()
    print(f"args: {args}")

    # 设置输出目录
    if args.output is not None:
        # 如果指定了输出目录
        if os.path.exists(args.output):
            # 如果目录存在，切换到该目录
            os.chdir(args.output)
        else:
            # 如果目录不存在，创建目录并切换到该目录
            os.makedirs(args.output, exist_ok=True)
            os.chdir(args.output)
    else:
        # 如果没有指定输出目录，切换到output目录
        print("No output directory specified.")

    print(f"loading data from {args.file}")
    data, file_extension = load_data_from_file(args.file)

    try:
        dispatch_plot(args, data, file_extension)
    except Exception as e:
        print(e)
        sys.exit(1)


# 执行入口函数
if __name__ == '__main__':
    main()