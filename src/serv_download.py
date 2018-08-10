from util import download_file
from util import exists

FILE_NAME = 'forge-1.7.10-10.13.4.1558-1.7.10-installer.jar'
if not exists(FILE_NAME):
    print('downloading server...')
    download_file('https://files.minecraftforge.net/maven/net/minecraftforge/forge/1.7.10-10.13.4.1558-1.7.10/forge-1.7.10-10.13.4.1558-1.7.10-installer.jar', FILE_NAME)
    print('downloading server finished')