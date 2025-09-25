import time
import numpy as np
import pandas as pd
from pyecharts.charts import Line
import pyecharts.options as opts
from pyecharts.globals import ThemeType


def rain_class(filename1, filename2, sheet1, sheet2, theme):
    sheet_post = pd.read_excel(filename1, sheet_name=sheet1, header=1)
    sheet_early = sheet = pd.read_excel(filename2, sheet_name=sheet2, header=1)
    sheet_post.head(6)

    data_early = sheet_early[['姓名']].dropna(axis=0).values
    data_post = sheet_post[['姓名']].dropna(axis=0).values
    sheet_name = [item for sublist in data_early for item in sublist]  # 姓名
    sheet_name_post = [item for sublist in data_post for item in sublist]  # 姓名
    sheet_grade_early = sheet_early[['总成绩']].dropna(axis=0).values.tolist()  # 前期成绩
    sheet_grade_post = sheet_post[['总成绩']].dropna(axis=0).values.tolist()  # 后期成绩
    list_early = [73] * 31  # 前期最好
    list_post = [70.9] * 31  # 后期最好
    average_early = [int(sheet_early['总成绩'].dropna().astype(float).mean())] * len(sheet_early.index)  # 前期平均
    average_post = [int(sheet_post['总成绩'].dropna().astype(float).mean())] * len(sheet_post.index)  # 后期平均

    x_data = sheet_name
    y_current_early = sheet_grade_early
    y_current_post = sheet_grade_post
    y_average_early = average_early
    y_average_post = average_post
    y_best_early = list_early
    y_best_post = list_post
    line = (
        Line(init_opts=opts.InitOpts(width="1200px",
                                     height="600px",
                                     theme=theme,
                                     page_title="Rain Class Page",
                                     renderer="svg",  # 设置无失真渲染方式
                                     )
             )
        .add_xaxis(x_data)

        .add_yaxis("前期学员成绩", y_current_early, is_smooth=True,
                   linestyle_opts=opts.LineStyleOpts(
                       color="#ba2121",
                       width=5, ),
                   itemstyle_opts=opts.ItemStyleOpts(color="#ba2121"),
                   )

        .add_yaxis("前期最好成绩", y_best_early, is_smooth=True,
                   linestyle_opts=opts.LineStyleOpts(
                       color="#ba2121",
                       type_="dotted",
                       width=3, ),
                   itemstyle_opts=opts.ItemStyleOpts(color="#ba2121"),  # 将图例颜色与线条颜色设置相同
                   is_symbol_show=False)

        .add_yaxis("前期平均成绩", y_average_early, is_smooth=True,
                   linestyle_opts=opts.LineStyleOpts(
                       color="#ba2121",
                       type_="dotted",
                       width=2, ),
                   itemstyle_opts=opts.ItemStyleOpts(color="#ba2121"),  # 将图例颜色与线条颜色设置相同
                   is_symbol_show=False)

        .add_yaxis("后期学员成绩", y_current_post, is_smooth=True,
                   linestyle_opts=opts.LineStyleOpts(
                       color="#4040ff",
                       width=5, ),
                   itemstyle_opts=opts.ItemStyleOpts(color="#4040ff"),
                   )

        .add_yaxis("后期最好成绩", y_best_post, is_smooth=True,
                   linestyle_opts=opts.LineStyleOpts(
                       color="#4040ff",
                       type_="dotted",
                       width=3),
                   itemstyle_opts=opts.ItemStyleOpts(color="#4040ff"),  # 将图例颜色与线条颜色设置相同
                   is_symbol_show=False)

        .add_yaxis("后期平均成绩", y_average_post, is_smooth=True,
                   linestyle_opts=opts.LineStyleOpts(
                       color="#4040ff",
                       type_="dotted",
                       width=2, ),
                   itemstyle_opts=opts.ItemStyleOpts(color="#4040ff"),  # 将图例颜色与线条颜色设置相同
                   is_symbol_show=False)

    )

    line.set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 50}, interval=0),
        yaxis_opts=opts.AxisOpts(min_=15),
        title_opts=opts.TitleOpts(title="雨课堂前后期成绩比较趋势", pos_right='25%', pos_bottom='88%'),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
    )
    # 未完成：1.字体调大 2. 宽度高度比调放 3. 主题颜色有的不会更改问题
    # 生成文件html
    path = "文件生成//"+str(int(time.time())) + '_雨课堂前后期成绩比较趋势.html'
    line.render(path=path)  # 自动生成的文件
    with open(path, 'r') as rf:
        return rf.read()
