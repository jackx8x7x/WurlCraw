VENV := ./virtual-environment/
SHELL := /bin/bash
GECKODRIVER := ./webdrivers/geckodriver

all: $(VENV) $(GECKODRIVER)
	@/bin/bash -c \
	"source $(VENV)/bin/activate\
	&& python3 wurlcraw.py"
	

$(VENV):
	python3 -m venv $(VENV)

$(GECKODRIVER):
	/bin/bash -c \
	"[ -d ./webdrivers ] || mkdir webdrivers\
	&& wget 'https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-macos.tar.gz' -O driver.tgz\
	&& tar zxvf driver.tgz\
	&& mv geckodriver $(GECKODRIVER)\
	&& rm driver.tgz"

.PHONY: test
test:
	/bin/bash -c \
	"source $(VENV)/bin/activate\
	&& python3 wurlcraw.py --test"

.PHONY: setup
setup: selenium download-all

.PHONY: selenium
selenium: $(VENV)
	/bin/bash -c \
	"source $(VENV)/bin/activate\
	&& pip3 install selenium"

.PHONY: download-all
download-all: $(GECKODRIVER)

clean: clean-venv clean-webdrivers

.PHONY: clean-venv
clean-venv:
	/bin/bash -c \
	"if [ -d $(VENV) ];\
		then rm -rf $(VENV);\
	fi"

.PHONY: clean-webdrivers
clean-webdrivers:
	/bin/bash -c "[ -d ./webdrivers ] && rm -rf ./webdrivers"

