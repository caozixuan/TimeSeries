import math
import random
import time
import numpy as np
import matplotlib.pyplot as plt
from granger_test import granger
from data_generation import generate_continue_data, GMM,forward_shift_continue_data
from Util import zero_change, change_to_zero_one, get_type_array_with_quantile, get_type_array_with_quantile_change,bh_procedure,get_type_array_with_quantile_change2
from Disc import calculate_difference, calculate_difference_with_weight_window, calculate_difference_with_quantile2,calculate_difference_with_weight,calculate_difference_with_quantile,calculate_difference_step
from cute import bernoulli, bernoulli2, cbernoulli, cbernoulli2






"""
window_length: the size of window
array_length: the length of tested array
is_causal: is causality test
is_linear: in causality test, if the cause and effect data is linear related
is_GMM: is data generated by GMM
is_test_CUTE: is test CUTE encoding consistency
noise: the standard deviation of noise:0.1, 0.2, 0.3
"""
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
    for i in range(0, 1000):
        if is_causal:
            lag = 10 #random.randint(1, 3)
            cause, effect = generate_continue_data(array_length, lag, noise)
            cause_tmp = list(cause)
            effect_tmp = list(effect)
            cause = zero_change(cause)
            effect = zero_change(effect)
            if not is_linear:
                for i in range(0, len(effect)):
                    effect[i] = math.tanh(effect[i])
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
        if ce_p < 0.05:
            flag1 = True
        flag2 = False
        ce2_p = granger(effect, cause, lag)
        if ce2_p < 0.05:
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
        if ce3_p < 0.05:
            flag3 = True
        flag4 = False
        ce4_p = granger(effect2, cause2, lag)
        if ce4_p < 0.05:
            flag4 = True
        if flag3 and flag4:
            counter11_01 += 1
        elif flag3 and not flag4:
            counter10_01 += 1
        elif not flag3 and flag4:
            counter01_01 += 1
        elif not flag3 and not flag4:
            counter00_01 += 1
        delta_ce = calculate_difference(cause, effect, window_length)
        delta_ec = calculate_difference(effect, cause, window_length)
        # print 'cause' + ' -> ' + 'effect' + ':' + str(delta_ce)
        # print 'effect' + ' -> ' + 'cause' + ':' + str(delta_ec)
        if delta_ce > delta_ec and delta_ce - delta_ec >= -math.log(0.05, 2):
            counter_true += 1
        elif delta_ec > delta_ce and delta_ec - delta_ce >= -math.log(0.05, 2):
            counter_false += 1
        else:
            counter_undecided += 1
        p = math.pow(2, -(delta_ce - delta_ec))
        p_array1.append(p)
        p_array2.append(math.pow(2, -(delta_ec - delta_ce)))
        cause = change_to_zero_one(cause_tmp)
        effect = change_to_zero_one(effect_tmp)
        cause2effect = bernoulli2(effect, window_length) - cbernoulli2(effect, cause, window_length)
        effect2cause = bernoulli2(cause, window_length) - cbernoulli2(cause, effect, window_length)
        p = math.pow(2, -(cause2effect - effect2cause))
        p_array_improve_CUTE1.append(p)
        p_array_improve_CUTE2.append(math.pow(2, -(effect2cause - cause2effect)))
        cause2effect = bernoulli(effect) - cbernoulli(effect, cause)
        effect2cause = bernoulli(cause) - cbernoulli(cause, effect)
        p_array_CUTE1.append(math.pow(2, -(cause2effect - effect2cause)))
        p_array_CUTE2.append(math.pow(2, -(effect2cause - cause2effect)))
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
    if is_causal:
        ourmodel = bh_procedure(p_array1, 0.05)
        cute = bh_procedure(p_array_CUTE1, 0.05)
        improve_cute = bh_procedure(p_array_improve_CUTE1, 0.05)
        print "Origin CUTE Accuracy:" + str(cute)
        print "Improved CUTE Accuracy:" + str(improve_cute)
        print "Our model Accuracy:" + str(ourmodel)
    else:
        ourmodel = (bh_procedure(p_array1, 0.05) + bh_procedure(p_array2, 0.05)) / 1000.0
        cute = (bh_procedure(p_array_CUTE1, 0.05) + bh_procedure(p_array_CUTE2, 0.05)) / 1000.0
        improve_cute = (bh_procedure(p_array_improve_CUTE1, 0.05) + bh_procedure(p_array_improve_CUTE2, 0.05)) / 1000.0
        print "Origin CUTE Accuracy:" + str(1 - cute)
        print "Improved CUTE Accuracy:" + str(1 - improve_cute)
        print "Our model Accuracy:" + str(1 - ourmodel)
    return cute, improve_cute, ourmodel


