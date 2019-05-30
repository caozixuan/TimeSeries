#encoding:utf-8
import xlrd
import math
import random
import time
import numpy as np
import matplotlib.pyplot as plt
from granger_test import granger
from data_generation import generate_continue_data, GMM,forward_shift_continue_data
from Util import zero_change, change_to_zero_one, get_type_array_with_quantile, get_type_array_with_quantile_change,bh_procedure
from Disc import calculate_difference, calculate_difference_with_weight_window, calculate_difference_with_weight,calculate_difference_with_quantile,calculate_difference_step
from cute import bernoulli, bernoulli2, cbernoulli, cbernoulli2
from statsmodels.tsa.stattools import grangercausalitytests
from synthetic_data_test import smooth,detect_segment


def granger_test():
    window_length = 4
    cause = np.random.normal(0, 1, 1000)
    effect =[]
    effect.append(random.random())
    effect.append(random.random())
    for i in range(2,1000):
        x =cause[i-1]+cause[i-2]+np.random.normal(0,0.1,1)[0]
        effect.append(x)
    a = []
    ans = []
    for i in range(0, window_length):
        ans.append([])
    cause = get_type_array_with_quantile(cause)
    effect = get_type_array_with_quantile(effect)
    for i in range(window_length, len(cause)):
        if effect[i] == 2:
            for j in range(1, window_length + 1):
                if effect[i - j] < cause[i - j]:
                    ans[j - 1].append(1)
                else:
                    ans[j - 1].append(0)
        elif effect[i] == 0:
            for j in range(1, window_length + 1):
                if effect[i - j] > cause[i - j]:
                    ans[j - 1].append(1)
                else:
                    ans[j - 1].append(0)
        else:
            for j in range(0, window_length):
                ans[j].append(0)
    results = []
    for i in range(0, window_length):
        results.append([])
        for j in range(0, len(ans[i])):
            if j == 0:
                results[i].append(ans[i][j])
            else:
                results[i].append(results[i][j - 1] + ans[i][j])
    for i in range(0, window_length):
        print sum(ans[i])

    for i in range(0, window_length):
        plt.plot(results[i])
    plt.show()
    ce = calculate_difference(cause,effect,4)
    ec = calculate_difference(effect,cause,4)
    print ce
    print ec
    a.append(effect)
    a.append(cause)
    a = np.array(a)
    grangercausalitytests(a,3)
    print len(effect)
    print len(cause)
    x1 = granger(cause,effect,1)
    x2 = granger(effect, cause, 1)
    print x1
    print x2
    x1 = granger(cause, effect, 2)
    x2 = granger(effect, cause, 2)
    print x1
    print x2
    x1 = granger(cause, effect, 3)
    x2 = granger(effect, cause, 3)
    print x1
    print x2


def read_csv():
    workbook = xlrd.open_workbook(r'2010.xlsx')
    sheet = workbook.sheet_by_name('2010')
    cols1 = sheet.col_values(1)[1:-1]
    cols2 = sheet.col_values(3)[1:-1]
    for i in range(0,len(cols1)):
        cols1[i] = 1.0/cols1[i]
        cols2[i] = 1.0 / cols2[i]
    return cols1,cols2


def read_excel():
    # 打开文件
    workbook = xlrd.open_workbook(r'price.xls')

    sheet2 = workbook.sheet_by_name('Corn-Time Series')
    sheet3 = workbook.sheet_by_name('Soybeans-Time Series')

    cols = sheet2.col_values(1)

    cols2 = sheet3.col_values(1)
    return cols[3:-1],cols2[3:-1]


def read_excel_corn():
    workbook = xlrd.open_workbook(r'Corn.xlsx')
    sheet = workbook.sheet_by_name('Sheet1')
    values = []
    results = []
    for i in range(1,13):
        cols = sheet.col_values(i)[38:-1]
        cols = cols[0:len(cols)]
        #print cols
        values.append(cols)
    for i in range(0, 12):
        for j in range(0, len(values[10])):
            results.append(values[i][j])
    return results


def read_excel_soybean():
    workbook = xlrd.open_workbook(r'Soybean.xlsx')
    sheet = workbook.sheet_by_name('Sheet1')
    values = []
    results = []
    for i in range(1,13):
        cols = sheet.col_values(i)[38:-1]
        cols = cols[0:len(cols)]
        #print cols
        values.append(cols)
    for i in range(0, 12):
        for j in range(0, len(values[10])):
            results.append(values[i][j])
    return results


