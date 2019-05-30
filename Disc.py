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
