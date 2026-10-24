"""Build original, owned-device-only W7 diagnostics into external scratch space."""
import argparse
import json
import shutil
import subprocess
from pathlib import Path

BASE = '840db2771cbcef83b50ee9355c7b6165b95f234a'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--virtualgamepad', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--libretro-header', type=Path, required=True)
    args = parser.parse_args()
    repo, output = args.virtualgamepad.resolve(), args.output.resolve()
    here = Path(__file__).resolve().parent
    if output.is_relative_to(repo) or output.is_relative_to(here.parents[1]):
        raise ValueError('Use scratch output outside both repositories')
    subprocess.run(['git', '-C', str(repo), 'diff', '--exit-code', BASE, '--',
                    'crates', 'Cargo.toml', 'Cargo.lock'], check=True)
    (output / 'src').mkdir(parents=True, exist_ok=True)
    deps = ''.join(name + '={path=' + json.dumps(str(repo / 'crates' / name)) + '}\n'
                   for name in ['gr-curated-controllers', 'gr-realization-api'])
    (output / 'Cargo.toml').write_text('[package]\nname="wii-w7-host-probe"\nversion="0.0.0"\n'
                                      'edition="2024"\n[dependencies]\n' + deps + 'serde_json="=1.0.145"\n')
    shutil.copyfile(here / 'host_probe.rs', output / 'src/main.rs')
    shutil.copyfile(here / 'Cargo.lock', output / 'Cargo.lock')
    subprocess.run(['cargo', 'build', '--locked', '--offline', '--manifest-path',
                    str(output / 'Cargo.toml')], check=True)
    shutil.copyfile(args.libretro_header, output / 'libretro.h')
    for source, target, extra in [
        ('xwiimote_probe.c', 'xwiimote_probe', ['-lxwiimote']),
        ('udev_control.c', 'udev_control', ['-ludev']),
        ('owned_io.c', 'owned_io.so', ['-shared', '-fPIC', '-ldl']),
        ('cemu_guard.c', 'cemu_guard.so', ['-shared', '-fPIC', '-ldl']),
        ('input_diagnostic.c', 'input_diagnostic.so', ['-shared', '-fPIC', '-I' + str(output)]),
    ]:
        subprocess.run(['cc', '-D_POSIX_C_SOURCE=200809L', '-Wall', '-Wextra', '-Werror',
                        str(here / source), *extra, '-o', str(output / target)], check=True)


if __name__ == '__main__':
    main()
