#!/usr/bin/env python -B
import base64
import binascii
class base64_decode:

	def transform(self,input,params={}):
		missing_padding = len(input) % 4
		if missing_padding != 0:
			input += b'='* (4 - missing_padding)		
		try:
			return base64.decodestring(input)
		except binascii.Error:
			return "input is not a valid base64 encode string"
		