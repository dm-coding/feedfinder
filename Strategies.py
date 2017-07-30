import urllib.parse
from .CacheManager import *

def check_attribs(node, check, check_contains, return_attrb):
	c = node.get(check, None)
	if c:
		for needed_attrib in check_contains:
			if needed_attrib in c:
				return node.get(return_attrb, None)
	return None

def find_child_pages(pages, url, cache):
	possible_pages = set()
	content = cache.get(key=url, itemName="page_content")

	parsed_url = urllib.parse.urlparse(cache.get(key=url, itemName='url'))
	base_url = parsed_url.scheme + "://" + parsed_url.hostname

	for a in content.findAll("a", href=True):
		href = a.get("href")
		for term in pages:
			if term in href or (a.text and term in a.text.lower()):
				if "://" in href: possible_pages.add(href)
				else: possible_pages.add(base_url + href)
	return possible_pages