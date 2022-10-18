#!/usr/bin/python3

'''
This program is wriiten to automatically clean the memory of the RPi so that it does not fill up
It will remove data that is older than 60 days than the current time from the data_backup and data_pad directories. The datatext.txt file will need to be cleared mannualy.
'''

import shutil
import glob
import datetime
import os

print((datetime.datetime.now()).strftime("%Y-%m-%d__%H_%M"))
#Get the amount of free space in the filesystem
total, used, free = shutil.disk_usage('/home/pi/data_backup')
freeGB = free/1024/1024/1024
#freeGB = 1
print(str(freeGB) + " Gb of Free Space")
#if less than 2GB do a clean up
if (freeGB<7.321):
    print("Less than 2Gb removing files to ensure 2Gb of space")
    #Aquire all the files in the data_backup and data_pad directory and sort they alphabetically
    #files = sorted(glob.glob("dummy/*.txt"))
    #files2 = sorted(glob.glob("dummypad/*.txt"))
    files = glob.glob("/home/pi/data_backup/*.txt")
    files2 = glob.glob("/home/pi/data_pad/*.txt")
    #Get current time
    now = datetime.datetime.now()
    # Loop over each file and strip path and .txt, check the filename for datetime of creation
    if len(files)>= len(files2):
        num = len(files)
    else:
        num = len(files2)
    for i in range(num):
        # remove oldest backup file
        if os.path.isfile(files[i]):
            print("Removing:" + files[i])
            os.remove(files[i])
            #freeGB = freeGB +0.5
        else:    ## Show an error ##
            print("Error: file not found:" + files[i])
        total, used, free = shutil.disk_usage('/home/pi/data_backup')
        freeGB = free/1024/1024/1024
        if freeGB>7.321:
            break
        
        # remove oldest padfile
        if os.path.isfile(files2[i]):
            print("Removing:" + files2[i])
            os.remove(files2[i])
            #freeGB = freeGB +0.5
        else:    ## Show an error ##
            print("Error: file not found:" + files2[i])
        total, used, free = shutil.disk_usage('/home/pi/data_backup')
        freeGB = free/1024/1024/1024
        if freeGB>7.321:
            break
quit()

