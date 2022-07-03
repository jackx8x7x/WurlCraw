import logging
from selenium.webdriver.firefox.service import Service
from seleniumwire import webdriver

logger = logging.getLogger(__name__)

class Crawler:
    def __init__(self, options):
        self.service = Service(executable_path='./webdrivers/geckodriver')
        self.webdriver = webdriver.Firefox(service=self.service)
        self.target = options.target
        logger.debug(f"target: {self.target}")

    def crawl(self):
        self.webdriver.get(self.target)
        for req in self.webdriver.requests:
            print(req.url)
            if req.response:
                print(req.response.headers)
        self.quit()

    def quit(self):
        self.webdriver.quit()
