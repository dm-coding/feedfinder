import requests
from bs4 import BeautifulSoup as bs4

class CacheManager(object):
	def __init__(self, root_url):
		#print("**** New cache manager" + root_url)
		self.cache = { root_url: { "url": root_url } }
		self.resolvers = {}
		self.addResolver('url', default_key_resolver)
		self.default_key = root_url
		self.addResolver(itemName="page_src",     resolver=remote_content_resolver)
		self.addResolver(itemName="page_content", resolver=page_content_resolver)

	def addResolver(self, itemName, resolver):
		self.resolvers[itemName] = resolver

	def get(self, key, itemName):
		if key not in self.cache:
			self.cache[key] = {}
		# print("Retrieving " + key)
		# print("Cache contents:")
		# for key in self.cache.keys():
		# 	print("---> " + key)
		if itemName not in self.cache[key]:
			if itemName in self.resolvers: self.cache[key][itemName] = self.resolvers[itemName](key=key, cache=self)
			else: raise LookupError
			#else: return None
		return self.cache[key][itemName]

def default_key_resolver(key, cache):
	return key

def remote_content_resolver(key, cache):
	print("Not found in local storage: " + key)
	try:
		return requests.get(key)
	except Exception:
		print("Remote retrieval failed")
		return None

def page_content_resolver(key, cache):
	return bs4(cache.get(key=key, itemName="page_src").text, "html5lib")