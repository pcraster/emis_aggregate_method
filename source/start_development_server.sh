#!/usr/bin/env bash
set -e


docker build -t test/emis_aggregate_method .
docker run \
    --env EMIS_CONFIGURATION=development \
    -p5000:5000 \
    -v$(pwd)/emis_aggregate_method:/emis_aggregate_method \
    test/emis_aggregate_method
