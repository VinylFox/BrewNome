baseurl = '/home/brewnome/www/brewnome.com'

import sys
import web
sys.path.append(baseurl)
sys.path.append(baseurl+'/api')

import simplejson as json
import sqlobject as db
from string import lstrip
from models import *
import operator

db.sqlhub.processConnection = db.connectionForURI("mysql://brewnome:password@localhost/brewnome")

urls = (
  '/api/beers/(\d+)', 'beer_details',
  '/api/beers/', 'beer_list',
  '/api/beers/find/(.*)', 'beer_autocomplete',
  '/api/beers/suggest/(\d+)', 'beer_suggest',
  '/api/beers/(\d+)/(\d+)/(\d+)', 'beer_feedback',
  '/api/beers/feedback/(\d+)/(\d+)', 'beer_check_feedback',
  '/api/users/create/(\d+)', 'user_create',
  )

application = web.application(urls, globals()).wsgifunc()

class user_create:
  def GET(self, user_fb_id):
    users = User.select(User.q.user_fb_id==int(user_fb_id))
    if users.count() > 0:
      resp = {'sts': 'err', 'desc': 'user id %s already exists' % str(user_fb_id)}
      return json.dumps(resp)
      
    u = User(user_fb_id=int(user_fb_id))
    
    resp = {'sts': 'ok'}
    web.header('Content-Type', 'application/json')
    return json.dumps(resp)
  
class beer_list:
  def GET(self):
    beers = Beer.select()
    
    resp = {'beers': []}
    for beer in beers:
      resp['beers'].append({'id': beer.id, 'name': beer.beer_name})

    web.header('Content-Type', 'application/json')
    return json.dumps(resp)

class beer_check_feedback:
  def GET(self, beer_id, user_fb_id):
    web.header('Content-Type', 'application/json')
    
    try:  
      b = Beer.get(int(beer_id))
      
      users = User.select(User.q.user_fb_id==int(user_fb_id))
      if users.count() == 0:
        resp = {'sts': 'err', 'desc': 'user id %s not found' % str(user_fb_id)}
        return json.dumps(resp)
      u = users[0]
      
      r = Rating.select(db.AND(Rating.q.rating_beer==b,Rating.q.rating_user==u))
      if r.count() > 0:
        resp = {'exists': 1}
      else:
        resp = {'exists': 0}
        
      return json.dumps(resp)
    except:
      resp = {'sts': 'err', 'desc': 'beer id %s not found' % str(beer_id)}
      return json.dumps(resp)

class beer_feedback:
  def GET(self, beer_id, user_fb_id, feedback):
    web.header('Content-Type', 'application/json')
    
    try:  
      b = Beer.get(int(beer_id))
      
      users = User.select(User.q.user_fb_id==int(user_fb_id))
      if users.count() == 0:
        resp = {'sts': 'err', 'desc': 'user id %s not found' % str(user_fb_id)}
        return json.dumps(resp)
      u = users[0]
      
      r = Rating.select(db.AND(Rating.q.rating_beer==b,Rating.q.rating_user==u))
      if r.count() == 0:
        if not (int(feedback) == 0 or int(feedback) == 1):
          resp = {'sts': 'ok', 'desc': 'invalid feedback value (try 0 or 1)'}
          return json.dumps(resp)
          
        if int(feedback) == 1:
          b.beer_likes += 1
        else:
          b.beer_dislikes += 1
          
        new_r = Rating(rating_beer=b,rating_user=u,rating_rate=int(feedback))
        resp = {'sts': 'ok'}
      else:
        resp = {'sts': 'err', 'reason': 'user %s already rated beer %s' % (str(u.id), str(b.id))}
            
      return json.dumps(resp)
    except:
      resp = {'sts': 'err', 'desc': 'beer id %s not found' % str(beer_id)}
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
    