def real_data_test():
    corn_1,soybean_1 = read_excel()
    corn_2 = read_excel_corn()
    tmp_corn_1 = corn_1
    tmp_corn_2 = corn_2
    soybean_2 = read_excel_soybean()
    tmp_soybean_1 = soybean_1
    tmp_soybean_2 = soybean_2
    corn_1 = zero_change(corn_1)
    corn_2 = zero_change(corn_2)
    soybean_1 = zero_change(soybean_1)
    soybean_2 = zero_change(soybean_2)
    x1 = granger(corn_1[150:250],corn_2[150:250],10)
    x2 = granger(corn_2[150:250], corn_1[150:250], 10)
    print x1
    print x2
    values = []
    causes = corn_1
    effects = corn_2

    for l in range(0, 7):
        values.append(0)
    delta_ces = calculate_difference_step(causes, effects, 6)
    delta_ecs = calculate_difference_step(effects, causes, 6)
    for i in range(0, len(delta_ces)):
        values.append(delta_ces[i] - delta_ecs[i])
    values = smooth(values, 20)
    pos_cau_start, pos_cau_end, neg_cau_start, neg_cau_end = detect_segment(values,20)
    print granger(causes,effects,3)
    for i in range(0,len(pos_cau_start)):
        tmp_x = []
        tmp_y = []
        for i in range(pos_cau_start[i],pos_cau_end[i]):
            tmp_x.append(i)
            tmp_y.append(0)
        plt.plot(tmp_x,tmp_y,c='r',linewidth=10.0)
    for i in range(0,len(neg_cau_start)):
        tmp_x = []
        tmp_y = []
        for i in range(neg_cau_start[i],neg_cau_end[i]):
            tmp_x.append(i)
            tmp_y.append(0)
        plt.plot(tmp_x,tmp_y,c='g',linewidth=10.0)
    plt.plot(values)
    #plt.plot(tmp_soybean_2)
    plt.show()

import pandas as pd
def test_change2(window_length):
    ans = []
    for i in range(0,window_length):
        ans.append([])
    #cause,effect = generate_continue_data(1000,3,0.1)
    cause =  np.random.normal(0, 1, 3000)
    effect = []
    effect.extend(np.random.normal(0, 1, 4))
    for i in range(4,1000):
        x = 0.5*effect[i-2] + 0.5*cause[i-4]
        effect.append(x)
    print cause
    print effect
    for i in range(1000,2000):
        x =-0.5*effect[i-2] + 0.5*cause[i-4]
        effect.append(x)
    for i in range(2000, 3000):
        x =0.5*cause[i-3]
        effect.append(x)
    print len(cause)
    print len(effect)
    #cause = zero_change(cause)
    #effect = zero_change(effect)
    cause = get_type_array_with_quantile(cause)
    effect = get_type_array_with_quantile(effect)
    #tmp = cause
    #cause = effect
    #effect = tmp
    print cause
    print effect
    for i in range(window_length,len(cause)):
        if effect[i]==2:
            #for j in range(1,window_length+1):
            #    if effect[i-j]<cause[i-j]:
            #        ans[j-1].append(1)
            #    else:
            #        ans[j-1].append(0)
            for j in range(1,window_length+1):
                if cause[i-j]==2:
                    ans[j-1].append(1)
                elif cause[i-j]==0:
                    ans[j - 1].append(-1)
                else:
                    ans[j-1].append(0)
        elif effect[i]==0:
            for j in range(1,window_length+1):
                if cause[i-j]==0:
                    ans[j-1].append(1)
                elif cause[i-j]==2:
                    ans[j - 1].append(-1)
                else:
                    ans[j-1].append(0)
        else:
            for j in range(0,window_length):
                ans[j].append(0)
            #continue
    results = []
    for i in range(0,window_length):
        results.append([])
        for j in range(0,len(ans[i])):
            if j==0:
                results[i].append(ans[i][j])
            else:
                results[i].append(results[i][j-1]+ans[i][j])
    #for i in range(0,window_length):
        #print sum(ans[i])
    sum = 0
    for i in range(0,len(results[0])):
        x = results[0][i]+results[1][i]+results[2][i]+results[3][i]+results[4][i]
        print x
        sum+=x
    for i in range(0,window_length):
        plt.plot(results[i])
        #print results[i]
        #f = open('normal'+str(i+1), 'w')
        #for x in  results[i]:
        #    print >> f, x
        #    print x
    plt.legend(['W1','W2','W3','W4','W5','W6'])
    plt.savefig("complex.eps")
    plt.show()