def test_linear_data():
    noises = [0.0, 0.1, 0.2, 0.3]
    for noise in noises:
        test_data(6, 150, 1, 1, 0, 0, noise)
    for noise in noises:
        test_data(7, 250, 1, 1, 0, 0, noise)
    for noise in noises:
        test_data(8, 350, 1, 1, 0, 0, noise)
    for noise in noises:
        test_data(9, 450, 1, 1, 0, 0, noise)


def test_window_length_effect():
    start = 5
    end = 20
    result = []
    for i in range(start,end+1):
        x,y,z=test_data(i, 450, 1, 1, 0, 0, 0.1)
        result.append(z)
    print result


def test_non_linear():
    noises = [0.0, 0.1, 0.2, 0.3]
    for noise in noises:
        test_data(6, 150, 1, 0, 0, 0, noise)
    for noise in noises:
        test_data(7, 250, 1, 0, 0, 0, noise)
    for noise in noises:
        test_data(8, 350, 1, 0, 0, 0, noise)
    for noise in noises:
        test_data(9, 450, 1, 0, 0, 0, noise)


def test_no_causality_consistency():
    test_data(6, 150, 0, 0, 0, 0, 0)
    test_data(7, 250, 0, 0, 0, 0, 0)
    test_data(8, 350, 0, 0, 0, 0, 0)
    test_data(9, 450, 0, 0, 0, 0, 0)

    #test_data(6, 150, 0, 0, 0, 1, 0)
    #test_data(7, 250, 0, 0, 0, 1, 0)
    #test_data(8, 350, 0, 0, 0, 1, 0)
    #test_data(9, 450, 0, 0, 0, 1, 0)


def test_causality_consistency():
    test_data(6, 150, 1, 1, 0, 0, 0)
    test_data(7, 250, 1, 1, 0, 0, 0)
    test_data(8, 350, 1, 1, 0, 0, 0)
    test_data(9, 450, 1, 1, 0, 0, 0)

    test_data(6, 150, 1, 1, 0, 1, 0)
    test_data(7, 250, 1, 1, 0, 1, 0)
    test_data(8, 350, 1, 1, 0, 1, 0)
    test_data(9, 450, 1, 1, 0, 1, 0)


def time_test_window(array_length, window_size):
    for i in range(0, 10):
        cause, effect = generate_continue_data(array_length, 3, 0)
        cause = zero_change(cause)
        effect = zero_change(effect)
        cause2effect = calculate_difference(cause, effect, window_size)
        effect2cause = calculate_difference(effect, cause, window_size)


def time_test_weighted_window(array_length, window_size):
    for i in range(0, 10):
        cause, effect = generate_continue_data(array_length, 3, 0)
        cause = zero_change(cause)
        effect = zero_change(effect)
        cause2effect = calculate_difference_with_weight_window(cause, effect, 0.7, window_size)
        effect2cause = calculate_difference_with_weight_window(effect, cause, 0.7, window_size)


def time_test_weighted(array_length, window_size):
    for i in range(0, 10):
        cause, effect = generate_continue_data(array_length, 3, 0)
        cause = zero_change(cause)
        effect = zero_change(effect)
        cause2effect = calculate_difference_with_weight(cause, effect, window_size)
        effect2cause = calculate_difference_with_weight(effect, cause, window_size)


def time_window():
    times = []
    xs = []
    for i in range(100, 5000, 100):
        xs.append(i / 100)
        start = time.clock()
        time_test_window(i, 6)
        end = time.clock()
        times.append((end - start) / 10)
    plt.plot(xs, times)
    plt.xlabel("Length($\\times10^2$)")
    plt.ylabel("Time Per Series(/s)")
    plt.show()


def time_weighted():
    times = []
    xs = []
    for i in range(100, 2000, 100):
        xs.append(i / 100)
        start = time.clock()
        time_test_weighted(i, 6)
        end = time.clock()
        times.append((end - start) / 10)
    plt.plot(xs, times)
    plt.xlabel("Length($\\times10^2$)")
    plt.ylabel("Time Per Series(/s)")
    plt.show()


