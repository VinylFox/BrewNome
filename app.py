baseurl = '/home/brewnome/www/brewnome.com'

import sys
sys.path.append(baseurl)
sys.path.append(baseurl+'/api')

import web
from api import autocomplete

urls = ('/api/autocomplete/.*', 'autocomplete')

application = web.application(urls, globals()).wsgifunc()