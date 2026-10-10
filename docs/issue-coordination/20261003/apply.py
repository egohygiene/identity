#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Preview prepared coordination edits; publish only when current issue bodies match."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--publish', action='store_true')
args = parser.parse_args()
updates = json.loads((root / 'updates.json').read_text(encoding="utf-8"))


def live_body(item):
    result = subprocess.run(
        ['gh', 'api', f'repos/{item["repository"]}/issues/{item["number"]}'],
        text=True, encoding="utf-8", capture_output=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip())
    return json.loads(result.stdout)['body']


def compare(item, current):
    before = (root / item['before']).read_text(encoding="utf-8")
    after = (root / item['after']).read_text(encoding="utf-8")
    if current == after:
        return False
    if current != before:
        raise RuntimeError(
            f'{item["repository"]}#{item["number"]} changed since preparation; '
            'reconcile the latest body before publishing. No stale replacement was sent.'
        )
    return True


try:
    if not args.publish:
        for item in updates:
            print(f'Prepared {item["repository"]}#{item["number"]}: {item["after"]}')
        print('Dry run only. Review coordination.patch; --publish requires authenticated gh.')
        raise SystemExit(0)
    # Check every target before the first write. Preserve other chats' newer edits.
    pending = [item for item in updates if compare(item, live_body(item))]
    for item in pending:
        if not compare(item, live_body(item)):
            continue
        payload = json.dumps({'body': (root / item['after']).read_text(encoding="utf-8")})
        result = subprocess.run(
            ['gh', 'api', '--method', 'PATCH',
             f'repos/{item["repository"]}/issues/{item["number"]}',
             '--input', '-', '--jq', '.html_url'],
            input=payload, text=True, encoding="utf-8", capture_output=True, check=False,
        )
        if result.returncode:
            raise RuntimeError(result.stderr.strip())
        print('Updated', result.stdout.strip(), flush=True)
except (OSError, RuntimeError, ValueError, KeyError) as error:
    print(f'Stopped: {error}', file=sys.stderr)
    raise SystemExit(1)
