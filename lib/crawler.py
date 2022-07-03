import logging
import time
import json
from urllib.parse import urlparse
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from seleniumwire import webdriver

logger = logging.getLogger(__name__)

class HostInfo:
    def __init__(self, netloc):
        self.netloc = netloc
        self.hrefs = list()
        self.srcs = list()
        self.requests = list()
        self.vhosts = list()
        self.servers = list()

class Crawler:
    def __init__(self, options):
        firefox_options = Options()
        if options.headless:
            firefox_options.add_argument('--headless')

        self.service = Service(executable_path='./webdrivers/geckodriver')
        self.webdriver = webdriver.Firefox(service=self.service, options=firefox_options)
        self.target = options.target
        logger.debug(f"target: {self.target}")

        self.hostInfos = {}

    def crawl(self):
        driver = self.webdriver
        driver.get(self.target)
        time.sleep(2)

        self.getUrlInDom()

    '''
    Code get all URL contained in elements with href or src attribute
    '''
    def getUrlInDom(self):
        driver = self.webdriver

        _ = '''return document.querySelectorAll('[href]')'''
        _ = driver.execute_script(_)
        hrefs = map(lambda x: x.get_attribute('href'), _)
        for u in hrefs:
            url = urlparse(u)
            netloc = url.netloc
            path = url.path
            if not netloc in self.hostInfos:
                self.hostInfos[netloc] = HostInfo(netloc)
            hostInfo = self.hostInfos[netloc]
            hostInfo.hrefs.append(path)

        _ = '''return document.querySelectorAll('[src]')'''
        _ = driver.execute_script(_)
        srcs = map(lambda x: x.get_attribute('src'), _)
        for u in srcs:
            url = urlparse(u)
            netloc = url.netloc
            path = url.path
            if not netloc in self.hostInfos:
                self.hostInfos[netloc] = HostInfo(netloc)
            hostInfo = self.hostInfos[netloc]
            hostInfo.srcs.append(path)

    def report(self):
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
            server = resp.headers.get('server')
            if server:
                hostInfo.servers.append(server)


        for host, info in self.hostInfos.items():
            dump = json.dumps(info.__dict__, indent=2)
            print(dump)

    def quit(self):
        self.webdriver.quit()
