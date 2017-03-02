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
''' This modula will write a dict to csv file'''
import csv
#take the write to task
def __write_dictionary_to_csvline__(contents, parent_key):
    ''' generate a lines of csv from a dictionary
        Arg:
            contents:a dictionary from which will generate lines of csv lines
            parent_key: list of parent key of contents.If depth of contents is zero, it can be [].
    '''
    is_first_line = True
    is_first_dict = True
    _lines = lines = []
    keys = [x for x in contents.keys()]
    keys.sort()
    count = 0
    for _ in parent_key:
        count += 1

    for key in keys:
        if not isinstance(contents[key], list):
            if is_first_dict:
                _lines = __write_dictionary_to_csvline__(contents[key], parent_key + [key])
                is_first_dict = False
            else:
                _lines = __write_dictionary_to_csvline__(contents[key], ['']*count + [key])
            for _line in _lines:
                lines.append(_line)
        else:
            if is_first_line:
                lines.append(parent_key + [key] + contents[key])
                is_first_line = False
            else:
                lines.append(['']*count + [key] + contents[key])

    return lines
#write a dict to csv
def write_to_csv(header, contents, file_name):
    ''' write a dict to csv file
        Arg:
            header: header of csv file
            contents:a dictionary which will be writtern
            file_name: a qualified file name which contents will be writtern to.
    '''
    if not isinstance(header, list):
        raise TypeError("The argument header must be a list!")
    if not isinstance(contents, dict) and isinstance(contents, list):
        raise TypeError("The argument contents must be a dict or a list!")
    with open(file_name, mode='w') as csvfile:
        writer = csv.writer(csvfile)
        #writer.writerow(header)
        csvlines = __write_dictionary_to_csvline__(contents, [])
        for line in csvlines:
            writer.writerow(line)