def time_weighted_window():
    times = []
    xs = []
    for i in range(100, 5000, 100):
        xs.append(i / 100)
        start = time.clock()
        time_test_weighted(i, 6)
        end = time.clock()
        times.append((end - start) / 10)
    plt.plot(xs, times)
    plt.xlabel("Length($\\times10^2$)")
    plt.ylabel("Time Per Series(/s)")
    plt.show()


def test_window(length,shift):
    causes = []
    effects = []
    results = []
    for i in range(0,1000):
        cause, effect = generate_continue_data(length,shift,0.0)
        cause = zero_change(cause)
        effect = zero_change(effect)
        cause = zero_change(cause)
        effect = zero_change(effect)
        #cause2 = get_type_array_with_quantile(cause)
        #effect2 = get_type_array_with_quantile(effect)
        causes.append(cause)
        effects.append(effect)

    for j in range(3,26):
        p_array = []
        for i in range(0,len(causes)):
            cause = causes[i]
            effect = effects[i]
            delta_ce = calculate_difference(cause, effect, j)
            delta_ec = calculate_difference(effect, cause, j)
            p = math.pow(2, -(delta_ce - delta_ec))
            p_array.append(p)
        ourmodel = bh_procedure(p_array, 0.05)
        results.append(ourmodel/1000.0)
    print results


def test_window_granger(length,shift):
    causes = []
    effects = []
    results11 = []
    results10 = []
    results01 = []
    results00 = []
    for i in range(0,1000):
        cause, effect = generate_continue_data(length,shift,0.0)
        #effect, effect2 = generate_continue_data(length, shift, 0.1)
        cause = zero_change(cause)
        effect = zero_change(effect)
        #cause2 = get_type_array_with_quantile(cause)
        #effect2 = get_type_array_with_quantile(effect)
        causes.append(cause)
        effects.append(effect)

    for j in range(3,26):
        counter11 = 0
        counter10=0
        counter01 = 0
        counter00 = 0
        for i in range(0,len(causes)):
            cause = causes[i]
            effect = effects[i]
            flag1 = False
            ce_p = granger(cause, effect, j)
            if ce_p < 0.05:
                flag1 = True
            flag2 = False
            ce2_p = granger(effect, cause, j)
            if ce2_p < 0.05:
                flag2 = True
            if flag1 and flag2:
                counter11 += 1
            elif flag1 and not flag2:
                counter10 += 1
            elif not flag1 and flag2:
                counter01 += 1
            elif not flag1 and not flag2:
                counter00 += 1
        results11.append(counter11/1000.0)
        results01.append(counter01/1000.0)
        results10.append(counter10/1000.0)
        results00.append(counter00/1000.0)
    return results11,results10,results01,results00

def test_icute_window(length,shift):
    causes = []
    effects = []
    results = []
    for i in range(0, 1000):
        cause, effect = generate_continue_data(length, shift, 0.1)
        cause = zero_change(cause)
        effect = zero_change(effect)
        # cause2 = get_type_array_with_quantile(cause)
        # effect2 = get_type_array_with_quantile(effect)
        causes.append(cause)
        effects.append(effect)

    for j in range(3, 26):
        p_array = []
        for i in range(0, len(causes)):
            cause = change_to_zero_one(causes[i])
            effect = change_to_zero_one(effects[i])
            cause2effect = bernoulli2(effect, j) - cbernoulli2(effect, cause, j)
            effect2cause = bernoulli2(cause, j) - cbernoulli2(cause, effect, j)
            p = math.pow(2, -(cause2effect - effect2cause))
            p_array.append(p)
        icute = bh_procedure(p_array, 0.05)
        results.append(icute / 1000.0)
    print results


from random import choice

def test_change_window():
    lengths = [150,250,350,450]
    lags = [1,2,3,4,5,6,7]
    segments = [2,3,4,5]
    causes = []
    effects = []
    for k in range(0,1000):
        cause = []
        effect = []
        num = choice(segments)
        for i in range(0,num):
            c, e = generate_continue_data(choice(lengths), choice(lags), 0.1)
            c = zero_change(c)
            e = zero_change(e)
            cause.extend(c)
            effect.extend(e)
        causes.append(cause)
        effects.append(effect)
    p_array = []
    for i in range(0, len(causes)):
        cause = causes[i]
        effect = effects[i]
        delta_ce = calculate_difference(cause, effect, 10)
        delta_ec = calculate_difference(effect, cause, 10)
        p = math.pow(2, -(delta_ce - delta_ec))
        p_array.append(p)
    ourmodel = bh_procedure(p_array, 0.05)
    print ourmodel


