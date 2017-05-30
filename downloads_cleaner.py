#!/usr/bin/env python3

import os
import datetime
import logging
import time
import shutil

LOGGING_FILE="/home/adityas/Logs/clearer.log"

logging.basicConfig(format="%(asctime)s : %(levelname)s - %(message)s",level=logging.DEBUG,filename=LOGGING_FILE)

WATCH_DIRS=["/home/adityas/Downloads/"]
STAGING="/home/adityas/Trash/"

def get_filenames():
    all_files=list()
    for _dir in WATCH_DIRS:
        files=os.listdir(_dir)
        files=list(map(lambda x:_dir+"/"+x,files))
        all_files.extend(files)
    return all_files

def get_stats(filenames):
    return list(map(lambda x:os.stat(x).st_mtime,filenames))

def print_files(filenames,stats,deltas):
    for i in range(len(filenames)):
        print("%50s file last accessed %15s delta %20s."%(filenames[i],str(time.ctime(stats[i])),deltas[i]))

def compute_delta(time_stats):
    now=datetime.datetime.now()
    deltas=map(lambda x:(now-x).days,map(datetime.datetime.fromtimestamp,time_stats))
    return list(deltas)
    
def queue_for_deletion(files,deltas,threshold=60):
    file_stats=zip(files,deltas)
    def is_old(file_stat):
        if file_stat[1]>threshold:
            return True
        else:
            return False
    return filter(is_old,file_stats)

def move_to_staging(files):
    for _file in files:
        logging.info("Moving %s to staging area. File not used since %s days."%(_file))
        shutil.move(_file[0],STAGING)

def main():
    logging.info("Starting cleaner.")
    for _dir in WATCH_DIRS:
        logging.info("Cleaning %s"%_dir)
    files=get_filenames()
    stats=get_stats(files)
    deltas=compute_delta(stats)
    old_files=list(queue_for_deletion(files,deltas))
    if len(old_files) == 0:
        logging.info("No files to be deleted.")
    else:
        move_to_staging(old_files)
    logging.info("Stopping cleaner.")

main()
