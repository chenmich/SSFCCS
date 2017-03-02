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
import writer_to_csv as write

FCUK_LIST = [25, 35, 45, 55]
PAST_RATE_LIST = [0.99, 0.98, 0.97, 0.96, 0.95, 0.9, 0.8, 0.50, 0.2]#pass rate
SIGMA_LIST = [3.5, 4.5, 5.5, 7.5, 9.5]#Variance

#number of simulating
ECHO = 10
#the standard probability density function value corresponding to the pass rate
PPF_LIST = stats.norm.ppf(PAST_RATE_LIST)
#pylint restrain too many parameters
def __accepted__(lambda1, lambda2, lambda3, average, std, fcu_k, fcu_min):
    ''' This function will simulate to accepte a batch of concrete
        Accepted conditions are both
            average - lambda1*std >= lambda2*fcu_k
            fcu_min >= lambda3*fcu_k
    '''
    accepted = False
    if (average - lambda1*std >= lambda2*fcu_k) and (fcu_min >= lambda3*fcu_k):
        accepted = True
    return accepted

def __valid_sampling_method__():
    ''' valid the GBJ107-87, GBJ50107-2010 and the TB10425
    '''
    #GBJ08-1987
    sample_size_list = [12, 20, 50]
    lam1_list = [1.70, 1.65, 1.60]
    lam2_list = [0.90, 0.90, 0.90]
    lam3_list = [0.90, 0.85, 0.85]

    print('simulating the GBJ107-1987......')
    #combination of judge factors under sample size
    results = {}
    for lam1, lam2, lam3, sample_size in zip(lam1_list,
                                             lam2_list,
                                             lam3_list,
                                             sample_size_list):
        strength_results = {}
        for fcuk in FCUK_LIST: #compressive strengh standard value
            sigma_results = {}
            for sigma in SIGMA_LIST:#for variance
                accepted_rate_list = []
                for ppf in PPF_LIST:#for the pass rate
                    preparation_strength = fcuk + ppf*sigma
                    receive_frequency = 0
                    for _ in np.arange(ECHO):
                        sample_data = stats.norm.rvs(loc=preparation_strength,
                                                     scale=sigma, size=sample_size)
                        average = stats.tmean(sample_data)
                        std = stats.tstd(sample_data)
                        fcumin = stats.tmin(sample_data)
                        if __accepted__(lam1, lam2, lam3, average, std, fcuk, fcumin):
                            receive_frequency += 1
                    accepted_rate = receive_frequency / ECHO
                    accepted_rate_list.append(accepted_rate)
                sigma_results[sigma] = accepted_rate_list
            strength_results[fcuk] = sigma_results
        results[sample_size] = strength_results
    header = ['sample_size', 'strength', 'sigma'] + [1 - x for x in PPF_LIST]
    file_name = 'c://tmp/data/result.csv'
    write.write_to_csv(header, results, file_name)
    #GBJ50107-2010
    print('simlating the GBJ50107-2010......')
    #TB10425-1994
    print('simulating the TB10425-1994......')

def main():
    '''control flow'''
    __valid_sampling_method__()


if __name__ == '__main__':
    main()
    