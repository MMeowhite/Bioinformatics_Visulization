from utils.load import *
from plots.plot_dispatcher import dispatch_plot


def main():
    # 解析参数
    args = parse_args()
    print(f"args:{args}")

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
        # 如果没有指定输出目录，切换到当前目录
        os.chdir(".")
        print("No output directory specified.")

    print(f"loading data from {args.file}")
    data = load_data_from_file(args.file)

    # 准备可选参数
    kwargs = {}
    if args.color:
        kwargs["color"] = args.color
    if args.linestyle:
        kwargs["linestyle"] = args.linestyle
    if args.marker:
        kwargs["marker"] = args.marker
    if args.bins:
        kwargs["bins"] = args.bins
    if args.preview:
        kwargs["preview"] = args.preview
    if args.regression:
        kwargs["regression"] = args.regression
    if args.annotate:
        kwargs["annotate"] = args.annotate


    try:
        dispatch_plot(args, data, **kwargs)
    except ValueError as e:
        print(e)
        sys.exit(1)


# 执行入口函数
if __name__ == '__main__':
    main()