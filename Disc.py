from Util import get_type_array_with_quantile, snml_b, snml_b2, mix_array, mix_array_with_weight, \
    mix_array_with_weight_window, calculate_mean_and_coe_sum_with_weight,get_type_array_with_normal,get_type_array_zero,get_type_array_with_quantile_change,get_type_array_with_quantile_change2


def calculate_difference_with_normal(cause, effect, length):
    cause_type = get_type_array_with_normal(cause)
    effect_type = get_type_array_with_normal(effect)
    effect_p_length_array = []
    cause_effect_p_length__array = []
    for i in range(length, len(effect) - 1):
        effect_p_length_array.append(snml_b(effect_type[i - length:i], effect_type[i]))
        target_array = mix_array(effect_type[i - length:i], cause_type[i - length:i], effect_type[i])
        cause_effect_p_length__array.append(snml_b(target_array, effect_type[i]))
    effect_length = sum(effect_p_length_array)
    cause_effect_length = sum(cause_effect_p_length__array)
    return effect_length - cause_effect_length


def calculate_difference(cause, effect, length):
    cause_type = get_type_array_with_quantile(cause)
    effect_type = get_type_array_with_quantile(effect)
    effect_p_length_array = []
    cause_effect_p_length__array = []
    for i in range(length, len(effect) - 1):
        effect_p_length_array.append(snml_b(effect_type[i - length:i], effect_type[i]))
        target_array = mix_array(effect_type[i - length:i], cause_type[i - length:i], effect_type[i])
        cause_effect_p_length__array.append(snml_b(target_array, effect_type[i]))
    effect_length = sum(effect_p_length_array)
    cause_effect_length = sum(cause_effect_p_length__array)
    return effect_length - cause_effect_length


from Util import fast_mix_array, fast_snml_b


def fast_calculate_difference(cause, effect, length):
    cause_type = get_type_array_with_quantile(cause)
    effect_type = get_type_array_with_quantile(effect)
    effect_p_length_array = []
    cause_effect_p_length__array = []
    max_2 = 0
    max_0 = 0
    min_2 = 0
    min_0 = 0
    happen_1_count = 0
    max_value = 0
    min_value = 0
    for i in range(0,len(effect)-1):
        if i >= length:
            effect_p_length_array.append(snml_b(effect_type[i - length:i], effect_type[i]))
            target_sum = fast_mix_array(max_2-max_0,min_2-min_0,max_value,min_value,happen_1_count!=0,length, effect_type[i])
            cause_effect_p_length__array.append(fast_snml_b(target_sum,length,effect_type[i]))
            last_value_cause = cause_type[i-length]
            last_value_effect = effect_type[i-length]
            max_value -= max(last_value_cause, last_value_effect)
            min_value -= min(last_value_cause, last_value_effect)
            if (last_value_cause== 0 and last_value_effect == 1) or (last_value_cause == 1 and last_value_effect == 0) \
                    or (last_value_cause == 1 and last_value_effect == 2) or (last_value_cause== 2 and last_value_effect== 1):
                happen_1_count -= 1
            if last_value_cause == last_value_effect:
                if last_value_cause== 0:
                    max_0 -= 1
                    min_0 -= 1
                elif last_value_cause== 2:
                    max_2 -= 1
                    min_2 -= 1
            else:
                value_max = max(last_value_cause, last_value_effect)
                value_min = max(last_value_cause, last_value_effect)
                if value_max == 2:
                    max_2 -= 1
                if value_min == 0:
                    min_0 -= 1
        max_value+=max(cause_type[i],effect_type[i])
        min_value += min(cause_type[i], effect_type[i])
        if (cause_type[i] == 0 and effect_type[i] == 1) or (cause_type[i] == 1 and effect_type[i] == 0) \
                or (cause_type[i] == 1 and effect_type[i] == 2) or (cause_type[i] == 2 and effect_type[i] == 1):
            happen_1_count += 1
        if cause_type[i] == effect_type[i]:
            if cause_type[i] == 0:
                max_0 += 1
                min_0 += 1
            elif cause_type[i] == 2:
                max_2 += 1
                min_2 += 1
        else:
            value_max = max(cause_type[i], effect_type[i])
            value_min = max(cause_type[i], effect_type[i])
            if value_max == 2:
                max_2 += 1
            if value_min == 0:
                min_0 += 1
    effect_length = sum(effect_p_length_array)
    cause_effect_length = sum(cause_effect_p_length__array)
    return effect_length - cause_effect_length



