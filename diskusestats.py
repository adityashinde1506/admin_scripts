#!/usr/bin/env python3
import subprocess
import json

def unique_entries(dirs):
    unique=list()
    for i in range(len(dirs)-1):
        if dirs[i] not in dirs[i+1]:
            unique.append(dirs[i])
            #print(dirs[i])
    return unique

def __print_table_entry(table_entry):
    for data in table_entry:
        print(data)

def __parse_individual_columns(instance):
    if len(instance)>7:
        return {"type":instance[0].decode()[0],"permissions":instance[0].decode(),"size":instance[4].decode(),"owner":instance[2].decode(),"group":instance[3].decode(),"nodename":instance[8].decode()}
    else:
        return {}

def __parse_columns(data):
    return list(map(lambda x:__parse_individual_columns(x.split()),data))

def __make_table_entry(entry):
    if len(entry)>2:
        return {"path":entry[0].decode(),"subdirs":__parse_columns(entry[2:])}
    else:
        return {"path":entry[0].decode(),"subdirs":{}}

def get_all_directories():
    all_dirs=subprocess.Popen(['ls','-lRt','/home/adityas'],stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
    entries=all_dirs.split(b"\n\n")
    fs_table=list(map(lambda entry:entry.split(b"\n"),entries))
    #__print_table_entry(fs_table[0])
    data=list(map(__make_table_entry,fs_table))
    data=json.dumps(data,indent=4)
    return data

def main():
    record=get_all_directories()

main()
