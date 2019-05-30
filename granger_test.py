import pandas as pd
from statsmodels.tsa.api import VAR


"""
This file provide method for Granger causality test
"""


def granger(cause,effect,lag):
    data = pd.DataFrame({'cause':cause,'effect':effect})
    return_vaule = 1
    model = VAR(data)
    try:
        if lag == -1:
            results = model.fit(maxlags=50,trend='nc',ic='aic')
        else:
            results = model.fit(lag)
    except Exception:
        # can not find a lag in interval [1, maxlags], that means they have no causality
        return 1
    try:
        #print results.summary()
        #xx = results.test_causality('effect', 'cause', kind='wald').summary()
        x = results.test_causality('effect', 'cause', kind='wald').summary().data
    except Exception:
        return 0
    return_vaule = x[1][2]

    return return_vaule