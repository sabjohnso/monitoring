"""

"""

import os
import re
import csv
from datetime import datetime

def validate_date(year, month, day):
    date = datetime(year)


def sort(xs : list) -> list:
    ys = [x for x in xs]
    ys.sort()
    return ys
LABEL_SEQUENCE1 = ['Province/State', 'Country/Region', 'Last Update',  'Confirmed', 'Deaths', 'Recovered']
LABEL_SEQUENCE2 = ['FIPS', 'Admin2', 'Province_State', 'Country_Region', 'Last_Update', 'Lat', 'Long_', 'Confirmed', 'Deaths', 'Recovered', 'Active', 'Combined_Key']

LABEL_SETS = [
    set(LABEL_SEQUENCE1),
    set(LABEL_SEQUENCE2)]

def inTexas(string : str) -> bool:
    return re.match("Texas.*") is None and not re.match(".*Texas.*") is None


class DailyReports(object):
    def __init__(self, reports_path):
        self.path = reports_path
        self.setupPaths()
        self.setupPathDict()
        self.setupDataDict()
        self.setupDates()

    def setupPaths(self):
        self.csv_file_names = filter(
            (lambda x: not re.match(".*\\.csv$", x) is None),
            os.listdir(self.path))

            
    def setupPathDict(self):
        self.path_dict = {}
        for file_name in self.csv_file_names:
            self.path_dict[self.pathToDate(file_name)] = self.path + '/' + file_name

    
    def extractLabels1(self, date, rows):
        for row in rows:
            if row['Province/State'] == '':
                location = row['Country/Region']
            else:
                location = row['Province/State'] + ', ' + row['Country/Region']
                self.data[date][location] = {
                    'LastUpdate' : row['Last Update'],
                    'Confirmed'   : int(row['Confirmed']),
                    'Deaths'      : int(row['Deaths']),
                    'Recovered'   : int(row['Recovered'])
                }

    def extractLabels2(self, date, rows):
        for row in rows:
            admin2 = row['Admin2'] + ', ' if not row['Admin2'] == '' else ''
            province = row['Province_State'] + ', ' if not row['Province_State'] == '' else ''
            location = admin2 + province + row['Country_Region']
            self.data[date][location] = {
                'LastUpdate' : row['Last_Update'],
                'Confirmed' : int(row['Confirmed']),
                'Deaths'    : int(row['Deaths']),
                'Recovered' : int(row['Recovered'])
        }
            

    def setupDataDict(self):
        self.data = {}
        for date in self.path_dict.keys():
            self.data[date] = {}
            with open(self.path_dict[date], 'r') as csv_file:
                reader = csv.DictReader(csv_file)                
                if set(reader.fieldnames) in LABEL_SETS:
                    if reader.fieldnames == LABEL_SEQUENCE1:
                        self.extractLabels1(date, reader)
                    elif reader.fieldnames == LABEL_SEQUENCE2:
                        self.extractLabels2(date, reader)
                    else:
                        ValueError('Unsupported key order: ', reader.fieldnames)
                else:
                    ValueError('Unsupported keys: ', reader.fieldnames)

    def setupDates(self):
        self.dates = list(self.data.keys())
        self.dates.sort()

    @property
    def TotalConfirmed(self):
        result = {}
        for date in self.dates:
            AllKeys = self.data[date].keys()
            confirmed = 0
            for key in AllKeys:
                confirmed += self.data[date][key]['Confirmed']
            result[date] = confirmed
        return result
        
                

    
    def pathToDate(self, string : str) -> datetime:
        m = re.match("(?P<month>[0-9]{2,2})-(?P<day>[0-9]{2,2})-(?P<year>[0-9]{4,4})\\.csv", string)
        if not m is None:
            components = m.groupdict()
            return datetime(int(components['year']),
                            int(components['month']),
                            int(components['day']))
        else:
            raise ValueError('Invalid path: ' + string)

        
    def dateToPath(self, date : datetime) -> str :
        return str(date.month) + '-' + str(date.day) +  '-' + str(date.year)

        
        
        

        