def test_change(window_length):
    ans = []
    for i in range(0,window_length):
        ans.append([])
    #cause,effect = generate_continue_data(1000,3,0.1)
    cause =  np.random.normal(0, 1, 3000)
    effect = []
    effect.extend(np.random.normal(0, 1, 4))
    for i in range(4,1000):
        x = -0.5*cause[i-3] + 0.5*cause[i-4]
        effect.append(x)
    print cause
    print effect
    for i in range(1000,2000):
        x =0.5*cause[i-1] + 0.5*cause[i-4]
        effect.append(x)
    for i in range(2000, 3000):
        x =cause[i-3]
        effect.append(x)
    print len(cause)
    print len(effect)
    #cause = zero_change(cause)
    #effect = zero_change(effect)
    cause = get_type_array_with_quantile(cause)
    effect = get_type_array_with_quantile(effect)
    #tmp = cause
    #cause = effect
    #effect = tmp
    print cause
    print effect
    for i in range(window_length,len(cause)):
        if effect[i]==2:
            for j in range(1,window_length+1):
                if effect[i-j]<cause[i-j]:
                    ans[j-1].append(1)
                elif effect[i-j]==cause[i-j]:
                    ans[j - 1].append(5.0/16.0)
                else:
                    ans[j-1].append(0)
        elif effect[i]==0:
            for j in range(1,window_length+1):
                if effect[i-j]>cause[i-j]:
                    ans[j-1].append(1)
                elif effect[i-j]==cause[i-j]:
                    ans[j - 1].append(5.0 / 16.0)
                else:
                    ans[j-1].append(0)
        else:
            for j in range(0,window_length):
                ans[j].append(5.0/16.0)
            #continue
    results = []
    for i in range(0,window_length):
        results.append([])
        for j in range(0,len(ans[i])):
            if j==0:
                results[i].append(ans[i][j]-5.0/16.0)
            else:
                results[i].append(results[i][j-1]+ans[i][j]-5.0/16.0)
    #for i in range(0,window_length):
        #print sum(ans[i])
    sum = 0
    for i in range(0,len(results[0])):
        x = results[0][i]+results[1][i]+results[2][i]+results[3][i]+results[4][i]
        print x
        sum+=x
    for i in range(0,window_length):
        plt.plot(results[i])
        #print results[i]
        #f = open('normal'+str(i+1), 'w')
        #for x in  results[i]:
        #    print >> f, x
        #    print x
    plt.legend(['W1','W2','W3','W4','W5','W6'])
    plt.savefig("complex.eps")
    plt.show()

def exchange_test():
    cause2,effect2 = read_csv()
    cause = []
    effect = []
    for i in range(0,len(cause2)):
        if i%4==0:
            cause.append(cause2[i])
            effect.append(effect2[i])
    tmp_cause = cause
    tmp_effect = effect
    cause = zero_change(cause)
    effect = zero_change(effect)
    x1 = granger(cause,effect,-1)
    x2 = granger(effect,cause,-1)
    print x1
    print x2
    x1 = granger(cause[1400:1700], effect[1400:1700], 10)
    x2 = granger(effect[1400:1700], cause[1400:1700], 10)
    print x1
    print x2
    values = []
    for l in range(0, 51):
        values.append(0)
    delta_ces = calculate_difference_step(cause, effect, 10)
    delta_ecs = calculate_difference_step(effect, cause, 10)
    for i in range(0, len(delta_ces)):
        values.append(delta_ces[i] - delta_ecs[i])
    values = smooth(values, 50)
    pos_cau_start, pos_cau_end, neg_cau_start, neg_cau_end = detect_segment(values,100)
    for i in range(0,len(pos_cau_start)):
        start = pos_cau_start[i]
        end = pos_cau_end[i]
        x1 = granger(cause[start:end], effect[start:end], -1)
        x2 = granger(effect[start:end], cause[start:end], -1)
        print x1
        print x2
        print '-----------------'
    print 'neg'
    for i in range(0,len(neg_cau_start)):
        start = neg_cau_start[i]
        end = neg_cau_end[i]
        x1 = granger(cause[start:end], effect[start:end], -1)
        x2 = granger(effect[start:end], cause[start:end], -1)
        print x1
        print x2
        print '-----------------'
    #print granger(causes,effects,3)
    for i in range(0,len(pos_cau_start)):
        tmp_x = []
        tmp_y = []
        for j in range(pos_cau_start[i],pos_cau_end[i]):
            tmp_x.append(j)
            tmp_y.append(0)
        plt.plot(tmp_x,tmp_y,c='r',linewidth=5.0)
    for i in range(0,len(neg_cau_start)):
        tmp_x = []
        tmp_y = []
        for j in range(neg_cau_start[i],neg_cau_end[i]):
            tmp_x.append(j)
            tmp_y.append(0)
        plt.plot(tmp_x,tmp_y,c='g',linewidth=5.0)
    plt.plot(tmp_cause)
    plt.plot(tmp_effect)

    plt.show()


#real_data_test()
test_change(5)
#granger_test()
#exchange_test()