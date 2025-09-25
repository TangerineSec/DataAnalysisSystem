import time
import pandas as pd
from pyecharts.render import make_snapshot
from snapshot_pyppeteer import snapshot
from pyecharts.globals import CurrentConfig
from pyecharts.charts import *
from pyecharts.charts import Line
# CurrentConfig.ONLINE_HOST = "https://cdn.kesci.com/lib/pyecharts_assets/"
from pyecharts import options as opts
from pyecharts.globals import ThemeType

# 指信专业
# 大数据专业
# 网络专业
# 信安专业
# 注意要更换的sheet1 2 3 4 5的名字
"""指信 前期 中期 后期数据"""


def generator_html_from_excel(file1, file2, file3, sheet1, sheet2, sheet3, theme):
    if(sheet1=="Sheet1" and sheet2=="Sheet1" and sheet3=="Sheet1"):
        print(theme)
        data_early_conductor = pd.read_excel(file1,
                                             sheet_name=sheet1, header=2)  # header=2表示索引为第3行
        data_middle_conductor = pd.read_excel(file2,
                                              sheet_name=sheet2, header=2)  # header=2表示索引为第3行
        data_later_conductor = pd.read_excel(file3,
                                             sheet_name=sheet3, header=2)  # header=2表示索引为第3行
        data_later_conductor.head()
        # 取出总分和姓名，去掉中文项。计算平均值，最大值，最小值，实际值
        # 首先删除缺考部分，设置值为0。然后获取名字和分数
        data_early_conductor = data_early_conductor.replace('缺考', 0)
        data_middle_conductor = data_middle_conductor.replace('缺考', 0)
        data_later_conductor = data_later_conductor.replace('缺考', 0)

        # 删除所有三个 DataFrame 中总分为 0 的行，这实际上就是删除那些缺考或未提交作业的学生。
        data_early_conductor = data_early_conductor[data_early_conductor['总分(1725.0)'] != 0]
        data_middle_conductor = data_middle_conductor[data_middle_conductor['总分(1725.0)'] != 0]
        data_later_conductor = data_later_conductor[data_later_conductor['总分(1675.0)'] != 0]

        # name=data_early_conductor.iloc[0:-1,2:3] # 第3列
        # score=data_early_conductor.iloc[0:-1,4:5] # 第5列
        data_middle_conductor.head(3)

        name = data_early_conductor['姓名/昵称'].tolist()
        score_early_conductor = data_early_conductor['总分(1725.0)'].tolist()
        score_middle_conductor = data_middle_conductor[
            '总分(1725.0)'].tolist()  # 在输入的第二个文件中检查有这一列吗？有的文件可能为总分(1725.0)或'总分(1725.0)
        score_later_conductor = data_later_conductor['总分(1675.0)'].tolist()

        def avg_score(t):
            a = sum(t) / len(t)
            return a

        avg_early_conductor = avg_score(score_early_conductor)
        avg_middle_conductor = avg_score(score_middle_conductor)
        avg_later_conductor = avg_score(score_later_conductor)

        max_early_conductor = max(score_early_conductor)
        max_middle_conductor = max(score_middle_conductor)
        max_later_conductor = max(score_later_conductor)
        # print(avg_early_conductor, avg_middle_conductor, avg_later_conductor, max_early_conductor, max_middle_conductor, max_later_conductor)
        # ThemeType.WHITE
        line = (Line(init_opts=opts.InitOpts(
            width="100%",  # 修改默认宽度
            height="700px",  # 修改默认高度
            theme=theme,
            page_title="Line chart page",
            renderer="svg",  # 设置无失真渲染方式
        ))
                .add_xaxis(name)  # LineStyleOpts中设置合适的颜色宽度。
                .add_yaxis("22年11月15日测试", score_early_conductor, symbol="circle", is_symbol_show=True,
                           linestyle_opts=opts.LineStyleOpts(width=3, color="#0000FF"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#0000FF"))
                .add_yaxis("22年11月15日平均", [int(avg_early_conductor)] * len(name), is_symbol_show=False,
                           linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#0000FF"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#0000FF"))
                .add_yaxis("22年11月15日最好", [int(max_early_conductor)] * len(name), is_symbol_show=False,
                           linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#0000FF"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#0000FF"))
                .add_yaxis("23年01月26日测试", score_middle_conductor, symbol="circle", is_symbol_show=True,
                           linestyle_opts=opts.LineStyleOpts(width=3, color="#008000"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#008000"))
                .add_yaxis("23年01月26日平均", [int(avg_middle_conductor)] * len(name), is_symbol_show=False,
                           linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#008000"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#008000"))
                .add_yaxis("23年01月26日最好", [int(max_middle_conductor)] * len(name), is_symbol_show=False,
                           linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#008000"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#008000"))
                .add_yaxis("23年04月11日测试", score_later_conductor, symbol="circle", is_symbol_show=True,
                           linestyle_opts=opts.LineStyleOpts(width=3, color="#FFAC00"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#FFAC00"))
                .add_yaxis("23年04月11日平均", [int(avg_later_conductor)] * len(name), is_symbol_show=False,
                           linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#FFAC00"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#FFAC00"))
                .add_yaxis("23年04月11日最好", [int(max_later_conductor)] * len(name), is_symbol_show=False,
                           linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#FFAC00"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#FFAC00"))

                )  # 以列表数据格式输入pyecharts，形成坐标图。
        line.set_global_opts(
            title_opts=opts.TitleOpts(title="21级指信PTA作业成绩", title_link="https://bing.com", pos_left='center',
                                      # 标题位置：pos_left='center'
                                      subtitle="", subtitle_link="https://baidu.com"),
            toolbox_opts=opts.ToolboxOpts(pos_left='left'),  # 工具箱位置 pos_left='left'
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(font_size=18, rotate=60),  # 设置字体大小为 16,合并设置倾斜度
                interval=0,
            ),  # 控制X轴
            yaxis_opts=opts.AxisOpts(
                min_='dataMin',
                axislabel_opts=opts.LabelOpts(font_size=20),  # y轴数据项字体调整
            ),  # 控制y轴
            # 全局图例设置
            legend_opts=opts.LegendOpts(
                pos_right="right", orient="vertical",  # 自定义图例位置为竖向右侧
                textstyle_opts=opts.TextStyleOpts(color="#696969", font_size=18),
            ),
        )
        f = "文件生成//"+str(int(time.time()))+'折线图生成.html'
        line.render(path=f)
        with open(f, 'r') as rf:
            return rf.read()

    elif sheet1 == "Sheet2" and sheet2 == "Sheet2" and sheet3 == "Sheet2":
            """指信 前期 中期 后期数据"""
            data_early_BigData = pd.read_excel(file1,
                                               sheet_name=sheet1, header=2)  # header=2表示索引为第3行
            data_middle_BigData = pd.read_excel(file2,
                                                sheet_name=sheet2, header=2)  # header=2表示索引为第3行
            data_later_BigData = pd.read_excel(file3,
                                               sheet_name=sheet3, header=2)  # header=2表示索引为第3行
            data_later_BigData.head()
            # 取出总分和姓名，去掉中文项。计算平均值，最大值，最小值，实际值
            # 首先删除缺考部分，设置值为0。然后获取名字和分数
            data_early_BigData = data_early_BigData.replace('缺考', 0)
            data_middle_BigData = data_middle_BigData.replace('缺考', 0)
            data_later_BigData = data_later_BigData.replace('缺考', 0)

            # 删除所有三个 DataFrame 中总分为 0 的行，这实际上就是删除那些缺考或未提交作业的学生。
            data_early_BigData = data_early_BigData[data_early_BigData['总分(1725.0)'] != 0]
            data_middle_BigData = data_middle_BigData[data_middle_BigData['总分(1725.0)'] != 0]
            data_later_BigData = data_later_BigData[data_later_BigData['总分(1675.0)'] != 0]

            # name=data_early_BigData.iloc[0:-1,2:3] # 第3列
            # score=data_early_BigData.iloc[0:-1,4:5] # 第5列
            data_middle_BigData.head(3)
            from pyecharts.globals import CurrentConfig
            CurrentConfig.ONLINE_HOST = "https://cdn.kesci.com/lib/pyecharts_assets/"
            name = data_early_BigData['姓名/昵称'].tolist()
            score_early_BigData = data_early_BigData['总分(1725.0)'].tolist()
            score_middle_BigData = data_middle_BigData['总分(1725.0)'].tolist()
            score_later_BigData = data_later_BigData['总分(1675.0)'].tolist()

            print(score_early_BigData, score_middle_BigData, score_later_BigData)

            def avg_score(t):
                a = sum(t) / len(t)
                return a

            avg_early_BigData = avg_score(score_early_BigData)
            avg_middle_BigData = avg_score(score_middle_BigData)
            avg_later_BigData = avg_score(score_later_BigData)

            max_early_BigData = max(score_early_BigData)
            max_middle_BigData = max(score_middle_BigData)
            max_later_BigData = max(score_later_BigData)
            print(avg_early_BigData, avg_middle_BigData, avg_later_BigData, max_early_BigData, max_middle_BigData,
                  max_later_BigData)
            line = (Line(init_opts=opts.InitOpts(width="1500px",  # 修改默认宽度
                                                 height="700px",  # 修改默认高度
                                                 theme=theme,
                                                 renderer="svg",  # 设置无失真渲染方式
                                                 ))
                    .add_xaxis(name)  # LineStyleOpts中设置合适的颜色宽度。
                    .add_yaxis('2022年11月15日测试', score_early_BigData, symbol="circle", is_symbol_show=True,
                               linestyle_opts=opts.LineStyleOpts(width=3, color="#0000FF"),
                               itemstyle_opts=opts.ItemStyleOpts(color="#0000FF"))
                    .add_yaxis("2022年11月15日平均", [int(avg_early_BigData)] * len(name), is_symbol_show=False,
                               linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#0000FF"),
                               itemstyle_opts=opts.ItemStyleOpts(color="#0000FF"))
                    .add_yaxis("2022年11月15日最好", [int(max_early_BigData)] * len(name), is_symbol_show=False,
                               linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#0000FF"),
                               itemstyle_opts=opts.ItemStyleOpts(color="#0000FF"))
                    .add_yaxis('2023年01月26日测试', score_middle_BigData, symbol="circle", is_symbol_show=True,
                               linestyle_opts=opts.LineStyleOpts(width=3, color="#008000"),
                               itemstyle_opts=opts.ItemStyleOpts(color="#008000"))
                    .add_yaxis("2023年01月26日平均", [int(avg_middle_BigData)] * len(name), is_symbol_show=False,
                               linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#008000"),
                               itemstyle_opts=opts.ItemStyleOpts(color="#008000"))
                    .add_yaxis("2023年01月26日最好", [int(max_middle_BigData)] * len(name), is_symbol_show=False,
                               linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#008000"),
                               itemstyle_opts=opts.ItemStyleOpts(color="#008000"))
                    .add_yaxis("2023年02月22日测试", score_later_BigData, symbol="circle", is_symbol_show=True,
                               linestyle_opts=opts.LineStyleOpts(width=3, color="#FFAC00"),
                               itemstyle_opts=opts.ItemStyleOpts(color="#FFAC00"))
                    .add_yaxis("2023年02月22日平均", [int(avg_later_BigData)] * len(name), is_symbol_show=False,
                               linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#FFAC00"),
                               itemstyle_opts=opts.ItemStyleOpts(color="#FFAC00"))
                    .add_yaxis("2023年02月22日最好", [int(max_later_BigData)] * len(name), is_symbol_show=False,
                               linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#FFAC00"),
                               itemstyle_opts=opts.ItemStyleOpts(color="#FFAC00"))

                    )  # 以列表数据格式输入pyecharts，形成坐标图。
            line.set_global_opts(
                title_opts=opts.TitleOpts(title="21级大数据PTA作业成绩", title_link="https://bing.com",
                                          pos_left='center',  # 标题位置：pos_left='center'
                                          subtitle="", subtitle_link="https://baidu.com"),
                toolbox_opts=opts.ToolboxOpts(pos_left='left'),  # 工具箱位置 pos_left='left'
                xaxis_opts=opts.AxisOpts(
                    interval=0,
                    axislabel_opts={"rotate": 45},
                ),  # 控制X轴
                # 全局图例设置
                legend_opts=opts.LegendOpts(
                    pos_right="right", orient="vertical",  # 自定义图例位置为竖向右侧
                    textstyle_opts=opts.TextStyleOpts(color="#696969", font_size=16),
                ),
            )
            print("正在生成图片和pdf文件：")
            # make_snapshot(snapshot, line.render(), "21级大数据PTA成绩趋势图.png", notebook=True)
            # make_snapshot(snapshot, line.render(), "21级大数据PTA成绩趋势图.pdf", notebook=True)
            # make_snapshot(snapshot, line.render(), "21级大数据PTA成绩趋势图.jpeg", notebook=True)
            # make_snapshot(snapshot, line.render(), "21级大数据PTA成绩趋势图.gif", notebook=True)
            f = "文件生成//"+str(int(time.time())) + '折线图生成.html'
            line.render(path=f)
            with open(f, 'r') as rf:
                return rf.read()
    elif(sheet1 == "Sheet3" and sheet2 == "Sheet3" and sheet3 == "Sheet3"):
        """指信 前期 中期 后期数据"""
        data_early_Internet = pd.read_excel(file1,
                                            sheet_name=sheet1, header=2)  # header=2表示索引为第3行
        data_middle_Internet = pd.read_excel(file2,
                                             sheet_name=sheet2, header=2)  # header=2表示索引为第3行
        data_later_Internet = pd.read_excel(file3,
                                            sheet_name=sheet3, header=2)  # header=2表示索引为第3行
        data_later_Internet.head()
        # 取出总分和姓名，去掉中文项。计算平均值，最大值，最小值，实际值
        # 首先删除缺考部分，设置值为0。然后获取名字和分数
        data_early_Internet = data_early_Internet.replace('缺考', 0)
        data_middle_Internet = data_middle_Internet.replace('缺考', 0)
        data_later_Internet = data_later_Internet.replace('缺考', 0)

        # 删除所有三个 DataFrame 中总分为 0 的行，这实际上就是删除那些缺考或未提交作业的学生。
        data_early_Internet = data_early_Internet[data_early_Internet['总分(1725.0)'] != 0]
        data_middle_Internet = data_middle_Internet[data_middle_Internet['总分(1725.0)'] != 0]
        data_later_Internet = data_later_Internet[data_later_Internet['总分(1675.0)'] != 0]

        name = data_early_Internet['姓名/昵称'].tolist()
        score_early_Internet = data_early_Internet['总分(1725.0)'].tolist()
        score_middle_Internet = data_middle_Internet['总分(1725.0)'].tolist()
        score_later_Internet = data_later_Internet['总分(1675.0)'].tolist()

        print(score_early_Internet, score_middle_Internet, score_later_Internet)

        def avg_score(t):
            a = sum(t) / len(t)
            return a

        avg_early_Internet = avg_score(score_early_Internet)
        avg_middle_Internet = avg_score(score_middle_Internet)
        avg_later_Internet = avg_score(score_later_Internet)

        max_early_Internet = max(score_early_Internet)
        max_middle_Internet = max(score_middle_Internet)
        max_later_Internet = max(score_later_Internet)
        print(avg_early_Internet, avg_middle_Internet, avg_later_Internet, max_early_Internet, max_middle_Internet,
              max_later_Internet)
        line = (Line(init_opts=opts.InitOpts(width="1500px",  # 修改默认宽度
                                             height="700px",  # 修改默认高度
                                             theme=theme,
                                             renderer="svg",  # 设置无失真渲染方式
                                             ))
                .add_xaxis(name)  # LineStyleOpts中设置合适的颜色宽度。
                .add_yaxis('2022年11月15日测试', score_early_Internet, symbol="circle", is_symbol_show=True,
                           linestyle_opts=opts.LineStyleOpts(width=3, color="#0000FF"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#0000FF"))
                .add_yaxis("2022年11月15日平均", [int(avg_early_Internet)] * len(name), is_symbol_show=False,
                           linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#0000FF"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#0000FF"))
                .add_yaxis("2022年11月15日最好", [int(max_early_Internet)] * len(name), is_symbol_show=False,
                           linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#0000FF"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#0000FF"))
                .add_yaxis('2023年01月26日测试', score_middle_Internet, symbol="circle", is_symbol_show=True,
                           linestyle_opts=opts.LineStyleOpts(width=3, color="#008000"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#008000"))
                .add_yaxis("2023年01月26日平均", [int(avg_middle_Internet)] * len(name), is_symbol_show=False,
                           linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#008000"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#008000"))
                .add_yaxis("2023年01月26日最好", [int(max_middle_Internet)] * len(name), is_symbol_show=False,
                           linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#008000"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#008000"))
                .add_yaxis("2023年02月22日测试", score_later_Internet, symbol="circle", is_symbol_show=True,
                           linestyle_opts=opts.LineStyleOpts(width=3, color="#FFAC00"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#FFAC00"))
                .add_yaxis("2023年02月22日平均", [int(avg_later_Internet)] * len(name), is_symbol_show=False,
                           linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#FFAC00"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#FFAC00"))
                .add_yaxis("2023年02月22日最好", [int(max_later_Internet)] * len(name), is_symbol_show=False,
                           linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#FFAC00"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#FFAC00"))

                )  # 以列表数据格式输入pyecharts，形成坐标图。
        line.set_global_opts(
            title_opts=opts.TitleOpts(title="21级网络PTA作业成绩", title_link="https://bing.com", pos_left='center',
                                      # 标题位置：pos_left='center'
                                      subtitle="", subtitle_link="https://baidu.com"),
            toolbox_opts=opts.ToolboxOpts(pos_left='left'),  # 工具箱位置 pos_left='left'
            xaxis_opts=opts.AxisOpts(
                interval=0,
                axislabel_opts={"rotate": 45},
            ),  # 控制X轴
            # 全局图例设置
            legend_opts=opts.LegendOpts(
                pos_right="right", orient="vertical",  # 自定义图例位置为竖向右侧
                textstyle_opts=opts.TextStyleOpts(color="#696969", font_size=16),
            ),
        )
        line.render(path="21级_网络_PTA成绩趋势图.html", )
        from snapshot_pyppeteer import snapshot
        from pyecharts.faker import Faker
        from pyecharts.render import make_snapshot
        print("正在生成图片和pdf文件：")
        # make_snapshot(snapshot, line.render(), "21级大数据PTA成绩趋势图.png", notebook=True)
        # make_snapshot(snapshot, line.render(), "21级大数据PTA成绩趋势图.pdf", notebook=True)
        # make_snapshot(snapshot, line.render(), "21级大数据PTA成绩趋势图.jpeg", notebook=True)
        # make_snapshot(snapshot, line.render(), "21级大数据PTA成绩趋势图.gif", notebook=True)
        f = str(int(time.time())) + '折线图生成.html'
        line.render(path=f)
        with open(f, 'r') as rf:
            return rf.read()
    elif(sheet1 == "Sheet4" & sheet2 == "Sheet4" & sheet3 == "Sheet4"):
        """指信 前期 中期 后期数据"""
        data_early_Security = pd.read_excel(file1,
                                            sheet_name=sheet1, header=2)  # header=2表示索引为第3行
        data_middle_Security = pd.read_excel(file2,
                                             sheet_name=sheet2, header=2)  # header=2表示索引为第3行
        data_later_Security = pd.read_excel(file3,
                                            sheet_name=sheet3, header=2)  # header=2表示索引为第3行
        data_later_Security.head()
        # 取出总分和姓名，去掉中文项。计算平均值，最大值，最小值，实际值
        # 首先删除缺考部分，设置值为0。然后获取名字和分数
        data_early_Security = data_early_Security.replace('缺考', 0)
        data_middle_Security = data_middle_Security.replace('缺考', 0)
        data_later_Security = data_later_Security.replace('缺考', 0)

        # 删除所有三个 DataFrame 中总分为 0 的行，这实际上就是删除那些缺考或未提交作业的学生。
        data_early_conductor = data_early_Security[data_early_Security['总分(1720.0)'] != 0]
        data_middle_conductor = data_early_Security[data_early_Security['总分(1725.0)'] != 0]
        data_later_conductor = data_early_Security[data_early_Security['总分(1725.0)'] != 0]

        # name=data_early_Security.iloc[0:-1,2:3] # 第3列
        # score=data_early_Security.iloc[0:-1,4:5] # 第5列
        name = data_early_Security['姓名/昵称'].tolist()
        score_early_Security = data_early_Security['总分(1720.0)'].tolist()
        score_middle_Security = data_middle_Security['总分(1725.0)'].tolist()
        score_later_Security = data_later_Security['总分(1725.0)'].tolist()

        print(score_early_Security, score_middle_Security, score_later_Security)

        def avg_score(t):
            a = sum(t) / len(t)
            return a

        avg_early_Security = avg_score(score_early_Security)
        avg_middle_Security = avg_score(score_middle_Security)
        avg_later_Security = avg_score(score_later_Security)

        max_early_Security = max(score_early_Security)
        max_middle_Security = max(score_middle_Security)
        max_later_Security = max(score_later_Security)
        print(avg_early_Security, avg_middle_Security, avg_later_Security, max_early_Security, max_middle_Security,
              max_later_Security)
        line = (Line(init_opts=opts.InitOpts(width="1500px",  # 修改默认宽度
                                             height="700px",  # 修改默认高度
                                             theme=theme,
                                             renderer="svg",  # 设置无失真渲染方式
                                             ))
                .add_xaxis(name)  # LineStyleOpts中设置合适的颜色宽度。
                .add_yaxis('2022年11月15日测试', score_early_Security, symbol="circle", is_symbol_show=True,
                           linestyle_opts=opts.LineStyleOpts(width=3, color="#0000FF"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#0000FF"))
                .add_yaxis("2022年11月15日平均", [int(avg_early_Security)] * len(name), is_symbol_show=False,
                           linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#0000FF"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#0000FF"))
                .add_yaxis("2022年11月15日最好", [int(max_early_Security)] * len(name), is_symbol_show=False,
                           linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#0000FF"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#0000FF"))
                .add_yaxis('2023年01月26日测试', score_middle_Security, symbol="circle", is_symbol_show=True,
                           linestyle_opts=opts.LineStyleOpts(width=3, color="#008000"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#008000"))
                .add_yaxis("2023年01月26日平均", [int(avg_middle_Security)] * len(name), is_symbol_show=False,
                           linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#008000"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#008000"))
                .add_yaxis("2023年01月26日最好", [int(max_middle_Security)] * len(name), is_symbol_show=False,
                           linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#008000"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#008000"))
                .add_yaxis("2023年02月22日测试", score_later_Security, symbol="circle", is_symbol_show=True,
                           linestyle_opts=opts.LineStyleOpts(width=3, color="#FFAC00"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#FFAC00"))
                .add_yaxis("2023年02月22日平均", [int(avg_later_Security)] * len(name), is_symbol_show=False,
                           linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#FFAC00"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#FFAC00"))
                .add_yaxis("2023年02月22日最好", [int(max_later_Security)] * len(name), is_symbol_show=False,
                           linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#FFAC00"),
                           itemstyle_opts=opts.ItemStyleOpts(color="#FFAC00"))

                )  # 以列表数据格式输入pyecharts，形成坐标图。
        line.set_global_opts(
            title_opts=opts.TitleOpts(title="21级信安PTA作业成绩", title_link="https://bing.com", pos_left='center',
                                      # 标题位置：pos_left='center'
                                      subtitle="", subtitle_link="https://baidu.com"),
            toolbox_opts=opts.ToolboxOpts(pos_left='left'),  # 工具箱位置 pos_left='left'
            xaxis_opts=opts.AxisOpts(
                interval=0,
                axislabel_opts={"rotate": 45},
            ),  # 控制X轴
            # 全局图例设置
            legend_opts=opts.LegendOpts(
                pos_right="right", orient="vertical",  # 自定义图例位置为竖向右侧
                textstyle_opts=opts.TextStyleOpts(color="#696969", font_size=16),
            ),
        )
        print("正在生成图片和pdf文件：")
        # make_snapshot(snapshot, line.render(), "21级大数据PTA成绩趋势图.png", notebook=True)
        # make_snapshot(snapshot, line.render(), "21级大数据PTA成绩趋势图.pdf", notebook=True)
        # make_snapshot(snapshot, line.render(), "21级大数据PTA成绩趋势图.jpeg", notebook=True)
        # make_snapshot(snapshot, line.render(), "21级大数据PTA成绩趋势图.gif", notebook=True)
        line.render_notebook()
        f = "文件生成//"+str(int(time.time())) + '折线图生成.html'
        line.render(path=f)
        with open(f, 'r') as rf:
            return rf.read()