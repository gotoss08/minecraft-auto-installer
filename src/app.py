import argparse

from pathlib import Path
from sys import exit
from os import chdir
from os import remove as rmfile
from shutil import copyfile
from shutil import rmtree
from os.path import exists

from json import load as jsload
from json import dump as jsdump

import requests
import gdrive
import zipfile

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

    for mod_obj in pack_settings['mods']:
        simple_obj = True
        gdrive_type = False
        zip_type = False
        zip_obj = {}

        if type(mod_obj) == type(''):
            mod_url = mod_obj.strip()
        elif type(mod_obj) == type({}):
            simple_obj = False

            if 'gdrive' in mod_obj:
                gdrive_type = True
                mod_name = mod_obj['name'].strip()
            elif 'zip' in mod_obj:
                zip_type = True
                zip_obj['name'] = mod_obj['zip_name']
                zip_obj['path'] = mod_obj['zip_path']
                mod_name = zip_obj['name'].strip()

            mod_url = mod_obj['url'].strip()

        if mod_url in local_info_mods:
            local_mod_name = local_info_mods[mod_url]
            mod_path = Path(local_mod_name)
            if mod_path.exists():
                print('Mod "{}" already downloaded.'.format(local_mod_name))
                continue
            else:
                del local_info_mods[mod_url]

        print('Downloading from "{}"'.format(mod_url))

        if gdrive_type: # if gdrive url
            gdrive.download_file_from_google_drive(mod_url, mod_name)
        else: # if regular url
            r = requests.get(mod_url)

            if simple_obj:
                mod_name = str(r.url).split('/')[-1]

            Path(mod_name).write_bytes(r.content)

            if zip_type: # if file zipped
                zip_ref = zipfile.ZipFile(zip_obj['name'], 'r')
                zip_ref.extract(zip_obj['path'])
                zip_ref.close()
                mod_name = mod_obj['name']
                copyfile(Path(zip_obj['path']).resolve(), Path().cwd().joinpath(mod_name))
                rmtree(Path(zip_obj['path']).parent)
                rmfile(Path(zip_obj['name']))

        print('Downloaded "{}"'.format(mod_name))
        local_info_mods[mod_url] = mod_name

        # to speed up debugging
        chdir('..')
        update_local_info()
        chdir('./mods/')

    to_remove_local_mods = []

    for mod_obj in pack_settings['mods']:
        if type(mod_obj) == type(''):
            pass
        elif type(mod_obj) == type({}):
            pass

    for mod_url_raw in local_info_mods:
        mod_url = mod_url_raw.strip()
        found = False

        for mod_obj in pack_settings['mods']:
            if type(mod_obj) == type(''):
                if mod_url_raw == mod_obj:
                    found = True
                    break
            elif type(mod_obj) == type({}):
                if mod_url_raw == mod_obj['url']:
                    found = True
                    break

        if not found:
            print('removing {}'.format(mod_url))
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
