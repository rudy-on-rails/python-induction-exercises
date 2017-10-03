from __future__ import division
import numpy as np
import pandas as pd
import csv
import re

class MRCalculator(object):
  def __init__(self, filepath):
    super(MRCalculator, self).__init__()
    self.filepath = filepath

  def calculate_attitudinal_equity(self):
    range_of_columns = xrange(118,126)
    with open(self.filepath, 'rb') as csvfile:
      brand_names_pattern = re.compile('""(\w|\W)+""')
      csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
      headers = csv_reader.next()
      brands = []
      for x in range_of_columns:
        brands.append(brand_names_pattern.search(headers[x]).group().replace('""',''))
      ranks = []
      respondent_data = []
      for row in csv_reader:
        respondent_ratings = []
        for x in range_of_columns:
          if row[x]:
            respondent_ratings.append(row[x])
          else:
            respondent_ratings.append(0)
        respondent_data.append(respondent_ratings)
        ranks.append(pd.Series(respondent_ratings).rank(method='average', ascending=False))
      ndranks = np.array(ranks)
      ndarray_respondent_ratings = np.array(respondent_data)
      ranks_sum_divided = (1 / ndranks).sum(axis=1)
      equity = 1 / (ndranks * np.split(np.repeat(ranks_sum_divided, 8), len(ranks_sum_divided)))
      print equity[0]

calculator = MRCalculator('./responses.csv')
calculator.calculate_attitudinal_equity()
