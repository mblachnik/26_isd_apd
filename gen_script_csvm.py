import pandas as pd
import numpy as np
from cascade_svm import CascadeSVC
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, StratifiedKFold
import time
import os

from sklearn.metrics import accuracy_score, roc_auc_score, balanced_accuracy_score

folder = "D:\\mblachnik\\datasets\\Datasets\\KeelNormCV"
#'D:\\mblachnik\\datasets\\large'
resFolder = "D:\\mblachnik\\RMResults\\csvm3"
files = [
    "codrnaNorm",
    "covtype",
    "spambase",
    "banana",
    "phoneme",
    "ring",
    "twonorm",
    "coil2000",
    "magic",
    "shuttle2"
]
res = {}
for file in files:
    dName = f"{resFolder}\\{file}"
    if not os.path.isdir(dName):
        os.mkdir(f"{resFolder}\\{file}")
    for i in range(1, 11):
        tr = pd.read_csv(f"{folder}\\{file}\\{file}-10-{i}tra.dat.csv",sep=";")
        te = pd.read_csv(f"{folder}\\{file}\\{file}-10-{i}tst.dat.csv",sep=";")
        cols = [col for col in tr.columns if col not in ["LABEL", "id"]]
        Xtr = tr.loc[:, cols].values
        ytr = tr.loc[:, "LABEL"].values

        Xte = te.loc[:, cols].values
        yte = te.loc[:, "LABEL"].values
        fold_size = 10000#Xtr.shape[0]/10
        model = CascadeSVC(fold_size=fold_size, C=1, gamma=1 / Xtr.shape[1])
        t0 = time.time()
        model.fit(Xtr, ytr)
        t1 = time.time()
        yte_p = model.predict(Xte)
        t2 = time.time()

        res = {"average(ModelOptimizationExecutionTime)": [],
               "average(ModelPredictionTime)": [],
               "average(ACC)": [],
               "average(BACC)": [],
               "standard_deviation(ModelOptimizationExecutionTime)": [],
               "standard_deviation(ModelPredictionTime)": [],
               "standard_deviation(ACC)": [],
               "standard_deviation(BACC)": []}

        res["average(ModelOptimizationExecutionTime)"].append(t1-t0)
        res["average(ModelPredictionTime)"].append(t2-t1)
        res["average(ACC)"].append(accuracy_score(yte, yte_p))
        res["average(BACC)"].append(balanced_accuracy_score(yte, yte_p))
        res["standard_deviation(ModelOptimizationExecutionTime)"].append(0)
        res["standard_deviation(ModelPredictionTime)"].append(0)
        res["standard_deviation(ACC)"].append(0)
        res["standard_deviation(BACC)"].append(0)

        resdf = pd.DataFrame(res)

        resdf.to_csv(f"{resFolder}\\{file}\\{file}-10-{i}tra.dat_CSVM_NonEnsemble.log",index=False,sep=";")

