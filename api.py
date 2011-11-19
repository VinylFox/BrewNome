import web
import json
import sqlobject as db
from models import *

db.sqlhub.processConnection = db.connectionForURI("mysql://brewnome:br3wl0v3r@localhost/brewnome")

class beer_list:
  def GET(self):
    beers = Beer.select()
    
    resp = {'beers': []}
    for beer in beers:
      resp['beers'].append({'id': beer.id, 'name': beer.beer_name})

    web.header('Content-Type', 'application/json')
    return json.dumps(resp)

class beer_details:
  def GET(self, id):
    b = Beer.get(int(id))
    
    resp = {}
    resp['beer_name'] = b.beer_name 
    resp['beer_class'] = b.beer_class
    resp['beer_sub_class'] = b.beer_sub_class
    resp['brewer_name'] = b.brewer_name
    resp['brewer_country'] = b.brewer_country
    resp['brewer_region'] = b.brewer_region
    resp['beer_color'] = b.beer_color
    resp['carbonation'] = b.carbonation
    resp['heaviness_or_fullness'] = b.heaviness_or_fullness
    resp['hoppiness'] = str(b.hoppiness)
    resp['food_flavor_1'] = b.food_flavor_1
    resp['food_flavor_2'] = b.food_flavor_2
    resp['food_flavor_3'] = b.food_flavor_3
    resp['food_flavor_4'] = b.food_flavor_4
    resp['food_flavor_5'] = b.food_flavor_5
    resp['sweetness'] = b.sweetness
    resp['starch_grain_type_1'] = b.starch_grain_type_1
    resp['starch_grain_type_2'] = b.starch_grain_type_2
    resp['starch_grain_type_3'] = b.starch_grain_type_3
    resp['starch_grain_type_4'] = b.starch_grain_type_4
    resp['starch_grain_type_5'] = b.starch_grain_type_5
    resp['starch_grain_sub_type_1'] = b.starch_grain_sub_type_1
    resp['starch_grain_sub_type_2'] = b.starch_grain_sub_type_2
    resp['starch_grain_sub_type_3'] = b.starch_grain_sub_type_3
    resp['starch_grain_sub_type_4'] = b.starch_grain_sub_type_4
    resp['starch_grain_sub_type_5'] = b.starch_grain_sub_type_5
    resp['malted_or_unmalted_starch_grain'] = b.malted_or_unmalted_starch_grain
    resp['hops_type_1'] = b.hops_type_1
    resp['hops_type_2'] = b.hops_type_2
    resp['hops_type_3'] = b.hops_type_3
    resp['hops_type_4'] = b.hops_type_4
    resp['hops_type_5'] = b.hops_type_5
    resp['yeast_type_1'] = b.yeast_type_1
    resp['yeast_type_2'] = b.yeast_type_2
    resp['yeast_type_3'] = b.yeast_type_3
    resp['yeast_type_4'] = b.yeast_type_4
    resp['yeast_type_5'] = b.yeast_type_5
    resp['seasonality']	= b.seasonality
    resp['alcohol_percentage'] = str(b.alcohol_percentage)
    resp['brewer_volume_of_distribution'] = b.brewer_volume_of_distribution
    resp['bottle_retail_price'] = b.bottle_retail_price
    resp['roasting_time'] = b.roasting_time
    resp['roasting_temperature'] = b.roasting_temperature
    resp['clarifying_agents'] = b.clarifying_agents
    resp['fermentation_style'] = b.fermentation_style
    resp['fermentation_temperature'] = b.fermentation_temperature
    resp['second_fermentation'] = b.second_fermentation
    resp['continuous_fermentation'] = b.continuous_fermentation
    resp['serving_temperature'] = b.serving_temperature
    resp['crispness'] = b.crispness
    resp['aroma'] = b.aroma
    resp['head_retention'] = b.head_retention
    resp['cask_conditioning'] = b.cask_conditioning
    resp['calorie_count'] = b.calorie_count
    resp['spices_1'] = b.spices_1
    resp['spices_2'] = b.spices_2
    resp['spices_3'] = b.spices_3
    resp['spices_4'] = b.spices_4
    resp['spices_5'] = b.spices_5
    resp['herbs_1'] = b.herbs_1
    resp['herbs_2'] = b.herbs_2
    resp['herbs_3'] = b.herbs_3
    resp['herbs_4'] = b.herbs_4
    resp['herbs_5'] = b.herbs_5
    resp['clarity'] = b.clarity
    resp['age'] = str(b.age)

    web.header('Content-Type', 'application/json')
    return json.dumps(resp)

class beer_autocomplete:
  def GET(self, name):
    beers = Beer.select(Beer.q.beer_name.startswith(web.websafe(name)))
    
    resp = {'beers': []}
    for beer in beers:
      resp['beers'].append({'id': beer.id, 'name': beer.beer_name})

    web.header('Content-Type', 'application/json')
    return json.dumps(resp)
    
class suggest:
  def GET(self, id):
    b = Beer.get(int(id))
    
    beers = Beer.select()
    
    resp = {'beers': []}
    for beer in beers:
      b_temp = {}
      
      b_temp['id'] = beer.id
      
      if beer.beer_class == b.beer_class:
        b_temp['beer_class'] = 1
        
      if beer.beer_sub_class == b.beer_sub_class:
        b_temp['beer_sub_class'] = 1
      
      resp['beers'].append(b_temp)  
  
  
    #resp = {'beers': []}
    #for beer in beers:
    #  resp['beers'].append({'id': beer.id, 'name': beer.beer_name})

    web.header('Content-Type', 'application/json')
    return json.dumps(resp)
    

