import os 
import shutil
from datetime import datetime

def temp_cleaner(folder='C:/Windows/Temp', out_file=False):
    if out_file:
        dateandtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dateandtime = datetime.now().strftime('%Y-%m-%d-%H-%m-%S')
        outfile = open(dateandtime + '_Cleaning.txt', 'w')
        outfile.write('Cleaning at {}'.format(dateandtime) + '\n' + '\n')   
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        indexNo = file_path.find('\\')
        itemName = file_path[indexNo+1:]
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                if out_file:
                    outfile.write( '%s file deleted' % itemName )
                deleteFileCount = deleteFileCount + 1

            elif os.path.isdir(file_path):
                if file_path.__contains__('chocolatey'):  continue
                shutil.rmtree(file_path)
                if out_file:
                    outfile.write( '%s folder deleted' % itemName )
                deleteFolderCount = deleteFolderCount + 1

        except Exception as ex:
            if out_file:
                outfile.write('\n')
                outfile.write('Access Denied: %s' % itemName )
                outfile.write('\n Error Details: {}'.format(ex))
    return 'Removed all Temp Files'
temp_cleaner('C:/Windows/Temp', True)