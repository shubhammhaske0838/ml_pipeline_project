import os
import sys
import logging
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%d-%m-%y_%H-%M')}.log"

LOG_DIR = os.path.join(os.getcwd(),'logs')

os.makedirs(LOG_DIR, exist_ok = True)

LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

logging.basicConfig(
    handlers=[logging.FileHandler(LOG_FILE_PATH, mode='w')],
    format = "[%(asctime)s] %(lineno)s %(name)s - %(levelname)s %(message)s",
    level = logging.INFO
)

if __name__ == '__main__':
    logging.info('Logging Started')