import math
import numpy as np
from collections import defaultdict


def lg(x):
    res = 0
    try:
        res = math.log(x, 2)
    except ValueError:
        pass
    return res


def exp(x):
    return 2 ** x


class Pro(object):
    def __init__(self, direction1=0, direction2=0):
        self.p1 = 0
        self.p2 = 0
        self.flag1 = False
        self.flag2 = False
        self.direction1 = direction1
        self.direction2 = direction2



import operator
def bh_procedure2(pros, alpha,direction=0):
    cmpfun = operator.attrgetter('p1')
    pros.sort(key=cmpfun)  #
    for k in range(len(pros), 0, -1):
        if pros[k - 1].p1 <= float(k) / float((len(pros))) * alpha:
            for i in range(0,k):
                pros[i].flag1 = True
            break
        else:
            continue
    cmpfun = operator.attrgetter('p2')
    pros.sort(key=cmpfun)  #
    for k in range(len(pros), 0, -1):
        if pros[k - 1].p2 <= float(k) / float((len(pros))) * alpha:
            for i in range(0, k):
                pros[i].flag2 = True
            break
        else:
            continue
    counter = 0
    for i in range(0,len(pros)):
        if pros[i].flag1 and pros[i].flag2 and pros[i].direction1==direction and pros[i].direction2==direction:
            counter+=1
    return counter

def bh_procedure(p_array, alpha):
    p_array.sort()
    for k in range(len(p_array), 0, -1):
        if p_array[k - 1] <= float(k) / float((len(p_array))) * alpha:
            return k
        else:
            continue
    return 0


def CnkD(n, k):
    C = defaultdict(int)
    for row in range(n + 1):
        C[row, 0] = 1
        for col in range(1, k + 1):
            if col <= row:
                C[row, col] = C[row - 1, col - 1] + C[row - 1, col]
    return C[n, k]


def get_b_p(n, k, p):
    coe = CnkD(n, k)
    p_result = coe * math.pow(p, k) * math.pow(1 - p, n - k)
    return p_result


# weight the year-by-year data
def get_wights(lower_coe):
    weights = []
    x = (math.pow(math.e, 1) - math.pow(math.e, lower_coe)) / 11
    for i in range(0, 12):
        weight = math.log(math.e - i * x, math.e)
        weights.append(weight)
    return weights


def get_all_weights(length, lower_coe, coe):
    weights = get_wights(lower_coe)
    result = []
    for i in range(0, length):
        c = math.pow(coe, (i + 1) / 12) * weights[(i + 1) % 12]
        result.append(c)
    return result


def zero_change(a):
    result = []
    for i in range(1, len(a)):
        try:
            result.append(a[i] - a[i - 1])
        except TypeError:
            print a[365]
            print "xxxxxxxxxx"
    return result


def change_to_zero_one(data):
    result = []
    for i in range(1, len(data)):
        if data[i] > data[i - 1]:
            result.append(1)
        else:
            result.append(0)
    return result


def decide_type_with_quantile(value, low, high):
    if value < low:
        return 0
    elif value > high:
        return 2
    else:
        return 1


def decide_type_normal(value,sigma,mean):
    if value < mean-0.68*sigma:
        return 0
    elif value >=mean-0.68*sigma and value <mean+0.68*sigma:
        return 1
    elif value >= mean+0.68*sigma:
        return 2
    return 0


def calculate_mean_and_std(data):
    return np.mean(data), np.std(data, ddof=1)


def get_type_array_with_normal(a):
    result = []
    mean, sigma= calculate_mean_and_std(a)
    for element in a:
        result.append(decide_type_normal(element, sigma,mean))
    return result


def get_type_array_with_quantile(a):
    result = []
    tmp_array = list(a)
    tmp_array.sort()
    low = tmp_array[int(0.25 * len(a))]
    high = tmp_array[int(0.75 * len(a))]
    for element in a:
        result.append(decide_type_with_quantile(element, low, high))
    return result


