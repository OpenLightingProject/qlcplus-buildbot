#!/bin/bash

BUILDBOT=/usr/local/bin/buildbot

repo=$(dirname $0)
cd $repo
git fetch origin
output=$(git log HEAD..origin/master --oneline)
if [ -n "$output" ]; then
  echo "Merging";
  set -x
  git merge origin/master;
  $BUILDBOT checkconfig master.cfg
  # checkconfig exits 0 if everything is ok.
  if [ $? -eq 0 ]; then
    $BUILDBOT reconfig
  else
    echo "Buildbot config is bad";
  fi;
fi
