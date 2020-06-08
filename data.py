"""

"""

import os
import re
import csv
from datetime import datetime
import numpy as np


from label_sequence import LabelSequence

def validate_date(year, month, day):
    date = datetime(year)


def sort(xs : list) -> list:
    ys = [x for x in xs]
    ys.sort()
    return ys

def countLines(file_name : str) -> int:
    count = 0
    with open(file_name, 'r') as file:
        for line in file.readlines():
            count += 1
    return count

def maybeInt(string : str):
    return int(string) if not string == '' else None


DAILY_REPORTS_PATH="/home/sbj/Sandbox/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports"
LABEL_SEQUENCE_PATHS=[
    "labelSequence1.json",
    "labelSequence1WithCoords.json",
    "labelSequence2.json",
    "labelSequence3.json"
]

LABEL_SEQUENCE1 = [
    'Province/State',
    'Country/Region',
    'Last Update',
    'Confirmed',
    'Deaths',
    'Recovered'
]
LABEL_SEQUENCE1_COORDS = [
    'Province/State',
    'Country/Region',
    'Last Update',
    'Confirmed',
    'Deaths',
    'Recovered',
    'Latitude',
    'Longitude'
]

LABEL_SEQUENCE2 = [
    'FIPS',
    'Admin2',
    'Province_State',
    'Country_Region',
    'Last_Update',
    'Lat',
    'Long_',
    'Confirmed',
    'Deaths',
    'Recovered',
    'Active',
    'Combined_Key'
]


LABEL_SETS = [
    set(LABEL_SEQUENCE1),
    set(LABEL_SEQUENCE2)]

def inTexas(string : str) -> bool:
    return re.match("Texas.*", string) is None and not re.match(".*Texas.*", string) is None

def inNewYork(string : str) -> bool:
    return not re.match(".*New York.*", string) is None

def inCalifornia(string : str) -> bool:
    return not re.match(".*California.*", string) is None

def ismatch(pattern, string):
    return not re.match(pattern, string) is None

def regexPredicate(pattern):
    return lambda x : ismatch(pattern, x)


def makeStatePredicate(state_name : str) -> bool:
    return regexPredicate(".*, " + state_name + ".*")


STATES = [
    'Alabama',
    'Alaska',
    'Arizona',
    'Arkansas',
    'California',
    'Colorado',
    'Connecticut',
    'Delaware',
    'Florida',
    'Georgia',
    'Hawaii',
    'Idaho',
    'Illinois',
    'Indiana',
    'Iowa',
    'Kansas',
    'Kentucky',
    'Louisiana',
    'Maine',
    'Maryland',
    'Massachusetts',
    'Michigan',
    'Minnesota',
    'Mississippi',
    'Missouri',
    'Montana',
    'Nebraska',
    'Nevada',
    'New Hampshire',
    'New Jersey',
    'New Mexico',
    'New York',
    'North Carolina',
    'North Dakota',
    'Ohio',
    'Oklahoma',
    'Oregon',
    'Pennsylvania',
    'Rhode Island',
    'South Carolina',
    'South Dakota',
    'Tennessee',
    'Texas',
    'Utah',
    'Vermont',
    'Virginia',
    'Washington',
    'West Virginia',
    'Wisconsin',
    'Wyoming']

def conditionCumulativeSequence(xs : list) -> list:
    result = []
    xprev = xs[0]
    for x in xs:
        if x == 0 and xprev != 0:
            result.append(xprev)
        else:
            result.append(x)
            xprev = x
    return result
    
    

    
