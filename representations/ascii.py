#!/usr/bin/env python -B
class ascii:

	def transform(self,input,params={}):
		return ' '.join(str(ord(c)) for c in input)