class beer_suggest:
  def GET(self, id):
    b = Beer.get(int(id))
    
    beers = Beer.select()
    
    resp = {'beers': []}
    for beer in beers:
      b_temp = {}
      
      b_temp['id'] = beer.id
      b_temp['beer_name'] = beer.beer_name
      b_temp['beer_description'] = beer.beer_description
      b_temp['beer_class'] = beer.beer_class
      b_temp['beer_sub_class'] = beer.beer_sub_class
      b_temp['count'] = 0.0
      
      factors = 0.0       
      if len(beer.beer_name) > 0:
        factors += 1
        if beer.beer_name == b.beer_name:
          b_temp['count'] += 1

      if len(beer.beer_class) > 0:
        factors += 1
        if beer.beer_class == b.beer_class:
          b_temp['count'] += 1
      
      if len(beer.beer_sub_class) > 0:
        factors += 1
        if beer.beer_sub_class == b.beer_sub_class:
          b_temp['count'] += 1
      
      if len(beer.brewer_name) > 0:
        factors += 1
        if beer.brewer_name == b.brewer_name:
          b_temp['count'] += 1
        
      if len(beer.brewer_country) > 0:
        factors += 1
        if beer.brewer_country == b.brewer_country:
          b_temp['count'] += 1
      
      if len(beer.brewer_region) > 0:
        factors += 1
        if beer.brewer_region == b.brewer_region:
          b_temp['count'] += 1
        
      if len(beer.beer_color) > 0:
        factors += 1
        if beer.beer_color == b.beer_color:
          b_temp['count'] += 1
        
      if len(beer.carbonation) > 0:
        factors += 1
        if beer.carbonation == b.carbonation:
          b_temp['count'] += 1
        
      if len(beer.heaviness_or_fullness) > 0:
        factors += 1
        if beer.heaviness_or_fullness == b.heaviness_or_fullness:
          b_temp['count'] += 1
        
      # FIXXX
      if beer.hoppiness is not None:
        factors += 1
        if b.hoppiness is not None and abs(beer.hoppiness - b.hoppiness) < 10:
            b_temp['count'] += 1
        
      if len(b.food_flavor_1) > 0:
        factors += 1
        if b.food_flavor_1 == b.food_flavor_1 \
          or b.food_flavor_1 == b.food_flavor_2 \
          or b.food_flavor_1 == b.food_flavor_3 \
          or b.food_flavor_1 == b.food_flavor_4 \
          or b.food_flavor_1 == b.food_flavor_5:
          b_temp['count'] += 1
          
      if len(b.food_flavor_2) > 0:
        factors += 1
        if b.food_flavor_2 == b.food_flavor_1 \
          or b.food_flavor_2 == b.food_flavor_2 \
          or b.food_flavor_2 == b.food_flavor_3 \
          or b.food_flavor_2 == b.food_flavor_4 \
          or b.food_flavor_2 == b.food_flavor_5:
          b_temp['count'] += 1

      if len(b.food_flavor_3) > 0:
        factors += 1
        if b.food_flavor_3 == b.food_flavor_1 \
          or b.food_flavor_3 == b.food_flavor_2 \
          or b.food_flavor_3 == b.food_flavor_3 \
          or b.food_flavor_3 == b.food_flavor_4 \
          or b.food_flavor_3 == b.food_flavor_5:
          b_temp['count'] += 1

      if len(b.food_flavor_4) > 0:
        factors += 1
        if b.food_flavor_4 == b.food_flavor_1 \
          or b.food_flavor_4 == b.food_flavor_2 \
          or b.food_flavor_4 == b.food_flavor_3 \
          or b.food_flavor_4 == b.food_flavor_4 \
          or b.food_flavor_4 == b.food_flavor_5:
          b_temp['count'] += 1
          
      if len(b.food_flavor_5) > 0:
        factors += 1
        if b.food_flavor_5 == b.food_flavor_1 \
          or b.food_flavor_5 == b.food_flavor_2 \
          or b.food_flavor_5 == b.food_flavor_3 \
          or b.food_flavor_5 == b.food_flavor_4 \
          or b.food_flavor_5 == b.food_flavor_5:
          b_temp['count'] += 1
                
      if len(beer.sweetness) > 0:
        factors += 1
        if beer.sweetness == b.sweetness:
          b_temp['count'] += 1
        
      if len(b.starch_grain_type_1) > 0:
        factors += 1
        if b.starch_grain_type_1 == b.starch_grain_type_1 \
          or b.starch_grain_type_1 == b.starch_grain_type_2 \
          or b.starch_grain_type_1 == b.starch_grain_type_3 \
          or b.starch_grain_type_1 == b.starch_grain_type_4 \
          or b.starch_grain_type_1 == b.starch_grain_type_5:
          b_temp['count'] += 1
          
      if len(b.starch_grain_type_2) > 0:
        factors += 1
        if b.starch_grain_type_2 == b.starch_grain_type_1 \
          or b.starch_grain_type_2 == b.starch_grain_type_2 \
          or b.starch_grain_type_2 == b.starch_grain_type_3 \
          or b.starch_grain_type_2 == b.starch_grain_type_4 \
          or b.starch_grain_type_2 == b.starch_grain_type_5:
          b_temp['count'] += 1
      
      if len(b.starch_grain_type_3) > 0:
        factors += 1
        if b.starch_grain_type_3 == b.starch_grain_type_1 \
          or b.starch_grain_type_3 == b.starch_grain_type_2 \
          or b.starch_grain_type_3 == b.starch_grain_type_3 \
          or b.starch_grain_type_3 == b.starch_grain_type_4 \
          or b.starch_grain_type_3 == b.starch_grain_type_5:
          b_temp['count'] += 1
      
      if len(b.starch_grain_type_4) > 0:
        factors += 1
        if b.starch_grain_type_4 == b.starch_grain_type_1 \
          or b.starch_grain_type_4 == b.starch_grain_type_2 \
          or b.starch_grain_type_4 == b.starch_grain_type_3 \
          or b.starch_grain_type_4 == b.starch_grain_type_4 \
          or b.starch_grain_type_4 == b.starch_grain_type_5:
          b_temp['count'] += 1
      
      if len(b.starch_grain_type_5) > 0:
        factors += 1
        if b.starch_grain_type_5 == b.starch_grain_type_1 \
          or b.starch_grain_type_5 == b.starch_grain_type_2 \
          or b.starch_grain_type_5 == b.starch_grain_type_3 \
          or b.starch_grain_type_5 == b.starch_grain_type_4 \
          or b.starch_grain_type_5 == b.starch_grain_type_5:
          b_temp['count'] += 1
      
      if len(b.starch_grain_sub_type_1) > 0:
        factors += 1
        if b.starch_grain_sub_type_1 == b.starch_grain_sub_type_1 \
          or b.starch_grain_sub_type_1 == b.starch_grain_sub_type_2 \
          or b.starch_grain_sub_type_1 == b.starch_grain_sub_type_3 \
          or b.starch_grain_sub_type_1 == b.starch_grain_sub_type_4 \
          or b.starch_grain_sub_type_1 == b.starch_grain_sub_type_5:
          b_temp['count'] += 1
          
      if len(b.starch_grain_sub_type_2) > 0:
        factors += 1
        if b.starch_grain_sub_type_2 == b.starch_grain_sub_type_1 \
          or b.starch_grain_sub_type_2 == b.starch_grain_sub_type_2 \
          or b.starch_grain_sub_type_2 == b.starch_grain_sub_type_3 \
          or b.starch_grain_sub_type_2 == b.starch_grain_sub_type_4 \
          or b.starch_grain_sub_type_2 == b.starch_grain_sub_type_5:
          b_temp['count'] += 1
      
      if len(b.starch_grain_sub_type_3) > 0:
        factors += 1
        if b.starch_grain_sub_type_3 == b.starch_grain_sub_type_1 \
          or b.starch_grain_sub_type_3 == b.starch_grain_sub_type_2 \
          or b.starch_grain_sub_type_3 == b.starch_grain_sub_type_3 \
          or b.starch_grain_sub_type_3 == b.starch_grain_sub_type_4 \
          or b.starch_grain_sub_type_3 == b.starch_grain_sub_type_5:
          b_temp['count'] += 1
      
      if len(b.starch_grain_sub_type_4) > 0:
        factors += 1
        if b.starch_grain_sub_type_4 == b.starch_grain_sub_type_1 \
          or b.starch_grain_sub_type_4 == b.starch_grain_sub_type_2 \
          or b.starch_grain_sub_type_4 == b.starch_grain_sub_type_3 \
          or b.starch_grain_sub_type_4 == b.starch_grain_sub_type_4 \
          or b.starch_grain_sub_type_4 == b.starch_grain_sub_type_5:
          b_temp['count'] += 1
      
      if len(b.starch_grain_sub_type_5) > 0:
        factors += 1
        if b.starch_grain_sub_type_5 == b.starch_grain_sub_type_1 \
          or b.starch_grain_sub_type_5 == b.starch_grain_sub_type_2 \
          or b.starch_grain_sub_type_5 == b.starch_grain_sub_type_3 \
          or b.starch_grain_sub_type_5 == b.starch_grain_sub_type_4 \
          or b.starch_grain_sub_type_5 == b.starch_grain_sub_type_5:
          b_temp['count'] += 1          
           
      if len(beer.malted_or_unmalted_starch_grain) > 0:
        factors += 1
        if beer.malted_or_unmalted_starch_grain == b.malted_or_unmalted_starch_grain:
          b_temp['count'] += 1
        
      if len(b.hops_type_1) > 0:
        factors += 1
        if b.hops_type_1 == b.hops_type_1 \
          or b.hops_type_1 == b.hops_type_2 \
          or b.hops_type_1 == b.hops_type_3 \
          or b.hops_type_1 == b.hops_type_4 \
          or b.hops_type_1 == b.hops_type_5:
          b_temp['count'] += 1
          
      if len(b.hops_type_2) > 0:
        factors += 1
        if b.hops_type_2 == b.hops_type_1 \
          or b.hops_type_2 == b.hops_type_2 \
          or b.hops_type_2 == b.hops_type_3 \
          or b.hops_type_2 == b.hops_type_4 \
          or b.hops_type_2 == b.hops_type_5:
          b_temp['count'] += 1
      
      if len(b.hops_type_3) > 0:
        factors += 1
        if b.hops_type_3 == b.hops_type_1 \
          or b.hops_type_3 == b.hops_type_2 \
          or b.hops_type_3 == b.hops_type_3 \
          or b.hops_type_3 == b.hops_type_4 \
          or b.hops_type_3 == b.hops_type_5:
          b_temp['count'] += 1
      
      if len(b.hops_type_4) > 0:
        factors += 1
        if b.hops_type_4 == b.hops_type_1 \
          or b.hops_type_4 == b.hops_type_2 \
          or b.hops_type_4 == b.hops_type_3 \
          or b.hops_type_4 == b.hops_type_4 \
          or b.hops_type_4 == b.hops_type_5:
          b_temp['count'] += 1
      
      if len(b.hops_type_5) > 0:
        factors += 1
        if b.hops_type_5 == b.hops_type_1 \
          or b.hops_type_5 == b.hops_type_2 \
          or b.hops_type_5 == b.hops_type_3 \
          or b.hops_type_5 == b.hops_type_4 \
          or b.hops_type_5 == b.hops_type_5:
          b_temp['count'] += 1
                
      if len(b.yeast_type_1) > 0:
        factors += 1
        if b.yeast_type_1 == b.yeast_type_1 \
          or b.yeast_type_1 == b.yeast_type_2 \
          or b.yeast_type_1 == b.yeast_type_3 \
          or b.yeast_type_1 == b.yeast_type_4 \
          or b.yeast_type_1 == b.yeast_type_5:
          b_temp['count'] += 1
          
      if len(b.yeast_type_2) > 0:
        factors += 1
        if b.yeast_type_2 == b.yeast_type_1 \
          or b.yeast_type_2 == b.yeast_type_2 \
          or b.yeast_type_2 == b.yeast_type_3 \
          or b.yeast_type_2 == b.yeast_type_4 \
          or b.yeast_type_2 == b.yeast_type_5:
          b_temp['count'] += 1
      
      if len(b.yeast_type_3) > 0:
        factors += 1
        if b.yeast_type_3 == b.yeast_type_1 \
          or b.yeast_type_3 == b.yeast_type_2 \
          or b.yeast_type_3 == b.yeast_type_3 \
          or b.yeast_type_3 == b.yeast_type_4 \
          or b.yeast_type_3 == b.yeast_type_5:
          b_temp['count'] += 1
      
      if len(b.yeast_type_4) > 0:
        factors += 1
        if b.yeast_type_4 == b.yeast_type_1 \
          or b.yeast_type_4 == b.yeast_type_2 \
          or b.yeast_type_4 == b.yeast_type_3 \
          or b.yeast_type_4 == b.yeast_type_4 \
          or b.yeast_type_4 == b.yeast_type_5:
          b_temp['count'] += 1
      
      if len(b.yeast_type_5) > 0:
        factors += 1
        if b.yeast_type_5 == b.yeast_type_1 \
          or b.yeast_type_5 == b.yeast_type_2 \
          or b.yeast_type_5 == b.yeast_type_3 \
          or b.yeast_type_5 == b.yeast_type_4 \
          or b.yeast_type_5 == b.yeast_type_5:
          b_temp['count'] += 1
                
      if len(beer.seasonality) > 0:
        factors += 1
        if beer.seasonality	== b.seasonality:
          b_temp['count'] += 1
        
      # FIXX
      if beer.alcohol_percentage is not None:
        factors += 1
        if b.alcohol_percentage is not None and abs(beer.alcohol_percentage - b.alcohol_percentage) < 1:
          b_temp['count'] += 1
        
      if len(beer.brewer_volume_of_distribution) > 0:
        factors += 1
        if beer.brewer_volume_of_distribution == b.brewer_volume_of_distribution:
          b_temp['count'] += 1
        
      # < 0.50
      if len(beer.bottle_retail_price) > 0:
        factors += 1
        if beer.bottle_retail_price == b.bottle_retail_price:
          b_temp['count'] += 1
        
      # within 30 minutes
      if len(beer.roasting_time) > 0:
        factors += 1
        if beer.roasting_time == b.roasting_time:
          b_temp['count'] += 1
        
      # within 5 degrees
      if len(beer.roasting_temperature) > 0:
        factors += 1
        if beer.roasting_temperature == b.roasting_temperature:
          b_temp['count'] += 1
        
      if len(beer.clarifying_agents) > 0:
        factors += 1
        if beer.clarifying_agents == b.clarifying_agents:
          b_temp['count'] += 1
        
      if len(beer.fermentation_style) > 0:
        factors += 1
        if beer.fermentation_style == b.fermentation_style:
          b_temp['count'] += 1
        
      # within 5 degrees
      if len(beer.fermentation_temperature) > 0:
        factors += 1
        if beer.fermentation_temperature == b.fermentation_temperature:
          b_temp['count'] += 1
        
      if len(beer.second_fermentation) > 0:
        factors += 1
        if beer.second_fermentation == b.second_fermentation:
          b_temp['count'] += 1
        
      if len(beer.continuous_fermentation) > 0:
        factors += 1
        if beer.continuous_fermentation == b.continuous_fermentation:
          b_temp['count'] += 1
        
      if len(beer.serving_temperature) > 0:
        factors += 1
        if beer.serving_temperature	== b.serving_temperature:
          b_temp['count'] += 1
        
      if len(beer.crispness) > 0:
        factors += 1
        if beer.crispness == b.crispness:
          b_temp['count'] += 1
        
      if len(beer.aroma) > 0:
        factors += 1
        if beer.aroma == b.aroma:
          b_temp['count'] += 1
        
      if len(beer.head_retention) > 0:
        factors += 1
        if beer.head_retention == b.head_retention:
          b_temp['count'] += 1
        
      if len(beer.cask_conditioning) > 0:
        factors += 1
        if beer.cask_conditioning == b.cask_conditioning:
          b_temp['count'] += 1
        
      # within 10 calories
      if len(beer.calorie_count) > 0:
        factors += 1
        if beer.calorie_count == b.calorie_count:
          b_temp['count'] += 1
        
      if len(b.spices_1) > 0:
        factors += 1
        if b.spices_1 == b.spices_1 \
          or b.spices_1 == b.spices_2 \
          or b.spices_1 == b.spices_3 \
          or b.spices_1 == b.spices_4 \
          or b.spices_1 == b.spices_5:
          b_temp['count'] += 1
          
      if len(b.spices_2) > 0:
        factors += 1
        if b.spices_2 == b.spices_1 \
          or b.spices_2 == b.spices_2 \
          or b.spices_2 == b.spices_3 \
          or b.spices_2 == b.spices_4 \
          or b.spices_2 == b.spices_5:
          b_temp['count'] += 1
      
      if len(b.spices_3) > 0:
        factors += 1
        if b.spices_3 == b.spices_1 \
          or b.spices_3 == b.spices_2 \
          or b.spices_3 == b.spices_3 \
          or b.spices_3 == b.spices_4 \
          or b.spices_3 == b.spices_5:
          b_temp['count'] += 1
      
      if len(b.spices_4) > 0:
        factors += 1
        if b.spices_4 == b.spices_1 \
          or b.spices_4 == b.spices_2 \
          or b.spices_4 == b.spices_3 \
          or b.spices_4 == b.spices_4 \
          or b.spices_4 == b.spices_5:
          b_temp['count'] += 1
      
      if len(b.spices_5) > 0:
        factors += 1
        if b.spices_5 == b.spices_1 \
          or b.spices_5 == b.spices_2 \
          or b.spices_5 == b.spices_3 \
          or b.spices_5 == b.spices_4 \
          or b.spices_5 == b.spices_5:
          b_temp['count'] += 1
              
      if len(b.herbs_1) > 0:
        factors += 1
        if b.herbs_1 == b.herbs_1 \
          or b.herbs_1 == b.herbs_2 \
          or b.herbs_1 == b.herbs_3 \
          or b.herbs_1 == b.herbs_4 \
          or b.herbs_1 == b.herbs_5:
          b_temp['count'] += 1
          
      if len(b.herbs_2) > 0:
        factors += 1
        if b.herbs_2 == b.herbs_1 \
          or b.herbs_2 == b.herbs_2 \
          or b.herbs_2 == b.herbs_3 \
          or b.herbs_2 == b.herbs_4 \
          or b.herbs_2 == b.herbs_5:
          b_temp['count'] += 1
      
      if len(b.herbs_3) > 0:
        factors += 1
        if b.herbs_3 == b.herbs_1 \
          or b.herbs_3 == b.herbs_2 \
          or b.herbs_3 == b.herbs_3 \
          or b.herbs_3 == b.herbs_4 \
          or b.herbs_3 == b.herbs_5:
          b_temp['count'] += 1
      
      if len(b.herbs_4) > 0:
        factors += 1
        if b.herbs_4 == b.herbs_1 \
          or b.herbs_4 == b.herbs_2 \
          or b.herbs_4 == b.herbs_3 \
          or b.herbs_4 == b.herbs_4 \
          or b.herbs_4 == b.herbs_5:
          b_temp['count'] += 1
      
      if len(b.herbs_5) > 0:
        factors += 1
        if b.herbs_5 == b.herbs_1 \
          or b.herbs_5 == b.herbs_2 \
          or b.herbs_5 == b.herbs_3 \
          or b.herbs_5 == b.herbs_4 \
          or b.herbs_5 == b.herbs_5:
          b_temp['count'] += 1
        
      if len(beer.clarity) > 0:
        factors += 1
        if beer.clarity == b.clarity:
          b_temp['count'] += 1
      
      # within 3 days
      if beer.age is not None:
        factors += 1
        if beer.age == b.age:
          b_temp['count'] += 1
      
      b_temp['perc_match'] = round((b_temp['count'] / factors) * 100.0,0)
    
      resp['beers'].append(b_temp)
    
    resp['beers'] = sorted(resp['beers'], key=lambda tup: tup['perc_match'], reverse=True)
    
    web.header('Content-Type', 'application/json')
    return json.dumps(resp)
    

