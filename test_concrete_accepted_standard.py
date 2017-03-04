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
''' test the concrete_accepted_standard modular'''

import unittest
import concrete_accepted_standard as caccep
class test_old_gbj(unittest.TestCase):
    ''' test the helper for old_gjb
    '''
    #test coefficient
    def test_get_old_gbj_coefficient(self):
        ''' test coeficient for statistical method with unknown variance
        '''
        sample_size = [4, 8, 12, 20, 50]
        lambda1, _, lambda3, _, _ = caccep.__get_old_gbj_coefficient__(sample_size[2])
        self.assertEqual(lambda1, 1.7)
        self.assertEqual(lambda3, 0.9)
        lambda1, _, lambda3, _, _ = caccep.__get_old_gbj_coefficient__(sample_size[3])
        self.assertEqual(lambda1, 1.65)
        self.assertEqual(lambda3, 0.85)
        lambda1, _, lambda3, _, _ = caccep.__get_old_gbj_coefficient__(sample_size[4])
        self.assertEqual(lambda1, 1.60)
        self.assertEqual(lambda3, 0.85)
    #test accepted wiht less samples
    def test_old_gbj_acception_with_less_samples(self):
        ''' test acception with less samples
        '''
        # accepted
        average = 33.5
        fcuk = 25
        fcumin = 26.4
        self.assertTrue(caccep.__old_gbj_acception__(average, fcuk, fcumin))
        #condition one is not satisfied
        average = 26.4
        self.assertFalse(caccep.__old_gbj_acception__(average, fcuk, fcumin))
        #condition two is not statisfied
        average = 33.5
        fcumin = 22.3
        self.assertFalse(caccep.__old_gbj_acception__(average, fcuk, fcumin))
        #the two conditions are not satisfied
        average = 26.2
        self.assertFalse(caccep.__old_gbj_acception__(average, fcuk, fcumin))

    #test acception with statistical method
    def test_old_gbj_acception_with_statistical_method(self):
        ''' test acception with statistical method
        '''
        average = 33.5
        std = 4.3
        fcuk = 25
        fcumin = 24.3
        sample_size = 13
        #accepted
        self.assertTrue(caccep.__old_gbj_acception__(average, fcuk, fcumin, std, sample_size))
        #the condition one is not satisfied
        average = 28.3
        self.assertFalse(caccep.__old_gbj_acception__(average, fcuk, fcumin, std, sample_size))
        average = 33.5
        std = 6.5
        self.assertFalse(caccep.__old_gbj_acception__(average, fcuk, fcumin, std, sample_size))
        #the condition two is not staisfied
        fcumin = 21.3
        self.assertFalse(caccep.__old_gbj_acception__(average, fcuk, fcumin, std, sample_size))
        
if __name__ == '__main__':
    unittest.main()
