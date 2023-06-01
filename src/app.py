from flask import Flask
from src.logger import logging

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def index():
    logging.info('We are enter into the flask application')
    return 'Hello Good Morning'


if __name__ == '__main__':
    app.run()