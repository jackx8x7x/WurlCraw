import logging
import time
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from seleniumwire import webdriver

logger = logging.getLogger(__name__)

class Crawler:
    def __init__(self, options):
        firefox_options = Options()
        if options.headless:
            firefox_options.add_argument('--headless')

        self.service = Service(executable_path='./webdrivers/geckodriver')
        self.webdriver = webdriver.Firefox(service=self.service, options=firefox_options)
        self.target = options.target
        logger.debug(f"target: {self.target}")

        self.hrefs = set()
        self.srcs = set()

    def crawl(self):
        driver = self.webdriver
        driver.get(self.target)
        time.sleep(2)

        self.getUrl()

    def getUrl(self):
        driver = self.webdriver

        # Code get all element with href
        _ = '''return document.querySelectorAll('[href]')'''
        _ = driver.execute_script(_)
        hrefs = map(lambda x: x.get_attribute('href'), _)
        self.hrefs.update(hrefs)

        # Code get all element with src
        _ = '''return document.querySelectorAll('[src]')'''
        _ = driver.execute_script(_)
        srcs = map(lambda x: x.get_attribute('src'), _)
        self.hrefs.update(srcs)

    def report(self):
        driver = self.webdriver
        for href in self.hrefs:
            print(href)
        for src in self.srcs:
            print(src)
        for req in set(driver.requests):
            url = req.url
            host = req.headers.get('Host', '')
            print(url, host)
            res = req.response
            if res:
                server = res.headers.get('server', '')
                if server:
                    print(server)

    def quit(self):
        self.webdriver.quit()