def calculate_difference_step(cause, effect, length):
    ans = []
    cause_type = get_type_array_with_quantile(cause)
    effect_type = get_type_array_with_quantile(effect)
    effect_p_length_array = []
    cause_effect_p_length__array = []
    for i in range(length, len(effect) - 1):
        effect_p_length_array.append(snml_b(effect_type[i - length:i], effect_type[i]))
        target_array = mix_array(effect_type[i - length:i], cause_type[i - length:i], effect_type[i])
        cause_effect_p_length__array.append(snml_b(target_array, effect_type[i]))
        ans.append(sum(effect_p_length_array)-sum(cause_effect_p_length__array))
    return ans

def calculate_difference_with_quantile(cause, effect, length,q):
    cause_type = get_type_array_with_quantile_change(cause,q)
    effect_type = get_type_array_with_quantile_change(effect,q)
    effect_p_length_array = []
    cause_effect_p_length__array = []
    for i in range(length, len(effect) - 1):
        effect_p_length_array.append(snml_b(effect_type[i - length:i], effect_type[i]))
        target_array = mix_array(effect_type[i - length:i], cause_type[i - length:i], effect_type[i])
        cause_effect_p_length__array.append(snml_b(target_array, effect_type[i]))
    effect_length = sum(effect_p_length_array)
    cause_effect_length = sum(cause_effect_p_length__array)
    return effect_length - cause_effect_length

def calculate_difference_with_quantile2(cause, effect, length,q):
    cause_type = get_type_array_with_quantile_change2(cause,q)
    effect_type = get_type_array_with_quantile_change2(effect,q)
    effect_p_length_array = []
    cause_effect_p_length__array = []
    for i in range(length, len(effect) - 1):
        effect_p_length_array.append(snml_b(effect_type[i - length:i], effect_type[i]))
        target_array = mix_array(effect_type[i - length:i], cause_type[i - length:i], effect_type[i])
        cause_effect_p_length__array.append(snml_b(target_array, effect_type[i]))
    effect_length = sum(effect_p_length_array)
    cause_effect_length = sum(cause_effect_p_length__array)
    return effect_length - cause_effect_length

def calculate_difference_zero(cause, effect, length):
    cause_type = get_type_array_zero(cause)
    effect_type = get_type_array_zero(effect)
    effect_p_length_array = []
    cause_effect_p_length__array = []
    for i in range(length, len(effect) - 1):
        effect_p_length_array.append(snml_b(effect_type[i - length:i], effect_type[i]))
        target_array = mix_array(effect_type[i - length:i], cause_type[i - length:i], effect_type[i])
        cause_effect_p_length__array.append(snml_b(target_array, effect_type[i]))
    effect_length = sum(effect_p_length_array)
    cause_effect_length = sum(cause_effect_p_length__array)
    return effect_length - cause_effect_length


def calculate_difference_with_weight_window(cause, effect, coe, length):
    cause_type = get_type_array_with_quantile(cause)
    effect_type = get_type_array_with_quantile(effect)
    effect_p_array = []
    cause_effect_p_array = []
    for i in range(length, len(effect) - 1):
        mean2, ll = calculate_mean_and_coe_sum_with_weight(
            effect_type[i - length:i], coe)
        effect_p_array.append(snml_b2(mean2, ll, effect_type[i]))
        mean, l = mix_array_with_weight_window(effect_type[i - length:i], cause_type[i - length:i], effect_type[i], coe)
        p2 = snml_b2(mean, l, effect_type[i])
        cause_effect_p_array.append(p2)
    effect_length = sum(effect_p_array)
    cause_effect_length = sum(cause_effect_p_array)
    return effect_length - cause_effect_length


def calculate_difference_with_weight(cause, effect, length):
    cause_type = get_type_array_with_quantile(cause)
    effect_type = get_type_array_with_quantile(effect)
    effect_p_array = []
    cause_effect_p_array = []
    values = []
    length0 = 0
    length2 = 0
    for i in range(length, len(effect) - 1):
        mean2, ll = calculate_mean_and_coe_sum_with_weight(
            effect_type[0:i], 0.7)
        effect_p_array.append(snml_b2(mean2, ll, effect_type[i]))
        mean, l, values, length0, length2 = mix_array_with_weight(i, effect_type[i - 1], cause_type[i - 1],
                                                                  effect_type[i], values, length0, length2)
        p2 = snml_b2(mean, l, effect_type[i])
        cause_effect_p_array.append(p2)
    effect_length = sum(effect_p_array)
    cause_effect_length = sum(cause_effect_p_array)
    return effect_length - cause_effect_length
