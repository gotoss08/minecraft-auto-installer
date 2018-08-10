import argparse

from pathlib import Path
from sys import exit
from os import chdir
from shutil import copyfile
from shutil import rmtree
from os.path import exists

from json import load as jsload
from json import dump as jsdump

import requests

MINECRAFT_PATH = Path.home().joinpath('AppData/Roaming/.minecraft/')
MINECRAFT_OPTIONS_PATH = Path.home().joinpath('AppData/Roaming/.minecraft/options.txt')
MINECRAFT_MODS_PATH = Path.home().joinpath('AppData/Roaming/.minecraft/mods/')
MINECRAFT_CONFIG_PATH = Path.home().joinpath('AppData/Roaming/.minecraft/config/')
MINECRAFT_RESOURCEPACKS_PATH = Path.home().joinpath('AppData/Roaming/.minecraft/resourcepacks/')

local_info_path = Path('cfg/local-info.json')
local_info = {
    "installed_mods": {},
    "installed_resourcepacks": []
}

def update_local_info():
    with open(local_info_path.resolve(), 'w') as local_info_file:
        jsdump(local_info, local_info_file)

pack_settings_path = Path('cfg/pack-settings.json')
pack_settings = None


def load_cfg():
    # load local info
    global local_info

    if local_info_path.exists():
        with open(local_info_path, 'r') as local_info_file:
            local_info = jsload(local_info_file)
    else:
        local_info_path.touch()
        with open(local_info_path, 'w') as local_info_file:
            jsdump(local_info, local_info_file)

    # load pack settings
    global pack_settings

    if not pack_settings_path.exists():
        print('Could not locate "{}", aborting...'.format(pack_settings_path))
        exit()

    with open(pack_settings_path, 'r') as psfile:
        pack_settings = jsload(psfile)


def install_client():
    print('Installing client.')

    # download mods
    mods_dir_path = Path('mods')
    mods_dir_path.mkdir(exist_ok=True)

    local_info_mods = local_info['installed_mods']

    chdir(mods_dir_path.resolve())

    for mod_url_raw in pack_settings['mods']:
        mod_url = mod_url_raw.strip()

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

    to_remove_local_mods = []

    for mod_url_raw in local_info_mods:
        mod_url = mod_url_raw.strip()
        if mod_url not in pack_settings['mods']:
            to_remove_local_mods.append(mod_url_raw)

    for to_remove_mod in to_remove_local_mods:
        del local_info_mods[to_remove_mod]

    # install mods
    if MINECRAFT_MODS_PATH.exists():
        rmtree(str(MINECRAFT_MODS_PATH))

    try:
        MINECRAFT_MODS_PATH.mkdir()
    except PermissionError:
        print('!!!Close mods folder and try again!!!')

    for mod_url in local_info_mods:
        mod_name = local_info_mods[mod_url]
        mod_path = Path(mod_name)
        if mod_path.exists():
            copyfile(str(mod_path), str(MINECRAFT_MODS_PATH.joinpath(mod_name)))
        else:
            print('Mod at path "{}" does not exists.'.format(mod_path.resolve()))
            continue

    chdir('..')
    update_local_info()

    # update .minecraft/options.txt


def install_server():
    print('Installing server.')


def main():
    load_cfg()

    parser = argparse.ArgumentParser()
    parser.add_argument('--server', help="Install server", action="store_true")
    args = parser.parse_args()

    if args.server:
        install_server()
    else:
        install_client()


if __name__ == '__main__':
    main()
