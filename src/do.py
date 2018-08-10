import argparse
from util import *
import sys
import json

HOME_PATH = Path.home()
MINECRAFT_PATH = HOME_PATH.joinpath('AppData/Roaming/.minecraft')
MINECRAFT_OPTIONS_PATH = HOME_PATH.joinpath('AppData/Roaming/.minecraft/options.txt')
MINECRAFT_MODS_PATH = HOME_PATH.joinpath('AppData/Roaming/.minecraft/mods')
MINECRAFT_CONFIGS_PATH = HOME_PATH.joinpath('AppData/Roaming/.minecraft/config')
MINECRAFT_LIBS_PATH = HOME_PATH.joinpath('AppData/Roaming/.minecraft/libraries')
MINECRAFT_LOGS_PATH = HOME_PATH.joinpath('AppData/Roaming/.minecraft/logs')
MINECRAFT_RESOURCEPACKS_PATH = HOME_PATH.joinpath('AppData/Roaming/.minecraft/resourcepacks')

resourcepack_names = []
preffered_lang = 'en_US'


def download_mods():
    with open('pack-settings.json', 'rb') as psf:
        psJSON = json.load(psf)

        for modURL in psJSON['mods']:
            modFile = download_file(modURL)


def normalize_folder_structure():
    print('normalizing folder structure...')
    remove_folder(str(MINECRAFT_MODS_PATH))
    remove_folder(str(MINECRAFT_CONFIGS_PATH))
    # remove_folder(str(MINECRAFT_LIBS_PATH))
    # remove_folder(str(MINECRAFT_LOGS_PATH))
    remove_folder(str(MINECRAFT_RESOURCEPACKS_PATH))

    create_folder(str(MINECRAFT_MODS_PATH))
    create_folder(str(MINECRAFT_RESOURCEPACKS_PATH))
    print('normalizing folder structure finished')


def install_mods():
    print('installing mods...')
    copy_file(CC_FILE_NAME, str(MINECRAFT_MODS_PATH))
    copy_file(NEI_FILE_NAME, str(MINECRAFT_MODS_PATH))
    copy_file(JM_FILE_NAME, str(MINECRAFT_MODS_PATH))
    copy_file(TFC_FILE_NAME, str(MINECRAFT_MODS_PATH))
    copy_file(TEXTURE_PACK_NAME, str(MINECRAFT_RESOURCEPACKS_PATH))
    copy_file(TEXTURE_PACK_ADDON_NAME, str(MINECRAFT_RESOURCEPACKS_PATH))
    print('installing mods finished')


def update_configs():
    if not MINECRAFT_OPTIONS_PATH.exists():
        print('options.txt does not exists. Please launch Minecraft first.')
        sys.exit()

    optionsLines = []

    resourcePacksStr = '['
    resourcePacksStrIndex = 0
    for rpName in resourcepack_names:
        resourcePacksStr += '"[{}]"'.format(rpName)
        if (resourcePacksStrIndex < len(resourcepack_names - 1)):
            resourcePacksStr += ','
    resourcePacksStr += ']'

    langStr = preffered_lang

    args = ['"SphaxTFC.128x.zip"', '"SphaxPureBDcraft64xMC17.zip"']
    print(args)

    with open(str(MINECRAFT_OPTIONS_PATH), 'r') as optionsFile:
        for line in optionsFile:
            paramArr = line.split(':')
            paramStr = ''

            paramName = paramArr[0].strip()
            paramValue = paramArr[1].strip()

            if paramName == 'lang':
                paramValue = langStr
            if paramName == 'resourcePacks':
                paramValue = resourcePacksStr

            paramStr = '{}:{}\n'.format(paramName, paramValue)

            optionsLines.append(paramStr)

    with open(str(MINECRAFT_OPTIONS_PATH), 'w') as optionsFile:
        for optionLine in optionsLines:
            optionsFile.write(optionLine)


def download_resourcepacks():
    with open('pack-settings.json', 'rb') as psf:
        psJSON = json.load(psf)

        for rp in psJSON['resourcepacks']:
            rpName = rp['name']
            rpURL = rp['url']
            resourcepack_names.append(rpName)
            download_file_raw(rpURL, rpName)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rp', help='download resourcepacks')
    args = parser.parse_args()

    if args.rp:
        download_resourcepacks()
    else:
        download_mods()
        normalize_folder_structure()
        install_mods()

    update_configs()
