from pathlib import Path
import logging
import re
import numpy
from functools import reduce

logging.basicConfig(level=logging.DEBUG)
logger=logging.getLogger(__name__)
main_path=Path("/home/adityas/Projects/Experiment_Results")

def path_visitor(path,names,found):
    '''
        Recursively traverses directory and looks for given files.
    '''
    for name in names:
        if name==path.parts[-1]:
            found.append(str(path))
    if not path.is_dir():
        return
    for _path in path.iterdir():
        path_visitor(_path,names,found)

def get_data_files(entry_dir,filenames):
    '''
        Recursively traverses entry_dir to find all filenames.
        Returns full path of found filenames.
    '''
#    assert type(entry_dir)==str, "Entry directory should be a string."
#    entry_dir=Path(entry_dir)
    logger.info(f"Looking for {filenames} in {entry_dir}")
    found=[]
    path_visitor(entry_dir,filenames,found)
#    logger.info(f"Found {len(found)} data files under {str(entry_dir)}.")
    return found

def get_array_from_file(filename):
    logger.debug(f"Reading {filename}")

    fd=open(filename)

    array=map(lambda x:list(map(float,re.split(r";|,",x.strip("\n")[1:-1]))),fd.readlines())
    
    fd.close()
    return numpy.array(list(array),dtype=numpy.float32)[:300]

def store(dest,array):
    logger.debug(f"Making {dest}")
    dest.touch()
    with dest.open(mode='wb') as _file:
        numpy.save(_file,array)
    logger.debug(f"Saved to {dest}")

def make_dataset(files,write_to):
    logger.info(f"Working on {files[0].split('/')[-3]}")
    arrays=numpy.concatenate(tuple(list(map(get_array_from_file,files))),axis=0)
    store(write_to/"data.npz",arrays)
    logger.info("Done")

def main():
    logger.info(f"Starting...")
    agg_files=get_data_files(main_path/"Aggregation",["ztomatrix.txt"])
    make_dataset(sorted(agg_files),Path("/home/adityas/Projects/SensorAnalysis/data/Agg"))
    broad_files=get_data_files(main_path/"Broadcast",["ztomatrix.txt"])
    make_dataset(sorted(broad_files),Path("/home/adityas/Projects/SensorAnalysis/data/Broad"))
    coll_files=get_data_files(main_path/"Collection",["ztomatrix.txt"])
    make_dataset(sorted(coll_files),Path("/home/adityas/Projects/SensorAnalysis/data/Coll"))
    con_files=get_data_files(main_path/"Consensus",["ztomatrix.txt"])
    make_dataset(sorted(con_files),Path("/home/adityas/Projects/SensorAnalysis/data/Con"))
    dgd_files=get_data_files(main_path/"DGD",["ztomatrix.txt"])   
    make_dataset(sorted(dgd_files),Path("/home/adityas/Projects/SensorAnalysis/data/DGD"))
    nothing_files=get_data_files(main_path/"Donothing",["ztomatrix.txt"])   
    make_dataset(sorted(nothing_files),Path("/home/adityas/Projects/SensorAnalysis/data/Donothing"))

if __name__=="__main__":
    main()


