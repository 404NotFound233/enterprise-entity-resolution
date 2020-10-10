import csv
def diff():
    t1 = open('text.csv', 'r',encoding='utf8')
    t2 = open('truth.csv', 'r',encoding='utf8')
    fileone = t1.readlines()
    filetwo = t2.readlines()
    t1.close()
    t2.close()

    outFile = open('update.csv', 'w')
    x = 0
    for i in fileone:
        i = excetu(i)
        filetwo[x] = excetu(filetwo[x])
        if i != filetwo[x]:
            outFile.write(i[:len(i) - 1] +" 对比 " +  filetwo[x])
        x += 1
    outFile.close()

def excetu(str1):
    for i in range(0, len(str1)):
        if (str1[i] == ','):
            return str1[i + 1:]
    return str1

# 对比两个csv文件的差异
if __name__ == '__main__':
    # print(excetu('0,南中医大国医堂门诊部,南中医大国医堂门诊部有限公司'))
    diff()