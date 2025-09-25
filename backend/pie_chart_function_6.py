# encoding: utf-8
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.commons.utils import JsCode
import time
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType

def pie_chart(file, sheet1, theme):
    df=pd.read_excel(file, header=0, sheet_name=sheet1)
    # 得到所有项目的值
    x=df['项目'].values.tolist()
    # 得到所有比例的值
    y=[]
    for i in range(len(df['比例'].values.tolist())):
        number=df['比例'].values.tolist()[i]*100
        y.append(number)
    color=[
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
    pie = (
        Pie(init_opts=opts.InitOpts(
            theme=theme,
            page_title="Pie chart",
        ))
        .add("", [list(z) for z in zip(x, y)]) # zip函数打包(x,y)进行迭代对象，使用list函数保存为这样的结果：[['SPOC成绩', 25], ['雨课堂成绩（课前测、课中测、课后测）', 25], ['PTA作业', 20], ['PTA测试', 20], ['project大作业', 10]]
        .set_colors(color)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="所有考核成绩比例图",pos_right="center",
                                     ),
            legend_opts=opts.LegendOpts(pos_left="right", orient="vertical",
                                       textstyle_opts=opts.TextStyleOpts(color=color, font_size=16),)# 图例字体大小自定义
            ) # 竖向标签更好看
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%"))
    )

    # 生成文件html
    path = str("文件生成//各项成绩考核比例图.html")
    pie.render(path=path)  # 自动生成的文件
    with open(path, 'r') as rf:
        return rf.read()