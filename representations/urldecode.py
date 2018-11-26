#!/usr/bin/env python -B
import urllib
class urldecode:

	def transform(self,input,params={}):
		return urllib.unquote(input).decode('utf8')