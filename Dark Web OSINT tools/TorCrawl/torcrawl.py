#!/usr/bin/python

import socket
import socks
import argparse

# TorCrawl Modules
from modules.crawler import crawler
from modules.extractor import extractor
from modules.checker import *

help = '''

TorCrawl.py is a python script to crawl and extract (regular or onion) 
webpages through TOR network. 

usage: python torcrawl.py [options]
python torcrawl.py -u l0r3m1p5umD0lorS1t4m3t.onion 
python torcrawl.py -v -w -u http://www.github.com -o github.htm 
python torcrawl.py -v -u l0r3m1p5umD0lorS1t4m3t.onion -c -d 2 -p 5
python torcrawl.py -v -w -u http://www.github.com -c -d 2 -p 5 -e -f GitHub

General:
-h, --help         : Help
-v, --verbose      : Show more informations about the progress
-u, --url *.onion  : URL of Webpage to crawl or extract
-w, --without      : Without the use of Relay TOR 

Extract:
-e, --extract           : Extract page's code to terminal or file.
                          (Defualt: terminal)
-i, --input filename    : Input file with URL(s) (seperated by line)
-o, --output [filename] : Output page(s) to file(s) (for one page)

Crawl:
-c, --crawl       : Crawl website (Default output on /links.txt)
-d, --cdepth      : Set depth of crawl's travel (Default: 1)
-z, --exclusions  : Paths that you don't want to include (TODO)
-s, --simultaneous: How many pages to visit at the same time (TODO)
-p, --pause       : The length of time the crawler will pause 
                    (Default: 0)
-f, --folder	  : The root directory which will contain the 
                    generated files
-l, --log         : Log file with visited URLs and their response code.

GitHub: github.com/MikeMeliz/TorCrawl.py
License: GNU General Public License v3.0

'''


# Set socket and connection with TOR network
def connecttor():
	try:
		port = 9050
		# Set socks proxy and wrap the urllib module
		socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', port)
		socket.socket = socks.socksocket

		# Perform DNS resolution through the socket
		def getaddrinfo(*args):
			return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

		socket.getaddrinfo = getaddrinfo
	except:
		e = sys.exc_info()[0]
		print(("Error: %s" % e + "\n## Can't establish connection with TOR"))


def main():
	# Initialize necessary variables
	inputfile = outputfile = ''
	cpause = 0
	cdepth = 1

	# Get arguments with argparse
	parser = argparse.ArgumentParser(
		description="TorCrawl.py is a python script to crawl and extract (regular or onion) webpages through TOR network.")

	# General
	parser.add_argument(
		'-v',
		'--verbose',
		action='store_true',
		help='Show more information about the progress'
	)
	parser.add_argument(
		'-u',
		'--url',
		help='URL of webpage to crawl or extract'
	)
	parser.add_argument(
		'-w',
		'--without',
		action='store_true',
		help='Without the use of Relay TOR'
	)

	# Extract
	parser.add_argument(
		'-e',
		'--extract',
		action='store_true',
		help='Extract page\'s code to terminal or file.'
	)
	parser.add_argument(
		'-i',
		'--input',
		help='Input file with URL(s) (seperated by line)'
	)
	parser.add_argument(
		'-o',
		'--output',
		help='Output page(s) to file(s) (for one page)'
	)

	# Crawl
	parser.add_argument(
		'-c',
		'--crawl',
		action='store_true',
		help='Crawl website (Default output on /links.txt)'
	)
	parser.add_argument(
		'-d',
		'--cdepth',
		help='Set depth of crawl\'s travel (Default: 1)'
	)
	parser.add_argument(
		'-p',
		'--cpause',
		help='The length of time the crawler will pause'
	)
	parser.add_argument(
		'-l',
		'--log',
		action='store_true',
		help='A save log will let you see which URLs were visited and their response code'
	)
	parser.add_argument(
		'-f',
		'--folder',
		help='The root directory which will contain the generated files'
	)

	args = parser.parse_args()

	# Parse arguments to variables
	if args.input:
		inputfile = args.input
	if args.output:
		outputfile = args.output
	if args.cdepth:
		cdepth = args.cdepth
	if args.cpause:
		cpause = args.cpause

	# Connect to TOR
	if args.without is False:
		checktor(args.verbose)
		connecttor()

	if args.verbose:
		checkip()
		print(('## URL: ' + args.url))

	# Canon/ion of website and create path for output
	if len(args.url) > 0:
		global website
		global outpath
		website = urlcanon(args.url, args.verbose)
		if args.folder is not None:
			outpath = folder(args.folder, args.verbose)
		else:
			outpath = folder(extract_domain(website), args.verbose)

	if args.crawl:
		lst = crawler(website, cdepth, cpause, outpath, args.log, args.verbose)
		lstfile = open(outpath + '/links.txt', 'w+')
		for item in lst:
			lstfile.write("%s\n" % item)
		lstfile.close()
		print(("## File created on " + os.getcwd() + "/" + outpath + "/links.txt"))
		if args.extract:
			inputfile = outpath + "/links.txt"
			extractor(website, args.crawl, outputfile, inputfile, outpath)
	else:
		extractor(website, args.crawl, outputfile, inputfile, outpath)


if __name__ == "__main__":
	main()
