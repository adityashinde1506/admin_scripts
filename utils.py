import numpy
import scipy.signal

def create_stacks(data,time_steps=50):
    '''
        Transform (time,sensors) to (batch,time_steps,sensors)
    '''
    assert 60000%time_steps==0, " Param time_steps have to a factor of 60000."
#    print(data.shape)
    data=numpy.stack(numpy.split(data,list(range(0,60000,time_steps)[1:])),axis=2)
#    print(data.shape)
    data=numpy.transpose(data,[2,0,1])
    return data


def remove_outliers(array):
    '''
        clips data points lying above or below Q+1.5 IQR.
    '''
    data=array.ravel()
    lower_q,upper_q=tuple(numpy.percentile(data,[25,75]))
    iqr=upper_q-lower_q 
    return numpy.clip(array,(lower_q-1.5*iqr),(upper_q-1.5*iqr))

def outliers_report(data,dataset_name="unnamed"):
    data=data.ravel()
    lower_q,upper_q=tuple(numpy.percentile(data,[25,75]))
    iqr=upper_q-lower_q
    print(f"Task {dataset_name}: Upper quartile is {upper_q}. Lower quartile is {lower_q}. IQR is {iqr}")
    num_outliers=data[(data < (lower_q-1.5*iqr)) | (data > (upper_q+1.5*iqr))].shape[0]
    print(f"Task {dataset_name}: Out of {data.shape[0]} samples, {num_outliers} are outliers i.e. {(num_outliers/data.shape[0])*100} % data is outliers.")

def moving_avg_filter(data,window):
    return scipy.signal.convolve(data,window)
