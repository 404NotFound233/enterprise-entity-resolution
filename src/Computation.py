from similarity_tools import edit_dis_similarity,iou_similarity
import jieba
import jieba.posseg as pseg
import re
import datetime
import pandas as pd
import numpy as np

#list1存放了与信息类一中属性最相似的信息类二中属性的下标，list2类似
#weight1存放了权重
list1=[]
weight1=[]
list2=[]
weight2=[]
#初始化属性之间的权重
def init():
    pd1 = pd.read_excel('../dict/task2.xlsx', '信息类一')
    pd2 = pd.read_excel('../dict/task2.xlsx', '信息类二')
    for i in range(0,len(pd1.iloc[0])):
        max_similar=0
        max_j=0
        for j in range(0,len(pd2.iloc[0])):
            d=edit_dis_similarity(pd1.iloc[0][i],pd2.iloc[0][j])
            if(d>max_similar):
                max_similar=d
                max_j=j
        weight1.append(max_similar)
        list1.append(max_j)
    for i in range(0,len(pd2.iloc[0])):
        max_similar=0
        max_j=0
        for j in range(0,len(pd1.iloc[0])):
            d=edit_dis_similarity(pd2.iloc[0][i],pd1.iloc[0][j])
            if(d>max_similar):
                max_similar=d
                max_j=j
        weight2.append(max_similar)
        list2.append(max_j)


def similarity_degree(obj1, obj2):
    init()
    sum=0
    for i in range(0,len(obj1)):
        #排除空值
        if(type(obj1[i])==type(0.3) or type(obj2[list1[i]])==type(0.3)):
            sum+=0
        else:
            sum+=weight1[list1[i]]*iou_similarity(obj1[i],obj2[list1[i]],'redundancy')
    return sum


init()
pd1 = pd.read_excel('../dict/task2.xlsx', '信息类一')
pd2 = pd.read_excel('../dict/task2.xlsx', '信息类二')
max=0
maxi=0
for i in range(0,100):
    print("正在计算第"+str(i)+"个")
    if(similarity_degree(pd1.iloc[1],pd2.iloc[i])>max):
        max=similarity_degree(pd1.iloc[1],pd2.iloc[i])
        maxi=i
# print(similarity_degree(pd1.iloc[1],pd2.iloc[2]))
# print(similarity_degree(pd1.iloc[1],pd2.iloc[80]))
print(maxi)