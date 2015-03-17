#!/bin/bash

mkdir buildbot && cd buildbot && buildbot create-master master && \
rm -f master/master.cfg.sample && \
cp ../build.config ../config_helper.py ../master.cfg master/. && \
cp ../pass_toucher.py master/. && \
cd master && ./pass_toucher.py && buildbot checkconfig master.cfg
