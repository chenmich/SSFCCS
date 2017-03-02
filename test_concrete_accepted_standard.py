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
class TestAccepted(unittest.TestCase):
    ''' test the __accepted__ method of concrete_accepted_standard modular
    '''
    def setUp(self):
        self.lambda1 = 1.65
        self.lambda2 = 0.9
        self.lambda3 = 0.85
        self.average = 35.8
        self.std = 4.3
        self.fcu_k = 30.0
        self.fcu_min = 26.0
    def test_first_condition_true(self):
        ''' the second condition is True
        '''
        self.assertTrue(
            caccep.__accepted__(self.lambda1, self.lambda2,
                                self.lambda3, self.average, self.std, self.fcu_k, self.fcu_min))
    def test_first_condition_false(self):
        ''' the second condition is True
        '''
        #average is less
        self.average = 33.2
        self.assertFalse(
            caccep.__accepted__(self.lambda1, self.lambda2,
                                self.lambda3, self.average, self.std, self.fcu_k, self.fcu_min))
        #std is larger
        self.average = 35.8
        self.std = 5.5
        self.assertFalse(
            caccep.__accepted__(self.lambda1, self.lambda2,
                                self.lambda3, self.average, self.std, self.fcu_k, self.fcu_min))

if __name__ == '__main__':
    unittest.main()
