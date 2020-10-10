from similarity_tools import edit_dis_similarity,iou_similarity
import jieba.posseg as pseg
import pandas as pd

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
    for pairs in company_name_list:
        if pairs in d_city_province:
            city_prov_lst.append(pairs.word)
        else:
            other_lst.append(pairs.word)
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
        # word = word.replace(' ', '')
    return company_name_list

# 初始加载步骤
# 输出需要使用的词典
def my_initial():
    # 加载城市名、省份名
    d_city_province = set()
    with open("../dict/co_City_Dim.txt", encoding='utf-8') as cts:
        for ct in cts.readlines():
            d_city_province.add(ct[:-1])
    with open("../dict/co_Province_Dim.txt", encoding='utf-8') as prvs:
        for prv in prvs.readlines():
            d_city_province.add(prv[:-1])

    # 加载公司后缀
    d_4_delete = set()
    with open("../dict/company_suffix.txt", encoding='utf-8') as sfs:
        for sf in sfs.readlines():
            d_4_delete.add(sf[:-1])

    # 加载停用词
    stop_word = set()
    with open("../dict/stopwords.txt", encoding='utf-8') as sts:
        for st in sts.readlines():
            stop_word.add(st[:-1])
    return d_4_delete, stop_word, d_city_province


#list1存放了与信息类一中属性最相似的信息类二中属性的下标，list2类似
#weight1存放了权重
list1=[]
weight1=[]
# list2=[]
# weight2=[]
#初始化属性之间的权重
def init():
    pd1 = pd.read_excel('../dict/task2.xlsx', '信息类一')
    pd2 = pd.read_excel('../dict/task2.xlsx', '信息类二')
    weight1.append(edit_dis_similarity(pd1.iloc[0][0],pd2.iloc[0][0]))
    list1.append(0)
    for i in range(1,len(pd1.iloc[0])):
        max_similar=0
        max_j=0
        for j in range(0,len(pd2.iloc[0])):
            d1=edit_dis_similarity(pd1.iloc[0][i],pd2.iloc[0][j])
            d2=iou_similarity(pd1.iloc[0][i],pd2.iloc[0][j],'redundancy')
            d=d1*0.5+d2*0.5
            if(d>max_similar):
                max_similar=d
                max_j=j
        weight1.append(max_similar)
        list1.append(max_j)
    # weight2.append(edit_dis_similarity(pd2.iloc[0][0],pd1.iloc[0][0]))
    # list2.append(0)
    # for i in range(1,len(pd2.iloc[0])):
    #     max_similar=0
    #     max_j=0
    #     for j in range(0,len(pd1.iloc[0])):
    #         d=edit_dis_similarity(pd2.iloc[0][i],pd1.iloc[0][j])
    #         if(d>max_similar):
    #             max_similar=d
    #             max_j=j
    #     weight2.append(max_similar)
    #     list2.append(max_j)


def similarity_degree(obj1, obj2):
    sum=0
    d_4_delete, stop_word, d_city_province = my_initial()
    company_name = obj1[0]
    company_name3, company_name_list = main_extract(company_name, d_4_delete, stop_word, d_city_province) # 经过上面的处理
    company_name2 = obj2[0]
    company_name4, company_name_list2 = main_extract(company_name2, d_4_delete, stop_word, d_city_province)
    sum += weight1[list1[0]] * iou_similarity(company_name3, company_name4, 'redundancy')
    for i in range(1,len(obj1)):
        #排除空值
        if(type(obj1[i])==type(0.3) or type(obj2[list1[i]])==type(0.3)):
            sum+=0
        else:
            sum+=weight1[list1[i]]*iou_similarity(obj1[i],obj2[list1[i]],'redundancy')
    return sum

# init()
# pd1 = pd.read_excel('../dict/task2.xlsx', '信息类一')
# pd2 = pd.read_excel('../dict/task2.xlsx', '信息类二')
# max=0
# maxi=0
# for i in range(0,100):
#     print("正在计算第"+str(i)+"个")
#     if(similarity_degree(pd1.iloc[1],pd2.iloc[i])>max):
#         max=similarity_degree(pd1.iloc[1],pd2.iloc[i])
#         maxi=i
# print(maxi)