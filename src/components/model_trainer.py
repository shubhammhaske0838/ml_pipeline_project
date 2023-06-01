import os, sys
import pandas as pd
import numpy as np
from src.exception import CustomException
from src.logger import logging
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from dataclasses import dataclass
from src.utils import save_object
from src.utils import evaluate_model
import warnings
warnings.filterwarnings('ignore')

@dataclass
class ModelTrainerConfig:

    train_model_file_path = os.path.join('artifacts/model_trainer','model.pkl')

class ModelTrainer:

    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self,train_array, test_array):

        try:
            
            x_train, y_train, x_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1],
            )

            models = {
                'Random Forest':RandomForestClassifier(),
                'Decision Tree': DecisionTreeClassifier(),
                'Logistic Regression': LogisticRegression()
            }

            params = {
                    "Random Forest":{
                        "class_weight":["balanced"],
                        'n_estimators': [20, 50, 30],
                        'max_depth': [10, 8, 5],
                        'min_samples_split': [2, 5, 10],
                    },
                    "Decision Tree":{
                        "class_weight":["balanced"],
                        "criterion":['gini',"entropy","log_loss"],
                        "splitter":['best','random'],
                        "max_depth":[3,4,5,6],
                        "min_samples_split":[2,3,4,5],
                        "min_samples_leaf":[1,2,3],
                        "max_features":["auto","sqrt","log2"]
                    },
                    "Logistic Regression":{
                        "class_weight":["balanced"],
                        'penalty': ['l1', 'l2'],
                        'C': [0.001, 0.01, 0.1, 1, 10, 100],
                        'solver': ['liblinear', 'saga']
                    }
                }
            
            model_report : dict = evaluate_model(x_train = x_train, y_train = y_train, x_test = x_test,
                                                y_test = y_test, models = models, params = params)
            
            # To gest best model from our report Dict

            best_model_score = max(sorted(list(model_report.values())))

            best_model_name = list(models.keys())[
                list(model_report.values()).index(best_model_score)]
            
            best_model = models[best_model_name]
            
            print(f"Best Model Found, Model Name is: {best_model_name},Accuracy_Score: {best_model_score}")

            save_object(filepath = self.model_trainer_config.train_model_file_path,
                        obj = best_model)
            
        except Exception as e:
            raise CustomException (e,sys)




        
