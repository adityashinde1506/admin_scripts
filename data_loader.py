from pathlib import Path
from sklearn.preprocessing import MinMaxScaler
import numpy
from utils import *

scaler=MinMaxScaler()

def get_files(task):
    main_path=Path("/home/adityas/Projects/SensorAnalysis/data")
    task_path=main_path/task
    return list(map(str,task_path.iterdir()))

def get_agg_files():
    return get_files("Agg")

def get_no_files():
    return get_files("Donothing")

def get_broad_files():
    return get_files("Broad")

def get_coll_files():
    return get_files("Coll")

def get_con_files():
    return get_files("Con")

def get_dgd_files():
    return get_files("DGD")

def get_data(task):
    path=Path("/home/adityas/Projects/SensorAnalysis/data")
    data_dir=path/task/"data.npz"
    return numpy.clip(numpy.load(data_dir),-1000.0,1000.0)

def get_agg_data():
    return get_data("Agg")

def get_broad_data():
    return get_data("Broad")

def get_coll_data():
    return get_data("Coll")

def get_con_data():
    return get_data("Con")

def get_dgd_data():
    return get_data("DGD")

def get_no_data():
    return get_data("Donothing")

def get_scaler():
    global scaler
    return scaler

def get_preprocessed_data():
    '''
        Scale data between 0 and 1 and return individual arrays.
        Returns a tuple of format
        (agg_data,coll_data,con_data,broad_data,dgd_data)
    '''
    global scaler

    agg=get_agg_data()
    coll=get_coll_data()
    con=get_con_data()
    broad=get_broad_data()
    dgd=get_dgd_data()
    no=get_no_data()

    all_data=numpy.concatenate((agg,coll,con,broad,dgd,no),axis=0)

    all_data=scaler.fit_transform(all_data)
    agg,coll,con,broad,dgd,no=tuple(numpy.split(all_data,list(range(0,all_data.shape[0],60000)[1:]),axis=0))

    return agg,coll,con,broad,dgd,no

def get_unscaled_data():

    agg=get_agg_data()
    coll=get_coll_data()
    con=get_con_data()
    broad=get_broad_data()
    dgd=get_dgd_data()
    no=get_no_data()

    all_data=numpy.concatenate((agg,coll,con,broad,dgd,no),axis=0)
    agg,coll,con,broad,dgd,no=tuple(numpy.split(all_data,list(range(0,all_data.shape[0],60000)[1:]),axis=0))

    return agg,coll,con,broad,dgd,no

