#!/usr/bin/env bash
set -e
docker build -t test/aggregate_method .
docker run --env ENV=TEST -p5000:5000 test/aggregate_method
