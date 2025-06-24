from datetime import datetime
import sys
from lib.logger import loggingMessage
class FutureDateException(Exception):
    pass
def futureDateException(given_date_star):
    loggingMessage.logger.info(f"Checking the Date Formate and Date for Data gathering.")
    #define the date format
    date_format = "%m/%d/%Y"
    try:                         
        #parse the date string into a date time object
        given_date = datetime.strptime(given_date_star,date_format)
        #get the today's date
        today_date = datetime.today()
        #compare the dates
        if given_date > today_date:
            print(f"Error: The Given Date {given_date_star} is grater than today's Date {today_date.strftime('%m/%d/%Y')}. You Can Generate the OBO Report for Same Date or Privious Date's Only.")
            loggingMessage.logger.info(f"Error: The Given Date {given_date_star} is grater than today's Date {today_date.strftime('%m/%d/%Y')}.")
            sys.exit()
        else:
            # print("############## OBO Data Gathering  #######################")
            # print(f"******OBO Data Gathering Started for the  {given_date_star} *******")
            loggingMessage.logger.info(f"The given Date {given_date_star} is not grater than Today date {today_date.strftime('%m/%d/%Y')}.")
            return given_date
        
    except FutureDateException as e:
        print(e)
        loggingMessage.logger.info(e)
        sys.exit()
    except ValueError:
        print(f"Invalid Date {given_date_star} Format Please enter the Date in MM/DD/YY format.")
        loggingMessage.logger.info(f"Invalid Date Format {given_date_star}. Please enter the Date in format MM/DD/YY format.")
        sys.exit()
        