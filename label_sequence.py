"""

"""

__all__ = ['LabelSequence']

import inspect
import os
import json
import jsonschema

def maybeInt(string : str):
    return int(string) if not string == '' else None

schema_basename = 'LabelSequence-schema.json'
schema_location = os.path.dirname(__file__) + '/' + schema_basename
with open(schema_location, 'r') as schema_file:
    schema = json.load(schema_file)

class LabelSequence(object):
    def __init__(self, file_name):
        with open(file_name, 'r') as label_file:
            data = json.load(label_file)
        jsonschema.validate(data, schema)
        self.__labels = data['labels']
        self.__location = data['labelMap']['Location']
        self.__confirmed = data['labelMap']['Confirmed']
        self.__deaths = data['labelMap']['Deaths']
        self.__recovered = data['labelMap']['Recovered']

    def __extractLocation(self, row):
        location = ''
        for part in self.__location[:-1]:
            if not row[part] == '': location += row[part] + ', '
        location += row[self.__location[-1]]
        return location

    def isMatch(self, labels):
        return labels == self.__labels

    def mapRows(self, rows):
        result = {}
        for row in rows:
            result[self.__extractLocation(row)] = {
                'Confirmed' : maybeInt(row[self.__confirmed]),
                'Deaths' : maybeInt(row[self.__deaths]),
                'Recovered' : maybeInt(row[self.__recovered])
            }
        return result