def test_change_window_icute():
    lengths = [150, 250, 350, 450]
    lags = [1, 2, 3, 4, 5, 6, 7]
    segments = [2, 3, 4, 5]
    causes = []
    effects = []
    for k in range(0, 1000):
        cause = []
        effect = []
        num = choice(segments)
        for i in range(0, num):
            c, e = generate_continue_data(choice(lengths), choice(lags), 0.1)
            c = zero_change(c)
            e = zero_change(e)
            cause.extend(c)
            effect.extend(e)
        causes.append(cause)
        effects.append(effect)
    p_array = []
    for i in range(0, len(causes)):
        cause = change_to_zero_one(causes[i])
        effect = change_to_zero_one(effects[i])
        cause2effect = bernoulli2(effect, 10) - cbernoulli2(effect, cause, 10)
        effect2cause = bernoulli2(cause, 10) - cbernoulli2(cause, effect, 10)
        p = math.pow(2, -(cause2effect - effect2cause))
        p_array.append(p)
    icute = bh_procedure(p_array, 0.05)
    print icute


def test_change_window_granger():
    lengths = [150, 250, 350, 450]
    lags = [1, 2, 3, 4, 5, 6, 7]
    segments = [2, 3, 4, 5]
    causes = []
    effects = []
    for k in range(0, 1000):
        cause = []
        effect = []
        num = choice(segments)
        for i in range(0, num):
            c, e = generate_continue_data(choice(lengths), choice(lags), 0.1)
            c = zero_change(c)
            e = zero_change(e)
            cause.extend(c)
            effect.extend(e)
        causes.append(cause)
        effects.append(effect)
    p_array = []
    counter11 =0
    counter10 = 0
    counter01 = 0
    counter00 = 0
    for i in range(0, len(causes)):
        cause = causes[i]
        effect = effects[i]
        flag1 = False
        ce_p = granger(cause, effect, -1)
        if ce_p < 0.05:
            flag1 = True
        flag2 = False
        ce2_p = granger(effect, cause, -1)
        if ce2_p < 0.05:
            flag2 = True
        if flag1 and flag2:
            counter11 += 1
        elif flag1 and not flag2:
            counter10 += 1
        elif not flag1 and flag2:
            counter01 += 1
        elif not flag1 and not flag2:
            counter00 += 1
    print counter11
    print counter10
    print counter01
    print counter00

def test_coding(length,window_length):
    causes = []
    effects = []
    results = []
    for i in range(0,1000):
        #cause, effect2 = generate_continue_data(length,random.randint(1,3),0.0)
        #effect, effect3 = generate_continue_data(length, random.randint(1, 3), 0.0)
        cause = np.random.standard_normal(length)
        effect = np.random.standard_normal(length)
        cause = zero_change(cause)
        effect = zero_change(effect)
        cause = zero_change(cause)
        effect = zero_change(effect)
        causes.append(cause)
        effects.append(effect)
    qs = [0.05,0.1,0.15,0.20,0.25,0.30,0.35,0.40,0.45]
    for q in qs:
        p_array = []
        p_array2 = []
        for i in range(0,len(causes)):
            cause = causes[i]
            effect = effects[i]
            delta_ce = calculate_difference_with_quantile(cause, effect, window_length,q)
            delta_ec = calculate_difference_with_quantile(effect, cause, window_length,q)
            p = math.pow(2, -(delta_ce - delta_ec))
            p_array.append(p)
            p2 = math.pow(2, -(delta_ec - delta_ce))
            p_array2.append(p2)
        #ourmodel = bh_procedure(p_array, 0.05)
        ourmodel = (bh_procedure(p_array, 0.05) + bh_procedure(p_array2, 0.05)) / 1000.0
        results.append(ourmodel)
    print results


