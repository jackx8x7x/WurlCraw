import logging
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

    def crawl(self):
        driver = self.webdriver
        driver.get(self.target)
        for req in driver.requests:
            print(req.url)
            if req.response:
                print(req.response.headers)
        self.quit()

    def quit(self):
        self.webdriver.quit()
