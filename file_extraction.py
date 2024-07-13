import os 
from datetime import datetime as dt
from validate import validate_file 
def file_checker():
    date = dt.today().strftime('%Y%m%d')
    os.chdir(f'D:\\Python\\Project\\incoming_files\\{date}')
    file_list =[file for file in  os.listdir() if file.endswith('.csv')]
    total = len(file_list)
    if total ==0:
        print('no file found in today''s folder')
    print(file_list)
    failed =0 
    passed =0

    for file in file_list:
        passed, failed = validate_file(file,passed,failed)


    print('no of files passed: ',passed)
    print('no of files failed: ',failed)