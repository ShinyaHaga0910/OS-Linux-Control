#!/usr/bin/env python3
"""Test real installer selection with mocked AWS discovery and existing resources."""
import json
import pathlib
import shlex
import subprocess
import tempfile

root = pathlib.Path(__file__).resolve().parents[1]
source = (root / 'install.sh').read_text()
function = 'select_lab_instance() {' + source.split('select_lab_instance() {', 1)[1].split('\nselection=', 1)[0]
metadata = {'InstanceTypes': [
    {'InstanceType': name, 'ProcessorInfo': {'SupportedArchitectures': [arch]}}
    for name, arch in [('t2.micro','x86_64'), ('t3.micro','x86_64'),
                       ('t3a.micro','x86_64'), ('t4g.micro','arm64'),
                       ('t12i.micro','x86_64'), ('m8i.micro','x86_64'),
                       ('t12i.small','x86_64')]]}
base = [('t2.micro','us-east-1e'), ('t3.micro','us-east-1a'),
        ('t3a.micro','us-east-1a'), ('t4g.micro','us-east-1a')]
cases = [
    ('newest standard', 'auto', '', '', base, 'us-east-1a us-east-1e', 't3.micro us-east-1a', ''),
    ('new generation numeric', 'auto', '', '', base+[('t12i.micro','us-east-1b')], 'us-east-1a us-east-1b', 't12i.micro us-east-1b', ''),
    ('unavailable newer zone', 'auto', '', '', base+[('t12i.micro','us-east-1b')], 'us-east-1a', 't3.micro us-east-1a', ''),
    ('older zone fallback', 'auto', '', '', base, 'us-east-1e', 't2.micro us-east-1e', ''),
    ('AMD alternate', 'auto', '', '', [('t3a.micro','us-east-1a'),('t2.micro','us-east-1a')], 'us-east-1a', 't3a.micro us-east-1a', ''),
    ('existing stays older', 'auto', 'us-east-1e', 't2.micro', base, 'us-east-1a us-east-1e', 't2.micro us-east-1e', ''),
    ('existing subnet only', 'auto', 'us-east-1e', '', base, 'us-east-1a us-east-1e', 't2.micro us-east-1e', ''),
    ('explicit choice', 't2.micro', '', '', base, 'us-east-1a us-east-1e', 't2.micro us-east-1e', ''),
    ('reject ARM', 't4g.micro', '', '', base, 'us-east-1a', None, ''),
    ('reject no matching AZ', 'auto', '', '', base, 'us-east-1f', None, ''),
    ('preserve incompatible existing', 'auto', 'us-east-1e', 't3.micro', base, 'us-east-1a us-east-1e', None, ''),
    ('metadata denied', 'auto', '', '', base, 'us-east-1a', None, 'describe-instance-types'),
    ('offerings denied', 'auto', '', '', base, 'us-east-1a', None, 'describe-instance-type-offerings'),
    ('zones denied', 'auto', '', '', base, 'us-east-1a', None, 'describe-availability-zones'),
]
for label, requested, existing_zone, existing_type, pairs, zones, expected, denied in cases:
    with tempfile.TemporaryDirectory() as work:
        wd = pathlib.Path(work)
        (wd/'metadata.json').write_text(json.dumps(metadata))
        (wd/'offerings.json').write_text(json.dumps({'InstanceTypeOfferings': [
            {'InstanceType': t, 'Location': z} for t,z in pairs]}))
        q = shlex.quote
        script = f'''set -euo pipefail
REGION=us-east-1
INSTANCE_TYPE={q(requested)}
STACK_NAME=test
work_dir={q(work)}
aws() {{
[[ "$2" != {q(denied)} ]] || return 7
case "$1 $2" in
'ec2 describe-instance-types') cat "$work_dir/metadata.json" ;;
'ec2 describe-instance-type-offerings') cat "$work_dir/offerings.json" ;;
'ec2 describe-availability-zones') printf '%s\\n' {q(zones)} ;;
'cloudformation describe-stack-resource')
  if [[ "$*" == *PublicSubnet* ]]; then
    {"echo subnet-test" if existing_zone else "return 1"}
  else
    {"echo i-test" if existing_type else "return 1"}
  fi ;;
'ec2 describe-subnets') printf '%s\\n' {q(existing_zone)} ;;
'ec2 describe-instances') printf '%s\\n' {q(existing_type)} ;;
*) return 9 ;;
esac
}}
{function}
select_lab_instance
'''
        result = subprocess.run(['bash', '-c', script], text=True, capture_output=True)
        if expected is None:
            assert result.returncode != 0, (label, result)
        else:
            assert result.returncode == 0 and result.stdout.strip() == expected, (label, result)
print('PASS Instance/AZ discovery: newest x86 micro, fallbacks, preservation, explicit choice, ARM and discovery errors')
