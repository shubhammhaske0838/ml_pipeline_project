import os, sys
from src.logger import logging

def error_message_detailed(error, error_detailed:sys):
    _,_,exc_tb = error_detailed.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_no = exc_tb.tb_lineno

    error_message = f"Error occured in python script name [{file_name}] line number [{line_no}] error message [{error}]"

    return error_message

class CustomException(Exception):

    def __init__(self,error_message,error_detailed):

        super().__init__(error_message)
        self.error_message = error_message_detailed(error_message,error_detailed=error_detailed)

    def __str__(self):
        return self.error_message
    
if __name__ == '__main__':
    try:
        logging.info("We are checking custom exception code")
        a = 1/0

    except Exception as e:
        raise CustomException(e,sys)