class DailyReports(object):
    def __init__(self, reports_path = DAILY_REPORTS_PATH, label_sequence_paths = LABEL_SEQUENCE_PATHS):

        self.path = reports_path
        self.__setupPaths()
        self.__setupPathDict()
        
        self.__label_sequence_paths = label_sequence_paths
        self.__setupLabelSequences()

        self.__setupDataDict()
        self.__setupDates()

    def __setupPaths(self):
        """ Set the csv_file_names member
        """
        self.csv_file_names = filter(
            (lambda x: not re.match(".*\\.csv$", x) is None),
            os.listdir(self.path))

            
    def __setupPathDict(self):
        self.path_dict = {}
        for file_name in self.csv_file_names:
            self.path_dict[self.__pathToDate(file_name)] = self.path + '/' + file_name


    def __setupLabelSequences(self):
        label_sequences = []
        for path in self.__label_sequence_paths:
            label_sequences.append(LabelSequence(path))
        self.__label_schemas = label_sequences

    def __extractData(self, file_name):
        with open(file_name, 'r') as csv_file:
            reader = csv.DictReader(csv_file)

        
    def __extractLabels1(self, rows):
        result = {}
        for row in rows:
            province = row['Province/State'] + ', ' if not row['Province/State'] == '' else ''
            location = province + row['Country/Region']
            result[location] = {
                'LastUpdate' : row['Last Update'],
                'Confirmed'   : maybeInt(row['Confirmed']),
                'Deaths'      : maybeInt(row['Deaths']),
                'Recovered'   : maybeInt(row['Recovered'])
            }
        return result    

    def __extractLabels2(self, rows):
        result = {}
        for row in rows:
            admin2 = row['Admin2'] + ', ' if not row['Admin2'] == '' else ''
            province = row['Province_State'] + ', ' if not row['Province_State'] == '' else ''
            location = admin2 + province + row['Country_Region']
            result[location] = {
                'LastUpdate' : row['Last_Update'],
                'Confirmed' : maybeInt(row['Confirmed']),
                'Deaths'    : maybeInt(row['Deaths']),
                'Recovered' : maybeInt(row['Recovered'])
            }
        return result

    def __setupDailyData(self, file_name):
        with open(file_name, 'r', encoding= 'utf-8-sig') as csv_file:
            reader = csv.DictReader(csv_file)
            fieldnames = reader.fieldnames
            for schema in self.__label_schemas:
                if schema.isMatch(fieldnames):
                    return schema.mapRows(reader)
            else:
                raise ValueError('Unsupported field names : ', fieldnames)
        # with open(file_name, 'r', encoding= 'utf-8-sig') as csv_file:
        #     reader = csv.DictReader(csv_file)
        #     fieldnames = reader.fieldnames
        #     if fieldnames == LABEL_SEQUENCE1 or fieldnames == LABEL_SEQUENCE1_COORDS:
        #         return self.__extractLabels1(reader)
        #     elif fieldnames == LABEL_SEQUENCE2:
        #         return self.__extractLabels2(reader)
        #     else:
        #         raise ValueError('Unsupported field names : ', fieldnames)
    
    def __setupDataDict(self):
        self.data = {}
        for date in self.path_dict.keys():
            try:
                self.data[date] = self.__setupDailyData(self.path_dict[date])
            except ValueError as e:
                raise ValueError(date,self.path_dict[date], e)


    def __setupDates(self):
        self.dates = list(self.data.keys())
        self.dates.sort()

    @property
    def TotalConfirmed(self):
        result = {}
        for date in self.dates:
            AllKeys = self.data[date].keys()
            confirmed = 0
            for key in AllKeys:
                if not self.data[date][key]['Confirmed'] is None:
                    confirmed += self.data[date][key]['Confirmed']
            result[date] = confirmed
        return result

    @property
    def TotalDeaths(self):
        result = {}
        for date in self.dates:
            AllKeys = self.data[date].keys()
            died = 0
            for key in AllKeys:
                if not self.data[date][key]['Deaths'] is None:
                    died += self.data[date][key]['Deaths']
            result[date] = died
        return np.array(result)

    def filteredDeaths(self, pred):
        result = {}
        for date in self.dates:
            Keys = filter(pred, self.data[date].keys())
            died = 0
            for key in Keys:
                if not self.data[date][key]['Deaths'] is None:
                    died += self.data[date][key]['Deaths']
            result[date] = died
        return np.array(conditionCumulativeSequence([result[date] for date in self.dates]))


    def filteredConfirmed(self, pred):
        result = {}
        for date in self.dates:
            Keys = filter(pred, self.data[date].keys())
            confirmed = 0
            for key in Keys:
                if not self.data[date][key]['Confirmed'] is None:
                    confirmed += self.data[date][key]['Confirmed']
            result[date] = confirmed
        return np.array(conditionCumulativeSequence([result[date] for date in self.dates]))
    
    def __pathToDate(self, string : str) -> datetime:
        m = re.match("(?P<month>[0-9]{2,2})-(?P<day>[0-9]{2,2})-(?P<year>[0-9]{4,4})\\.csv", string)
        if not m is None:
            components = m.groupdict()
            return datetime(int(components['year']),
                            int(components['month']),
                            int(components['day']))
        else:
            raise ValueError('Invalid path: ' + string)

    # TODO: Unused, delete
    def __dateToPath(self, date : datetime) -> str :
        return str(date.month) + '-' + str(date.day) +  '-' + str(date.year)

        

        
def delta(xs):
    return xs[1:]-x[:-1]


