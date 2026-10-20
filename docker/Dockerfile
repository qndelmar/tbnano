# Shared tbnano sandbox image: ONE image for the whole benchmark
# (unlike TerminalBench 1.0's per-task images). Each task is a directory
# mounted fresh at /task; reset between tasks = new container.
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        bash coreutils grep sed gawk findutils \
        jq sqlite3 gcc libc6-dev make git bc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir numpy pandas pytest

WORKDIR /task
