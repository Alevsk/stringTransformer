#!/usr/bin/env python -B
import codecs
class rot13_encode:

	def transform(self,input,params={}):

		encoding = "utf-8"
		cipher = "rot_13"

		if hasattr(params, 'encoding'):
			encoding = params.encoding

		if hasattr(params, 'cipher'):
			cipher = params.cipher

		input = input.decode(encoding or 'ascii')
		return codecs.encode(input, cipher)