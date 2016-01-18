#!/bin/bash

# This script is triggered from the script section of .travis.yml
# It runs the appropriate commands depending on the task requested.

if [[ $TASK = 'flake8' ]]; then
  flake8 --max-line-length 80 --exclude *_pb2.py,.git,__pycache --ignore E111,E121,E129 config_helper.py master.cfg pass_toucher.py
  # build.config has to be checked seperately, as it's not strictly a Python file
  flake8 --max-line-length 80 --exclude *_pb2.py,.git,__pycache --ignore E111,E121,E129,F821 build.config
elif [[ $TASK = 'pychecker' ]]; then
  # Can't check these files as they aren't true .py files: build.config master.cfg 
  pychecker --quiet --maxargs 12 config_helper.py pass_toucher.py
else
  # Otherwise run checkconfig as normal
  mkdir buildbot && cd buildbot && buildbot create-master master && \
  rm -f master/master.cfg.sample && \
  cp ../build.config ../config_helper.py ../master.cfg master/. && \
  cp ../pass_toucher.py master/. && \
  cd master && ./pass_toucher.py && buildbot checkconfig master.cfg
fi
