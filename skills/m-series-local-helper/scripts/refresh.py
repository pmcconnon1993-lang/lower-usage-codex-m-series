#!/usr/bin/env python3
"""Check upstream metadata as data only. Never install, execute, or upload."""
import argparse
import datetime as dt
import json
from pathlib import Path
import re
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = 'pmcconnon1993-lang/lower-usage-codex-m-series'

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('Redirect refused; review the canonical source URL.')


def fetch(url):
    # All callers construct URLs on fixed primary-source hosts from constrained IDs.
    req = urllib.request.Request(url, headers={'User-Agent': 'm-series-local-helper-metadata/1', 'Accept': 'application/json'})
    with urllib.request.build_opener(NoRedirect()).open(req, timeout=12) as r:
        blob = r.read(2_000_001)
    if len(blob) > 2_000_000:
        raise ValueError('Metadata response exceeded limit.')
    return json.loads(blob)


def check(offline=False):
    cat = json.loads((ROOT / 'data/catalog.json').read_text())
    today = dt.date.today()
    age = (today - dt.date.fromisoformat(cat['reviewed_at'])).days
    result = {'schema_version': 1, 'checked_at': today.isoformat(), 'catalog_reviewed_at': cat['reviewed_at'],
              'stale': age < 0 or age > cat['review_interval_days'], 'mode': 'offline' if offline else 'online',
              'updates_applied': False, 'models': [], 'runtimes': [], 'errors': []}
    if offline:
        result['next'] = 'Review current primary sources before installing. Offline age check is not freshness verification.'
        return result
    for key, model in cat['models'].items():
        repo = model['id']
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
            result['errors'].append({'source': key, 'error': 'invalid model identifier'}); continue
        try:
            info = fetch('https://huggingface.co/api/models/' + repo)
            result['models'].append({'id': repo, 'pinned': model['revision'], 'current': info.get('sha'),
                                     'changed': info.get('sha') != model['revision'], 'gated': info.get('gated'),
                                     'license': info.get('cardData', {}).get('license')})
        except (ValueError, OSError, urllib.error.URLError) as e:
            result['errors'].append({'source': repo, 'error_type': type(e).__name__})
    for repo in ('incoai/splash', 'jundot/omlx', 'ml-explore/mlx-lm', 'paperniuk/splash', REPOSITORY):
        try:
            info = fetch('https://api.github.com/repos/' + repo + '/commits/HEAD')
            pinned = cat.get('runtime_revisions', {}).get(repo)
            result['runtimes'].append({'repository': repo, 'head': info.get('sha'), 'reviewed_head': pinned, 'changed': None if pinned is None else info.get('sha') != pinned, 'url': 'https://github.com/' + repo})
        except (ValueError, OSError, urllib.error.URLError) as e:
            result['errors'].append({'source': repo, 'error_type': type(e).__name__})
    result['next'] = 'Compare source/release changes to the installed versions; review a diff and rerun local qualification before adoption.'
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--offline', action='store_true'); p.add_argument('--output', type=Path)
    a = p.parse_args(); result = check(a.offline)
    content = json.dumps(result, indent=2, allow_nan=False) + '\n'
    if a.output:
        with a.output.open('x') as f:
            f.write(content)
    else:
        print(content, end='')
    return 1 if result['errors'] else 0

if __name__ == '__main__':
    raise SystemExit(main())
