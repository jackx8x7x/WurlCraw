# Wurlcraw
## Overview
---
Wurlcraw, a Web URL Crawler using selenium/selenium-wire
- A hobby project
- Still under development

## Setup
---
Setup a `venv` virtual environment, install `selenium` and download webdrivers.
```bash
$ make setup
```

## Run
---
Run the script in a virtual environment
```bash
$ source ./virtual-environment/bin/activate
(virtual-environment)$ python3 wurlcrow.py -h
```

## Information gathering
---
- URLs
    - mentioned in DOM element
	- `href` attribute in tag `a`
	- `src` attribute
	- form's `action`
    - URLs contained in javascripts
    - HTTP requests initiated by javascripts
- Virtual hosts
    - Host name in the URLs we crawl
- Backend server
    - mentioned in HTTP response's `server` header
- Version information
    - We parse strings like "version" in the content we parse

## Mode
---
- Casual
Crawl the site in a casual way with random move
- Straightforward

## Usage
---
- Require `selenium-wire`
```bash
usage: wurlcraw.py [-h] [--target http[s]://<HOST>[:<PORT>]] [--test] [-d LEVEL] [-H]

Wurlcraw, web url crawler

optional arguments:
  -h, --help            show this help message and exit
  --target http[s]://<HOST>[:<PORT>]
                        Target to crawl
  --test                Test
  -d LEVEL, --debug LEVEL
                        Debug level
  -H, --headless        Run browser in headless mode
```
- Or run `./start.sh` which will create a virtualenv and install require module automatically
```bash
$ ./start.sh -h
```
