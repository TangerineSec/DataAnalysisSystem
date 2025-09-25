from pyecharts import options as opts
from pyecharts.charts import Radar
from pyecharts.globals import CurrentConfig
# CurrentConfig.ONLINE_HOST = "https://cdn.jsdelivr.net/npm/echarts@5.2.2/dist/"
from pyecharts.globals import ThemeType
import pandas as pd

def dimension_radar_chart(file, sheet1, theme):
    try:
        # 读取表格数据
        df = pd.read_excel(file, sheet_name=sheet1, header=0)
        # 将第一列保存成字典形式，保存在一个列表里
        dict_list = [{"name": row[df.columns[0]], "max": 10, "min": 0} for _, row in df.iterrows()]
        # 将第二列和第三列保存成一个列表
        list_data1 = [row[df.columns[1]] for _, row in df.iterrows()]
        list_data2 = [row[df.columns[2]] for _, row in df.iterrows()]
        # 获取第一行的标题
        title = df.loc[0, "标题"]
        legend_1 = df.loc[0, "图例名字1"]
        legend_2 = df.loc[0, "图例名字2"]

        value_bj = [list_data1]
        value_sh = [list_data2]
        c_schema = dict_list
        color=[
            "#f9713c",
            "#008000",
            "#FF007F",  # 热情的粉红色
            "#FFA500",  # 鲜艳的橙色
            "#FFFF00",  # 鲜艳的黄色
            "#7CFC00",  # 草绿色
            "#00BFFF",  # 湛蓝色
            "#8B00FF",  # 紫罗兰色
            "#800000",  # 酒红色
            "#00FFFF",  # 青色
            "#FF0000",  # 纯红色
            "#00FF00",  # 鲜艳的绿色
            "#FF1493",  # 亮粉红色
            "#FF8C00",  # 暗橙色
            "#FFFFE0",  # 浅黄色
            "#ADFF2F",  # 黄绿色
            "#1E90FF",  # 闪蓝色
            "#9932CC",  # 暗紫色
            "#B22222",  # 砖红色
            "#7FFFD4",  # 水绿色
            "#FF4500",  # 橙红色
            "#228B22",  # 森林绿色
            "#9400D3",  # 深紫色
            "#DC143C",  # 猩红色
            "#00FA9A",  # 中海蓝色
            "#FF69B4",  # 热情的粉红色 II
            "#FFD700",  # 金色
            "#98FB98",  # 淡绿色
            "#8A2BE2",  # 紫罗兰色 II
            "#FA8072",  # 淡珊瑚色
            "#32CD32",  # 酸橙色
            "#9932CC",  # 深兰花紫
            "#556B2F",  # 暗橄榄色
            "#FFC0CB",  # 粉红色
            "#20B2AA",  # 浅海蓝色
            "#BA55D3",  # 中紫色
            "#FF6347",  # 番茄色
            "#4169E1",  # 皇家蓝色
            "#483D8B",  # 暗紫色 II
            "#FF69B4",  # 亮粉红色 II
            "#FFD700",  # 金色 II
            "#98FB98",  # 苍绿色
            "#8A2BE2",  # 紫罗兰色 III
            "#FA8072",  # 珊瑚色
            "#32CD32",  # 明亮的绿色
            "#9932CC",  # 深兰花紫 II
            "#556B2F",  # 深橄榄绿色
            "#FFC0CB",  # 浅粉红色
            "#20B2AA",  # 海蓝宝石色
            "#BA55D3",  # 深紫罗兰色
            "#FF6347",  # 番茄红
            "#4169E1",  # 宝蓝色
            "#483D8B",  # 暗紫色 III
            "#FF69B4",  # 热情的粉红色 III
            "#FFD700",  # 金色 III
            "#98FB98",  # 淡绿色 II
            "#8A2BE2",  # 紫罗兰色 IV
            "#FA8072",  # 珊瑚色 II
            "#32CD32",  # 酸橙绿色
        ]
        radar = (
            Radar(init_opts=opts.InitOpts(
                theme=theme,
                page_title="Dimension radar chart",
                renderer="svg",  # 设置无失真渲染方式
                                        )
            )
            .add_schema(schema=c_schema, shape="polygon", textstyle_opts=opts.TextStyleOpts(font_size=20, color="#201e2f"),
                        angleaxis_opts=opts.AngleAxisOpts(),
                        radiusaxis_opts=opts.RadiusAxisOpts(min_=0, max_=10, interval=1, ),
                        polar_opts=opts.PolarOpts(),
                        splitarea_opt=opts.SplitAreaOpts(is_show=False),
                        splitline_opt=opts.SplitLineOpts(is_show=False),
                        )
            .add(legend_1, value_bj, color=color[0], linestyle_opts=opts.LineStyleOpts(width=3))
            .add(legend_2, value_sh, color=color[1], linestyle_opts=opts.LineStyleOpts(type_="dashed", width=3))
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False, font_size=18),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title=title, pos_left="30%"),
                legend_opts=opts.LegendOpts(pos_left="52%", orient="horizontal",
                                            textstyle_opts=opts.TextStyleOpts(font_size=18)),
            )
        )

        # 生成文件html
        path = str("各项维度比例图.html")
        radar.render(path=path)  # 自动生成的文件
        with open(path, 'r') as rf:
            return rf.read()
    except:
        # 读取表格数据
        df = pd.read_excel(file, sheet_name=sheet1, header=0)
        # 将第一列保存成字典形式，保存在一个列表里
        dict_list = [{"name": row[df.columns[0]], "max": 10, "min": 0} for _, row in df.iterrows()]
        # 将第二列和第三列保存成一个列表
        list_data1 = [row[df.columns[1]] for _, row in df.iterrows()]
        list_data2 = [row[df.columns[2]] for _, row in df.iterrows()]
        # 获取第一行的标题
        title = df.loc[0, "标题"]
        legend_1 = df.loc[0, "图例名字1"]
        legend_2 = df.loc[0, "图例名字2"]

        value_bj = [[4, 7, 5, 3, 4, 6, 5, 3]]
        value_sh = [[7, 8, 7, 7, 7, 7, 7, 6]]
        c_schema = dict_list
        color = [
            "#f9713c",
            "#008000",
            "#FF007F",  # 热情的粉红色
            "#FFA500",  # 鲜艳的橙色
            "#FFFF00",  # 鲜艳的黄色
            "#7CFC00",  # 草绿色
            "#00BFFF",  # 湛蓝色
            "#8B00FF",  # 紫罗兰色
            "#800000",  # 酒红色
            "#00FFFF",  # 青色
            "#FF0000",  # 纯红色
            "#00FF00",  # 鲜艳的绿色
            "#FF1493",  # 亮粉红色
            "#FF8C00",  # 暗橙色
            "#FFFFE0",  # 浅黄色
            "#ADFF2F",  # 黄绿色
            "#1E90FF",  # 闪蓝色
            "#9932CC",  # 暗紫色
            "#B22222",  # 砖红色
            "#7FFFD4",  # 水绿色
            "#FF4500",  # 橙红色
            "#228B22",  # 森林绿色
            "#9400D3",  # 深紫色
            "#DC143C",  # 猩红色
            "#00FA9A",  # 中海蓝色
            "#FF69B4",  # 热情的粉红色 II
            "#FFD700",  # 金色
            "#98FB98",  # 淡绿色
            "#8A2BE2",  # 紫罗兰色 II
            "#FA8072",  # 淡珊瑚色
            "#32CD32",  # 酸橙色
            "#9932CC",  # 深兰花紫
            "#556B2F",  # 暗橄榄色
            "#FFC0CB",  # 粉红色
            "#20B2AA",  # 浅海蓝色
            "#BA55D3",  # 中紫色
            "#FF6347",  # 番茄色
            "#4169E1",  # 皇家蓝色
            "#483D8B",  # 暗紫色 II
            "#FF69B4",  # 亮粉红色 II
            "#FFD700",  # 金色 II
            "#98FB98",  # 苍绿色
            "#8A2BE2",  # 紫罗兰色 III
            "#FA8072",  # 珊瑚色
            "#32CD32",  # 明亮的绿色
            "#9932CC",  # 深兰花紫 II
            "#556B2F",  # 深橄榄绿色
            "#FFC0CB",  # 浅粉红色
            "#20B2AA",  # 海蓝宝石色
            "#BA55D3",  # 深紫罗兰色
            "#FF6347",  # 番茄红
            "#4169E1",  # 宝蓝色
            "#483D8B",  # 暗紫色 III
            "#FF69B4",  # 热情的粉红色 III
            "#FFD700",  # 金色 III
            "#98FB98",  # 淡绿色 II
            "#8A2BE2",  # 紫罗兰色 IV
            "#FA8072",  # 珊瑚色 II
            "#32CD32",  # 酸橙绿色
        ]
        radar = (
            Radar(init_opts=opts.InitOpts(
                theme=theme,
                page_title="Dimension radar chart",
            )
            )
            .add_schema(schema=c_schema, shape="polygon",
                        textstyle_opts=opts.TextStyleOpts(font_size=20, color="#201e2f"),
                        angleaxis_opts=opts.AngleAxisOpts(),
                        radiusaxis_opts=opts.RadiusAxisOpts(min_=0, max_=10, interval=1, ),
                        polar_opts=opts.PolarOpts(),
                        splitarea_opt=opts.SplitAreaOpts(is_show=False),
                        splitline_opt=opts.SplitLineOpts(is_show=False),
                        )
            .add(legend_1, value_bj, color=color[0], linestyle_opts=opts.LineStyleOpts(width=3))
            .add(legend_2, value_sh, color=color[1], linestyle_opts=opts.LineStyleOpts(type_="dashed", width=3))
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False, font_size=18),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="默认维度雷达图", pos_left="30%"),
                legend_opts=opts.LegendOpts(pos_left="52%", orient="horizontal",
                                            textstyle_opts=opts.TextStyleOpts(font_size=18)),
            )
        )

        # 生成文件html
        path = "文件生成//"+str("默认维度比例图.html")
        radar.render(path=path)  # 自动生成的文件
        with open(path, 'r') as rf:
            return rf.read()