def test_coding2(length,window_length):
    causes = []
    effects = []
    results = []
    for i in range(0,1000):
        cause, effect2 = generate_continue_data(length,random.randint(1,3),0.1)
        effect, effect3 = generate_continue_data(length, random.randint(1, 3), 0.1)
        cause = zero_change(cause)
        effect = zero_change(effect)
        cause = zero_change(cause)
        effect = zero_change(effect)
        causes.append(cause)
        effects.append(effect)
    qs = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    for q in qs:
        p_array = []
        for i in range(0,len(causes)):
            cause = causes[i]
            effect = effects[i]
            delta_ce = calculate_difference_with_quantile2(cause, effect, window_length,q)
            delta_ec = calculate_difference_with_quantile2(effect, cause, window_length,q)
            p = math.pow(2, -(delta_ce - delta_ec))
            p_array.append(p)
        ourmodel = bh_procedure(p_array, 0.05)
        results.append(1-ourmodel/1000.0)
    print results

def test_motivation(length):
    p_array = []
    counter =0
    for i in range(0,1000):
        x1 = np.random.normal(0, 1, length)
        x2 = np.random.normal(0, 1, length)
        y = []
        for j in range(0,length):
            y.append(x1[j]+x2[j])
        forward_shift_continue_data(y,5)
        delta_ce = calculate_difference(x1, y, 10)
        delta_ec = calculate_difference(y, x1, 10)
        p = math.pow(2, -(delta_ce - delta_ec))
        p_array.append(p)
        if p<=0.5:
            counter+=1
    outmodel = bh_procedure(p_array,0.05)
    print outmodel
    print counter


def smooth(values,window):
    ans =[]
    left = window/2
    right = window /2
    for i in range(0,len(values)):
        if i<left or i >= len(values)-right:
            ans.append(values[i])
        else:
            value = 0
            for w in range(1,left+1):
                value +=values[i-w]
            for w in range(1,right+1):
                value+=values[i+w]
            value+=values[i]
            value = value/(left+right+1)
            ans.append(value)
    return ans


def detect_segment(values,min_length):
    delta = -math.log(0.05
                      ,2)
    pos_cau_start = []
    pos_cau_end = []
    neg_cau_start = []
    neg_cau_end = []
    i = 1
    difference = 0
    start = 0
    end = 1
    if values[start]<values[end]:
        up = True
    else:
        up = False
    while i<len(values):
        if up:
            if values[i]>values[i-1]:
                end = i
                difference = values[end]-values[start]
            else:
                if (abs(difference) > delta) and end-start>min_length:
                    pos_cau_start.append(start)
                    pos_cau_end.append(end)
                start = i-1
                end = i

                up = False
                difference = values[end]-values[start]
        else:
            if values[i]<values[i-1]:
                end = i
                difference = values[end]-values[start]
            else:
                if (abs(difference) > delta) and end-start>min_length:
                    neg_cau_start.append(start)
                    neg_cau_end.append(end)
                start = i-1
                end = i

                up = True
                difference = values[end] - values[start]
        i+=1
    if (abs(difference) > delta) and end - start > min_length:
        if difference<0:
            neg_cau_start.append(start)
            neg_cau_end.append(end)
        else:
            pos_cau_start.append(start)
            pos_cau_end.append(end)
    print pos_cau_start
    print pos_cau_end
    print neg_cau_start
    print neg_cau_end
    return pos_cau_start,pos_cau_end,neg_cau_start,neg_cau_end


# Definition for an interval.
class Interval:
     def __init__(self, s=0, e=0):
         self.start = s
         self.end = e


def intervalIntersection(A,B):
    m = len(A)
    n = len(B)
    res = []
    i = 0
    j = 0
    while i < m and j < n:
        left = max(A[i].start, B[j].start)
        if A[i].end < B[j].end:
            right = A[i].end
            i += 1
        else:
            right = B[j].end
            j += 1
        if left <= right:
            res.append(Interval(left, right))
    return res

