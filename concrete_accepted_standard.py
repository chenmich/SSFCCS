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
import datetime
import csv
import argparse
from scipy import stats
import numpy as np
import write_to_csv as saver

FCUK_LIST = [25, 35, 45, 55, 65]
PAST_RATE_LIST = [0.99, 0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.9, 0.8, 0.50, 0.2]#pass rate
SIGMA_LIST = [3.5, 4.5, 5.5, 7.5, 9.5]#Variance
SAMPLE_SIZE_LIST = [4, 8, 12, 18, 30, 50]
#number of simulating
ECHO = 10000
#the standard probability density function value corresponding to the pass rate
PPF_LIST = stats.norm.ppf(PAST_RATE_LIST)

#set lambad coefficient
def __get_tb_coefficient__(fcuk, sample_size):
    ''' set all the lambad coefficient
    '''
    lambda1 = 0.95
    lambda2 = 1.0
    lambda3 = 0.0
    lambda4 = 0.0
    lambda5 = 0.0
    lambda6 = 0.0
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
    lambda1 = 0.0
    lambda2 = 0.9
    lambda3 = 0.0
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
    lambda1 = 0.0
    lambda2 = 1.0
    lambda3 = 0.0
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
#save result
def __save_to__(headers, result, file_name):
    writer = saver.write_to_csv(headers, result, file_name)
def __valid_sampling_method__(data_dir):
    ''' valid the GBJ107-87, GBJ50107-2010 and the TB10425
    '''
    start = datetime.datetime.now()
    print(start)
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

    #write result to file
    header = ['样本数量', '强度等级', '标准差', "不合格率"]
    headers = []
    headers.append(header)
    header = ['', '', ''] + [1 - x for x in PPF_LIST]

    results = [old_gbj_result, new_gbj_result, tb_result]
    filenames = ['old_gbj', 'new_gbj', 'tb']
    for result, filename in zip(results, filenames):
        __save_to__(headers, result, data_dir + filename + ".csv")
    end = datetime.datetime.now()
    print(end)
    print("All the time are ", (end - start))
#simulating for get the two accepted rates
def __get_accepted_rate__(lambda1, lambda2, ppf, sample_size):
    fcuk = 40
    sigma = 6.0
    preparared_strength0 = fcuk + ppf*sigma
    accepted_frequence = 0
    for _ in range(ECHO):
        sample_data = stats.norm.rvs(loc=preparared_strength0, scale=sigma, size=sample_size)
        mean = stats.tmean(sample_data)
        std = stats.tstd(sample_data)
        if mean >= lambda1*fcuk + lambda2*std:
            accepted_frequence += 1
    ap = accepted_frequence / ECHO
    return ap