def get_type_array_with_quantile_change(a,quantile):
    result = []
    tmp_array = list(a)
    tmp_array.sort()
    low = tmp_array[int(quantile * len(a))]
    high = tmp_array[int((1-quantile) * len(a))]
    for element in a:
        result.append(decide_type_with_quantile(element, low, high))
    return result


def get_type_array_with_quantile_change2(a,quantile):
    x1 = pow(1-quantile,2)
    x2 = 2*(1-quantile)*quantile
    x3 = pow(quantile,2)
    result = []
    tmp_array = list(a)
    tmp_array.sort()
    low = tmp_array[int(x1 * len(a))]
    high = tmp_array[int((1-x3) * len(a))]
    for element in a:
        result.append(decide_type_with_quantile(element, low, high))
    return result

def get_type_array_zero(a):
    result = []
    for element in a:
        if element<0:
            result.append(0)
        elif element>0:
            result.append(2)
        else:
            result.append(1)
    return result


def snml_b(data, next_value):
    p = 0
    log_f_0 = 0
    log_f_1 = 0
    log_f_2 = 0
    data_sum = sum(data)
    double_length = 2 * len(data)
    try:
        log_f_0 = data_sum * lg(data_sum) + (double_length - data_sum + 2) * lg(double_length - data_sum + 2)
        log_f_1 = lg(2) + (data_sum + 1) * lg(data_sum + 1) + (double_length - data_sum + 1) * lg(
            double_length - data_sum + 1)
        log_f_2 = (data_sum + 2) * lg(data_sum + 2) + (double_length - data_sum) * lg(double_length - data_sum)
        max_value = max([log_f_0, log_f_1, log_f_2])
        lg_denom = max_value + math.log(
            math.pow(2, log_f_0 - max_value) + math.pow(2, log_f_1 - max_value) + math.pow(2, log_f_2 - max_value))
    except ValueError:
        print data_sum
        print double_length
    if next_value == 0:
        lg_numer = log_f_0
    elif next_value == 1:
        lg_numer = log_f_1
    elif next_value == 2:
        lg_numer = log_f_2
    return lg_denom - lg_numer


def fast_snml_b(data_sum,length,  next_value):
    p = 0
    log_f_0 = 0
    log_f_1 = 0
    log_f_2 = 0
    double_length = 2 * length
    try:
        log_f_0 = data_sum * lg(data_sum) + (double_length - data_sum + 2) * lg(double_length - data_sum + 2)
        log_f_1 = lg(2) + (data_sum + 1) * lg(data_sum + 1) + (double_length - data_sum + 1) * lg(
            double_length - data_sum + 1)
        log_f_2 = (data_sum + 2) * lg(data_sum + 2) + (double_length - data_sum) * lg(double_length - data_sum)
        max_value = max([log_f_0, log_f_1, log_f_2])
        lg_denom = max_value + math.log(
            math.pow(2, log_f_0 - max_value) + math.pow(2, log_f_1 - max_value) + math.pow(2, log_f_2 - max_value))
    except ValueError:
        print data_sum
        print double_length
    if next_value == 0:
        lg_numer = log_f_0
    elif next_value == 1:
        lg_numer = log_f_1
    elif next_value == 2:
        lg_numer = log_f_2
    return lg_denom - lg_numer


def snml_b2(mean, length, next_value):
    log_f_0 = 0
    log_f_1 = 0
    log_f_2 = 0
    data_sum = mean * length
    double_length = 2 * length
    try:
        log_f_0 = data_sum * lg(data_sum) + (double_length - data_sum + 2) * lg(double_length - data_sum + 2)
        log_f_1 = lg(2) + (data_sum + 1) * lg(data_sum + 1) + (double_length - data_sum + 1) * lg(
            double_length - data_sum + 1)
        log_f_2 = (data_sum + 2) * lg(data_sum + 2) + (double_length - data_sum) * lg(double_length - data_sum)
        max_value = max([log_f_0, log_f_1, log_f_2])
        lg_denom = max_value + math.log(
            math.pow(2, log_f_0 - max_value) + math.pow(2, log_f_1 - max_value) + math.pow(2, log_f_2 - max_value))
    except ValueError:
        print data_sum
        print double_length
    if next_value == 0:
        lg_numer = log_f_0
    elif next_value == 1:
        lg_numer = log_f_1
    elif next_value == 2:
        lg_numer = log_f_2
    return lg_denom - lg_numer


