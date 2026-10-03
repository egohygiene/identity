#!/usr/bin/env python3
"""Preview or publish the Identity audit roadmap using an authenticated gh CLI."""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
START = '<!-- identity-roadmap-links:start -->'
END = '<!-- identity-roadmap-links:end -->'


def api(endpoint, method='GET', payload=None, paginate=False):
    cmd = ['gh', 'api', '--method', method, endpoint]
    if paginate:
        cmd += ['--paginate', '--slurp']
    if payload is not None:
        cmd += ['--input', '-']
    result = subprocess.run(cmd, input=json.dumps(payload) if payload is not None else None,
                            text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f'GitHub API {method} {endpoint} failed:\n{result.stderr.strip()}')
    return json.loads(result.stdout)


def marker(manifest, entry):
    return f'<!-- identity-audit-roadmap:{manifest["audit_id"]}:{entry["id"]} -->'


def managed_section(entry, manifest, records):
    def reference(key):
        record = records.get(key)
        return f'#{record["number"]}' if record else key

    lines = [START, '## Roadmap links', '']
    if entry['id'] == 'TRACKER':
        names = {1: 'Authority boundaries', 2: 'Compatibility and recovery',
                 3: 'Reproducible development', 4: 'Documentation and cleanup'}
        for milestone, name in names.items():
            lines += [f'### Milestone {milestone}: {name}', '']
            for child in manifest['issues']:
                if child['milestone'] == milestone:
                    closed = records.get(child['id'], {}).get('state') == 'closed'
                    lines.append(f'- [{"x" if closed else " "}] {reference(child["id"])} — {child["title"]} ({child["id"]}, {child["priority"]})')
            lines.append('')
    else:
        lines += [f'Tracker: {reference("TRACKER")}.', '']
        dependencies = entry.get('depends_on', [])
        lines.append('Depends on: ' + ', '.join(reference(key) for key in dependencies) + '.'
                     if dependencies else 'Dependencies: none; this issue can start independently.')
        children = [other['id'] for other in manifest['issues']
                    if entry['id'] in other.get('depends_on', [])]
        if children:
            lines += ['', 'Unblocks: ' + ', '.join(reference(key) for key in children) + '.']
    return '\n'.join(lines + ['', END])


def draft_body(entry, manifest, records):
    body = (ROOT / entry['body_file']).read_text().rstrip()
    return checked_body(body + '\n\n' + marker(manifest, entry) + '\n\n'
                        + managed_section(entry, manifest, records) + '\n')


def checked_body(body):
    if len(body) > 65536:
        raise ValueError(f'Issue body exceeds GitHub\'s 65,536-character limit: {len(body)}')
    return body


def save_records(manifest, records):
    path = ROOT / 'published.json'
    temp = path.with_suffix('.json.tmp')
    temp.write_text(json.dumps({'repository': manifest['repository'], 'issues': records}, indent=2) + '\n')
    temp.replace(path)


def publish(manifest):
    repository = manifest['repository']
    endpoint = f'repos/{repository}/issues'
    entries = [manifest['tracker']] + manifest['issues']
    # Validate every draft before making even the first external write.
    for entry in entries:
        draft_body(entry, manifest, {})
    repo = api(f'repos/{repository}')
    if not repo.get('has_issues', True):
        raise RuntimeError('Issues are disabled on the target repository.')
    pages = api(endpoint + '?state=all&per_page=100', paginate=True)
    existing = [issue for page in pages for issue in page if 'pull_request' not in issue]
    records = {}
    # Resolve duplicates for the entire roadmap before creating anything.
    for entry in entries:
        owned = [issue for issue in existing if marker(manifest, entry) in (issue.get('body') or '')]
        if len(owned) > 1:
            raise RuntimeError(f'Duplicate roadmap markers for {entry["id"]}; resolve before publishing.')
        if owned:
            records[entry['id']] = owned[0]
            current = owned[0].get('body') or ''
            if current.count(START) != 1 or current.count(END) != 1 or current.index(START) > current.index(END):
                raise RuntimeError(f'{entry["id"]} has altered generated-link delimiters; review before publishing.')
        elif any(issue['title'] == entry['title'] for issue in existing):
            raise RuntimeError(f'An existing issue has the same title as {entry["id"]} without its roadmap marker. Review it before publishing to avoid a duplicate.')
    for entry in entries:
        key = entry['id']
        if key not in records:
            records[key] = api(endpoint, 'POST', {'title': entry['title'],
                                                 'body': draft_body(entry, manifest, records)})
            print(f'Created {key}: {records[key]["html_url"]}', flush=True)
        else:
            print(f'Reusing {key}: {records[key]["html_url"]}', flush=True)
        # Retain partial progress if a later API call fails. Reruns also scan remote markers.
        save_records(manifest, records)
    # Once every issue exists, update only our generated links; preserve notes and edits.
    pattern = re.compile(re.escape(START) + r'.*?' + re.escape(END), re.S)
    for entry in entries:
        key = entry['id']
        current = api(f'{endpoint}/{records[key]["number"]}')
        body = current.get('body') or ''
        if marker(manifest, entry) not in body or body.count(START) != 1 or body.count(END) != 1:
            raise RuntimeError(f'Ownership/link markers changed on {key}; refusing to overwrite the body.')
        replacement = managed_section(entry, manifest, records)
        updated, count = pattern.subn(lambda _: replacement, body)
        if count != 1:
            raise RuntimeError(f'Could not update links on {key}.')
        checked_body(updated)
        if updated != body:
            current = api(f'{endpoint}/{current["number"]}', 'PATCH', {'body': updated})
        records[key] = current
        save_records(manifest, records)
    print(f'Published {len(entries)} linked issues. Tracker: {records["TRACKER"]["html_url"]}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--publish', action='store_true', help='Create issues and link dependencies on GitHub.')
    mode.add_argument('--dry-run', action='store_true', help='Preview and validate all drafts without GitHub access (default).')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'roadmap.json').read_text())
    entries = [manifest['tracker']] + manifest['issues']
    keys = {entry['id'] for entry in entries}
    if len(keys) != len(entries):
        raise ValueError('Duplicate roadmap IDs.')
    for entry in entries:
        if any(key not in keys for key in entry.get('depends_on', [])):
            raise ValueError(f'Unknown dependency on {entry["id"]}.')
    if args.publish:
        publish(manifest)
    else:
        for entry in entries:
            body = draft_body(entry, manifest, {})
            print(f'{entry["id"]}: {entry["title"]} ({len(body)} characters)')
        print(f'Validated {len(entries)} drafts for {manifest["repository"]}. No GitHub writes performed.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
