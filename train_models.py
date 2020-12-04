import sys
import logging
from data_loader import *
from utils import *
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.metrics import accuracy_score,classification_report
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans

import argparse

logger=logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,filename="first_run.log")

argparser=argparse.ArgumentParser()

# Get data of individual tasks.

def create_sequence_dataset():
    
    agg_labels=numpy.ones(agg.shape[0])*0.0
    coll_labels=numpy.ones(coll.shape[0])*1.0
    con_labels=numpy.ones(con.shape[0])*2.0
    broad_labels=numpy.ones(broad.shape[0])*3.0
    dgd_labels=numpy.ones(dgd.shape[0])*4.0

    X=numpy.concatenate((agg,coll,con,broad,dgd),axis=0)
    y=numpy.concatenate((agg_labels,coll_labels,con_labels,broad_labels,dgd_labels),axis=0)

    return X,y

#X,y=create_sequence_dataset()

def create_flat_dataset(time_steps=75):

    agg,coll,con,broad,dgd,no=get_preprocessed_data()
    logger.info("Fetched task data.")
    del no
    # Transform data into fixed time steps per sample.
    logger.info(f"Dividing data into timesteps.")
    agg=create_stacks(agg,time_steps)
    logger.debug(f"Agg data transformed to dim {agg.shape}")
    coll=create_stacks(coll,time_steps)
    logger.debug(f"Coll data transformed to dim {coll.shape}")
    con=create_stacks(con,time_steps)
    logger.debug(f"Con data transformed to dim {con.shape}")
    broad=create_stacks(broad,time_steps)
    logger.debug(f"Broad data transformed to dim {broad.shape}")
    dgd=create_stacks(dgd,time_steps)
    logger.debug(f"Dgd data transformed to dim {dgd.shape}")

    window=numpy.ones(11)[numpy.newaxis,:,numpy.newaxis]/11
    agg=moving_avg_filter(agg,window)
    coll=moving_avg_filter(coll,window)
    con=moving_avg_filter(con,window)
    broad=moving_avg_filter(broad,window)
    dgd=moving_avg_filter(dgd,window)


# Flatten the dataset for shallow classifiers
    logger.info(f"Flattening datasets.")
    agg=agg.reshape((agg.shape[0],-1))
    logger.debug(f"Agg dataset flattened to dimensions {agg.shape}")
    coll=coll.reshape((coll.shape[0],-1))
    logger.debug(f"Coll dataset flattened to dimensions {coll.shape}")
    con=con.reshape((con.shape[0],-1))
    logger.debug(f"Con dataset flattened to dimensions {con.shape}")
    broad=broad.reshape((broad.shape[0],-1))
    logger.debug(f"Broad dataset flattened to dimensions {broad.shape}")
    dgd=dgd.reshape((dgd.shape[0],-1))
    logger.debug(f"DGD dataset flattened to dimensions {dgd.shape}")

# Attach labels to datasets
    logger.info(f"Creating labels.")

# Create labels for Agg
    agg_labels=numpy.ones((agg.shape[0],1))*0
    agg_dataset=numpy.hstack((agg,agg_labels))
    logger.info(f"Agg has label {agg_labels[0][0]}")

# Create labels for Coll
    coll_labels=numpy.ones((coll.shape[0],1))*1
    coll_dataset=numpy.hstack((coll,coll_labels))
    logger.info(f"Coll has label {coll_labels[0][0]}")

# Create labels for Con
    con_labels=numpy.ones((con.shape[0],1))*2
    con_dataset=numpy.hstack((con,con_labels))
    logger.info(f"Con has label {con_labels[0][0]}")

# Create labels for Broad
    broad_labels=numpy.ones((broad.shape[0],1))*3
    broad_dataset=numpy.hstack((broad,broad_labels))
    logger.info(f"Broad has label {broad_labels[0][0]}")

# Create labels for DGD
    dgd_labels=numpy.ones((dgd.shape[0],1))*4
    dgd_dataset=numpy.hstack((dgd,dgd_labels))
    logger.info(f"DGD has label {dgd_labels[0][0]}")

# Combine the dataset.
    logger.info("Combining all tasks into one dataset.")
    dataset=numpy.concatenate((agg_dataset,coll_dataset,con_dataset,broad_dataset,dgd_dataset),axis=0)
    numpy.random.shuffle(dataset)
    logger.info(f"Dataset created of size {dataset.shape}")
    X,y=tuple(numpy.hsplit(dataset,[dataset.shape[1]-1]))
    logger.info(f"X is of size {X.shape}")
    logger.info(f"y is of size {y.shape}")

    return X,y

# Perform the train-test split on the dataset.


sgd_classifier=SGDClassifier(loss='hinge',penalty='elasticnet',verbose=0,max_iter=1000,n_jobs=5)


rf_classifier=RandomForestClassifier(n_estimators=10,verbose=0,max_depth=20)
dt_classifier=DecisionTreeClassifier(random_state=42)
km_classifier=KMeans(n_clusters=5,n_init=5,max_iter=1000)

classifiers=[(rf_classifier,"RandomForest"),(dt_classifier,"DecisionTree"),(km_classifier,"KMeans")]

times=[5,10,15,30,50,75,100,150,300]

for _classifier in classifiers:
    scores=[]
    classifier,name=_classifier
    for time in times:
        X,y=create_flat_dataset(time)
        logger.info(f"Training {name} for {time} time_steps.")
        X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,shuffle=True)
        classifier.fit(X_train,y_train.squeeze())
        scores.append(classifier.score(X_test,y_test))
    logger.info(f"{name} done performance: {scores}")
    fig=plotter.figure()
    plotter.plot(times,scores)
    fig.suptitle(name,font_size=20)
    fig.savefig(name+".png")
    logger.info(f"Figure saved for {name}")

"""
with open('train_X.npz','wb') as f:
    numpy.save(f,X_train)

with open('test_X.npz','wb') as f:
    numpy.save(f,X_test)

with open('train_y.npz','wb') as f:
    numpy.save(f,y_train)

with open('test_y.npz','wb') as f:
    numpy.save(f,y_test)
"""
