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
''' test writer_to_csv modular
'''
import csv
import unittest
import write_to_csv as saver

class test_write_to_csv(unittest.TestCase):
    '''test write_to_csv modular
    '''
    def test_write_to_csv(self):
        header = ['11', '12']
        headers = []
        headers.append(header)
        header = ['', '', '23', '24']
        headers.append(header)
        file_name = "c://tmp/data/old_gbj_result.csv"
        result = {32:{22:{55:[1, 2, 3, 4, 5],
                          77:[6, 7, 8, 9, 10]}}}
        saver.write_to_csv(headers, result, file_name)
        with open(file_name, newline='') as csvfile:
            reader = csv.reader(csvfile)
            lines = []
            for line in reader:
                lines.append(line)
                print(line)
            self.assertEqual(lines[0], ["11", '12'])
            self.assertEqual(lines[1], ['', '', '23', '24'])
            self.assertEqual(lines[2], ['32', '22', '55', '1', '2', '3', '4', '5'])
            self.assertEqual(lines[3], ['', '', '77', '6', '7', '8', '9', '10'])
#main control
if __name__ == "__main__":
    unittest.main()


