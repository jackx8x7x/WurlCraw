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
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)

def get_args_list(do_some):
    '''
    Let method get arguments as list
    '''
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

        self.last_selected = []
        self.history = []
        self.hostInfos = {}
        self.prompt = '[WurlCraw]> '

        firefox_options = Options()
        if options.headless:
            firefox_options.add_argument('--headless')

        self.service = Service(executable_path='./webdrivers/geckodriver')
        self.webdriver = webdriver.Firefox(service=self.service,
                options=firefox_options)

        if options.target:
            self.webdriver.get(options.target)
            self._update_prompt()
            self._appendHistory(options.target)

    def _update_prompt(self):
        title = self.webdriver.title
        if len(title) > 10:
            title = title[:12].ljust(15, '.')
        self.prompt = f'[WurlCraw][{title}]> '

    def _switch_to(self, handle):
        try:
            self.webdriver.switch_to.window(handle)
            self._update_prompt()
        except Exception as e:
            print(e)
            logger.warning(f'_switch_to to handle error {handle}')

    def _appendHistory(self, url):
        if not url in self.history:
            if len(self.history) < 10:
                self.history.append(url)
            else:
                self.history.pop(0)
                self.history.append(url)

    def emptyline(self):
        pass

    # Navigation relative command
    @get_args_list
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
            self._appendHistory(target)
        except:
            p.print_help()

    def complete_navigate(self, text, line, start, end):
        _match = ['http', 'https']

        if _match[-1] in line:
            return None

        return [m for m in _match if m.startswith(text)]

    
    @get_args_list
    def do_createTab(self, args):
        '''
        Create a new tab and switch to it
        '''
        p = argparse.ArgumentParser(prog='createTab')
        p.add_argument('-t', '--target', metavar='http(s)://<host>')
        try:
            target = p.parse_args(args).target
            self.webdriver.switch_to.new_window('tab')
            if target:
                self.webdriver.get(target)
                self._appendHistory(target)
                
            self._update_prompt()
        except:
            p.print_help()

    def complete_createTab(self, text, line, start, end):
        _match = ['http', 'https']
        if not '-t' in line:
            return ['-t']

        if _match[-1] in line:
            return 

        return [m for m in _match if m.startswith(text)]

    @get_args_list
    def do_switchTo(self, args):
        '''
        Switch to specified tab or window
        '''
        driver = self.webdriver
        p = argparse.ArgumentParser(prog='switchTo')
        p.add_argument('handle', metavar='HANDLE',
                help='handle string to match')
        try:
            handle = p.parse_args(args).handle
            for h in driver.window_handles:
                if h.startswith(handle):
                    self._switch_to(h)
                    break
        except:
            p.print_help()

    def complete_switchTo(self, text, line, start, end):
        return [h for h in self.webdriver.window_handles if h.startswith(text)]

    def do_forward(self, args):
        self.webdriver.forward()

    def do_back(self, args):
        self.webdriver.back()

    def do_refresh(self, args):
        self.webdriver.refresh()

    def do_eval(self, args):
        try:
            res = eval(args)
            print(res)
        except Exception as e:
            print(e)

    # Data process relate
    @get_args_list
    def do_takeScreenshot(self, args):
        '''
        Navigate to the specified URL
        '''
        p = argparse.ArgumentParser(prog='takeScreenshot')
        p.add_argument('path', metavar='PAHT_TO_SAVE')
        try:
            path = p.parse_args(args).path
            self.webdriver.save_screenshot(path)
        except:
            p.print_help()

    def complete_takeScreenshot(self, text, line, start, end):
        import os
        li = os.listdir('.')
        return [l for l in li if l.startswith(text)]

    def do_clean(self):
        '''
        Clean selenium-wire cache, i.e, driver.requests
        '''
        del self.webdriver.requests

    # Brower status, history and cookies information
    @get_args_list
    def do_getCookies(self, args):
        '''
        Dump cookies for the current URL
        '''
        p = argparse.ArgumentParser(prog='getCookies')
        p.add_argument('--domain', metavar='DOMAIN',
                help='Pattern to match cookie domain')

        cookies = self.webdriver.get_cookies()
        for c in cookies:
            print(c)

    @get_args_list
    def do_setCookies(self, args):
        '''
        Dump cookies for the current URL
        '''
        p = argparse.ArgumentParser(prog='setCookies')
        p.add_argument('name', metavar='NAME',
                help='Cookie name')
        p.add_argument('value', metavar='VALUE',
                help='Cookie value')
        p.add_argument('-d', '--domain', metavar='DOMAIN',
                help='Cookie domain')
        p.add_argument('-p', '--path', metavar='PATH',
                help='Cookie path')
        p.add_argument('-s', '--secure', action='store_true',
                default=True, help='Secure flag')
        p.add_argument('--httpOnly', action='store_true',
                default=True, help='httpOnly flag')
        try:
            options = p.parse_args(args)
            self.webdriver.add_cookie(options.__dict__)
        except:
            pass

    def do_getWindows(self, args):
        '''
        Get all windows handles and their title
        '''
        driver = self.webdriver
        handle = driver.current_window_handle
        for w in driver.window_handles:
            driver.switch_to.window(w)
            title = driver.title
            print("{handle}: {title}".format(handle=w, title=title))
        driver.switch_to.window(handle)

    def do_getHistory(self, args):
        for h in self.history:
            print(h)

    # Element locating and interactive command
    @get_args_list
    def do_queryNodes(self, args):
        '''
        Find node with specified CSS selector
        '''
        p = argparse.ArgumentParser(prog='queryNodes', exit_on_error=False)
        p.add_argument('selector', metavar='CSS_selector')
        p.add_argument('-a', '--attribute', metavar='attribute')
        try:
            options = p.parse_args(args)
            query = options.selector
            nodes = self.webdriver.find_elements(By.CSS_SELECTOR, query)
            self.last_selected = nodes
            for i in range(len(nodes)):
                n = nodes[i]
                a = options.attribute
                if a:
                    print(i, n.get_attribute(a))
                else:
                    print(i, n.get_attribute('outerHTML'))

        except:
            p.print_help()

    @get_args_list
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

    @get_args_list
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

    @get_args_list
    def do_fillForm(self, args):
        pass

    @get_args_list
    def do_click(self, args):
        '''
        Click the first CSS_SELECTOR matching element
        '''
        p = argparse.ArgumentParser(prog='click')
        p.add_argument('selector', metavar='CSS_SELECTOR')
        try:
            query = p.parse_args(args).selector
            if query.isdigit() and 0 <= int(query) < len(self.last_selected):
                node = self.last_selected[int(query)]
            else:
                node = self.webdriver.find_element(By.CSS_SELECTOR, query)
            if node:
                node.click()
        except:
            pass

    def quit(self):
        self.webdriver.quit()
