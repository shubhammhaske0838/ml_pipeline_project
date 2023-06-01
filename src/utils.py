import os, sys
from src.logger import logging
from src.exception import CustomException
import pickle

def save_object (filepath,obj):

    dir_obj = os.path.dirname(filepath)

    os.makedirs(dir_obj, exist_ok= True)

    with open(filepath,'wb')as file_obj:
        pickle.dump(obj, file_obj)