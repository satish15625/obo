"""
File Name tracjerSheetUpdate.py
Created By : Satish Kumar
Created Date : 16/09/2024
Modified Date : 16/09/2024
File Description : This file created for update the OBO Tracker Sheet Data update.
"""
import pandas as pd

class oboUpdaterTrackerSheet:
    def __init__(self,tracker_sheet_path):

        """ Initialize with the Excel file path"""
        self.tracker_sheet_path=tracker_sheet_path
        self.df_tracker = None
    
    def load_data(self):
        """
        Load the Excel into a DataFrame
        """
        self.df_tracker=pd.read_excel(self.tracker_sheet_path,sheet_name='Sheet1')
        print(f"Tracker Sheet Data Loaded Successfully.")

    def update_column_based_on_api(self,condition_col,condition_values,target_columns_with_values):
        print("API 14 - Checking for matching Conditions...")
        """
        Update row in target columns where condition_col (API 14) matched condition_values
        :param condition_col: Columnto match condition (eg. "API 14")
        param : condition_values : List of values to match
        param : target cols : List of columns to update
        param : new_values: list of new values corresponding to target columns

        """
        print(f"=========================API 14 =============================")
        for i, condition_value in enumerate(condition_values):
            #check if the condition_value exist in the tracker sheet and updat corrsponding row
            if condition_value in self.df_tracker[condition_col].values:
                for target_col,values in target_columns_with_values.items():
                    
                    try:
                        self.df_tracker.loc[self.df_tracker[condition_col] == condition_value,target_col]=values[i]

                        
                        print(f"Updated row where {condition_col} is {condition_value} for {target_col} : {values[i]}")
                    except IndexError:
                        print(f"No Matching Value for {target_col} at index {i}; skiping or filling as needed.")
        #print(self.df_tracker)


    
    def save_data(self,output_path):
        """
        Save the Updated Data Freame in the Excel File
        """
        self.df_tracker.to_excel(output_path,index=False)
        print(f"Tracker Sheet Updated Successfully {output_path}.")



#