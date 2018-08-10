from util import *
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

SERVER_MODS_PATH = os.path.join('server', 'mods')
create_folder(SERVER_MODS_PATH)

print('installing mods to ' + SERVER_MODS_PATH + ' ...')
copy_file(CC_FILE_NAME, str(SERVER_MODS_PATH))
copy_file(NEI_FILE_NAME, str(SERVER_MODS_PATH))
copy_file(JM_FILE_NAME, str(SERVER_MODS_PATH))
copy_file(TFC_FILE_NAME, str(SERVER_MODS_PATH))
print('installing mods finished')