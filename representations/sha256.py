#!/usr/bin/env python -B
import hashlib
class sha256:

	def transform(self,input,params={}):
		hash_object = hashlib.sha256(input)
		return hash_object.hexdigest()