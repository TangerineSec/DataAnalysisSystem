# encoding: utf-8
import time

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType


def bar_chart(file, sheet1, theme):
    df = pd.read_excel(file, header=0, sheet_name=sheet1)

    # 将所有含有'补考'的成绩都替换成59
    df = df.applymap(lambda x: 59 if x == '补考' else x)

    # 第一种缓考处理办法是移除所有含有缓考的行（即平时总成绩、终结性成绩和总评成绩中有任何一列的值是缺失值的行）
    # df.dropna(subset=['平时总成绩（数字格式）', '终结性成绩（数字格式）', '总评成绩（数字格式）'], inplace=True)

    # 第二种缓考处理方法是把缓考先换为0，然后再算出高于59之外的最低分，以最低分计算。
    # 补考：填充59
    # 缓考：填充最低分
    # NaN值：填充最低分

    # 使用最小值填充缺失值，inplace=True 是一种参数设置，它通常用于表明对数据进行操作时是否是原地修改。
    df.fillna(df.min(), inplace=True)

    # 删除低于60分的行
    df1 = df.applymap(lambda x: 0 if x == '缓考' else x)
    df1 = df1.iloc[:, 2:][df1.iloc[:, 2:] >= 60].dropna()  # 只保留分数大于等于60的行，并删除缺失值

    # 计算每列的最低分
    min_scores1 = df1['平时总成绩（数字格式）'].min()
    min_scores2 = df1['终结性成绩（数字格式）'].min()
    min_scores3 = df1['总评成绩（数字格式）'].min()

    df['平时总成绩（数字格式）'].replace('缓考', min_scores1, inplace=True)
    df['终结性成绩（数字格式）'].replace('缓考', min_scores2, inplace=True)
    df['总评成绩（数字格式）'].replace('缓考', min_scores3, inplace=True)

    # 新增一列'评级'，表示每个学生的总评成绩所处的优秀、良好、中等、及格、不及格分数段
    def classify_score(score):
        if score >= 90:
            return '优秀'
        elif score >= 80:
            return '良好'
        elif score >= 70:
            return '中等'
        elif score >= 60:
            return '及格'
        else:
            return '不及格'

    df['平时总成绩评级'] = df['平时总成绩（数字格式）'].apply(classify_score)
    df['终结性成绩评级'] = df['终结性成绩（数字格式）'].apply(classify_score)
    df['总评成绩评级'] = df['总评成绩（数字格式）'].apply(classify_score)

    # 统计每个评级的人数
    count_by_grade = df.groupby(['平时总成绩评级', '终结性成绩评级', '总评成绩评级']).size().reset_index(name='人数')

    # 计算每一列中优秀的人数
    count_excellent_by_col = pd.DataFrame({
        '平时总成绩评级': [count_by_grade[(count_by_grade['平时总成绩评级'] == '优秀')]['人数'].sum()],
        '终结性成绩评级': [count_by_grade[(count_by_grade['终结性成绩评级'] == '优秀')]['人数'].sum()],
        '总评成绩评级': [count_by_grade[(count_by_grade['总评成绩评级'] == '优秀')]['人数'].sum()]
    })

    # 计算每一列中良好的人数
    count_good_by_col = pd.DataFrame({
        '平时总成绩评级': [count_by_grade[(count_by_grade['平时总成绩评级'] == '良好')]['人数'].sum()],
        '终结性成绩评级': [count_by_grade[(count_by_grade['终结性成绩评级'] == '良好')]['人数'].sum()],
        '总评成绩评级': [count_by_grade[(count_by_grade['总评成绩评级'] == '良好')]['人数'].sum()]
    })

    # 计算每一列中中等的人数
    count_medium_by_col = pd.DataFrame({
        '平时总成绩评级': [count_by_grade[(count_by_grade['平时总成绩评级'] == '中等')]['人数'].sum()],
        '终结性成绩评级': [count_by_grade[(count_by_grade['终结性成绩评级'] == '中等')]['人数'].sum()],
        '总评成绩评级': [count_by_grade[(count_by_grade['总评成绩评级'] == '中等')]['人数'].sum()]
    })

    # 计算每一列中优秀的人数
    count_pass_by_col = pd.DataFrame({
        '平时总成绩评级': [count_by_grade[(count_by_grade['平时总成绩评级'] == '及格')]['人数'].sum()],
        '终结性成绩评级': [count_by_grade[(count_by_grade['终结性成绩评级'] == '及格')]['人数'].sum()],
        '总评成绩评级': [count_by_grade[(count_by_grade['总评成绩评级'] == '及格')]['人数'].sum()]
    })

    # 计算每一列中优秀的人数
    count_fail_by_col = pd.DataFrame({
        '平时总成绩评级': [count_by_grade[(count_by_grade['平时总成绩评级'] == '不及格')]['人数'].sum()],
        '终结性成绩评级': [count_by_grade[(count_by_grade['终结性成绩评级'] == '不及格')]['人数'].sum()],
        '总评成绩评级': [count_by_grade[(count_by_grade['总评成绩评级'] == '不及格')]['人数'].sum()]
    })

    # 计算每一列中总人数
    total_count_by_col = count_by_grade['人数'].sum()

    # 计算每一列中优秀的比例
    ratio_excellent_by_col = count_excellent_by_col / total_count_by_col

    # 计算每一列中良好的比例
    ratio_good_by_col = count_good_by_col / total_count_by_col

    # 计算每一列中中等的比例
    ratio_medium_by_col = count_medium_by_col / total_count_by_col

    # 计算每一列中及格的比例
    ratio_pass_by_col = count_pass_by_col / total_count_by_col

    # 计算每一列中不及格的比例
    ratio_fail_by_col = count_fail_by_col / total_count_by_col

    data_a = [int(ratio_excellent_by_col['平时总成绩评级'] * 100), int(ratio_good_by_col['平时总成绩评级'] * 100),
              int(ratio_medium_by_col['平时总成绩评级'] * 100), int(ratio_pass_by_col['平时总成绩评级'] * 100),
              int(ratio_fail_by_col['平时总成绩评级'] * 100)]
    data_b = [int(ratio_excellent_by_col['终结性成绩评级'] * 100), int(ratio_good_by_col['终结性成绩评级'] * 100),
              int(ratio_medium_by_col['终结性成绩评级'] * 100), int(ratio_pass_by_col['终结性成绩评级'] * 100),
              int(ratio_fail_by_col['终结性成绩评级'] * 100)]
    data_c = [int(ratio_excellent_by_col['总评成绩评级'] * 100), int(ratio_good_by_col['总评成绩评级'] * 100),
              int(ratio_medium_by_col['总评成绩评级'] * 100), int(ratio_pass_by_col['总评成绩评级'] * 100),
              int(ratio_fail_by_col['总评成绩评级'] * 100)]

    pdt_list = ["优秀", "良好", "中等", "及格", "不及格"]
    bar_dict = {'data': [data_a, data_b, data_c], 'head': ['平时总成绩', '终结性总成绩', '总评成绩'], 'item': pdt_list}

    bar_item = bar_dict['item']  #
    bar_head = bar_dict['head']  #
    bar_data = bar_dict['data']  #

    bar = (
        Bar(
            init_opts=opts.InitOpts(theme=theme,  # 主题设置
                                    page_title="Histogram page",  # 页面标题头定制
                                    renderer="svg", # 设置无失真渲染方式
                                    )
        )
        .add_xaxis(bar_item)
        .set_global_opts(title_opts=opts.TitleOpts(title="评级情况", subtitle="占比情况"),
                         xaxis_opts=opts.AxisOpts(
                             axislabel_opts=opts.LabelOpts(font_size=17, rotate=60),  # 设置字体大小为 16,合并设置倾斜度
                             interval=0,
                         ),  # 控制X轴
                         )
    )

    for i in range(len(bar_head)):  # 两个头部元素
        bar.add_yaxis(bar_head[i], bar_data[i], label_opts=opts.LabelOpts(formatter="{c} %", font_size=18), gap="0%",
                      category_gap="5%")  # gap控制柱子内部间隙，category_gap控制柱子外部间隙
    bar.set_global_opts(
        yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value} %", font_size=17), interval=10),
        # y轴字体大小
        legend_opts=opts.LegendOpts(
            textstyle_opts=opts.TextStyleOpts(color="#696969", font_size=15),  # 图例大小
        ),
    )
    # 生成文件html
    path = '文件生成//'+str(int(time.time())) + '_柱状图比例图.html'
    bar.render(path=path)  # 自动生成的文件
    with open(path, 'r') as rf:
        return rf.read()
    # return path
