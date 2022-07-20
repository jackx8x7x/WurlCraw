import argparse
import cmd
import logging
import time
import json
import shlex
from functools import wraps
from urllib.parse import urlparse
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from seleniumwire import webdriver

logger = logging.getLogger(__name__)

def command(do_some):
    @wraps(do_some)
    def do_something(obj, args):
        argv = shlex.split(args)
        do_some(obj, argv)
    return do_something

class HostInfo:
    def __init__(self, netloc):
        self.netloc = netloc
        self.hrefs = list()
        self.srcs = list()
        self.requests = list()
        self.vhosts = list()
        self.servers = list()

class Crawler(cmd.Cmd):
    def __init__(self, options):
        cmd.Cmd.__init__(self)
        firefox_options = Options()
        if options.headless:
            firefox_options.add_argument('--headless')

        self.service = Service(executable_path='./webdrivers/geckodriver')
        self.webdriver = webdriver.Firefox(service=self.service,
                options=firefox_options)

        if options.target:
            self.webdriver.get(options.target)

        self.hostInfos = {}

    @command
    def do_navigate(self, args):
        '''
        Navigate to the specified URL
        '''
        p = argparse.ArgumentParser(prog='navigate')
        p.add_argument('target', metavar='http(s)://<host>')
        try:
            options = p.parse_args(args)
            target = options.target
            driver = self.webdriver
            driver.get(target)
        except:
            pass

    def do_eval(self, args):
        res = eval(args)
        print(res)

    @command
    def do_getCookies(self, args):
        '''
        Dump cookies
        '''
        print(self.webdriver.get_cookies())

    @command
    def do_findNodes(self, args):
        '''
        Find node with specified CSS selector
        '''
        p = argparse.ArgumentParser(prog='findNodes', exit_on_error=False)
        p.add_argument('selector', metavar='CSS_selector')
        p.add_argument('-a', '--attribute', metavar='attribute')
        try:
            options = p.parse_args(args)
            code = "return document.querySelectorAll('{selector}')".format(
                **options.__dict__)
            nodes = self.webdriver.execute_script(code)
            for n in nodes:
                a = options.attribute
                if a:
                    print(n.get_attribute(a))
                else:
                    print(n.get_attribute('innerHTML'))

        except:
            pass

    @command
    def do_getUrlInDom(self, args):
        '''
        Code get all URL contained in elements with href or src attribute
        '''
        driver = self.webdriver

        _ = '''return document.querySelectorAll('[href]')'''
        _ = driver.execute_script(_)
        hrefs = map(lambda x: x.get_attribute('href'), _)

        _ = '''return document.querySelectorAll('[src]')'''
        _ = driver.execute_script(_)
        srcs = map(lambda x: x.get_attribute('src'), _)
        for li in hrefs, srcs:
            for u in li:
                print(u)
                url = urlparse(u)
                netloc = url.netloc
                path = url.path
                if not netloc in self.hostInfos:
                    self.hostInfos[netloc] = HostInfo(netloc)
                hostInfo = self.hostInfos[netloc]
                if li == hrefs:
                    hostInfo.hrefs.append(path)
                else:
                    hostInfo.srcs.append(path)

    @command
    def do_getRequestsInitiated(self, args):
        '''
        Get all URL referred to in the current page
        '''
        driver = self.webdriver
        for req in driver.requests:
            url = urlparse(req.url)
            netloc = url.netloc
            path = url.path
            if not netloc in self.hostInfos:
                self.hostInfos[netloc] = HostInfo(netloc)
            hostInfo = self.hostInfos[netloc]
            hostInfo.requests.append(path)
            vhost = req.headers.get('Host')
            if vhost:
                hostInfo.vhosts.append(vhost)
            resp = req.response
            if resp and resp.headers.get('server'):
                server = resp.headers.get('server')
                hostInfo.servers.append(server)

        for host, info in self.hostInfos.items():
            dump = json.dumps(info.__dict__, indent=2)
            print(dump)

    def quit(self):
        self.webdriver.quit()
