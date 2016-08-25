#!/usr/bin/env python -B
import codecs
class rot_encode:

	def transform(self,input,params={}):

		encoding = "utf-8"
		cipher = 13

		if 'encoding' in params:
			encoding = params['encoding']

		if 'cipher' in params:
			cipher = int(params['cipher'])

		cipher %= 26
		alpha = "abcdefghijklmnopqrstuvwxyz" * 2
		alpha += alpha.upper()
		def get_i():
			for i in range(26):
				yield i
			for i in range(53, 78):
				yield i
			
		ROT = {alpha[i]: alpha[i + cipher] for i in get_i()}
		
		return "".join(ROT.get(i, i) for i in input)