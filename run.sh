#!/usr/bin/bash

rm -rf ~/tmp/some-project
mkdir -p ~/tmp/some-project
export TMPDIR=~/tmp/some-project
rm -rf results/*

python app.py "books infographic" 2
