#!/usr/bin/env python -B
import codecs
class rot13_encode:

	def transform(self,input,encoding='utf-8'):
		input = input.decode(encoding or 'ascii')
		return codecs.encode(input, 'rot_13')