def fast_mix_array(inblance_max,inblance_min,max_value,min_value,is_0_1_happen, window_length, next_value):
    if next_value==2:
        return max_value
    if next_value==0:
        return min_value
    if inblance_min>0:
        return min_value
    elif inblance_max<0:
        return max_value
    if is_0_1_happen or inblance_max%2==0:
        return window_length
    return window_length-1



def mix_array(effect_type, cause_type, next_type):
    counter_0_0 = 0
    counter_0_1 = 0
    counter_0_2 = 0
    counter_2_0 = 0
    counter_2_1 = 0
    counter_2_2 = 0
    is_0_2_happen = False
    is_0_1_happen = False
    target_array = []
    for i in range(0, len(effect_type)):
        cur_effect_type = effect_type[i]
        cur_cause_type = cause_type[i]
        if cur_effect_type == cur_cause_type:
            if cur_effect_type == 0:
                counter_0_0 += 1
                counter_2_0 += 1
            elif cur_effect_type == 2:
                counter_0_2 += 1
                counter_2_2 += 1
            elif cur_effect_type == 1:
                counter_0_1 += 1
                counter_2_1 += 1
        else:
            if (cur_cause_type == 0 and cur_effect_type == 1) or (cur_cause_type == 1 and cur_effect_type == 0):
                counter_0_0 += 1
                counter_2_1 += 1
                is_0_1_happen = True
            elif (cur_cause_type == 0 and cur_effect_type == 2) or (cur_cause_type == 2 and cur_effect_type == 0):
                is_0_2_happen = True
                counter_0_0 += 1
                counter_2_2 += 1
            elif (cur_cause_type == 1 and cur_effect_type == 2) or (cur_cause_type == 2 and cur_effect_type == 1):
                counter_2_2 += 1
                counter_0_1 += 1
                is_0_1_happen = True
    if next_type == 0:
        for i in range(0, counter_0_0):
            target_array.append(0)
        for i in range(0, counter_0_1):
            target_array.append(1)
        for i in range(0, counter_0_2):
            target_array.append(2)
    elif next_type == 2:
        for i in range(0, counter_2_0):
            target_array.append(0)
        for i in range(0, counter_2_1):
            target_array.append(1)
        for i in range(0, counter_2_2):
            target_array.append(2)
    elif next_type == 1:
        x0 = counter_0_2 - counter_0_0
        x2 = counter_2_2 - counter_2_0
        if x0 * x2 > 0:
            if abs(x0) < abs(x2):
                for i in range(0, counter_0_0):
                    target_array.append(0)
                for i in range(0, counter_0_1):
                    target_array.append(1)
                for i in range(0, counter_0_2):
                    target_array.append(2)
            else:
                for i in range(0, counter_2_0):
                    target_array.append(0)
                for i in range(0, counter_2_1):
                    target_array.append(1)
                for i in range(0, counter_2_2):
                    target_array.append(2)
        else:
            if is_0_1_happen:#not is_0_2_happen:
                return [0, 0, 0, 1, 1, 1, 2, 2, 2]
            else:
                if abs(x0) % 2 == 0:
                    return [0, 0, 0, 1, 1, 1, 2, 2, 2]
                else:
                    k = abs(x0) / 2
                    for i in range(0, counter_0_0 - k):
                        target_array.append(0)
                    for i in range(0, counter_0_2 + k):
                        target_array.append(2)
                    for i in range(0, counter_0_1):
                        target_array.append(1)
    return target_array


def calculate_mean_and_coe_sum_with_weight(data, coe):
    weights = get_wights(0.7)  # 0.7
    data_length = len(data)
    coe_sum = 0
    sum = 0
    std = 0
    sigma_sum = 0
    for i in range(0, data_length):
        tmp_coe = math.pow(coe, (i + 1) / 12) * weights[(i + 1) % 12]
        sum = sum + tmp_coe * data[data_length - i - 1]
        coe_sum = tmp_coe + coe_sum
    average = sum / coe_sum
    for i in range(0, data_length):
        tmp_coe = math.pow(coe, (i + 1) % 12) * weights[(i + 1) % 12]
        sigma_sum = sigma_sum + tmp_coe * math.pow(data[data_length - i - 1] - average, 2)
    return average, coe_sum


