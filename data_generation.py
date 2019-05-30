import numpy as np
from statsmodels.tsa.api import VAR


"""
The functions in thi file provide data generations methods
to do synthetic data experiments 
"""


# move the coninue sequence forward by shift bits
def forward_shift_continue_data(seq, shift):
    lseq = len(seq)
    sseq = [None] * lseq
    for i in xrange(lseq):
        if i >= shift:
            sseq[i] = seq[i - shift]
        else:
            sseq[i] = np.random.normal(0, 1, 1)[0]
    return sseq


# generate random walk cause and effect time series
def generate_continue_data(length, shift,noise):
    cause = []
    main = np.random.normal(0, 1, length)
    for i in range(0, length):
        if i == 0:
            cause.append(main[i])
        else:
            cause.append(cause[i - 1] + main[i])
    effect = forward_shift_continue_data(cause, shift)
    if noise!=0.0:
        noises = np.random.normal(0, noise, length)
        for j in range(0, length):
            effect[j] = effect[j] + noises[j]
    return cause, effect


# generate Gaussian distribution time series
def GMM(k, n):
    w = np.random.rand(1, k)
    wsum = np.sum(w)
    w = w / wsum
    wsumt = 0
    mu = 2 * np.random.rand(1, k) - 1
    level = np.zeros(k)
    sigma = 10 * np.random.rand(1, k)
    X = []
    for ii in range(k):
        wsumt += w[0][ii]
        level[ii] = wsumt
    # for ij in range(k-1):
    # level[ij+1]=level[ij]+level[ij+1]
    for ik in range(n):
        lev = np.random.random_sample()
        count = 0
        for alp in range(k):
            if lev < level[alp]:
                count = alp
                break
        x = np.random.normal(mu[0][count], sigma[0][count], 1)
        X.extend(x.tolist())
    return X


