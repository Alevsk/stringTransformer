#!/usr/bin/env python -B
import cgi
class html_entities_encode:

	def transform(self,input,params={}):
		encoding = "utf-8"

		if 'encoding' in params:
			encoding = params['encoding']
		
		source = unicode(input, encoding)
		return cgi.escape(source).encode(encoding, 'xmlcharrefreplace')