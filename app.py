#Code runner 
import argparse
import time
import sys
from lib.mesure_execution_time import measure_execution_time


# set the arguments parsing #
@measure_execution_time
def main():
   
    parser = argparse.ArgumentParser(description="Check if a given date is in the Future.")
    parser.add_argument("date",nargs="?",help="The date to check in MM/DD/YY format.")
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    if len(sys.argv) !=3:
        print("Usage Python app.py  <start_date> <end_date>")
        print("Dates must be in MM/DD/YYY format (e.g 11/15/2024 or 11/3/2024 or 1/30/2024)")
        sys.exit(1)

    from lib.pdswdx import PDSWDX
    pdswdx = PDSWDX(start_date,end_date)
    #print(pdswdx.loginPage("https://pdswdx.com/login/","sakum49","Success12@#$"))
    print(pdswdx.loginPage())
    print(pdswdx.clickOnMyWllData())
    time.sleep(8)
    print(pdswdx.exportMyWellData())
    time.sleep(2)
    print(pdswdx.myWellDataFilter())
    pdswdx.itterateWellInfomation()
    #print(measure_execution_time())
    print("Successfully Completd Your PDSWDX Reporting.")

if __name__=="__main__":
    main()


