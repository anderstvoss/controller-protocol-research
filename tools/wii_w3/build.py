"""Build original W3 diagnosis tools against the unchanged reviewed runtime."""
import argparse
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess

REVISIONS = {'baseline': 'b23fd2570069c59e4815f66329fe78ab7b87ad3c'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', choices=REVISIONS, required=True)
    parser.add_argument('--virtualgamepad', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--sdl-pkg-config-path', required=True)
    args = parser.parse_args()
    repo, output = args.virtualgamepad.resolve(), args.output.resolve()
    here = Path(__file__).resolve().parent
    if output.is_relative_to(repo) or output.is_relative_to(here.parents[1]):
        raise ValueError('Use scratch output outside both repositories')
    actual = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip()
    if actual != REVISIONS[args.case]:
        raise ValueError('Wrong comparison revision')
    if subprocess.check_output(['git', '-C', str(repo), 'status', '--porcelain'], text=True).strip():
        raise ValueError('Use a clean comparison checkout')
    (output / 'src').mkdir(parents=True, exist_ok=True)
    dependencies = ''.join(n + '={path=' + json.dumps(str(repo / 'crates' / n)) + '}\n'
                           for n in ['gr-curated-controllers', 'gr-realization-api'])
    (output / 'Cargo.toml').write_text('[package]\nname="wii-w2-host-probe"\nversion="0.0.0"\nedition="2024"\n[dependencies]\n' + dependencies + 'serde_json="=1.0.145"\n')
    shutil.copyfile(here / 'host_probe.rs', output / 'src/main.rs')
    shutil.copyfile(here / 'Cargo.lock', output / 'Cargo.lock')
    subprocess.run(['cargo', 'build', '--locked', '--offline', '--manifest-path', str(output / 'Cargo.toml')], check=True)
    env = dict(os.environ, PKG_CONFIG_PATH='', PKG_CONFIG_LIBDIR=args.sdl_pkg_config_path)

    def pkg(*options):
        return subprocess.check_output(['pkg-config', *options, 'sdl3'], env=env, text=True).strip()

    if pkg('--modversion') != '3.2.10':
        raise ValueError('Select the recorded SDL3.2.10 installation explicitly')
    subprocess.run(['cc', '-shared', '-fPIC', '-Wall', '-Wextra', '-Werror', str(here / 'trace.c'), '-ldl', '-o', str(output / 'trace.so')], check=True)
    subprocess.run(['cc', '-std=c11', '-Wall', '-Wextra', '-Werror', str(here / 'sdl_probe.c'),
                    *shlex.split(pkg('--cflags', '--libs')), '-Wl,-rpath,' + pkg('--variable=libdir'),
                    '-o', str(output / 'sdl_probe')], check=True)


if __name__ == '__main__':
    main()
