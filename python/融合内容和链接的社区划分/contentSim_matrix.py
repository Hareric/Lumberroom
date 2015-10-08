#coding=utf-8
__author__ = 'Eric_Chan'


import jieba
import re
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

def blog_crawling(filename,CORPUS):
    file1 = open('/Users/Har/Desktop/weibo_blog/%s'%filename+'.txt','r')
    unit_data = file1.read()
    file1.close()
    pattern0 = re.compile('text:(.*)')
    originText = re.findall(pattern0,unit_data)
    unit = ""
    for i in originText:
        temp = jieba.cut(i)
        seg_list = " ".join(temp)
        unit += seg_list
    CORPUS.append(unit)

class ContentSim:

    def __init__(self,dataMatrix): #输入 用户-文本 矩阵
        self.dataMatrix = dataMatrix

    class TFIDF:
        def __init__(self):
            self.weight = []

        def calculate_TFIDF(self,CORPUS): #计算每个用户的全部博文的每个词语的TFITF 返回 用户-词语TFITF 矩阵
            vectorizer = CountVectorizer()     #该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
            transformer = TfidfTransformer()     #该类会统计每个词语的tf-idf权值
            tfidf = transformer.fit_transform(vectorizer.fit_transform(CORPUS))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
            word = vectorizer.get_feature_names()#获取词袋模型中的所有词语
            weight = tfidf.toarray()             #将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
            self.weight = weight
            # for i in range(len(weight)):       #打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
            #     print u"-------这里输出第",i+1,u"类文本的词语tf-idf权重------"
            #     for j in range(len(word)):
            #         print word[j],weight[i][j]
            print weight
            print len(weight[0])
            return weight

        def get_TFIDF(self):
            return self.weight

    '''
    CORPUS=["我 来到 北京 清华大学",#第一类文本切词后的结果，词之间以空格隔开
    "他 来到 了 网易 杭研 大厦",#第二类文本的切词结果
    "小明 硕士 毕业 与 中国 科学院",#第三类文本的切词结果
    "我 爱 北京 天安门"]#第四类文本的切词结果
    CORPUS = ["他 来到 了","小明 硕士"]
    '''

    '''主成分分析'''
    class PCA:

        def __zeroMean(self,dataMat):
            meanVal = np.mean(dataMat,axis=0)
            newData = dataMat - meanVal
            return newData,meanVal

        def __percentage2n(self,eigVals,percentage):
            sortArray = np.sort(eigVals)   #升序
            sortArray = sortArray[-1::-1]  #逆转，即降序
            arraySum = sum(sortArray)
            tmpSum = 0
            num = 0
            for i in sortArray:
                tmpSum += i
                num += 1
                if tmpSum>=arraySum*percentage:
                    return num

        def calculate_pca(self,dataMat,percentage=0.99):
            newData,meanVal = self.__zeroMean(dataMat)
            covMat = np.cov(newData,rowvar=0)               #求协方差矩阵,return ndarray；若rowvar非0，一列代表一个样本，为0，一行代表一个样本
            eigVals,eigVects = np.linalg.eig(np.mat(covMat))#求特征值和特征向量,特征向量是按列放的，即一列代表一个特征向量
            n = self.__percentage2n(eigVals,percentage)     #要达到percent的方差百分比，需要前n个特征向量
            eigValIndice = np.argsort(eigVals)              #对特征值从小到大排序
            n_eigValIndice = eigValIndice[-1:-(n+1):-1]     #最大的n个特征值的下标
            n_eigVect = eigVects[:,n_eigValIndice]          #最大的n个特征值对应的特征向量
            lowDDataMat = newData * n_eigVect               #低维特征空间的数据
            return lowDDataMat



    class CreateSimMatrix:
        #利用余弦相似度计算用户-用户之间的相似度
        #输入 用户-特征 矩阵  返回 用户-用户 相似度矩阵
        def __init__(self,dataMat):
            self.dataMat = dataMat
            print self.dataMat
            self.userNum = len(dataMat)  #用户的个数
            self.feaNum  = len(dataMat[0])#特征的个数

        def __calculate_users_sim(self,user_1_array,user_2_array ):
            d = 0   #表示 用户1 和 用户2 之间的距离  距离越大 相似度越低
            for i in range(self.feaNum):
                d += (user_1_array[i] + user_2_array[i]) ** 2
            d = d ** 0.5
            return d

        def return_content_sim_matrix(self):
            matrix = np.zeros((self.userNum,self.userNum))#创建用户-用户 相似度距离矩阵
            Max = -1   #记录 用户-用户 之间的最大相似度
            Min = 1000 #记录 用户-用户 之间的最小相似度
            for i in range(self.userNum):
                for j in range(self.userNum):
                    if matrix[i][j] > 0:
                        continue
                    matrix[i][j] = self.__calculate_users_sim(self.dataMat[i],self.dataMat[j])
                    matrix[j][i] = matrix[i][j]
                    if matrix[i][j] > Max:
                        Max = matrix[i][j]
                    if matrix[i][j] < Min:
                        Min = matrix[i][j]

            #对矩阵进行归一化处理
            normal_matrix = np.zeros((self.userNum,self.userNum))#创建用户归一化后的相似度矩阵
            temp = Max - Min
            for i in range(self.userNum):
                for j in range(self.userNum):
                    if (i==j)|(normal_matrix[i][j]>0):
                        continue
                    normal_matrix[i][j] = (Max - matrix[i][j]) / temp
                    normal_matrix[j][i] = normal_matrix[i][j]

            return normal_matrix

    def getContentSim(self):
        user_TFIDF_matrix = self.TFIDF().calculate_TFIDF(self.dataMatrix) #首先构建 用户-TFIDF 矩阵
        matrix_pca = self.PCA().calculate_pca(user_TFIDF_matrix)   #接着对 用户-TFIDF 矩阵使用PCA 进行降维
        matrix_sim = self.CreateSimMatrix(matrix_pca).return_content_sim_matrix() #最后获得归一化后的 用户-用户 相似度矩阵
        return matrix_sim
corpus = []
for i in range(5)[1:]:
    blog_crawling('blog%s'%i,corpus)

sim_matrix = ContentSim(corpus).getContentSim()
print sim_matrix

