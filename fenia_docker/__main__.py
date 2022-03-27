import argparse
import subprocess
from pathlib import Path
from pprint import pprint
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', nargs='?', default='linLMTerm', help='FENIA command')
    parser.add_argument('-i', '--image', default='10.254.55.75/fenia:latest',
                        help='FENIA image')
    parser.add_argument('-a', '--archive', default='fenia_latest.tar.gz',
                        help='FENIA archive')
    parser.add_argument('-d', '--detached', action='store_true', help='Detached mode')
    parser.add_argument('--rm', action='store_true', help='Remove container')
    args = vars(parser.parse_args())
    print('Args')
    pprint(args)
    # Check
    print(f'\nChecking image {args["image"]}')
    inspect_args = ["docker", "inspect", args['image']]
    print(f'Command: {inspect_args}')
    c = subprocess.run(args=inspect_args,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if c.returncode == 0:
        print('OK!')
    else:  # Load
        print('BAD!')
        print(f'Return code: {c.returncode}')
        print(f'Stdout: {c.stdout}')
        print(f'Stderr: {c.stderr}')
        p = Path(__file__).resolve().parent / args['archive']
        print(f'\nTrying to load archive {p}')
        load_args = ["docker", "load", "-i", str(p)]
        print(f'Command: {load_args}')
        l = subprocess.run(args=load_args,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if l.returncode == 0:
            print('OK!')
        else:
            print('BAD!')
            print(f'Return code: {l.returncode}')
            print(f'Stdout: {l.stdout}')
            print(f'Stderr: {l.stderr}')
            sys.exit(1)
    print(f'\nChecking image {args["image"]}')
    print(f'Command: {inspect_args}')
    c = subprocess.run(args=inspect_args,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if c.returncode == 0:  # Run
        print('OK!')
        print(f'\nRunning image {args["image"]}')
        p = Path.cwd().resolve()
        run_args = ["docker", "run"]
        if args['detached']:
            run_args.append('-d')
        if args['rm']:
            run_args.append('--rm')
        run_args.extend(["-v", f"{str(p)}:/work",
                         "10.254.55.75/fenia:latest",
                         args['cmd']])
        print(f'Command: {run_args}')
        r = subprocess.run(args=run_args,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if r.returncode == 0:
            print('Done!')
        else:
            print('BAD!')
            print(f'Return code: {r.returncode}')
            print(f'Stdout: {r.stdout}')
            print(f'Stderr: {r.stderr}')
            sys.exit(1)
    else:
        print('BAD!')
        print(f'Return code: {c.returncode}')
        print(f'Stdout: {c.stdout}')
        print(f'Stderr: {c.stderr}')
        sys.exit(1)
