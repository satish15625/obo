'''
Auther Name : satish Kumar
Created Date :20/07/2024
File name : logger.py
Description : File is used for loging mesaage
Update Date : 22/07/2024

'''
import logging
import os
from datetime import datetime

class loggingMessage():
    today = datetime.now().strftime("%m%d%Y")
    if not os.path.exists(".//logs//"):
        os.makedirs(".//logs//")
    #Create and configure logger
    filename =f".//logs//dailyDrilling_{today}.log"
    logging.basicConfig(filename=filename,
                        format='%(asctime)s %(message)s',
                        filemode='w')

    # Creating an object
    logger = logging.getLogger()
    # Setting the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)