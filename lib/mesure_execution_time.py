import time
def measure_execution_time(fun):
    def wrapper(*args,**kwargs):
        start_time= time.time()
        result = fun(*args,**kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        total_time_minuts = total_time / 60
        print(f"Total Execution Time : {total_time_minuts :.4f} Minutes.")
        return result
    return wrapper