#find argument for sampling method
def __find_argument_sampling__(file_name):
    ''' Find the argument for sampling method
        In general, we accepte a batch of concrete by statistical method with unknown variance.
        The universal equations is:
            average - lambda1*std >= lambda2*fcuk
            fcumin >= lambda3*fcuk + lambda4
        It is well known that the first equation is base equation because
        it is base on statistics.
        And the second equation is for limiting the minimum value of sample data for preventing from
        the minumum is to small. This is base on industry facts.
        For simplicity, the arguments of the first equation are found.
        The Criterion for the arguments are based on the fact:
            when pass_rate of groups of samples is larger than 95%,
                the accepted rate must be larger than 95%;
            when pass_rate of groups of samples is less than 80%,
                the accepted rate must be less than 20%;
            so, when pass_rate of groups of samples is less than 95%,
                the accepted rate must have sharp drop.
        By formal, it is written as:
            p1 >= 95% if p1 < 95%, then |p1 - 95%|/95% <= 5% .........(1)
            p2 <= 20% if p2 > 20%, then |p2 - 20%|/20% <= 5% .........(2)
        where:
            p1:the accepted rate at pass rate is 95%, the expected value is 95%
            p2:the accepted rate at pass rate is 80%, the expected value is 20%
        Only if (1) and (2) statisfied, the other accepted rate will be got by simulating acception
    '''
    lambdas1 = np.arange(0.85, 2.5, 0.05)
    lambdas2 = np.arange(0.70, 2.0, 0.05)
    pr0 = 0.95
    pr1 = 0.80
    alpha = 0.95
    beta = 0.30
    error_rate0 = 0.15
    error_rate1 = 0.50
    ppf0 = stats.norm.ppf(pr0)
    ppf1 = stats.norm.ppf(pr1)
    start = datetime.datetime.now()
    print(start)
    all_candidates = {}
    for sample_size in SAMPLE_SIZE_LIST:
        lambda_candidates = []
        for lambda1 in lambdas1:
            for lambda2 in lambdas2:
                OK = False
                ap0 = __get_accepted_rate__(lambda1, lambda2, ppf0, sample_size)
                ap1 = __get_accepted_rate__(lambda1, lambda2, ppf1, sample_size)
                diffi0 = abs(ap0 - alpha) <= alpha*error_rate0
                diffi1 = abs(ap1 - beta) <= beta*error_rate1
                if ap0 >= alpha and ap1 <= beta:
                    OK = True
                if ap0 < alpha and ap1 <= beta:
                    if diffi0:
                        OK = True
                if ap0 >= alpha and ap1 > beta:
                    if diffi1:
                        OK = True
                if ap0 < alpha and ap1 > beta:
                    if diffi0 and diffi1:
                        OK = True
                if OK:
                    lambda_candidate = [lambda1, lambda2, ap0, ap1]
                    lambda_candidates.append(lambda_candidate)
        all_candidates[sample_size] = lambda_candidates


    result = {}
    for sample_size in SAMPLE_SIZE_LIST:
        lambda_and_aps = all_candidates[sample_size]
        lambda_and_allap = []
        for lambda_and_ap  in lambda_and_aps:
            ap = 0
            aps = []
            lambda1 = lambda_and_ap[0]
            lambda2 = lambda_and_ap[1]
            ap0 = lambda_and_ap[2]
            ap1 = lambda_and_ap[3]
            for ppf in PPF_LIST:
                if ppf == ppf0:
                    ap = ap0
                if ppf == ppf1:
                    ap = ap1
                if ppf != ppf0 and ppf != ppf1:
                    ap = __get_accepted_rate__(lambda1, lambda2, ppf, sample_size)
                aps.append(ap)
            lambda_and_allap.append([lambda1, lambda2] + aps)
        result[sample_size] = lambda_and_allap

    with open(file_name, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["数据批量", "lambda1", "lambda2", "不合格率"])
        writer.writerow(['', '', ''] + [1-x for x in PAST_RATE_LIST])
        for sample_size in SAMPLE_SIZE_LIST:
            lines = result[sample_size]
            writer.writerow([sample_size] + lines[0])
            for line in lines[1:]:
                writer.writerow([''] + line)

    end = datetime.datetime.now()
    print(end)
    print("difference of time is ", (end - start))



#main control
def main(args):
    '''control flow'''
    if args.valid:
        print("Simulating the standard:")
        __valid_sampling_method__(args.result_dir)
    if args.find:
        print("Fining the arguments for sampling method of acception of concrete:")
        __find_argument_sampling__(args.result_dir + "found_result.csv")


if __name__ == '__main__':
    PARPASER = argparse.ArgumentParser()
    PARPASER.add_argument("--valid", "-V", help="valid the current standard",
                          action="store_true")
    PARPASER.add_argument("--find", "-F", help="find argument for method of acception",
                          action="store_true")
    PARPASER.add_argument("--result_dir",
                          help="the path of file of results after executing",
                          type=str, default="c://tmp/data/")
    PARS = PARPASER.parse_args()
    main(PARS)
