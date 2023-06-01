import os, sys
from src.logger import logging
from src.exception import CustomException
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
import warnings
warnings.filterwarnings('ignore')

def save_object (filepath,obj):

    dir_obj = os.path.dirname(filepath)

    os.makedirs(dir_obj, exist_ok= True)

    with open(filepath,'wb')as file_obj:
        pickle.dump(obj, file_obj)


def load_object(filepath):
    try:
        with open(filepath, 'rb') as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e,sys)

def evaluate_model(x_train, y_train, x_test, y_test,models,params):

    try:

        report = {}

        for i in range (len(list(models))):        

            model = list(models.values())[i]
            parameters = params[list(models.keys())[i]]

            GS = GridSearchCV(model, parameters, cv = 5)
            GS.fit(x_train,y_train)

            model.set_params(**GS.best_params_)
            model.fit(x_train,y_train)

            #make prediction on test data

            y_pred_test = model.predict(x_test)
            model_accuracy_score = accuracy_score(y_test,y_pred_test)

            report[list(models.keys())[i]] = model_accuracy_score

            print(f'model name:[{list(models.keys())[i]}] accuracy:[{model_accuracy_score}]')            

        return report
    
    except Exception as e:
        raise CustomException(e,sys)