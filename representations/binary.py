#!/usr/bin/env python -B
class binary:

	def transform(self,input,params={}):
		return ' '.join(format(ord(x), 'b') for x in input)