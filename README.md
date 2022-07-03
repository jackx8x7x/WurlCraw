# Wurlcraw
## Overview
Wurlcraw, A Web URL Crawler using webdriver

## Information gathering
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
- Casual
Crawl the site in a casual way with random move
- Straightforward

## Usage
