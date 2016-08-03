#!/usr/bin/env python -B
import cgi
class html_entities_encode:

	def transform(self,input):
		return cgi.escape(input).encode('utf-8', 'xmlcharrefreplace')