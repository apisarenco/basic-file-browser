.PYTHON36:=$(shell PATH=$(subst $(CURDIR)/.venv/bin:,,$(PATH)) which python3.6)

.venv/bin/python:
	# if .venv is already a symlink, don't overwrite it
	mkdir -p .venv
	# go into the new dir and build it there as venv doesn't work if the target is a symlink
	cd .venv && $(.PYTHON36) -m venv --copies --prompt='[$(shell basename `pwd`)/.venv]' .
	# set environment variables
	echo export FLASK_DEBUG=1 >> .venv/bin/activate
	echo export FLASK_APP=$(shell pwd)/app/app.py >> .venv/bin/activate
	# add the project directory to path
	echo $(shell pwd) > `echo .venv/lib/*/site-packages`/path.pth
	# install minimum set of required packages
	# wheel needs to be early to be able to build wheels
	.venv/bin/pip install --upgrade pip wheel requests setuptools pipdeptree
	# Workaround problems with un-vendored urllib3/requests in pip on ubuntu/debian
	# This forces .venv/bin/pip to use the vendored versions of urllib3 from the installed requests version
	# see https://stackoverflow.com/a/46970344/1380673
	-rm -v .venv/share/python-wheels/{requests,chardet,urllib3}-*.whl
