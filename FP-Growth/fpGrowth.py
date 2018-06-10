# -*- coding: utf-8 -*-
__author__ = 'buzz'
__date__ = '2018/6/10 下午9:13'


class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        """

        :param nameValue: 结点名字
        :param numOccur: 结点的计数
        :param parentNode: 父节点，通常不使用这个结点
        """
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, ind=1):
        print("    " * ind, self.name, '    ', self.count)
        for child in self.children.values():
            child.disp(ind + 1)


def createTree(dataSet, minSup=1):
    """
    create FP tree
    :param dataSet: 数据集
    :param minSup: 最小支持度
    :return:
    """

    # 项头表
    headerTable = {}

    # 扫描数据库，对每个项计数
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]

    # 生成频繁 1 项集
    for k in headerTable.keys():
        if headerTable[k] < minSup:
            del (headerTable[k])

    freqItemsSet = set(headerTable.keys())
    if len(freqItemsSet) == 0:
        return None, None

    for k in headerTable:
        headerTable[k] = [headerTable[k], None]

    # 头结点
    retTree = treeNode('Null Set', 1, None)

    for tranSet, count in dataSet.items():
        localD = {}

        # 对每个事务中的项进行降序排序，只考虑在 L1 中有的项
        for item in tranSet:
            if item in freqItemsSet:
                localD[item] = headerTable[item][0]

        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]

            updateTree(orderedItems, retTree, headerTable, count)
    return retTree, headerTable


def updateTree(items, inTree, headerTable, count):
    """
    更新树
    :type items: 已经排好序的项集
    :type inTree: 当前树
    :type headerTable: 头指针表
    :type count: 每个项的计数
    :rtype:
    """

    # 如果该项集的第一个项在当前树中的子结点中则直接增加计数
    # 如果没有就生成该项的子结点
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1],
                         inTree.children[items[0]])
    if len(items) > 1:
        # 对剩下的项迭代调用 updateTree
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)


def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


# 简单数据集集数据包装器
def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat


def createInitSet(dataset):
    retDict = {}
    for trans in dataset:
        # 集合不可更改 无add remove方法
        retDict[frozenset(trans)] = 1
    return retDict


# 条件模式基
def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:  # 迭代上溯整颗树
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def findPrefixPath(basePat, treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


# 条件 FP 树
def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda e: e[1])]  # 从头指针表的底端开始

    for basePat in bigL:  # bigL为头指针，basePat为“t”,"r"等等
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])  # 创建“t”的条件模式基
        myCondTree, myHead = createTree(condPattBases, minSup)  # 以条件模式基构建条件FP树，得到的结果用于下一次迭代

        if myHead != None:  # myHead由createTree函数得到，本质是头指针表变量。
            print("conditional tree for: ", newFreqSet)
            myCondTree.disp(1)
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)
