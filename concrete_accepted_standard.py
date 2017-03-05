# Copyright 2017 The Chenmich Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
''' I will simulate the standard of a batch of concrete to be accepted.
    And find the more sampling and testing method of concrete.
    In practice, the standard deviation is unknown. This is our focus in this simulating.
    In general, we use the sample  data to judge statistical population's quality.
    In detail, we use the pass rate of sample to judge the statistical population's pass rate
    Because the parameters of probability distributions of samples
    are not same with the statistical population's, so we may make two class of errors.
    When statistical population is qualified
    we judge it un_qualified by the probability distributions of samples.
    This is the first class of errors.
    When statistical population is not qualified,
    we judge it qualified by the probability distributions of samples.
    And this is the second class of errors.
    The essence of the design sampling method is that
    when the pass rate of the sample is large enough, the probability of reception
    is also large enough, and when the pass rate of the sample is less than a certain value(alph),
    the probability of reception should be drastically reduced to a sufficientlly small value(beta)
    In general, the alph is 95% and beta is 20%.

    In mathematic, we can use the equation:
        average - lambda1*std >= lambda2*fcu_k
    where:
        average is average of sample data
        std is standard deviation of sample data
        fcu_k is compressive strengh standard value of concrete
        lambda1,lambad2 are judgment factors

    The design of sampling method is to find the two factors
    to ensure us not to make the two class of errors.
'''
import argparse
from scipy import stats
import numpy as np
import writer_to_csv as save

FCUK_LIST = [25, 35, 45, 55]
PAST_RATE_LIST = [0.99, 0.98, 0.97, 0.96, 0.95, 0.9, 0.8, 0.50, 0.2]#pass rate
SIGMA_LIST = [3.5, 4.5, 5.5, 7.5, 9.5]#Variance
SAMPLE_SIZE_LIST = [4, 8, 12, 18, 50]
#number of simulating
ECHO = 10
#the standard probability density function value corresponding to the pass rate
PPF_LIST = stats.norm.ppf(PAST_RATE_LIST)

#set lambad coefficient
def __get_tb_coefficient__(fcuk, sample_size):
    ''' set all the lambad coefficient
    '''
    lambda1 = 0.95
    lambda2 = 1
    lambda3 = 0
    lambda4 = 0
    lambda5 = 0
    lambda6 = 0
    if sample_size < 5:
        if fcuk < 20:
            lambda5 = 3.6
            lambda6 = 2.4
        if fcuk >= 20 and fcuk <= 40:
            lambda5 = 4.7
            lambda6 = 3.1
        if fcuk > 40:
            lambda5 = 5.8
            lambda6 = 3.9
    else:
        if sample_size >= 5 and sample_size < 10:
            lambda3 = 0.85
        if sample_size >= 10 and sample_size < 20:
            lambda3 = 1.10
        if sample_size >= 20:
            lambda3 = 1.20
        if fcuk < 20:
            lambda4 = 3.5
        if fcuk >= 20 and fcuk <= 40:
            lambda4 = 4.5
        if fcuk > 40:
            lambda4 = 5.5
    return lambda1, lambda2, lambda3, lambda4, lambda5, lambda6
def __get_old_gbj_coefficient__(sample_size):
    ''' set all the lambda coefficients
    '''
    lambda1 = 0
    lambda2 = 0.9
    lambda3 = 0
    lambda4 = 1.15
    lambda5 = 0.95
    if  sample_size >= 10:
        if sample_size >= 10 and sample_size <= 14:
            lambda1 = 1.70
            lambda3 = 0.90
        if sample_size > 15 and sample_size < 24:
            lambda1 = 1.65
            lambda3 = 0.85
        if sample_size >= 25:
            lambda1 = 1.60
            lambda3 = 0.85
    return lambda1, lambda2, lambda3, lambda4, lambda5
def __get_new_gbj_coefficient__(fcuk, sample_size):
    ''' set coefficient for new gbj
    '''
    lambda1 = 0
    lambda2 = 1.0
    lambda3 = 0
    lambda4 = 1.15
    lambda5 = 0.95
    if sample_size < 10:
        if fcuk < 60:
            lambda4 = 1.15
        else:
            lambda4 = 1.10
    else:
        if sample_size >= 10 and sample_size <= 14:
            lambda1 = 1.15
            lambda3 = 0.9
        if sample_size <= 19 and sample_size >= 15:
            lambda1 = 1.05
            lambda3 = 0.85
        if sample_size >= 20:
            lambda1 = 0.95
            lambda3 = 0.85
    return lambda1, lambda2, lambda3, lambda4, lambda5
#pylint restrain too many parameters
#define accepted for tb
def __tb_acception__(average, fcuk, fcumin, std, sample_size):
    ''' This function is for acception by tb
    '''
    isaccepted = False
    lambda1, lambda2, lambda3, lambda4, lambda5, lambda6 = __get_tb_coefficient__(fcuk, sample_size)
    if sample_size < 5:
        if average >= fcuk + lambda5 and fcumin >= fcuk - lambda6:
            isaccepted = True
    else:
        if average >= lambda2*fcuk + lambda1*std and fcumin >= fcuk - lambda3*lambda4:
            isaccepted = True
    return isaccepted

