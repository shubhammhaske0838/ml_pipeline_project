import os, sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation

@dataclass
class DataIngestionConfig:
    train_data_path = os.path.join('artifacts/data_ingestion','train.csv')
    test_data_path = os.path.join('artifacts/data_ingestion','test.csv')
    raw_data_path = os.path.join('artifacts/data_ingestion','raw.csv')

class DataIngestion:

    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):

        logging.info("Data Ingestion Started")

        try:

            logging.info("Data reading by using pandas from local system")

            data = pd.read_csv(r'dataset\income_cleandata.csv')

            logging.info('Data read sucessfully')

            os.makedirs(os.path.dirname(self.data_ingestion_config.raw_data_path), exist_ok= True)

            data.to_csv(self.data_ingestion_config.raw_data_path, index = False, header = True)

            logging.info('Data splitted into the train and test')

            train_set, test_set = train_test_split(data, test_size = 0.30, random_state = 42)

            train_set.to_csv(self.data_ingestion_config.train_data_path,index = False, header = True)
            test_set.to_csv(self.data_ingestion_config.test_data_path,index = False, header = True)

            logging.info('Data Ingestion Completed')

            return(
                self.data_ingestion_config.train_data_path,
                self.data_ingestion_config.test_data_path
            )
        
        except Exception as e:
            logging.info("Erro occured in data ingestion stage")
            raise CustomException(e,sys)
        

if __name__ == '__main__':
    obj = DataIngestion()
    train_data_path, test_data_path = obj.initiate_data_ingestion()

    data_transformer_obj = DataTransformation()
    data_transformer_obj.initiate_date_transformation(train_data_path,test_data_path)