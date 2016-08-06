#!/usr/bin/env python -B
import cgi
class html_entities_encode:

	def transform(self,input,params={}):
		source = unicode(input, 'utf-8')
		return cgi.escape(source).encode('utf-8', 'xmlcharrefreplace')