def test_segment_causality():
    c = [0,1,0,1,0,1]
    causes = []
    effects2 = []
    tmp_causes = []
    tmp_effects2 = []
    effects = []
    causes2 = []
    tmp_effects = []
    tmp_causes2 = []
    values = []
    for i in c:
        if i==0:
            cause, xx = generate_continue_data(1000, random.randint(1, 3), 0.1)
            effect, xx = generate_continue_data(1000, random.randint(1, 3), 0.1)
            tmp_causes.extend(cause)
            tmp_effects.extend(effect)
            cause = zero_change(cause)
            effect = zero_change(effect)
            causes.extend(cause)
            effects.extend(effect)
        else:
            cause, effect = generate_continue_data(1000, random.randint(1, 3), 0.1)
            tmp_causes.extend(cause)
            tmp_effects.extend(effect)
            cause = zero_change(cause)
            effect = zero_change(effect)
            causes.extend(cause)
            effects.extend(effect)
    causes2= causes[::-1]
    effects2 = effects[::-1]
    for l in range(0,7):
        values.append(0)
    print tmp_causes
    print tmp_effects
    f = open('tmp_causes2', 'w')
    for x in tmp_causes:
        print >> f,x
        print x
    f.close()
    f = open('tmp_effects2', 'w')
    for x in tmp_effects:
        print >> f, x
        #print x
    f.close()
    delta_ces = calculate_difference_step(causes, effects, 6)
    delta_ecs = calculate_difference_step(effects, causes, 6)
    for i in range(0,len(delta_ces)):
        values.append(delta_ces[i]-delta_ecs[i])
    values = smooth(values,50)
    f = open('values2', 'w')
    for x in values:
        print >> f, x
        #print x
    f.close()
    pos_cau_start, pos_cau_end, neg_cau_start, neg_cau_end = detect_segment(values,100)
    As = []
    for i in range(0, len(pos_cau_start)):
        As.append(Interval(pos_cau_start[i], pos_cau_end[i]))
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
        for i in range(neg_cau_start[i],neg_cau_end[i]):
            tmp_x.append(i)
            tmp_y.append(0)
        plt.plot(tmp_x,tmp_y,c='g',linewidth=5.0)
    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 23,
             }
    plt.plot(tmp_causes,label="cause")
    plt.plot(tmp_effects,label="effect")
    plt.xlabel("x",font1)
    plt.ylabel("y",font1)
    foo_fig = plt.gcf()  # 'get current figure'
    foo_fig.savefig('dy.eps', format='eps')
    plt.show()
    for i in range(0,len(pos_cau_start)):
        tmp_x = []
        tmp_y = []
        for i in range(pos_cau_start[i],pos_cau_end[i]):
            tmp_x.append(i)
            tmp_y.append(0)
        plt.plot(tmp_x,tmp_y,c='r',linewidth=5.0)
    for i in range(0,len(neg_cau_start)):
        tmp_x = []
        tmp_y = []
        for i in range(neg_cau_start[i],neg_cau_end[i]):
            tmp_x.append(i)
            tmp_y.append(0)
        plt.plot(tmp_x,tmp_y,c='g',linewidth=5.0)
    plt.xlabel("x",font1)
    plt.ylabel('$\Delta$',font1)
    plt.plot(values)
    foo_fig = plt.gcf()  # 'get current figure'
    foo_fig.savefig('dy_v.eps', format='eps')
    print len(tmp_causes)
    print len(tmp_effects)
    plt.show()

    values = []
    delta_ces = calculate_difference_step(effects2, causes2, 6)
    delta_ecs = calculate_difference_step(causes2, effects2, 6)
    for i in range(0, len(delta_ces)):
        values.append(delta_ces[i] - delta_ecs[i])
    values = values[::-1]
    values = smooth(values, 50)
    f = open('values2', 'w')
    for x in values:
        print >> f, x
        #print x
    f.close()
    pos_cau_start, pos_cau_end, neg_cau_start, neg_cau_end = detect_segment(values, 100)
    Bs = []
    for i in range(0,len(neg_cau_start)):
        Bs.append(Interval(neg_cau_start[i],neg_cau_end[i]))


    for i in range(0, len(pos_cau_start)):
        tmp_x = []
        tmp_y = []
        for j in range(pos_cau_start[i], pos_cau_end[i]):
            tmp_x.append(j)
            tmp_y.append(0)
        plt.plot(tmp_x, tmp_y, c='r', linewidth=5.0)
    for i in range(0, len(neg_cau_start)):
        tmp_x = []
        tmp_y = []
        for i in range(neg_cau_start[i], neg_cau_end[i]):
            tmp_x.append(i)
            tmp_y.append(0)
        plt.plot(tmp_x, tmp_y, c='g', linewidth=5.0)
    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 23,
             }
    plt.plot(tmp_causes, label="cause")
    plt.plot(tmp_effects, label="effect")
    plt.xlabel("x", font1)
    plt.ylabel("y", font1)
    foo_fig = plt.gcf()  # 'get current figure'
    foo_fig.savefig('dy.eps', format='eps')
    plt.show()
    for i in range(0, len(pos_cau_start)):
        tmp_x = []
        tmp_y = []
        for i in range(pos_cau_start[i], pos_cau_end[i]):
            tmp_x.append(i)
            tmp_y.append(0)
        plt.plot(tmp_x, tmp_y, c='r', linewidth=5.0)
    for i in range(0, len(neg_cau_start)):
        tmp_x = []
        tmp_y = []
        for i in range(neg_cau_start[i], neg_cau_end[i]):
            tmp_x.append(i)
            tmp_y.append(0)
        plt.plot(tmp_x, tmp_y, c='g', linewidth=5.0)
    plt.xlabel("x", font1)
    plt.ylabel('$\Delta$', font1)
    plt.plot(values)
    foo_fig = plt.gcf()  # 'get current figure'
    foo_fig.savefig('dy_v.eps', format='eps')
    print len(tmp_causes)
    print len(tmp_effects)
    plt.show()
    res = intervalIntersection(As,Bs)
    for i in res:
        print str(i.start) + " " + str(i.end)
    s1 = Interval(1000,2000)
    s2 = Interval(3000, 4000)
    s3 = Interval(5000, 6000)

    s4 = Interval(0, 1000)
    s5 = Interval(2000, 3000)
    s6 = Interval(4000, 5000)
    cau_seg = [s1,s2,s3]
    no_cau_seg = [s4, s5, s6]
    total_recall_points = 0
    res2 = intervalIntersection(cau_seg,As)
    for i in res2:
        total_recall_points= total_recall_points+i.end-i.start
    print total_recall_points/3000.0
    total_wrong_points = 0
    res3 = intervalIntersection(no_cau_seg,As)
    for i in res3:
        print str(i.start) + " " + str(i.end)
    for i in res3:
        total_wrong_points= total_wrong_points+i.end-i.start
    print 1-total_wrong_points/3000.0







