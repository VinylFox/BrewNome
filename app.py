baseurl = '/home/brewnome/www/brewnome.com'

import sys
import web
import api
sys.path.append(baseurl)
sys.path.append(baseurl+'/api')

urls = (
  '/api/beers/(\d+)', 'beer_details',
  '/api/beers/', 'beer_list',
  '/api/beers/find/(.*)', 'beer_autocomplete',
  '/api/beers/suggest/(\d+)', 'suggest',
  )

application = web.application(urls, globals()).wsgifunc()