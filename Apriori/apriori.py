# -*- coding: utf-8 -*-
__author__ = 'buzz'
__date__ = '2018/4/7 下午9:20'

"""
Apriori 算法的 Python 实现

环境：Python3
"""


def load_dataset():
    """
    load a dataset
    :return: A data set, list.
    """
    dataset = [['l1', 'l2', 'l5'], ['l2', 'l4'], ['l2', 'l3'],
               ['l1', 'l2', 'l4'], ['l1', 'l3'], ['l2', 'l3'],
               ['l1', 'l3'], ['l1', 'l2', 'l3', 'l5'], ['l1', 'l2', 'l3']]
    return dataset


def create_C1(dataset):
    """
    生成候选 1 项集
    :param dataset: sample dataset
    :return:
    """
    C1 = set()
    for i in dataset:
        for item in i:
            item_set = frozenset([item])
            C1.add(item_set)

    return C1


def is_apriori(Ck_item, Lk_sub1):
    """
    Judge wheather a frequent candidate k-itemset satisfy Apriori property
    :param Ck_item: 候选 K 项集的一个项集
    :param Lk_sub1: Lk-1, a set which contains all frequent candidate (k-1)-itemsets
    :return: True or False, True: satisfying Apriori property; False: Not satisfying Apriori property.
    """
    for i in Ck_item:
        Ck_item_sub = Ck_item - frozenset([i])
        if Ck_item_sub not in Lk_sub1:
            return False
    return True


def create_Ck(Lk_sub1, k):
    """
    生成候选 k 项集
    :param Lk_sub1: Lk-1, 频繁 k-1 项集
    :param k: 频繁项集的数目
    :return: 候选 k 项集
    """
    Ck = set()
    len_Lk_sub1 = len(Lk_sub1)
    list_Lk_sub1 = list(Lk_sub1)

    for i in range(len_Lk_sub1):
        for j in range(1, len_Lk_sub1):
            itemset1 = list(list_Lk_sub1[i])
            itemset2 = list(list_Lk_sub1[j])
            itemset1.sort()
            itemset2.sort()
            if itemset1[:k - 2] == itemset2[:k - 2]:
                Ck_item = list_Lk_sub1[i] | list_Lk_sub1[j]
                if is_apriori(Ck_item, Lk_sub1):
                    Ck.add(Ck_item)

    return Ck


def generate_Lk_by_Ck(dataset, Ck, min_support, support_data):
    """
    生成频繁 k 项集
    :param dataset: sample dataset
    :param Ck: 候选 k 项集
    :param min_support: 最小支持度阈值
    :param support_data: A dictionary. The key is frequent itemset and the value is support.
    :return: 频繁 k 项集
    """
    Lk = set()
    item_count = {}
    # 计数
    for i in dataset:
        for Ck_item in Ck:
            if Ck_item.issubset(i):
                if Ck_item not in item_count:
                    item_count[Ck_item] = 1
                else:
                    item_count[Ck_item] += 1

    t_num = float(len(dataset))
    # 判断
    for item in item_count:
        if (item_count[item] / t_num) >= min_support:
            Lk.add(item)
            support_data[item] = item_count[item] / t_num
    return Lk


def generate_final_L(data_set, k, min_support):
    """
    Generate all frequent itemsets.
    :param data_set: sample dataset
    :param k: Maximum number of items for all frequent itemsets.
    :param min_support: 最小支持度阈值
    :return: 频繁项集；A dictionary. The key is frequent itemset and the value is support.
    """
    support_data = {}
    C1 = create_C1(data_set)
    L1 = generate_Lk_by_Ck(data_set, C1, min_support, support_data)
    Lksub1 = L1.copy()
    L = []
    L.append(Lksub1)
    for i in range(2, k + 1):
        Ci = create_Ck(Lksub1, i)
        Li = generate_Lk_by_Ck(data_set, Ci, min_support, support_data)
        Lksub1 = Li.copy()
        L.append(Lksub1)
    return L, support_data


def generate_big_rules(L, support_data, min_conf):
    """
    从频繁项集中产生强关联规则
    :param L: 所有的频繁项集的集合
    :param support_data: A dictionary. The key is frequent itemset and the value is support.
    :param min_conf: 最小置信度阈值
    :return: 返回规则
    """
    big_rule_list = []
    subset_list = []
    for i in range(0, len(L)):
        for freq_set in L[i]:
            for subset in subset_list:
                if subset.issubset(freq_set):
                    conf = support_data[freq_set] / support_data[freq_set - subset]
                    big_rule = (freq_set - subset, subset, conf)
                    if conf >= min_conf and big_rule not in big_rule_list:
                        big_rule_list.append(big_rule)
            subset_list.append(freq_set)
    return big_rule_list


if __name__ == '__main__':
    dataset = load_dataset()
    L, support_data = generate_final_L(dataset, k=3, min_support=0.2)
    big_rule_list = generate_big_rules(L, support_data, min_conf=0.7)
    for Lk in L:
        print("="*50)
        print("frequent " + str(len(list(Lk)[0])) + "-itemsets\t\tsupport")
        print("=" * 50)
        for freq_set in Lk:
            print(freq_set, support_data[freq_set])

    print("")
    print("Big Rules")
    for i in big_rule_list:
        print(i[0], "=>", i[1], "conf", i[2])

