#!/usr/bin/env python -B
class hexa:

	def transform(self,input,params={}):
		return  "0x".join("{:02x} ".format(ord(c)) for c in input)