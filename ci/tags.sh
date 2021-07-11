#!/bin/bash

git -c 'versionsort.suffix=-' ls-remote --exit-code --refs \
    --sort='version:refname' --tags $URL '*.*.*'
