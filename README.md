# Causal-Discovery-from-Continuous-Time-Series-by-Compression

## 1. Code Summary
In data directory, we provide all data that we use in our experiments and a data generator of MATLAB Simulink to generate mechatronic engineering data.
In cute.py, there are methods provided by [Causal Inference on Event Sequences](http://kailashbuki.github.io/manuscript/cute.pdf)   to allow our methods to compare with others.
In granger.py, we provide Granger Causality test method.
In Util.py, we provide all functions that will be used in DISC and our experiments.
In Disc.py, core methods of DISC are provided.
synthetic_data_test.py and real_data_test.py provide synthetic data test and real world data test results separately. 

## 2. Time Complexity
**synthetic_data_test.py**

    time_window()
    time_weighted()
    time_weighted_window()

## 3. Validation for Encoding Method 
**synthetic_data_test.py**

    test_causality_consistency()

    test_no_causality_consistency()

## 4. Synthetic Experimental Results 

####  4.1 Simple Linear Causality
**synthetic_data_test.py**

    test_linear_data()

#### 4.2  Nonlinear Monotonic Causality
**synthetic_data_test.py**

    test_non_linear()

## 5. EMPIRICAL RESULTS ON REAL WORLD DATA 

#### 5.1 River Data 
**real_data_test.py**

    river_test()
    river_test2()

#### 5.2  Temperature and Ozone Data
    ozone_test(1)
    ozone_test(2)
    ozone_test(3)

#### 5.3 Mechatronic Engineering Data 
    test_engineering(1, 0)
    test_engineering(2, 0)
    test_engineering(1, 1)
    test_engineering(2, 1)

## Supplement to our code

The methods above only provide main results of our experiments.  The code for other models(G-test, cute, icute) is annotated. These functions can also be used.

From the point of view of code simplicity, all of our synthetic data related tests are imported from test_data(). Make sure to read comments before you use this method by yourself.

## Experiment Results
We provide detailed results of all the experiments in this paper in directory **Experiment Result**.
In addition, as the noise is random, the last real world data experiment will get different results every time you run. Therefore we store the data that we use in this paper in excel of the directory.
