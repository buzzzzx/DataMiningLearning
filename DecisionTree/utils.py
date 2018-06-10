# -*- coding: utf-8 -*-
__author__ = 'buzz'
__date__ = '2018/4/16 上午10:08'

from math import log2
from pandas import DataFrame


def load_data():
    _index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    age = ['youth', 'youth', 'middle_aged', 'senior', 'senior', 'senior', 'middle_aged', 'youth', 'youth', 'senior',
           'youth', 'middle_aged', 'middle_aged', 'senior']
    income = ['high', 'high', 'high', 'medium', 'low', 'low', 'low', 'medium', 'low', 'medium', 'medium', 'medium',
              'high', 'medium']
    student = ['no', 'no', 'no', 'no', 'yes', 'yes', 'yes', 'no', 'yes', 'yes', 'yes', 'no', 'yes', 'no']
    credit_rating = ['fair', 'excellent', 'fair', 'fair', 'fair', 'excellent', 'excellent', 'fair', 'fair', 'fair',
                     'excellent', 'excellent', 'fair', 'excellent']
    class_buys_computer = ['no', 'no', 'yes', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'yes', 'yes', 'yes', 'yes', 'no']
    value = {'age': age, 'income': income, 'student': student, 'credit_rating': credit_rating,
             'class_buys_computer': class_buys_computer}
    data = DataFrame(value, index=_index, columns=['age', 'income', 'student', 'credit_rating', 'class_buys_computer'])
    return data


def get_unique_counts(col):
    results = {}
    for i in col:
        if i not in results:
            results[i] = 1
        else:
            results[i] += 1

    return results


def get_entropy(data, attr):
    counts = get_unique_counts(data[attr])
    ent = 0.0
    for i in counts.keys():
        p = float(counts[i]) / len(data[attr])
        ent = ent - p * log2(p)
    return ent


def get_condition_entropy(data, attr):
    counts = get_unique_counts(data[attr])
    attr_p = []
    infoaD = 0
    for i in counts.keys():
        p = float(counts[i]) / len(data[attr])
        attr_p.append(p)

        infoaD += p * (get_entropy(data[data[attr] == i], class_attr))

    return infoaD


def get_info_gain(infoD, infoaD):
    return infoD - infoaD


def get_info_gain_ratio(gain_aD, attr, data):
    splitInfoaD = get_entropy(data, attr)
    return gain_aD / splitInfoaD


def get_gini():
    pass


class_attr = 'class_buys_computer'

# if __name__ == '__main__':
#     class_attr = 'class_buys_computer'
#     data = load_data()
#     print(get_entropy(data, class_attr))
#     print(get_condition_entropy(data, 'age'))
