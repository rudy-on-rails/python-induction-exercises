from __future__ import division
import csv
import re

class AttitudinalEquity(object):
  def __init__(self, respondents_brands_ratings):
    super(AttitudinalEquity, self).__init__()
    self.respondents_brands_ratings = respondents_brands_ratings

  def calculate(self):
    ranking_per_respondent = self.ranking_per_respondent();
    for ranking in ranking_per_respondent:
      ranks_sum = 0
      for brand_rating in ranking:
        if brand_rating['rank']:
          ranks_sum += 1 / brand_rating['rank']
      for brand_rating in ranking:
        if brand_rating['rank']:
          attitudinal_equity = 1 / (brand_rating['rank'] * ranks_sum)
        else:
          attitudinal_equity = 0.0
        brand_rating['attitudinal_equity'] = attitudinal_equity
    return ranking_per_respondent

  def ranking_per_respondent(self):
    rankings = []
    for respondent_brands_rating in self.respondents_brands_ratings:
      start_pos = 1
      respondent_data = []
      for brands_rated in respondent_brands_rating.rank_ratings():
        brands = brands_rated[1].split("|")
        respondent_data.append({
          'rating': brands_rated[0],
          'brands': brands,
          'rank': sum(xrange(start_pos, start_pos + len(brands))) / len(brands) if brands_rated[0] else 0
        })
        start_pos+=1
      rankings.append(respondent_data)
    return rankings

  def avg_rating_per_brand(self):
    avg_rating_per_brand = {}
    for respondent_brand_performance in self.respondents_brands_ratings:
      for brand_performance in respondent_brand_performance.respondent_brands_ratings_array:
        if not avg_rating_per_brand.has_key(brand_performance.brand_name):
          avg_rating_per_brand[brand_performance.brand_name] = {
            'count': 0,
            'score': 0
          }

        if brand_performance.rating:
          avg_rating_per_brand[brand_performance.brand_name]['score'] += brand_performance.rating
          avg_rating_per_brand[brand_performance.brand_name]['count'] += 1

    for brand, score in avg_rating_per_brand.iteritems():
      avg_rating_per_brand[brand] = avg_rating_per_brand[brand]['score'] / avg_rating_per_brand[brand]['count']

    return avg_rating_per_brand

  def total_respodents(self):
    return len(self.respondents_brands_ratings)

  def __repr__(self):
    return str(self.respondents_brands_ratings[0])

class RespondentBrandsRating(object):
  def __init__(self, respondent_brands_ratings_array):
    super(RespondentBrandsRating, self).__init__()
    self.respondent_brands_ratings_array = respondent_brands_ratings_array

  def rank_ratings(self):
    ranked = {}
    max_rank = len(self.respondent_brands_ratings_array)
    for respondent_brand_rating in self.respondent_brands_ratings_array:
      if ranked.has_key(respondent_brand_rating.rating):
        ranked[respondent_brand_rating.rating] += "|" + respondent_brand_rating.brand_name
      else:
        ranked[respondent_brand_rating.rating] = respondent_brand_rating.brand_name
    return sorted(ranked.items())[::-1]

class BrandRating(object):
  def __init__(self, brand_name, rating):
    super(BrandRating, self).__init__()
    self.brand_name = brand_name
    self.rating = None
    if rating:
      self.rating = int(rating)

  def __repr__(self):
    return self.brand_name + ' => ' + str(self.rating)

class MRCalculator(object):
  def __init__(self, filepath):
    super(MRCalculator, self).__init__()
    self.filepath = filepath

  def calculate_attitudinal_equity(self):
    range_of_columns = xrange(118,125)
    with open(self.filepath, 'rb') as csvfile:
      brand_names_pattern = re.compile('""(\w|\W)+""')
      csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
      headers = csv_reader.next()
      brands = []
      for x in range_of_columns:
        brands.append(brand_names_pattern.search(headers[x]).group().replace('""',''))
      respondent_branding_performances = []
      for row in csv_reader:
        count = 0
        respondent_ratings = []
        for x in range_of_columns:
          respondent_ratings.append(BrandRating(brands[count], row[x]))
          count+=1
        respondent_branding_performances.append(RespondentBrandsRating(respondent_ratings))
      print AttitudinalEquity(respondent_branding_performances).calculate()

calculator = MRCalculator('./responses.csv')
calculator.calculate_attitudinal_equity()
