#!/usr/bin/env bash
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
# Linux/amd64 check runner only; ordinary standalone setup does not require Task.
set -euo pipefail
destination="${1:?Usage: install_task_for_checks.sh DIRECTORY}"
mkdir -p -- "$destination"
temporary="$(mktemp -d "$destination/.task-download.XXXXXX")"
trap 'rm -rf -- "$temporary"' EXIT
curl --fail --silent --show-error --location --connect-timeout 10 --max-time 60 \
  https://github.com/go-task/task/releases/download/v3.45.3/task_linux_amd64.tar.gz \
  --output "$temporary/task.tar.gz"
printf '%s  %s\n' \
  2c39d989ba8ab6ed37c025e9094e37240360fa2d69158504fc7a7486c88dc26f \
  "$temporary/task.tar.gz" | sha256sum --check
tar --extract --gzip --file "$temporary/task.tar.gz" --directory "$temporary" task
install -m 755 "$temporary/task" "$destination/task"
"$destination/task" --version
