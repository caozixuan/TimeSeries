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

from Util import bh_procedure2, Pro
def test_data(window_length, array_length, is_causal, is_linear, is_GMM, is_test_CUTE, noise):
    counter11 = 0
    counter10 = 0
    counter01 = 0
    counter00 = 0
    counter11_01 = 0
    counter10_01 = 0
    counter01_01 = 0
    counter00_01 = 0
    counter_undecided = 0
    counter_true = 0
    counter_false = 0
    p_array_CUTE1 = []
    p_array_CUTE2 = []
    p_array_improve_CUTE1 = []
    p_array_improve_CUTE2 = []
    p_array1 = []
    p_array2 = []

    pros1 = []
    pros2 = []

    pros_cute = []
    for i in range(0, 1000):
        if is_causal:
            lag = random.randint(1, 3)
            cause, effect = generate_continue_data(array_length, lag, noise)
            cause_tmp = list(cause)
            effect_tmp = list(effect)
            cause = zero_change(cause)
            effect = zero_change(effect)
            #cause = zero_change(cause)
            #effect = zero_change(effect)
            if not is_linear:
                for i in range(0, len(effect)):
                    effect[i] = math.exp(effect[i])
        else:
            lag = 5  # give a fixed lag if no causality
            if is_GMM:
                cause = GMM(3, array_length)
                effect = GMM(5, array_length)
            else:
                cause = np.random.standard_normal(array_length)
                effect = np.random.standard_normal(array_length)
            cause_tmp = list(cause)
            effect_tmp = list(effect)
            cause = zero_change(cause)
            effect = zero_change(effect)

        flag1 = False
        ce_p = granger(cause, effect, lag)
        ce_p_reverse = granger(effect[::-1], cause[::-1], lag)
        if ce_p < 0.05 and ce_p_reverse<0.05:
            flag1 = True
        flag2 = False
        ce2_p = granger(effect, cause, lag)
        ce2_p_reverse = granger(cause[::-1],effect[::-1],lag)
        if ce2_p < 0.05 and ce2_p_reverse<0.05:
            flag2 = True
        if flag1 and flag2:
            counter11 += 1
        elif flag1 and not flag2:
            counter10 += 1
        elif not flag1 and flag2:
            counter01 += 1
        elif not flag1 and not flag2:
            counter00 += 1
        if is_test_CUTE:
            cause2 = change_to_zero_one(cause)
            effect2 = change_to_zero_one(effect)
        else:
            cause2 = get_type_array_with_quantile(cause)
            effect2 = get_type_array_with_quantile(effect)
        flag3 = False
        ce3_p = granger(cause2, effect2, lag)
        ce3_p_reverse = granger(effect2[::-1], cause2[::-1], lag)
        if ce3_p < 0.05 and ce3_p_reverse<0.05:
            flag3 = True
        flag4 = False
        ce4_p = granger(effect2, cause2, lag)
        ce4_p_reverse = granger(cause2[::-1],effect2[::-1],lag)
        if ce4_p < 0.05 and ce4_p_reverse<0.05:
            flag4 = True
        if flag3 and flag4:
            counter11_01 += 1
        elif flag3 and not flag4:
            counter10_01 += 1
        elif not flag3 and flag4:
            counter01_01 += 1
        elif not flag3 and not flag4:
            counter00_01 += 1
        cause_tra = cause[::-1]
        effect_tra = effect[::-1]
        delta_ce = calculate_difference(cause, effect, window_length)
        delta_ec = calculate_difference(effect, cause, window_length)

        delta_ce2 = calculate_difference(effect_tra, cause_tra, window_length)
        delta_ec2 = calculate_difference(cause_tra, effect_tra, window_length)
        # print 'cause' + ' -> ' + 'effect' + ':' + str(delta_ce)
        # print 'effect' + ' -> ' + 'cause' + ':' + str(delta_ec)
        if delta_ce > delta_ec and delta_ce - delta_ec >= -math.log(0.05, 2):
            counter_true += 1
        elif delta_ec > delta_ce and delta_ec - delta_ce >= -math.log(0.05, 2):
            counter_false += 1
        else:
            counter_undecided += 1
        p = math.pow(2, -abs(delta_ce - delta_ec))
        p_tra = math.pow(2, -abs(delta_ce2 - delta_ec2))
        p_array1.append(p)
        element = Pro()
        element.p1 = p
        element.p2 = p_tra
        if delta_ce-delta_ec>0:
            element.direction1 = 0
        else:
            element.direction1 = 1
        if delta_ce2-delta_ec2>0:
            element.direction2 = 0
        else:
            element.direction2 = 1
        pros1.append(element)

        p = math.pow(2, -(delta_ec - delta_ce))
        p_tra = math.pow(2, -(delta_ec2 - delta_ce2))
        p_array1.append(p)
        element = Pro()
        element.p1 = p
        element.p2 = p_tra
        pros2.append(element)

        p_array2.append(math.pow(2, -(delta_ec - delta_ce)))
        cause = change_to_zero_one(cause_tmp)
        effect = change_to_zero_one(effect_tmp)
        cause2effect = bernoulli2(effect, window_length) - cbernoulli2(effect, cause, window_length)
        effect2cause = bernoulli2(cause, window_length) - cbernoulli2(cause, effect, window_length)
        cause2effect_reverse = bernoulli2(cause[::-1], window_length) - cbernoulli2(cause[::-1], effect[::-1], window_length)
        effect2cause_reverse = bernoulli2(effect[::-1], window_length) - cbernoulli2(effect[::-1], cause[::-1], window_length)
        p = math.pow(2, -abs(cause2effect - effect2cause))
        p_tra = math.pow(2, -abs(cause2effect_reverse - effect2cause_reverse))
        element = Pro()
        element.p1 = p
        element.p2 = p_tra
        if cause2effect - effect2cause > 0:
            element.direction1 = 0
        else:
            element.direction1 = 1
        if cause2effect_reverse - effect2cause_reverse > 0:
            element.direction2 = 0
        else:
            element.direction2 = 1
        pros_cute.append(element)
        p = math.pow(2, -(cause2effect - effect2cause))
        p_array_improve_CUTE1.append(p)
        p_array_improve_CUTE2.append(math.pow(2, -(effect2cause - cause2effect)))
        cause2effect = bernoulli(effect) - cbernoulli(effect, cause)
        effect2cause = bernoulli(cause) - cbernoulli(cause, effect)
        p_array_CUTE1.append(math.pow(2, -(cause2effect - effect2cause)))
        p_array_CUTE2.append(math.pow(2, -(effect2cause - cause2effect)))
    """
    print "Continuous data, Granger causality test:"
    print "Two-way causality:" + str(counter11)
    print "Correct causality:" + str(counter10)
    print "Wrong causality:" + str(counter01)
    print "No causality:" + str(counter00)
    print "-----------------"
    print "Encoding data, Granger causality test:"
    print "Two-way causality:" + str(counter11_01)
    print "Correct causality:" + str(counter10_01)
    print "Wrong causality:" + str(counter01_01)
    print "No causality:" + str(counter00_01)
    print "-----------------"
    print "Encoding data, Our test:"
    print "Correct cause and effect:" + str(counter_true)
    print "Wrong cause and effect:" + str(counter_false)
    print "Undecided:" + str(counter_undecided)
    print "-----------------"
    """

    if is_causal:
        ourmodel = bh_procedure(p_array1, 0.05)
        #cute = bh_procedure(p_array_CUTE1, 0.05)
        cute = bh_procedure2(pros_cute,0.05)/1000.0
        improve_cute = bh_procedure(p_array_improve_CUTE1, 0.05)
        #print "Origin CUTE Accuracy:" + str(cute)
        #print "Improved CUTE Accuracy:" + str(improve_cute)
        #print "Our model Accuracy:" + str(ourmodel)
        new_model = bh_procedure2(pros1,0.05)/1000.0
    else:
        #ourmodel = (bh_procedure(p_array1, 0.05) + bh_procedure(p_array2, 0.05)) / 1000.0
        #cute = (bh_procedure(p_array_CUTE1, 0.05) + bh_procedure(p_array_CUTE2, 0.05)) / 1000.0
        cute = 1-bh_procedure2(pros_cute, 0.05)/1000.0
        improve_cute = (bh_procedure(p_array_improve_CUTE1, 0.05) + bh_procedure(p_array_improve_CUTE2, 0.05)) / 1000.0
        #print "Origin CUTE Accuracy:" + str(1 - cute)
        #print "Improved CUTE Accuracy:" + str(1 - improve_cute)
        #print "Our model Accuracy:" + str(1 - ourmodel)
        new_model = 1-(bh_procedure2(pros1, 0.05)) / 1000.0
    dict = {}
    dict['granger'] = [counter10,counter00]
    dict['grangerD'] = [counter10_01,counter00_01]
    dict['disc2'] = [cute]
    dict['disc'] = [new_model]
    return dict


def granger_test2():
    counter = 0
    counter2 = 0
    for i in range(0,1001):
        cause, effect = generate_continue_data(300,3,0.1)
        ce_p = granger(cause, effect, 3)
        ce_p2 = granger(effect, cause, 3)
        flag1 = False
        if ce_p<0.05 and ce_p2>0.05:
            flag1 = True
            counter2+=1
        ce2_p = granger(effect[::-1], cause[::-1], 3)
        ce2_p2 = granger(cause[::-1], effect[::-1], 3)
        flag2 = False
        if ce2_p<0.05 and ce2_p2>0.05:
            flag2 = True
        if flag1 and flag2:
            counter+=1
    print(counter)
    print(counter2)



if __name__ == '__main__':
    dict = test_data(10, 600, 0, 0, 0, 0, 0.0)
    # ef test_data(window_length, array_length, is_causal, is_linear, is_GMM, is_test_CUTE, noise):
    #print(new_model)
    #granger_test2()
#real_data_test()
#test_change(5)
#granger_test()
#exchange_test()