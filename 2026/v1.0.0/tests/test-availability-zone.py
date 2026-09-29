#!/usr/bin/env python3
"""Exercise AZ selection against the UAT failure and existing subnet updates."""
import pathlib
import subprocess
import tempfile

root = pathlib.Path(__file__).resolve().parents[1]
source = (root / 'install.sh').read_text()
function = source.split('select_lab_availability_zone() {', 1)[1].split('\nlab_availability_zone=', 1)[0]
for existing, offered, available, expected in [
    ('', 'us-east-1a us-east-1b', 'us-east-1e us-east-1b', 'us-east-1b'),
    ('us-east-1b', 'us-east-1a us-east-1b', 'us-east-1a us-east-1b', 'us-east-1b'),
    ('', 'us-east-1a', 'us-east-1e', None),
    ('us-east-1e', 'us-east-1a', 'us-east-1a us-east-1e', None),
]:
    with tempfile.TemporaryDirectory() as work:
        script = f'''set -euo pipefail
REGION=us-east-1
INSTANCE_TYPE=t3.micro
STACK_NAME=test
work_dir={work!r}
aws() {{
case "$1 $2" in
'ec2 describe-instance-type-offerings') printf '%s\\n' {offered!r} ;;
'ec2 describe-availability-zones') printf '%s\\n' {available!r} ;;
'cloudformation describe-stack-resource') {'echo subnet-test' if existing else 'return 1'} ;;
'ec2 describe-subnets') printf '%s\\n' {existing!r} ;;
*) return 9 ;;
esac
}}
select_lab_availability_zone() {{{function}
select_lab_availability_zone
'''
        result = subprocess.run(['bash', '-c', script], text=True, capture_output=True)
        if expected is None:
            assert result.returncode != 0, result
        else:
            assert result.returncode == 0 and result.stdout.strip() == expected, result
print('PASS Availability Zone selection: offerings, availability, preservation, rejection')
