#!/usr/bin/env python -B
import hashlib
class md5:

	def transform(self,input):
		m = hashlib.md5()
		m.update(input)
		return m.hexdigest()