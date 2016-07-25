#!/usr/bin/env python -B
import urllib
class urlencode:

	def transform(self,input):
		return urllib.quote_plus(input)