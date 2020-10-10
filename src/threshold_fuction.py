from Computation import similarity_degree
from Computation import init
import pandas as pd
import time

def threshold():
    first_index = []
    second_index = []
    pd1 = pd.read_excel('../dict/task2.xlsx', '信息类一')
    pd2 = pd.read_excel('../dict/task2.xlsx', '信息类二')
    for i in range(0, len(pd1)):
        max_degree = 0
        max_degree_indexi = 0
        max_degree_indexj = 0
        for j in range(0, len(pd2)):
            print("正在计算第" + str(i) + "个和第" + str(j) + "个...")
            if (similarity_degree(pd1.iloc[i], pd2.iloc[j]) > max_degree):
                max_degree = similarity_degree(pd1.iloc[i], pd2.iloc[j])
                max_degree_indexi = i
                max_degree_indexj = j
        first_index.append(pd1.iloc[max_degree_indexi][0])
        second_index.append(pd2.iloc[max_degree_indexj][0])
    df = pd.DataFrame({'first_col': first_index, 'second_col': second_index})
    df.to_csv('truth.csv', na_rep='NA', columns=['first_col', 'second_col'])

if __name__ == '__main__':
    init()
    start_time = time.time()
    threshold()
    end_time = time.time()
    print('此次运行时间为 %f' % (end_time - start_time))