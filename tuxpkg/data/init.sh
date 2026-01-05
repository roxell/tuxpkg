#!/bin/sh

set -exu

if [ ! -f pyproject.toml ] || [ "${TUXPKG_FORCE:-}" = "1" ]; then
    flit init
fi
