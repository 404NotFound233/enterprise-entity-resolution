import jieba
import jieba.posseg as pseg
import re
import datetime
import pandas as pd
import numpy as np


# 提示：可以分析公司全称的组成方式，将“地名”、“公司主体部分”、“公司后缀”区分开，并制定一些启发式的规则
# TODO：建立main_extract，当输入公司名，返回会被统一的简称
def main_extract(company_name, d_4_delete, stop_word, d_city_province):
    """
    company_name  输入的公司名
    stop_word 停用词
    d_4_delete 后缀名
    d_city_province 地区
    """
    company_name_list = pseg.cut(company_name)
    # 去除获取到的地名
    company_name_list = city_prov_ahead(company_name_list, d_city_province)
    # 去除通用后缀
    company_name_list = delete_suffix(company_name_list, d_4_delete)

    # 你的自定义function
    company_name_list = my_function(company_name_list)

    company_name = ''.join(company_name_list)
    return company_name, company_name_list


# 功能：将公司名中地名提前
def city_prov_ahead(company_name_list, d_city_province):
    # 公司名中地名的部分
    city_prov_lst = []
    # 公司名中其他部分
    other_lst = []
    # TODO: 将公司名中地名的部分添加至city_prov_lst，将公司名中非地名的部分添加至other_lst。
    for word, flag in company_name_list:
        if word in d_city_province:
            city_prov_lst.append(word)
        else:
            other_lst.append(word)
    return other_lst


# 功能：去除通用后缀
def delete_suffix(company_name_list, d_4_delete):
    # TODO：识别公司名中通用后缀并删除
    for word in company_name_list[:]:
        if word in d_4_delete:
            company_name_list.remove(word)
    return company_name_list


# 你的自定义function
def my_function(company_name_list):
    other_stop_word = set(('分行', '财务', '商贸', '管理', '房地产', '投资', '有限责任', '银行', '餐饮公司'))
    for word in company_name_list[:]:
        if word in other_stop_word:
            company_name_list.remove(word)
        # 去除空格
        word = word.replace(' ', '')
    return company_name_list

# 计算编辑距离
def compute(name1, name2):
    if len(name1) < len(name2):
        return compute(name2, name1)
    count = 0
    for x in name1:
        if (x == '(' or x == ')'):
            if x in name2:
                count = count + 1
                continue
            else:
                return 0
        if x in name2:
            count = count + 1
    return count / len(name1)


# 初始加载步骤
# 输出需要使用的词典
def my_initial():
    # 加载城市名、省份名
    d_city_province = set()
    with open("./data/dict/co_City_Dim.txt", encoding='utf-8') as cts:
        for ct in cts.readlines():
            d_city_province.add(ct[:-1])
    with open("./data/dict/co_Province_Dim.txt", encoding='utf-8') as prvs:
        for prv in prvs.readlines():
            d_city_province.add(prv[:-1])

    # 加载公司后缀
    d_4_delete = set()
    with open(r"./data/dict/company_suffix.txt", encoding='utf-8') as sfs:
        for sf in sfs.readlines():
            d_4_delete.add(sf[:-1])

    # 加载停用词
    stop_word = set()
    with open(r"./data/dict/stopwords.txt", encoding='utf-8') as sts:
        for st in sts.readlines():
            stop_word.add(st[:-1])
    return d_4_delete, stop_word, d_city_province


d_4_delete, stop_word, d_city_province = my_initial()
company_name = ""
a = []
b = []
c = []
d = []
data = {}
data1 = {}
data2 = {}
# 读取两个表格
pd1 = pd.read_excel('./data/dict/task2.xlsx', '信息类一')
pd2 = pd.read_excel('./data/dict/task2.xlsx', '信息类二')

# 处理第一个表格
for index in range(1, len(pd1)):
    company_name = pd1.iloc[index, 0] # 第一列
    company_name3, company_name_list = main_extract(company_name, d_4_delete, stop_word, d_city_province) # 经过上面的处理
    a.append(company_name3) #处理之后的公司名存在a里
    data1[company_name3] = company_name # 处理之后的公司名 : 处理之前的公司名 形成字典
# 处理第二个表格 其他同上
for index in range(1, len(pd2)):
    company_name2 = pd2.iloc[index, 0]
    company_name4, company_name_list2 = main_extract(company_name2, d_4_delete, stop_word, d_city_province)
    b.append(company_name4)
    data2[company_name4] = company_name2

# 两个for循环对比每行，选出匹配度最高的两个分别存进c和d
for name1 in a:
    max = 0
    maxname = ""
    for name2 in b:
        degree = compute(name1, name2)
        if (degree > max):
            max = degree
            maxname = name2
    data['col1'] = c.append(data1[name1])
    data['col2'] = d.append(data2[maxname])

# 输出成csv文件
df = pd.DataFrame({'col1': c, 'col2': d})
df.to_csv('text.csv', na_rep='NA', columns=['col1','col2'])
