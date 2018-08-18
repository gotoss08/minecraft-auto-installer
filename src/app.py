import argparse

from pathlib import Path
from sys import exit
from os import chdir
from os import remove as rmfile
from shutil import copyfile, copytree, rmtree
from os.path import exists

from json import load as jsload
from json import dump as jsdump

import requests
import gdrive
import zipfile
import urllib

import util

LOCAL_VENDOR_PATH = Path('vendor').resolve()
LOCAL_VENDOR_CONFIG_PATH = LOCAL_VENDOR_PATH.joinpath('config')

MINECRAFT_PATH = Path.home().joinpath('AppData/Roaming/.minecraft/').resolve()
MINECRAFT_OPTIONS_PATH = Path.home().joinpath('AppData/Roaming/.minecraft/options.txt')
MINECRAFT_MODS_PATH = Path.home().joinpath('AppData/Roaming/.minecraft/mods/')
MINECRAFT_CONFIG_PATH = Path.home().joinpath('AppData/Roaming/.minecraft/config/')
MINECRAFT_RESOURCEPACKS_PATH = Path.home().joinpath('AppData/Roaming/.minecraft/resourcepacks/')

local_info_path = Path('cfg/local-info.json')
local_info = {
    "installed_mods": {},
    "installed_resourcepacks": {}
}


def update_local_info():
    with open(local_info_path.resolve(), 'w') as local_info_file:
        jsdump(local_info, local_info_file, indent=4)


pack_settings_path = Path('cfg/pack-settings.json')
pack_settings = None


minecraft_options = util.Options(MINECRAFT_OPTIONS_PATH)


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


def install_mods():
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
                mod_name = urllib.parse.unquote(str(r.url)).split('/')[-1]

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
            to_remove_local_mods.append(mod_url_raw)

    for to_remove_mod in to_remove_local_mods:
        del local_info_mods[to_remove_mod]

    # install mods
    try:
        if MINECRAFT_MODS_PATH.exists():
            rmtree(MINECRAFT_MODS_PATH)
        MINECRAFT_MODS_PATH.mkdir()

        if MINECRAFT_CONFIG_PATH.exists():
            rmtree(MINECRAFT_CONFIG_PATH)

        copytree(LOCAL_VENDOR_CONFIG_PATH, MINECRAFT_CONFIG_PATH)

    except PermissionError:
        print('***!!!Close .minecraft folder and all .minecraft subdirectories and try again!!!***')

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


def install_resourcepacs():
    # download resourcepacks
    resourcepacks_dir_path = Path('resourcepacks')
    resourcepacks_dir_path.mkdir(exist_ok=True)

    local_info_resourcepacks = local_info['installed_resourcepacks']

    chdir(resourcepacks_dir_path.resolve())

    for rp_obj in pack_settings['resourcepacks']:
        rp_name = rp_obj['name']
        rp_url = rp_obj['url']

        rp_path = Path(rp_name)
        if rp_path.exists():
            print(f'Resourcepack "{rp_name}" already downloaded.')
            local_info_resourcepacks[rp_url] = rp_name
            continue

        print(f'Downloading "{rp_name}" from "{rp_url}"')

        r = requests.get(rp_url)
        Path(rp_name).write_bytes(r.content)
        print(f'Downloaded "{rp_name}"')
        local_info_resourcepacks[rp_url] = rp_name

        chdir('..')
        update_local_info()
        chdir(resourcepacks_dir_path)

    to_remove_local_resourcepacks = []

    for local_rp_url in local_info_resourcepacks:
        found = False

        for rp_obj in pack_settings['resourcepacks']:
            rp_url = rp_obj['url']
            if local_rp_url == rp_url:
                found = True

        if not found:
            to_remove_local_resourcepacks.append(rp_url)

    for to_remove_rp in to_remove_local_resourcepacks:
        del local_info_resourcepacks[to_remove_rp]

    # install resourcepacks
    if MINECRAFT_RESOURCEPACKS_PATH.exists():
        rmtree(MINECRAFT_RESOURCEPACKS_PATH)
    MINECRAFT_RESOURCEPACKS_PATH.mkdir()

    for local_rp_url in local_info_resourcepacks:
        local_rp_name = local_info_resourcepacks[local_rp_url]
        copyfile(Path(local_rp_name), MINECRAFT_RESOURCEPACKS_PATH.joinpath(local_rp_name))


    chdir('..')
    update_local_info()


def install_client():
    print('Installing client...')

    install_mods()
    install_resourcepacs()

    # update .minecraft/options.txt
    minecraft_options_resourcepacks_str = '['

    resourcepack_index = 0
    resourcepacks_length = len(pack_settings['resourcepacks'])

    for resourcepack_obj in pack_settings['resourcepacks']:
        resourcepack_name = resourcepack_obj['name']
        minecraft_options_resourcepacks_str += f'"{resourcepack_name}"'

        if resourcepack_index < resourcepacks_length - 1:
            minecraft_options_resourcepacks_str += ','
        resourcepack_index += 1

    minecraft_options_resourcepacks_str += ']'

    minecraft_options.set('resourcePacks', minecraft_options_resourcepacks_str)
    minecraft_options.save()

    print('Client installed.')


def install_server():
    print('Installing server...')
    print('Server installed.')


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
