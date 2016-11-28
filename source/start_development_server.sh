#!/usr/bin/env bash
set -e
docker build -t test/aggregate_method .
docker run --env ENV=DEVELOPMENT -p5000:5000 -v$(pwd)/aggregate_method:/aggregate_method test/aggregate_method
