# add any other imports you need here!
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt, exp



# use this to compute distance, not Euclidean Distance!
def haversine(lat1, lon1, lat2, lon2):

      R = 3959.87433 # this is in miles.  For Earth radius in kilometers use 6372.8 km

      dLat = radians(lat2 - lat1)
      dLon = radians(lon2 - lon1)
      lat1 = radians(lat1)
      lat2 = radians(lat2)

      a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
      c = 2*asin(sqrt(a))

      return R * c

def logistic(x):
  return 1 / (1 + exp(-4*x))

def optimal_center_formula(county_lat, county_long, potential_center_lat, potential_center_long, county_classification):
    distance = haversine(county_lat, county_long, potential_center_lat, potential_center_long)
    
    # perform some mathematical operation with this calculated distance and the county classification!
    LARGEST_DISTANCE = 3000 # rough distance accross the US
    MAX_CLASSIFICATION = 8
    distance_score = 2 * (1 - logistic(distance / (LARGEST_DISTANCE))) # multiply by 2 to get a normalized value between 0 and 1
    need_score = ((county_classification) / MAX_CLASSIFICATION) ** (1 / 2)
    
    score = distance_score * need_score
    return score








#Below are Simply Test Cases





def test_optimal_center_formula():
    # testcase 1: should return a high value, since coordinates are close and need is high
    montgomery_lat = 39.746151
    montgomery_long = -084.207549
    xenia_center_lat = 39.686560
    xenia_center_long = -83.924960
    montgomery_classification = 8
    print("Testcase 1 (should return a value close to 1): ", optimal_center_formula(montgomery_lat, montgomery_long, xenia_center_lat, xenia_center_long, montgomery_classification))
    
    # testcase 2: should return a low value, since coordinates are far and need is low
    orange_county_lat = 33.733953
    orange_county_long = -117.862880
    fayetsville_center_lat = 35.148310
    fayetsville_center_long = -86.579200
    orange_county_classification = 0
    print("Testcase 2 (should return a value close to 0): ", optimal_center_formula(orange_county_lat, orange_county_long, fayetsville_center_lat, fayetsville_center_long, orange_county_classification))
    
    # testcase 3: should return a moderate-low value, since coordinates are far even though need is high
    toelle_county_lat = 40.560780
    toelle_county_long = -112.379217
    fayetsville_center_lat = 35.148310
    fayetsville_center_long = -86.579200
    toelle_county_classification = 8
    print("Testcase 3 (should return a lower value (~0.1-0.3)): ", optimal_center_formula(toelle_county_lat, toelle_county_long, fayetsville_center_lat, fayetsville_center_long, toelle_county_classification))
    
    # testcase 4: should return a moderate-high value, since coordinates are close and need is moderate
    williamson_tx_lat = 30.554707
    williamson_tx_long = -97.711430
    round_rock_center_lat = 30.533330
    round_rock_center_long = -97.694740
    williamson_classification = 4
    print("Testcase 4 (should return moderate value (~0.5-0.9)): ", optimal_center_formula(williamson_tx_lat, williamson_tx_long, round_rock_center_lat, round_rock_center_long, williamson_classification))

#test_optimal_center_formula()