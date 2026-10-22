#!/usr/bin/env python3
"""Read-only hardware probe and conservative candidate router; never installs."""
import argparse
import datetime as dt
import json
import math
from pathlib import Path
import platform
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'data/catalog.json'


def parse_chip(value):
    m = re.fullmatch(r'(?:Apple\s+)?M([1-9][0-9]*)(?:\s+(Pro|Max|Ultra))?', value.strip(), re.I)
    if not m:
        raise ValueError('Use the exact Apple chip, for example Apple M2 Max; Intel is unsupported.')
    return int(m[1]), (m[2] or 'base').lower()


def version(value):
    if not re.fullmatch(r'\d+(?:\.\d+){0,2}', value):
        raise ValueError('macOS must be a numeric version, for example 26.4')
    return tuple((list(map(int, value.split('.'))) + [0, 0])[:3])


def recommend(chip, ram_gb, macos, free_gb=None, mode='focused', catalog=None):
    cat = catalog or json.loads(CATALOG.read_text())
    gen, variant = parse_chip(chip)
    if not math.isfinite(ram_gb) or ram_gb <= 0 or (free_gb is not None and (not math.isfinite(free_gb) or free_gb < 0)):
        raise ValueError('Memory and free space must be finite positive values (free space may be zero).')
    os_ver = version(macos)
    base = {'chip': chip, 'ram_gb': ram_gb, 'macos': macos, 'mode': mode,
            'catalog_reviewed': cat['reviewed_at'], 'status': 'research_required',
            'downloads_authorized': False, 'is_universal_best': False}
    machine = cat['machines'].get(f'm{gen}')
    if not machine or variant not in machine['variants']:
        return {**base, 'reason': 'Chip variant is outside this dated catalog. Verify Apple specifications and runtime support first.'}
    base['guide'] = f'references/machines/m{gen}.md'
    minimum, maximum = machine['ram_bounds_gb'][variant]
    if not minimum <= ram_gb <= maximum:
        return {**base, 'reason': 'Reported RAM contradicts this dated chip-family range. Confirm About This Mac and refresh Apple product sources before selection.'}
    base['hardware_check'] = 'Bounds are a plausibility screen, not every sold configuration. Confirm actual Mac/product and RAM.'
    if os_ver < (15, 0, 0):
        return {**base, 'reason': 'Default oMLX path requires macOS 15+. Research an OS-compatible runtime; do not upgrade the OS automatically.'}
    tiers = [t for t in cat['tiers'] if ram_gb >= t['min_ram_gb']]
    if not tiers:
        return {**base, 'reason': 'Below the conservative 8 GB starting tier. Retain Codex-only work or qualify a smaller model manually.'}
    tier = tiers[-1]
    model = cat['models'][tier['model']]
    is_35b = tier['model'].startswith('qwen35-')
    splash_ok = gen >= 3 and os_ver >= (26, 4, 0) and is_35b
    fork_candidate = gen in (1, 2) and is_35b
    if splash_ok:
        runtime = 'omlx-splash' if mode == 'multi-model' else 'splash'
        why_runtime = 'Inco Splash is the preferred supported path for the matching 35B target/draft; oMLX can manage it alongside other models.'
    else:
        runtime = 'omlx-mlx'
        why_runtime = 'Use the Apple MLX path for this smaller model or OS/hardware combination. Official Splash support is not established for this selection.'
    alternate_tiers = [t for t in tiers if t['min_ram_gb'] <= 32 and t['model'] != tier['model']]
    alternate = cat['models'][alternate_tiers[-1]['model']] if alternate_tiers else None
    draft = cat['models']['dflash35'] if splash_ok else None
    download = model['repository_bytes'] + (draft['repository_bytes'] if draft else 0)
    # Disk margin is planning policy, not a prediction of runtime memory.
    disk_budget = math.ceil(download / 1e9 * 1.25 + tier['ssd_cache_gb'] + 5)
    blockers = []
    if gen == 6:
        blockers.append('Verify actual M6 initialization: the reviewed oMLX explicit chip list ended at M5; no M6 task has been qualified here.')
    if free_gb is None:
        blockers.append('Verify free space on the actual chosen destination.')
    elif free_gb < disk_budget:
        blockers.append(f'Need at least {disk_budget} GB planning space at the chosen destination; includes download, cache and margin.')
    if ram_gb < 16:
        blockers.append('8–12 GB is experimental for tool work; use very short inputs and decline delegation if the desktop swaps or quality fails.')
    age = (dt.date.today() - dt.date.fromisoformat(cat['reviewed_at'])).days
    if age > cat['review_interval_days'] or age < 0:
        blockers.append('Catalog is stale or clock disagrees: refresh primary sources before setup.')
    return {**base, 'status': 'candidate_needs_qualification', 'candidate': model,
            'runtime': runtime, 'runtime_reason': why_runtime, 'draft': draft,
            'optional_lighter_model': alternate,
            'optional_model_reason': 'Smaller artifact and a potential headroom tradeoff; task quality and actual speed require local comparison. Offer only if useful, and do not download both by default.',
            'm1_m2_splash_fork_candidate': fork_candidate,
            'alternative': 'oMLX manages multiple models and can host supported Splash profiles; load one heavy model at a time.',
            'context_tokens_start': tier['context_tokens'], 'output_tokens_start': tier['output_tokens'], 'ssd_cache_gb_start': tier['ssd_cache_gb'],
            'reserve_gb_policy': max(6, math.ceil(ram_gb * .25)),
            'download_bytes': download, 'disk_budget_gb': disk_budget, 'checks_before_setup': blockers,
            'evidence': 'Recorded M5 Ultra 256 GB configuration only; requalify exact runtime/model and task on this machine.' if tier['model'] == 'qwen35-8' else 'Source-backed candidate, not locally benchmarked across this memory tier.',
            'reason': tier['reason'], 'next': 'Confirm the runtime mode only if preference is unknown; review sources and show an exact approval plan.'}


def detect(storage):
    if platform.system() != 'Darwin':
        return {'status': 'ask_user', 'reason': 'This process is not on macOS; ask about the target Mac.'}
    def run(*args):
        return subprocess.run(args, check=True, capture_output=True, text=True, timeout=10).stdout.strip()
    p = Path(storage).expanduser().resolve(strict=True)
    return {'chip': run('/usr/sbin/sysctl', '-n', 'machdep.cpu.brand_string'),
            'ram_gb': round(int(run('/usr/sbin/sysctl', '-n', 'hw.memsize')) / 1024**3),
            'macos': run('/usr/bin/sw_vers', '-productVersion'),
            'storage': str(p), 'free_gb': round(shutil.disk_usage(p).free / 1e9, 1),
            'note': 'Confirm this is the target Mac. No serial number or account identity collected.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sp = p.add_subparsers(dest='command', required=True)
    d = sp.add_parser('detect'); d.add_argument('--storage', required=True)
    r = sp.add_parser('recommend'); r.add_argument('--chip', required=True); r.add_argument('--ram-gb', type=float, required=True)
    r.add_argument('--macos', required=True); r.add_argument('--free-gb', type=float)
    r.add_argument('--mode', choices=['focused', 'multi-model'], default='focused')
    a = p.parse_args()
    try:
        result = detect(a.storage) if a.command == 'detect' else recommend(a.chip, a.ram_gb, a.macos, a.free_gb, a.mode)
    except (ValueError, OSError, subprocess.SubprocessError) as e:
        p.exit(2, f'{type(e).__name__}: {e}\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
