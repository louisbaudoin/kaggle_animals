# Import dependencies
from __future__ import division
import pandas as pd
import csv
import numpy as np
import datetime #from datetime import datetime
import calendar #necessary to convert a timestamp into a date
import time
from math import sqrt
import numpy.random as random
from datetime import datetime
import time
from datetime import datetime

# Dummify what needs to be dummified
def dummify_data(datap, features_to_dummify):
  # select features to dummify
  data_to_dumm = datap[features_to_dummify]
  # change months to str to allow dummify
  data_to_dumm['Month'] = data_to_dumm['Month'].map(lambda x: str(x))
  # dummify
  data_dumm = pd.get_dummies(data_to_dumm)
  # delete redundant features
  for feature in features_to_dummify:
      del datap[feature]
  # merge dummy and non-dummy features
  data_model = datap.merge(data_dumm, how = 'left', left_index = True, right_index = True)
  return data_model


def process_data(data):
  # Process names
  data['Name_known'] = data.apply(known_vs_unknown_name, axis = 1)
  del data['Name']
  # Process dates
  data = process_date(data)
  del data['DateTime']
  # Process type (cat or dog)
  data = process_type(data)
  # Process SexuponOutcume (clear Nan)
  data['SexuponOutcome'].fillna('Unknown', inplace = True)
  # Process age
  data = process_age(data)
  data['age_number'] = data.apply(_refresh_age_metric, axis = 1)
  # delete animal ID and former age column
  del data['AgeuponOutcome']
  del data['AnimalID']
  # Simplify breeds
  #breeds_to_keep = data['Breed'].value_counts(dropna = False).head(27)
  #data['Breed_simpl'] = data['Breed'].map(lambda breed: _streamline_breed(breed, breeds_to_keep))
  data['Is_mix'] = data['Breed'].map(lambda breed: 1 if 'Mix' in breed else 0)
  data['simpl_breed'] = data['Breed'].map(simpl_breed)
  del data['Breed']
  # delete second level of outcome (for now)
  del data['OutcomeSubtype']
  # del color (for now)
  data['simpl_color'] = data['Color'].map(simpl_color)
  del data['Color']
  # Create Sex column
  data['Sex'] = data['SexuponOutcome'].map(split_Sex)
  # Create State column
  data['State'] = data['SexuponOutcome'].map(split_State)
  # Delete former sex column
  del data['SexuponOutcome']
  return data


# Known vs unknow name
def known_vs_unknown_name(row):
  if pd.isnull(row['Name']):
    return 1
  else:
    return 0

# Change dates from string to dates and create a columns 'month'
def process_date(data):
  data['DateTime'] = data['DateTime'].map(lambda date: datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))
  data['Month'] = data.apply(lambda row: row['DateTime'].month, axis = 1)
  data['Hour'] = data.apply(lambda row: row['DateTime'].hour, axis = 1)
  data['Is_morning'] = data['DateTime'].map(_is_morning)
  return data

def _is_morning(day):
  if day.hour >= 12:
    return 0
  else:
    return 1

# Process type (cat or dog)
def process_type(data):
  type_mapping = {'Dog': 1, 'Cat': 0}
  data['Is_Dog'] = data['AnimalType'].map(type_mapping)
  del data['AnimalType']
  return data

# Process age
def process_age(data):
  # fix naans
  data['AgeuponOutcome'].fillna('Unknown Unknown', inplace = True)
  # dummy column if age known
  data['Age_known'] = data['AgeuponOutcome'].map(lambda x: 0 if x == 'Unknown Unknown' else 1)
  # split age number and metric and create columns
  data['age_temp'] = data['AgeuponOutcome'].map(lambda x: x.split(' '))
  data['age_number'] = data['AgeuponOutcome'].map(lambda x: x.split(' ')[0])
  data['age_metric'] = data['AgeuponOutcome'].map(lambda x: x.split(' ')[1])
  # reprocess age metric
  data = _reprocess_age_metrics(data)
  # reprocess age number
  data['age_number'] = data['age_number'].map(_reprocess_age_number)
  # deleter age_temp
  del data['age_temp']
  return data

# Reprocess age_metric
def _reprocess_age_metrics(data):
  age_metrics = {
    'years': 'years',
    'year': 'years',
    'weeks': 'weeks',
    'week': 'weeks',
    'day': 'days',
    'days':'days',
    'month': 'month',
    'months': 'month',
    'Unknown':'Unknown'
  }
  data['age_metric'] = data['age_metric'].map(age_metrics)
  return data

# put age to 0 if not in years
def _refresh_age_metric(row):
  if row['age_metric'] != 'years':
    return 0
  else:
    return row['age_number']


# Converts age from string to integer
def _reprocess_age_number(age):
  if age != 'Unknown':
    return int(age)
  else:
    return age

# Create sex column
def split_Sex(sex_state):
  if sex_state == 'Unknown':
    return 'Unknown'
  else:
    return sex_state.split(' ')[1]

# Crete State Column
def split_State(sex_state):
  if sex_state == 'Unknown':
    return 'Unknown'
  else:
    return sex_state.split(' ')[0]

# simplify breed

def simpl_breed(breed):
  # Ignore the mix
  if 'Mix' in breed:
    breed = breed[:len(breed) -4]

  # Take only the first one
  if ' ' in breed:
    return breed.split(' ')[0]
  elif '/' in breed:
    return breed.split('/')[0]
  else:
    return breed

def simpl_color(color):

  # Take only the first one
  if ' ' in color:
    return color.split(' ')[0]
  elif '/' in color:
    return color.split('/')[0]
  else:
    return color



# Streamline breed
# def _streamline_breed(breed, breeds_to_keep):
# if breed in breeds_to_keep:
#     return breed
# else:
#   return 'Other'

# Breed - mix or not mix







