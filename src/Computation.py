from similarity_tools import edit_dis_similarity,iou_similarity
import jieba
import jieba.posseg as pseg
import re
import datetime
import pandas as pd
import numpy as np

list1=[]
list2=[]
def init():
    pd1 = pd.read_excel('../dict/task2.xlsx', '信息类一')
    pd2 = pd.read_excel('../dict/task2.xlsx', '信息类二')
    for i in range(0,len(pd1.iloc[0])):
        max_similar=0
        max_j=0
        for j in range(0,len(pd2.iloc[0])):
            d=iou_similarity(pd1.iloc[0][i],pd2.iloc[0][j],'single')
            if(d>max_similar):
                max_similar=d
                max_j=j
        list1.append(max_j)
    for i in range(0,len(pd2.iloc[0])):
        max_similar=0
        max_j=0
        for j in range(0,len(pd1.iloc[0])):
            d=iou_similarity(pd2.iloc[0][i],pd1.iloc[0][j],'redundancy')
            if(d>max_similar):
                max_similar=d
                max_j=j
        list2.append(max_j)


def similarity_degree(obj1, obj2):
    init()
    sum=0
    for i in range(0,len(obj1)):
        sum+=iou_similarity(obj1[i],obj2[list1[i]],'redundancy')
    return sum

# init()
# pd1 = pd.read_excel('../dict/task2.xlsx', '信息类一')
# pd2 = pd.read_excel('../dict/task2.xlsx', '信息类二')
# max=0
# maxi=0
# for i in range(0,100):
#     print(i)
#     if(similarity_degree(pd1.iloc[1],pd2.iloc[i])>max):
#         max=similarity_degree(pd1.iloc[1],pd2.iloc[i])
#         maxi=i
# print(similarity_degree(pd1.iloc[1],pd2.iloc[2]))
# print(similarity_degree(pd1.iloc[1],pd2.iloc[80]))
# print(maxi)