if __name__ == '__main__':
    #test_causality_consistency()
    #test_no_causality_consistency()

    #test_linear_data()
    #test_non_linear()
    #test_coding2(150,6)
    #test_coding2(250, 7)
    #test_coding2(350, 8)
    #test_coding2(450, 9)
    #time_window()
    #time_weighted()
    #time_weighted_window()
    #results11,result10,result01,results00 = test_window_granger(240,5)
    test_segment_causality()
    #test_window_length_effect()

    #test_motivation(2850)
    for i in range(3,11):
        print "***********"+str(i)+"*****************"
        test_window(150,i)
        test_window(250, i)
        test_window(350,i)
        test_window(450, i)
        test_window(550, i)
        test_window(650, i)
        test_window(750, i)
        test_window(850, i)
        #test_icute_window(150,i)
        #test_icute_window(250, i)
        #test_icute_window(350, i)
        #test_icute_window(450, i)
        #test_icute_window(550, i)
        #test_icute_window(650, i)
        #test_icute_window(750, i)
        #test_icute_window(850, i)
        """
        results11, result10, result01, results00 = test_window_granger(150, i)
        print results11
        print result10
        print result01
        print results00
        print "-------------------------------------------"
        results11, result10, result01, results00 = test_window_granger(250, i)
        print results11
        print result10
        print result01
        print results00
        print "-------------------------------------------"
        results11, result10, result01, results00 = test_window_granger(350, i)
        print results11
        print result10
        print result01
        print results00
        print "-------------------------------------------"
        results11, result10, result01, results00 = test_window_granger(450, i)
        print results11
        print result10
        print result01
        print results00
        print "-------------------------------------------"
        results11, result10, result01, results00 = test_window_granger(550, i)
        print results11
        print result10
        print result01
        print results00
        print "-------------------------------------------"
        results11, result10, result01, results00 = test_window_granger(650, i)
        print results11
        print result10
        print result01
        print results00
        print "-------------------------------------------"
        results11, result10, result01, results00 = test_window_granger(750, i)
        print results11
        print result10
        print result01
        print results00
        print "-------------------------------------------"
        results11, result10, result01, results00 = test_window_granger(850, i)
        print results11
        print result10
        print result01
        print results00
        print "-------------------------------------------"
"""
    #test_change_window()
    #test_change_window_icute()
    test_change_window_granger()
    #test_coding(150,6)
    #test_coding(250, 7)
    #test_coding(350, 8)
    #test_coding(450, 9)

