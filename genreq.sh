#!/bin/sh

# Generate requirements.txt from Poetry
poetry export -f requirements.txt -o requirements.txt --without-hashes
