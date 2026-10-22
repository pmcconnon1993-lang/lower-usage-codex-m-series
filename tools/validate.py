#!/usr/bin/env python3
"""Offline public-package checks; no third-party dependencies."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/m-series-local-helper'

def main():
    errors=[]
    portable=json.loads((ROOT/'plugin.json').read_text())
    legacy=json.loads((ROOT/'.codex-plugin/plugin.json').read_text())
    market=json.loads((ROOT/'.agents/plugins/marketplace.json').read_text())
    if portable.get('$schema')!='https://agent-plugins.org/schemas/1.0.0/plugin.schema.json':
        errors.append('Invalid portable plugin schema.')
    if any(key in portable for key in ('skills','mcpServers','apps','interface','hooks')):
        errors.append('Portable component metadata is in the wrong location.')
    for key in ('name','version','description','author','homepage','repository','license','keywords'):
        if portable.get(key)!=legacy.get(key):errors.append('Plugin manifest drift: '+key)
    interface=portable.get('extensions',{}).get('com.openai',{}).get('interface',{})
    if legacy.get('interface')!=interface:errors.append('Plugin presentation drift.')
    if not re.fullmatch(r'\d+\.\d+\.\d+',portable.get('version','')):errors.append('Plugin version must use SemVer.')
    if legacy.get('skills')!='./skills/':errors.append('Compatibility skill path is invalid.')
    if not 1<=len(interface.get('shortDescription',''))<=30:errors.append('Invalid plugin subtitle length.')
    if interface.get('category')!='Developer Tools':errors.append('Invalid plugin category.')
    if not isinstance(interface.get('capabilities'),list):errors.append('Invalid plugin capabilities.')
    prompts=interface.get('defaultPrompt',[])
    if not isinstance(prompts,list) or not 1<=len(prompts)<=3 or any(not isinstance(p,str) or not 1<=len(p)<=128 for p in prompts):
        errors.append('Invalid plugin starter prompts.')
    entries=market.get('plugins',[])
    if len(entries)!=1 or entries[0].get('name')!=portable.get('name') or entries[0].get('source')!={'source':'local','path':'./'}:
        errors.append('Marketplace does not resolve this plugin root.')
    elif entries[0].get('policy')!={'installation':'AVAILABLE','authentication':'ON_INSTALL'} or entries[0].get('category')!=interface.get('category'):
        errors.append('Marketplace policy or category drift.')
    if market.get('name')!='m-series-local-helpers':errors.append('Marketplace identity drift.')
    skill=(SKILL/'SKILL.md').read_text()
    if not skill.startswith('---\nname: m-series-local-helper\ndescription:'):
        errors.append('Skill frontmatter missing required identity.')
    cat=json.loads((SKILL/'data/catalog.json').read_text())
    for key, model in cat['models'].items():
        if not re.fullmatch('[a-f0-9]{40}',model['revision']): errors.append('Invalid model pin: '+key)
        if type(model['repository_bytes']) is not int or model['repository_bytes']<=0: errors.append('Invalid artifact size: '+key)
    for machine in cat['machines'].values():
        if not (SKILL/machine['guide']).is_file(): errors.append('Missing guide: '+machine['guide'])
    for p in ROOT.rglob('*'):
        if any(x in p.parts for x in ('.git','__pycache__','local','private')) or not p.is_file() or p.name=='.project-security.json': continue
        if p.suffix in ('.gguf','.safetensors','.pem','.key'):errors.append('Forbidden bundled artifact: '+str(p.relative_to(ROOT)))
        if p.suffix not in ('.md','.json','.yaml','.yml'):continue
        text=p.read_text()
        if '/Users/macstudio' in text or '/Volumes/4TB Lexar' in text:errors.append('Private workstation path: '+str(p.relative_to(ROOT)))
        if p.suffix=='.md':
            for target in re.findall(r'\]\(([^)]+)\)',text):
                target=target.strip('<>').split('#')[0]
                if not target or '://' in target or target.startswith('mailto:'):continue
                if not (p.parent/target).exists():errors.append(f'Broken relative link in {p.relative_to(ROOT)}: {target}')
    bp=SKILL/'scripts/benchmark.py'
    if bp.exists():
        spec=importlib.util.spec_from_file_location('benchvalidate',bp); mod=importlib.util.module_from_spec(spec)
        sys.path.insert(0,str(bp.parent)); spec.loader.exec_module(mod)
        for p in (ROOT/'evidence/community').rglob('*.json'):
            try: errors += [f'{p.relative_to(ROOT)}: {e}' for e in mod.validate_report(json.loads(p.read_text()))]
            except (ValueError,KeyError,TypeError) as e:errors.append(f'{p.relative_to(ROOT)}: invalid report {type(e).__name__}')
    sums=ROOT/'SHA256SUMS'
    if sums.exists():
        for line in sums.read_text().splitlines():
            expected,name=line.split('  ',1); p=ROOT/name
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:errors.append('Checksum mismatch: '+name)
    if errors:
        print('\n'.join(errors));return 1
    print('Package/plugin identity, model pins, local links, privacy markers and submitted-report schemas passed. This is not a model quality or full security assessment.')
    return 0

if __name__=='__main__':raise SystemExit(main())
