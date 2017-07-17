#!/usr/bin/python
from FeedFinder import FeedFinder
import argparse

parser = argparse.ArgumentParser(description='Finds feeds embedded within a webpage')
parser.add_argument('url', help='The URL to search')
parser.add_argument('--rss', action='store_true', help='Find RSS feeds')
parser.add_argument('--ics', action='store_true', help='Find ICS/ical feeds')
args = parser.parse_args()

feedfinder = FeedFinder(args.url)
if args.rss:
	print(feedfinder.get_rss_feed())
if args.ics:
	print(feedfinder.get_rss_feed())