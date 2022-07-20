#!/usr/bin/env python3

import sys
import argparse
import logging
from lib.crawler import Crawler

logger = logging.getLogger(__name__)

def clean_on_exit(crawler):
    crawler.quit()

def main(args):
    crawler = Crawler(args)

    import atexit
    atexit.register(clean_on_exit, crawler)
    try:
        crawler.cmdloop()
    except KeyboardInterrupt:
        crawler.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Wurlcraw, web url crawler')
    parser.add_argument('--target', metavar='http[s]://<HOST>[:<PORT>]',
            help="Target to crawl")
    parser.add_argument('--test', action="store_true", help="Test")
    parser.add_argument('-d', '--debug', metavar='LEVEL',
            choices=['INFO', 'DEBUG'], help="Debug level")
    parser.add_argument('-H', '--headless', action="store_true",
            help="Run browser in headless mode")

    args = parser.parse_args()
    if args.debug == 'DEBUG':
        logging.basicConfig(level=logging.DEBUG)
    elif args.debug == 'INFO':
        logging.basicConfig(level=logging.INFO)

    main(args)
