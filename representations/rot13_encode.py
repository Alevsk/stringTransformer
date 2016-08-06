#!/usr/bin/env python -B
import codecs
class rot13_encode:

	def transform(self,input,params={}):

		encoding = "utf-8"

		if hasattr(params, 'encoding'):
			encoding = params.encoding

		input = input.decode(encoding or 'ascii')
		return codecs.encode(input, 'rot_13')