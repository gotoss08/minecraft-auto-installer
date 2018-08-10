import argparse

from pathlib import Path
from sys import exit
from os import chdir

from json import load as jsload
from json import dump as jsdump

import requests

def download_mods(pack_settings, local_info):
    mods_dir_path = Path('mods')
    mods_dir_path.mkdir(exist_ok=True)
    chdir(mods_dir_path.resolve())

    for mod_url_raw in pack_settings['mods']:
        mod_url = mod_url_raw.strip()

        local_info_mods = local_info['installed_mods']

        if mod_url in local_info_mods:
            mod_name = local_info_mods[mod_url]
            mod_path = Path(mod_name)
            if mod_path.exists():
                print('Mod "{}" already downloaded.'.format(mod_name))
                continue
            else:
                del local_info_mods[mod_url]

        print('Downloading from "{}"'.format(mod_url))
        r = requests.get(mod_url)
        mod_name = str(r.url).split('/')[-1]
        print('Downloaded "{}"'.format(mod_name))
        Path(mod_name).write_bytes(r.content)

        local_info_mods[mod_url] = mod_name

    chdir('..')


def install_client():
    local_info = {
        "installed_mods": {},
        "installed_resourcepacks": []
    }

    local_info_path = Path('cfg/local-info.json')
    if local_info_path.exists():
        with open(local_info_path, 'r') as local_info_file:
            local_info = jsload(local_info_file)
    else:
        local_info_path.touch()
        with open(local_info_path, 'w') as local_info_file:
            jsdump(local_info, local_info_file)

    pack_settings_path = Path('cfg/pack-settings.json')
    if not pack_settings_path.exists():
        print('Could not locate "{}", aborting...'.format(pack_settings_path))
        exit()

    with open(pack_settings_path, 'r') as psfile:
        pack_settings = jsload(psfile)

        download_mods(pack_settings, local_info)

        with open(local_info_path.resolve(), 'w') as local_info_file:
            jsdump(local_info, local_info_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', help="Install server", action="store_true")
    args = parser.parse_args()

    if args.server:
        print('Installing server.')
        install_server()
    else:
        print('Installing client.')
        install_client()


if __name__ == '__main__':
    main()
