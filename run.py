#!venv/bin/python

import argparse
import glob
import os
import subprocess
import sys
from datetime import date


HELP = '''
Run locust against a host using a specified locustfile.

The host to target, number of users to create, the rate to spawn users, and the length
of the locust run time can all be specified through command line arguments.

Once the locust test has completed, the stats output file will be moved to the specified
directory with a name that contains information about the locust run.
'''


parser = argparse.ArgumentParser(prog='./run.py', formatter_class=argparse.RawTextHelpFormatter, description=HELP)

parser.add_argument(
    'locust_file',
    type=str,
    help='Locust file name to use when running the locust test.'
)

parser.add_argument(
    '--users',
    type=int,
    default=10,
    help='Number of users to spawn when running the test. Default is 10 users.'
)

parser.add_argument(
    '--spawn_rate',
    type=int,
    default=1,
    help='Rate at which to spawn users when running the test (per second). Default is 1 user per second.'
)

parser.add_argument(
    '--run_time',
    type=str,
    default='5m',
    help='''
Amount of time to run the locust test.
Should be in the format of TIME/INTERVAL, where TIME is an integer and INTERVAL is one of (s,m,h).
Default is 5 minutes (5m).
'''
)

parser.add_argument(
    '--host',
    type=str,
    default='https://moodytunes.vm',
    help='''
Moodytunes host to run the locust test against.
Should be the fully qualified domain name, including the protocol.
Default is %(default)s.
'''
)

parser.add_argument(
    '--output_directory',
    type=str,
    default=f'{os.getenv("HOME")}/development/Moodytunes/data/load_tests/baseline_{date.today().isoformat()}',
    help='''
Directory to write the test results to. Will create the directory if it does not exist.
Default is $HOME/development/Moodytunes/data/load_tests/baseline_$CURRENT_DATE_IN_ISO_FORMAT
'''
)

parser.add_argument(
    '--output_prefix',
    type=str,
    default='',
    help='Optional prefix to include in output filename'
)

args = parser.parse_args()

locust_file = args.locust_file
users = args.users
spawn_rate = args.spawn_rate
run_time = args.run_time
host = args.host
output_directory = args.output_directory
output_filename_prefix = args.output_prefix

if not os.path.exists(locust_file):
    print(f'ERROR: {locust_file} does not exist!', file=sys.stderr)
    sys.exit(1)

# Parse test target from locust file name to build output prefix
test_target = locust_file.split('/')[1].replace('.py', '')
output_prefix = f'{output_filename_prefix}{test_target}_{users}_users_{spawn_rate}_per_sec'

command = [
    'locust',
    f'--locustfile {locust_file}',
    f'--users {users}',
    f'--spawn-rate {spawn_rate}',
    f'--host {host}',
    '--headless',
    f'--run-time {run_time}',
    f'--csv {output_prefix}'
]

cmd = ' '.join(command)
subprocess.run(cmd, check=True, shell=True)

# Write output file to output directory
os.makedirs(output_directory, exist_ok=True)
os.rename(f'{output_prefix}_stats.csv', f'{output_directory}/{output_prefix}_{run_time}.csv')

# Delete other CSV files from locust
for f in glob.glob('*.csv'):
    os.unlink(f)
