#!/usr/bin/env bash

set -e

IMAGE="hypo-inv"

case "$1" in
  build)
    docker build -t "$IMAGE" .
    ;;
  tests)
    docker run --rm \
    -v $(pwd):/app \
    -it \
    "$IMAGE" \
    pytest -vv
    ;;
  dev)
    docker run --rm \
      -v $(pwd):/app \
      --publish 8000:8000 \
      -it \
      "$IMAGE" \
      fastapi dev --host 0.0.0.0 --port 8000
    ;;
  prod)
    docker run --rm \
      -v $(pwd):/app \
      --publish 8000:8000 \
      -it \
      "$IMAGE"
    ;;
  *)
    echo "Usage: $0 {build|tests|dev|prod}"
    exit 1
    ;;
esac