#define accepted for new gbj
def __new_gbj_acception__(average, fcuk, fcumin, std, sample_size):
    ''' This fucntion is for acception by new gbj
    '''
    isaccepted = False
    lambda1, lambda2, lambda3, lambda4, lambda5 = __get_new_gbj_coefficient__(fcuk, sample_size)
    if  sample_size < 10:
        if average >= lambda4*fcuk and fcumin >= lambda5*fcuk:
            isaccepted = True
    else:
        if average >= lambda2*fcuk + lambda1*std and fcumin >= lambda3*fcuk:
            isaccepted = True
    return isaccepted

#define accepted for old gbj
def __old_gbj_acception__(average, fcuk, fcumin, std, sample_size):
    '''This function is for acception by old gbj
    '''
    isaccepted = False
    lambda1, lambda2, lambda3, lambda4, lambda5 = __get_old_gbj_coefficient__(sample_size)
    #sample_size < 10, by non-statistical method
    if sample_size < 10:
        if average >= lambda4*fcuk and fcumin >= lambda5*fcuk:
            isaccepted = True
    #sample_size >=10,by statistical methon
    else:
        if average - lambda1*std >= lambda2*fcuk and fcumin >= lambda3*fcuk:
            isaccepted = True
    return isaccepted


def __valid_sampling_method__():
    ''' valid the GBJ107-87, GBJ50107-2010 and the TB10425
    '''
    old_gbj_result = {}
    new_gbj_result = {}
    tb_result = {}
    for sample_size in SAMPLE_SIZE_LIST:
        old_gbj_sample_size_result = {}
        new_gbj_sample_size_result = {}
        tb_sample_size_result = {}
        for fcuk in FCUK_LIST:
            old_gbj_fcuk_result = {}
            new_gbj_fcuk_result = {}
            tb_fcuk_result = {}
            for sigma in SIGMA_LIST:
                old_gbj_accepted_rate_list = []
                new_gbj_accepted_rate_list = []
                tb_accepted_rate_list = []
                for ppf in PPF_LIST:
                    old_gbj_accepted_frequence = 0
                    new_gbj_accepted_frequence = 0
                    tb_accepted_frequence = 0
                    for _ in range(ECHO):
                        preparation_strength = fcuk + ppf*sigma
                        sample_data = stats.norm.rvs(loc=preparation_strength,
                                                     scale=sigma, size=sample_size)
                        average = stats.tmean(sample_data)
                        std = stats.tstd(sample_data)
                        fcumin = stats.tmin(sample_data)
                        if __old_gbj_acception__(average, fcuk, fcumin, std, sample_size):
                            old_gbj_accepted_frequence += 1
                        if __new_gbj_acception__(average, fcuk, fcumin, std, sample_size):
                            new_gbj_accepted_frequence += 1
                        if __tb_acception__(average, fcuk, fcumin, std, sample_size):
                            tb_accepted_frequence += 1
                    old_gbj_accepted_rate = old_gbj_accepted_frequence / ECHO
                    old_gbj_accepted_rate_list.append(old_gbj_accepted_rate)
                    new_gbj_accepted_rate = new_gbj_accepted_frequence /ECHO
                    new_gbj_accepted_rate_list.append(new_gbj_accepted_rate)
                    tb_accepted_rate = tb_accepted_frequence / ECHO
                    tb_accepted_rate_list.append(tb_accepted_rate)
                old_gbj_fcuk_result[sigma] = old_gbj_accepted_rate_list
                new_gbj_fcuk_result[sigma] = new_gbj_accepted_rate_list
                tb_fcuk_result[sigma] = tb_accepted_rate_list
            old_gbj_sample_size_result[fcuk] = old_gbj_fcuk_result
            new_gbj_sample_size_result[fcuk] = new_gbj_fcuk_result
            tb_sample_size_result[fcuk] = tb_fcuk_result
        old_gbj_result[sample_size] = old_gbj_sample_size_result
        new_gbj_result[sample_size] = new_gbj_sample_size_result
        tb_result[sample_size] = tb_sample_size_result

    #header = ['sample_size', 'strength', 'sigma'] + [1 - x for x in PPF_LIST]
    #file_name = 'c://tmp/data/result.csv'
    #write.write_to_csv(header, results, file_name)
    #GBJ50107-2010
    print(old_gbj_result)
    print(new_gbj_result)
    print(tb_result)
    print('simlating the GBJ50107-2010......')
    #TB10425-1994
    print('simulating the TB10425-1994......')

def main():
    '''control flow'''
    __valid_sampling_method__()


if __name__ == '__main__':
    main()
    