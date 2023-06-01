import os, sys
import pandas as pd
import numpy as np
from src.exception import CustomException
from src.logger import logging
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from dataclasses import dataclass
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_path = os.path.join('artifacts/data_transformation','preprocessor.pkl')

class DataTransformation:

    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformation_obj(self):

        try:

            logging.info(" Data Transformation Started")

            numerical_features = ['age', 'workclass',  'education_num', 'marital_status',
                'occupation', 'relationship', 'race', 'sex', 'capital_gain',
                'capital_loss', 'hours_per_week', 'native_country']
            
            num_pipeline = Pipeline(steps=[
                ('imputer',SimpleImputer(strategy='median')),
                ('scaler',StandardScaler())
            ])

            preprocessor = ColumnTransformer([
                ('num_pipeline',num_pipeline,numerical_features)
            ])

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def remove_outliers_iqr(self, col, df):

        try:

            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)

            IQR = Q3 - Q1

            upper_limit = Q3 + (1.5 * IQR)
            lower_limit = Q1 - (1.5 * IQR) 

            df.loc[(df[col]>upper_limit), col] = upper_limit
            df.loc[(df[col]<lower_limit), col] = lower_limit

            return df

        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_date_transformation(self, train_path, test_path):

        try:
            
            preprocessor_obj = self.get_data_transformation_obj()

            numerical_features = ['age', 'workclass',  'education_num', 'marital_status',
                'occupation', 'relationship', 'race', 'sex', 'capital_gain',
                'capital_loss', 'hours_per_week', 'native_country']

            train_data = pd.read_csv(train_path)
            test_data = pd.read_csv(test_path)

            for col in numerical_features:
                self.remove_outliers_iqr(col = col, df = train_data)

            logging.info("Outliers capped on our train data")

            for col in numerical_features:
                self.remove_outliers_iqr(col = col, df = test_data)

            logging.info("Outliers capped on our test data")

            target_col = 'income'
            drop_col = [target_col]

            logging.info("Splitting train data into dependent (y) and independent features (x)")

            input_feature_train_data  = train_data.drop(drop_col, axis = 1 )
            traget_feature_train_data  = train_data[drop_col]

            logging.info("Splitting test data into dependent (y) and independent features (x)")

            input_feature_test_data  = test_data.drop(drop_col, axis = 1 )
            traget_feature_test_data  = test_data[drop_col]

            logging.info("Apply transformation on train and test data")

            input_train_data_arr = preprocessor_obj.fit_transform(input_feature_train_data)
            input_test_data_arr = preprocessor_obj.transform(input_feature_test_data)

            logging.info("After transformation Concatenate independent train and test data with dependent data")

            train_arr = np.c_[input_train_data_arr,np.array(traget_feature_train_data)]
            test_arr = np.c_[input_test_data_arr,np.array(traget_feature_test_data)]

            save_object(filepath = self.data_transformation_config.preprocessor_obj_path,
                        obj = preprocessor_obj)
            
            logging.info("Data Transformation Completed")

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_path
            )
        
        except Exception as e:
            raise CustomException(e,sys)




