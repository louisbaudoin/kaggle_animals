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
from sklearn import metrics
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
from sklearn import cross_validation
from sklearn import metrics

def get_metrics(y_actual, y_pred):
  labels = ['Adoption', 'Transfer', 'Return_to_owner', 'Euthanasia', 'Died']
  conf_mat = metrics.confusion_matrix(y_actual, y_pred, labels = labels)
  actual_sum = conf_mat.sum(axis = 1)
  predicted_sum = conf_mat.sum(axis = 0)
  for i in range(0,5):
    precision = conf_mat[i,i]/actual_sum[i]
    recall = conf_mat[i,i]/predicted_sum[i]
    print '----------------Metrics of %s---------------' %labels[i]
    print 'Precision :  %s' %precision
    print 'Recall :  %s' %recall
  return
