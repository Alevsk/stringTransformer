#!/usr/bin/env python -B
class octal:

	def transform(self,input,params={}):
		return ' '.join(str(oct(ord(i))) for i in input)