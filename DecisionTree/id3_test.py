# -*- coding: utf-8 -*-
__author__ = 'buzz'
__date__ = '2018/4/16 下午2:00'

from utils import *
from utils import class_attr
import operator
import pandas as pd

dataset = load_data()


def createTree(dataset, dropCol):
    cols = dataset.columns.tolist()[:-1]
    classList = dataset[dataset.columns.tolist()[-1]].tolist()

    # 若数据集中所有实例属于同一类Ck，则为单节点树，并将Ck作为该节点的类标记
    if classList.count(classList[0]) == len(classList):
        return classList[0]

    # 若特征集为空集，则为单节点树，并将数据集中实例数最大的类Ck作为该节点的类标记
    if len(dataset[0:1]) == 0:
        return majorityCnt(classList)

    print('特征集和类别：', dataset.columns.tolist())
    bestFeature, bestInfoGain = chooseBestFeatureToSplit(dataset)
    print('bestFeture:', bestFeature)

    myTree = {bestFeature: {}}

    print(bestFeature)

    featureValues = dataset[bestFeature]
    uniqueValues = set(featureValues)
    for value in uniqueValues:
        myTree[bestFeature][value] = createTree(splitDataSet(dataset, bestFeature, value), bestFeature)
    return myTree


def chooseBestFeatureToSplit(dataset):
    numFeatures = dataset.shape[1] - 1
    cols = dataset.columns.tolist()
    infoD = get_entropy(dataset, class_attr)

    bestFeature = ""
    bestInfoGain = 0.0

    for i in range(numFeatures):
        infoaD = get_condition_entropy(dataset, cols[i])
        info_gain_a = infoD - infoaD
        print(cols[i], info_gain_a)
        if info_gain_a > bestInfoGain:
            bestInfoGain = info_gain_a
            bestFeature = cols[i]

    return bestFeature, bestInfoGain


def splitDataSet(dataset, axis, value):
    '''
    输入：数据集，所占列，选择值
    输出：划分数据集
    描述：按照给定特征划分数据集；选择所占列中等于选择值的项
    '''
    cols = dataset.columns.tolist()
    axisFeat = dataset[axis].tolist()
    # 更新数据集
    retDataSet = pd.concat([dataset[featVec] for featVec in cols if featVec != axis], axis=1)
    i = 0
    dropIndex = []  # 删除项的索引集
    for featVec in axisFeat:
        if featVec != value:
            dropIndex.append(i)
            i += 1
        else:
            i += 1
    newDataSet = retDataSet.drop(dropIndex)
    return newDataSet.reset_index(drop=True)


def majorityCnt(classList):
    '''
    输入：分类类别列表
    输出：子节点的分类
    描述：数据集已经处理了所有属性，但是类标签依然不是唯一的，
          采用多数判决的方法决定该子节点的分类
    '''
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reversed=True)
    return sortedClassCount[0][0]


dropCol = []
myTree = createTree(dataset, dropCol)
print(myTree)
