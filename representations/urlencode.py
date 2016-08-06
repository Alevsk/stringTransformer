#!/usr/bin/env python -B
import urllib
class urlencode:

	def transform(self,input,params={}):
		return urllib.quote_plus(input)