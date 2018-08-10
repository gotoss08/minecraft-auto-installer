import os
import time

import shutil
from pathlib import Path

import requests
import gdrive

from pySmartDL import SmartDL

TFC_FILE_ID = '0B39mDZWrwjROR3V2REVkSVdiRzQ'
TFC_FILE_NAME = '[1.7.10]TerraFirmaCraft-0.79.29.922.jar'

NEI_FILE_URL = 'https://minecraft.curseforge.com/projects/notenoughitems/files/2302312/download'
NEI_FILE_NAME = 'NotEnoughItems-1.7.10-1.0.5.120-universal.jar'

CC_FILE_URL = 'https://minecraft.curseforge.com/projects/codechickencore/files/2262089/download'
CC_FILE_NAME = 'CodeChickenCore-1.7.10-1.0.7.47-universal.jar'

JM_FILE_URL = 'https://minecraft.curseforge.com/projects/journeymap/files/2367915/download'
JM_FILE_NAME = 'journeymap-1.7.10-5.1.4p2.jar'

TEXTURE_PACK_NAME = 'SphaxPureBDcraft64xMC17.zip'
TEXTURE_PACK_URL = 'http://www.creeperrepo.net/direct/sphax/028a58c7771f79e15cd878a95df52837/Sphax%20PureBDcraft%20%2064x%20MC17.zip'

TEXTURE_PACK_ADDON_URL = 'https://github.com/KillAshley/SphaxTFC/releases/download/0.1/SphaxTFC.128x.zip'
TEXTURE_PACK_ADDON_NAME = 'SphaxTFC.128x.zip'

def exists(path):
    return os.path.exists(path)

def download_file_raw(url, filename, destPath='.'):
    with (open(filename, 'wb')) as downloadedFile:
        downloadedFile.write(requests.get(url).content)
        return downloadedFile

def download_file(url, destPath='.'):
    head = requests.head(url, allow_redirects=False)
    final_url = head.url

    if head.status_code != 200:
        final_url = requests.get(url, allow_redirects=False).headers['location']
        print('final url created from location')

    filename = os.path.basename(final_url)

    if not exists(os.path.join(os.path.abspath(destPath), filename)):
        print('Downloading "{}" from "{}" ...'.format(filename, url))
        fileDownloadTimeStart = time.time()
        with (open(filename, 'wb')) as downloadedFile:
            downloadedFile.write(requests.get(url).content)
            print('Finished downloading "{}" in {:,.2} seconds'.format(filename, time.time() - fileDownloadTimeStart))
            return downloadedFile

def remove_folder(path):
    print('removing folder "{}"'.format(path))
    if os.path.exists(path):
        shutil.rmtree(path)

def create_folder(path):
    print('creating folder "{}"'.format(path))
    if not os.path.exists(path):
        os.makedirs(path)

def move_file(file, dest):
    print('moving "{}" to "{}"'.format(file, dest))
    shutil.move(file, dest)

def copy_file(file, dest):
    print('copying "{}" to "{}"'.format(file, dest))
    shutil.copyfile(file, dest + '/' + file)