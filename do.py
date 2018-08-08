from util import *

HOME_PATH = Path.home()
MINECRAFT_PATH = HOME_PATH.joinpath('AppData/Roaming/.minecraft')
MINECRAFT_MODS_PATH = HOME_PATH.joinpath('AppData/Roaming/.minecraft/mods')
MINECRAFT_CONFIG_PATH = HOME_PATH.joinpath('AppData/Roaming/.minecraft/config')
MINECRAFT_LIBS_PATH = HOME_PATH.joinpath('AppData/Roaming/.minecraft/libraries')
MINECRAFT_LOGS_PATH = HOME_PATH.joinpath('AppData/Roaming/.minecraft/logs')
MINECRAFT_RESOURCEPACKS_PATH = HOME_PATH.joinpath('AppData/Roaming/.minecraft/resourcepacks')

def normalize_folder_structure():
    print('normalizing folder structure...')
    remove_folder(str(MINECRAFT_MODS_PATH))
    remove_folder(str(MINECRAFT_CONFIG_PATH))
    # remove_folder(str(MINECRAFT_LIBS_PATH))
    # remove_folder(str(MINECRAFT_LOGS_PATH))
    remove_folder(str(MINECRAFT_RESOURCEPACKS_PATH))

    create_folder(str(MINECRAFT_MODS_PATH))
    create_folder(str(MINECRAFT_RESOURCEPACKS_PATH))
    print('normalizing folder structure finished')

def download_mods():
    print('downloading mods...')
    download_file(CC_FILE_URL, CC_FILE_NAME)
    download_file(NEI_FILE_URL, NEI_FILE_NAME)
    download_file(JM_FILE_URL, JM_FILE_NAME)
    if not exists(TFC_FILE_NAME):
        print('downloading "{}" from google drive'.format(TFC_FILE_NAME))
        gdrive.download_file_from_google_drive(TFC_FILE_ID, TFC_FILE_NAME)
    download_file(TEXTURE_PACK_URL, TEXTURE_PACK_NAME)
    download_file(TEXTURE_PACK_ADDON_URL, TEXTURE_PACK_ADDON_NAME)
    print('downloading mods finished')

def install_mods():
    print('installing mods...')
    copy_file(CC_FILE_NAME, str(MINECRAFT_MODS_PATH))
    copy_file(NEI_FILE_NAME, str(MINECRAFT_MODS_PATH))
    copy_file(JM_FILE_NAME, str(MINECRAFT_MODS_PATH))
    copy_file(TFC_FILE_NAME, str(MINECRAFT_MODS_PATH))
    copy_file(TEXTURE_PACK_NAME, str(MINECRAFT_RESOURCEPACKS_PATH))
    copy_file(TEXTURE_PACK_ADDON_NAME, str(MINECRAFT_RESOURCEPACKS_PATH))
    print('installing mods finished')

download_mods()
normalize_folder_structure()
install_mods()