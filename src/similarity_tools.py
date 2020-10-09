'''
    不同的相似度计算函数
'''

# 以编辑距离计算相似度
def edit_dis_similarity(str1, str2):
    n = len(str1)
    m = len(str2)
    dis = [[0 for _ in range(m+1)] for _ in range(n+1)]
    for i in range(m+1):
        dis[0][i] = i
    for i in range(n+1):
        dis[i][0] = i
    for i in range(1, n+1):
        for j in range(1, m+1):
            ele = 1 if str1[i-1] != str2[j-1] else 0
            dis[i][j] = min(dis[i-1][j]+1, dis[i][j-1]+1, dis[i-1][j-1]+ele)
    return 1 / dis[n][m]

# 以交并比计算相似度
# pattern取值single和redundancy 分别表示不考虑重复字和考虑重复字
def iou_similarity(str1,str2, pattern):
    def generate_dict(str):
        lst = list(str)
        dic = {}
        for i in lst:
            if dic.__contains__(i):
                dic[i] += 1
            else:
                dic[i] = 1
        return dic
    if pattern == 'single':
        set1 = set(str1)
        set2 = set(str2)
        return len(set1&set2) / len(set1|set2)
    elif pattern == 'redundancy':
        dict1 = generate_dict(str1)
        dict2 = generate_dict(str2)
        insection = 0
        union = 0
        # 计算交集
        for key in dict1.keys():
            if dict2.__contains__(key):
                insection += min(dict1[key],dict2[key])
        # 计算并集
        for key in dict1.keys():
            if dict2.__contains__(key):
                union += max(dict1[key], dict2[key])
            else:
                union += dict1[key]
        for key in dict2.keys():
            if not dict1.__contains__(key):
                union += dict2[key]
        return insection / union

# if __name__ == '__main__':
#     print(edit_dis_similarity('海星有限公司','江苏海星科技有限公司'))
#     print(iou_similarity('海星有限公司','江苏海星科技有限公司','single'))
#     print(iou_similarity('海海有限公司', '江苏海海星科技有限公司', 'redundancy'))
#     print(iou_similarity('海海有限公司', '江苏海海星星科技有限公司', 'redundancy'))
#     print(iou_similarity('海海有限公司', '江苏海海星科技有限公司', 'single'))