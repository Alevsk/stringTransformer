#!/usr/bin/env python -B
import hashlib
class sha1:

	def transform(self,input):
		hash_object = hashlib.sha1(input)
		return hash_object.hexdigest()