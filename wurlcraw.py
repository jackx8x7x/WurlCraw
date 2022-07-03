#!/usr/bin/env python3

import sys
import argparse
import logging
from lib.crawler import Crawler

logger = logging.getLogger(__name__)

def main(args):
    crawler = Crawler(args)
    crawler.crawl()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Wurlcraw, web url crawler')
    parser.add_argument('target', metavar='http[s]://<HOST>[:<PORT>]', help="Target to crawl")
    parser.add_argument('--test', action="store_true", help="Test")
    parser.add_argument('-d', '--debug', action="store_true", help="Debug mode")
    parser.add_argument('-H', '--headless', action="store_true", help="Run browser in headless mode")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    main(args)
