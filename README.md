# modernize-cobol-to-python

[![CI](https://github.com/corentinlevet/modernize-cobol-to-python/actions/workflows/ci.yml/badge.svg)](https://github.com/corentinlevet/modernize-cobol-to-python/actions/workflows/ci.yml)
[![Tests](https://github.com/corentinlevet/modernize-cobol-to-python/actions/workflows/ci.yml/badge.svg?event=push&label=tests)](https://github.com/corentinlevet/modernize-cobol-to-python/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/corentinlevet/modernize-cobol-to-python)](https://github.com/corentinlevet/modernize-cobol-to-python/releases)
[![Last commit](https://img.shields.io/github/last-commit/corentinlevet/modernize-cobol-to-python)](https://github.com/corentinlevet/modernize-cobol-to-python/commits/main)

This repository contains a small COBOL -> Python modernization project and a CI workflow that builds a Docker image and runs the Python test-suite.

Quick commands

Build the Docker image locally:

```bash
docker build -f docker/Dockerfile -t cobol-python-ci:latest .
```

Run tests inside the built image:

```bash
docker run --rm -v "$PWD":/app cobol-python-ci:latest bash -lc "cd /app && pytest -q code/python/tests"
```

Test artifacts and logs are uploaded by CI and available on the workflow run page.
