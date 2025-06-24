import time
import os
def exportDataPath(download_path,timeout=35):
    seconds =0
    while not any([filename.endswith(".crdownload") for filename in os.listdir(download_path)]):
        time.sleep(2)
        seconds += 1
        if seconds > timeout:
            break
    
    return download_path