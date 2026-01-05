#!/bin/sh

set -exu

if [ ! -f pyproject.toml ]; then
    flit init
fi
