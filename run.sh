#!/usr/bin/bash

rm -rf ~/tmp/some-project
mkdir -p ~/tmp/some-project
export TMPDIR=/home/at/tmp/some-project
rm -rf results/*

python app.py **term** 
