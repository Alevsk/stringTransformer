#!/usr/bin/env python -B
from unicodedata import normalize
class slug:

	def transform(self,input,params={}):

		encoding = "utf-8"
		permitted_chars='abcdefghijklmnopqrstuvwxyz0123456789-'

		if hasattr(params, 'encoding'):
			encoding = params.encoding

		if hasattr(params, 'permitted_chars'):
			permitted_chars = params.permitted_chars

		if isinstance(input, str):
			input = input.decode(encoding or 'ascii')
		clean_text = input.strip().replace(' ', '-').lower()
		
		while '--' in clean_text:
			clean_text = clean_text.replace('--', '-')
		ascii_text = normalize('NFKD', clean_text).encode('ascii', 'ignore')
		strict_text = map(lambda x: x if x in permitted_chars else '', ascii_text)
		
		return ''.join(strict_text)