def mix_array_with_weight_window(effect_type, cause_type, next_type, coe):
    length_0 = 0
    length_2 = 0
    weights = get_all_weights(len(effect_type), 0.7, coe)
    weights.reverse()
    target_length = sum(weights)
    counter = 0
    values = []
    while counter < len(effect_type):
        cause_type_value = weights[counter] * cause_type[counter]
        effect_type_value = weights[counter] * effect_type[counter]
        if abs(cause_type_value - effect_type_value) < 0.00001:
            length_0 = length_0 + cause_type_value
            length_2 = length_2 + cause_type_value
        else:
            length_0 = length_0 + min([cause_type_value, effect_type_value])
            length_2 = length_2 + max([cause_type_value, effect_type_value])
            values.append(abs(cause_type_value - effect_type_value) * 10)
        counter += 1
    imbalance_0 = length_0 - target_length
    imbalance_2 = length_2 - target_length
    if next_type == 0:
        return length_0 / target_length, target_length
    elif next_type == 2:
        return length_2 / target_length, target_length
    else:
        if imbalance_0 * imbalance_2 > 0:
            if abs(imbalance_0) < abs(imbalance_2):
                return length_0 / target_length, target_length
            else:
                return length_2 / target_length, target_length
        else:
            target = abs(imbalance_0)
            for i in range(0, len(values)):
                values[i] = values[i] / 10.0
            values.sort(reverse=True)
            down_min = greedy(target, values)
            target2 = abs(imbalance_2)
            up_min = greedy(target2, values)
            if up_min < down_min:
                return (target_length + up_min) / target_length, target_length
            else:
                return (target_length - down_min) / target_length, target_length


def mix_array_with_weight(cur_len, current_effect_type, current_cause_type, next_type, values_array, length_0,
                          length_2):
    weights = get_all_weights(cur_len, 0.2, 0.7)
    current_weight = weights[-1]
    target_length = sum(weights)
    current_effect_type = current_effect_type * current_weight
    current_cause_type = current_cause_type * current_weight
    if abs(current_effect_type - current_cause_type) < 0.00001:
        length_0 = length_0 + current_effect_type
        length_2 = length_2 + current_effect_type
    else:
        length_0 = length_0 + min([current_cause_type, current_effect_type])
        length_2 = length_2 + max([current_cause_type, current_effect_type])
        value = abs(current_cause_type - current_effect_type)
        if len(values_array) == 0:
            values_array.append(value)
        else:
            for i in range(0, len(values_array)):
                if value >= values_array[i]:
                    values_array.insert(i, value)
                    break
                if i == len(values_array) - 1:
                    values_array.append(value)
                    break
    imbalance_0 = length_0 - target_length
    imbalance_2 = length_2 - target_length
    if next_type == 0:
        return length_0 / target_length, target_length, values_array, length_0, length_2
    elif next_type == 2:
        return length_2 / target_length, target_length, values_array, length_0, length_2
    else:
        if imbalance_0 * imbalance_2 > 0:
            if abs(imbalance_0) < abs(imbalance_2):
                return length_0 / target_length, target_length, values_array, length_0, length_2
            else:
                return length_2 / target_length, target_length, values_array, length_0, length_2
        else:
            target = abs(imbalance_0)
            down_min = greedy(target, values_array)
            target2 = abs(imbalance_2)
            up_min = greedy(target2, values_array)
            if up_min < down_min:
                return (target_length + up_min) / target_length, target_length, values_array, length_0, length_2
            else:
                return (target_length - down_min) / target_length, target_length, values_array, length_0, length_2


def greedy(target, values):
    sum = 0
    for i in range(0, len(values)):
        if sum + values[i] < target:
            sum = sum + values[i]
    return sum


