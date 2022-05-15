from PIL import Image
import pytesseract
import datetime
import sys
import os
import re
import numpy as np


class Dl_Validator:
    def __init__(self, text):
        self.text = text
        self.return_params = {}

    def is_license(self):
        result = self.text.split('/n')
        for word in result:
            if word == 'Driving' or 'DRIVING':
                print('Valid Drivers License')
                self.return_params['is_valid'] = True
                return True
            else:
                print('Document is not a valid Drivers License')
                print('Please try again')
                self.return_params['is_valid'] = False
                return False

    def age(self, year, month, day):
        '''
        Function to extract the Date Of Birth.
        '''
        dob = datetime.date(year, month, day)
        today = datetime.date.today()
        years = today.year - dob.year
        if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
            years -= 1
        return years

    def is_valid(self):
        '''
        Function to check if the Drivers License is Expired or not.
        '''
        if self.is_license():
            self.return_params['id_type'] = 'Drivers License'
            res = self.text.split()
            match = None
            day = None
            month = None
            year = None
            date_of_expiry = None
            dob = None
            count = 0
            strings_with_states = []
            list_of_states = {'JK', 'HP', 'PN', 'CH', 'UK', 'UA', 'HR', 'DL', 'RJ', 'UP', 'BR', 'SK', 'AR',
                              'AS', 'NL', 'MN', 'ML', 'TR', 'MZ', 'WB', 'JH', 'OR', 'OD', 'CG', 'MP', 'GJ', 'MH', 'DD', 'DN', 'TS',
                              'AP', 'KA', 'KL', 'TN', 'PY', 'GA', 'AN', 'LD'}

            # re to get all dates:
            date_re = re.compile('[0-9]+\/[0-9]+\/[0-9]+')
            if date_re.findall(self.text):
                dates = date_re.findall(self.text)
            else:
                date_re = re.compile('[0-9]+-[0-9]+-[0-9]+')
                dates = date_re.findall(self.text)

            now = datetime.datetime.now()

            for date in dates:
                if '/' in date:
                    day, month, year = date.split('/')
                else:
                    day, month, year = date.split('-')
                age = self.age(int(year), int(month), int(day))
                temp_date = datetime.datetime(int(year), int(month), int(day))
                if temp_date >= now:
                    date_of_expiry = temp_date
                if age >= 18:
                    dob = temp_date

            if date_of_expiry:
                print("Date of expiry :" +
                      str(date_of_expiry.strftime('%Y-%m-%d')))
                self.return_params['expiry_date'] = date_of_expiry.strftime(
                    '%Y-%m-%d')
            else:
                print("Cannot determine the date of expiry or the licence has expired")
                self.return_params['expiry_date'] = None

            if dob:
                print("Date of birth :" + str(dob.strftime('%Y-%m-%d')))
                self.return_params['DOB'] = dob.strftime('%Y-%m-%d')
            elif 'DOB' in res:
                index = res.index('DOB')
                if ':' not in res[index+1]:
                    print('DOB is: ' + res[index+1])
                    self.return_params['DOB'] = res[index + 1]
                else:
                    print('DOB is: ' + res[index+2])
                    self.return_params['DOB'] = res[index + 2]
            else:
                print("Cannot determine the date of birth")
                self.return_params['DOB'] = None

            for word in res:
                for state in list_of_states:
                    if state in word:
                        strings_with_states.append(word)

            for string in strings_with_states:
                for i in string:
                    if(i.isdigit()):
                        count = count+1

                if count < 13:
                    index = res.index(string)
                    s = res[index] + res[index + 1]
                    if len(s) >= 15:
                        for i in s:
                            if(i.isdigit()):
                                count = count+1
                        if count > 13:
                            s = s[-16:]
                            self.return_params['license_number'] = s
                            print('Driving licence # is :' + s)
                            break
                else:
                    self.return_params['license_number'] = string
                    print('Driving licence # is :' + string)
                    break

            self.return_params['first_name'] = None
            self.return_params['middle_name'] = None
            self.return_params['last_name'] = None
            lines = self.text.split('\n')
            lines = [x for x in lines if x != '']
            print(lines)
            for i in range(len(lines)):
                if 'Licence No.' in lines[i]:
                    break
                i += 1
            name_re = re.compile("[a-zA-Z]+ [[a-zA-Z]+")
            names = name_re.findall(lines[i+1].strip())[0].split(' ')
            self.return_params['first_name'] = names[0]
            if len(names) == 2:
                self.return_params['last_name'] = names[1]
            elif len(names) == 3:
                self.return_params['last_name'] = names[2]
                self.return_params['middle_name'] = names[1]
            # if 'Name' in res:
            #     index = res.index('Name')
            #     name = res[index + 1] + ' ' + res[index + 2]
            #     print('Name of licence holder: ' + name)
            #     self.return_params['name'] = name
            # else:
            #     self.return_params['name'] = None
            return self.return_params
