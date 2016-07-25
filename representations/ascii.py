#!/usr/bin/env python -B
class ascii:

	def transform(self,input):
		return ' '.join(str(ord(c)) for c in input)