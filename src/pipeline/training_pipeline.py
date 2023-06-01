import os, sys
from src.logger import logging
from src.exception import CustomException
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from dataclasses import dataclass

if __name__ == '__main__':
    data_ingestion_obj = DataIngestion()
    train_data_path, test_data_path = data_ingestion_obj.initiate_data_ingestion()
    data_transformation_obj = DataTransformation()
    train_arr, test_arr, _ = data_transformation_obj.initiate_date_transformation(train_data_path, test_data_path)
    model_training_obj = ModelTrainer()
    model_training_obj.initiate_model_trainer(train_arr,test_arr)

    # src\pipeline\training_pipeline.py