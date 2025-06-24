from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
import re
import time
import os
import fitz
import shutil
import pandas as pd
from datetime import datetime
import sys
from lib.logger import loggingMessage
from lib.downloadPath import exportDataPath
from lib.futureDateException import futureDateException
import json

class PDSWDX():

    def __init__(self,start_date,end_date):
        loggingMessage.logger.info(f"Initiated the OBO Data Gathering for the Date {start_date} and {end_date} ....")
        ##get the project path 
        self.project_directory = os.path.abspath(os.curdir)
        #First check the Date of report genration 
        futureDateException(start_date)
        ###chrome driver path 
        self.service = Service(executable_path=r'.\\chromedriver\chromedriver.exe')
        options=Options()
        ### get the current date time
        now = datetime.now()
        self.today = now.strftime("%d/%m/%Y")
        self.today_file= datetime.now().strftime("%m%d%Y")
        filename = f"My Well Data - {self.today_file}.csv"
        #start and enddate input 
        self.start_date= start_date
        self.end_date = end_date
        ## load the creds from csv file 
        creds = os.path.join(self.project_directory,"input","input.xlsx")
        operatoer_json_data = os.path.join(self.project_directory,"input","operator_dict.json")
        cred_df = pd.read_excel(creds)
        tracker_sheet_path =cred_df.loc[0,'TRACKER SHEET PATH']
        lan_path =cred_df.loc[0,'LAN PATH']
        self.pdswdx_username =cred_df.loc[0,'pdswdx_username']
        self.pdswdx_password =cred_df.loc[0,'pdswdx_password']
        self.pdxwdx_url =cred_df.loc[0,'pdswdx_url']
        self.region = cred_df.loc[0,'REGIONS']
        if self.region =='bakken':

            self.state_to_include = ['NORTH DAKOTA','Montana']
        if self.region == 'oklahoma':
            self.state_to_include = ['OKLAHOMA']

        ## check the region and meke filter ofr Operator
        
        print("############## OBO Data Gathering  #######################")
        print(f"******OBO Data Gathering Started Between Date Range {start_date} to {end_date} for Region {self.region}*******")

        ##check if tracker sheet already opend 
        try:
            with open(tracker_sheet_path,"a"):
                pass
        except PermissionError:
            print("========================================================================")
            print(f"Tracker Sheet is already Opend Or Someone Using Please Close it First\n File Path is : {tracker_sheet_path}")
            print("=======================================================================")
            sys.exit(1)

        ###load operator Json Data
        with open(operatoer_json_data,'r') as file:
            self.operator_dict = json.load(file)
        self.download_path = lan_path
        self.tracker_sheet_path = tracker_sheet_path
        self.export_path = os.path.join(self.project_directory,"download")
        self.file_path = os.path.join(self.project_directory,"download",filename)
        self.df_tracker = None
        ## check if path exist than remove and daownload
        try:
            if os.path.exists(self.export_path ):
                shutil.rmtree(self.export_path)
        except Exception as e:

            print("----------------------------Error------------------------------------")
            print(f"File Are in Used Please closed File First:  {self.file_path}")
            print("---------------------------------------------------------------------")
            sys.exit(1)

        ##create the pathe for download 
        os.environ['DOWNLOAD_PATH'] = self.export_path
        prefs= {
            'download.default_directory':self.export_path,
            'download.prompt_for_download':False,
            'download.directory_upgrade':True,
            'safebrowsing.enabled':False
            
        }
        options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(service=self.service, options=options)
        self.wait = WebDriverWait(self.driver, 10)

    ### Login the EMASDB Page
    def loginPage(self):
        loggingMessage.logger.info("PDSWDX Web page Loaded..")
        try:
            self.driver.get(self.pdxwdx_url)
            loggingMessage.logger.info(f"PDSWDX WEB URL IS : {self.pdxwdx_url}.")
            ## find the user filed and enter the user name
            self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='ContentPlaceHolder1_FullColumn_RightColumn_RightColumn_tbUsername']"))).send_keys(self.pdswdx_username)
            ##find the password field and Enter the password
            self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='ContentPlaceHolder1_FullColumn_RightColumn_RightColumn_tbPassword']"))).send_keys(self.pdswdx_password)
            # #submit the Login Form
            self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ContentPlaceHolder1_FullColumn_RightColumn_RightColumn_btnSubmit"]'))).send_keys(Keys.RETURN)
            success_element = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ContentPlaceHolder1_FullColumn_nav1_pnlNavigation"]/div/ul/li[1]')))
            if success_element:
                return "Login Successfully !."
        except NoSuchElementException:
            return "Login failed . Could not find expected elements."
        except TimeoutException:
            return "Login Failed Due to TimeOut ."
        except Exception as e:
            return f"An error occured : {str(e)}"
        # finally:
        #     self.driver.quit()

    #click on My well data and lod the well data 
    def clickOnMyWllData(self):
        loggingMessage.logger.info("Clicking on the My Well Data")
        try:
            #self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ContentPlaceHolder1_FullColumn_nav1_pnlNavigation"]/div/ul/li[4]/a'))).click()
            my_Well_Data = self.driver.find_element(By.XPATH,'//*[@id="ContentPlaceHolder1_FullColumn_nav1_pnlNavigation"]/div/ul/li[4]/a')
            my_Well_Data.click()
            loggingMessage.logger.info("Wait for Loading the My well data and Visibale the Export Button :")
            time.sleep(15)
            view_export_button = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="wellDataTable_wrapper"]/div[1]/button')))
            if view_export_button:
                return "Clicked On My Well Data."
        except NoSuchElementException:
            return "My well Data Clicked failed . Could not find expected elements."
        except TimeoutException:
            return "My Well Data Clicked Failed Due to TimeOut ."
        except Exception as e:
            return f"An error occured : {str(e)}"
    

    #export Mywell data and download in folder
    def exportMyWellData(self):
        loggingMessage.logger.info("Exporting the My Well Data")
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="wellDataTable_wrapper"]/div[1]/button'))).click()
            time.sleep(2)
            exportDataPath(self.export_path)
            time.sleep(2)

            if self.file_path:
                loggingMessage.logger.info(f"My Well Data Exported Successfully : {self.file_path}")
                return f"My Well Data Exported Successfully : {self.file_path}"
        except NoSuchElementException:
            loggingMessage.logger.info(f"My well Data export failed . Could not find expected elements.")
            return "Export Button failed . Could not find expected elements."
            
        except TimeoutException:
            return "Export Button Clicked Failed Due to TimeOut ."
        except Exception as e:
            return f"An error occured : {str(e)}"
        
    ### Function for filte the Well Data
    def myWellDataFilter(self):
        try:
            
            loggingMessage.logger.info(f"############# Filterd Well Data for the Date Range {self.start_date} to {self.end_date} and for the Completion Region {self.region} ####################")
            self.filterd_csv_path = f"{self.export_path}/Filtered_WellData_{self.start_date.replace("/","")}.csv"
            df = pd.read_csv(self.file_path)
            df_filtered =df[
            (df['Operator'] != 'XTO Energy')

            ]
            #state_to_include = ['NORTH DAKOTA','Montana']
            #state_to_include = ['OKLAHOMA']
            df_filtered = df_filtered[df_filtered['State'].isin(self.state_to_include)]
            df_filtered['Latest File (Count)'] = pd.to_datetime(df_filtered['Latest File (Count)'].str.split(' ').str[0],format='%m/%d/%Y',errors='coerce')
            filtered_date = self.start_date
            df_filtered = df_filtered[(df_filtered['Latest File (Count)'] >= filtered_date) & (df_filtered['Latest File (Count)'] <= self.end_date)]
            if df_filtered['Well Name'].isna().all():
                print(f"############# Data is Not avalible for the {self.start_date}. Please check the Date Format or try dd/mm/yy if not working with mm//dd/yy ####################")
                loggingMessage.logger.info(f"############# Data is Not avalible for the {self.start_date}. Please check the Date Format or try dd/mm/yy if not working with mm//dd/yy ####################")
                sys.exit()
            else:
                print(f"############# Filterd Well Data for the Date Range {self.start_date} to {self.end_date} and for the Completion Region {self.region} ####################")
                df_filtered.to_csv(self.filterd_csv_path,index=False)
                loggingMessage.logger.info(f"############# Filterd Well Data for the Date Range {self.start_date} to {self.end_date} and for the Completion Region {self.region} ####################")
                loggingMessage.logger.info(df_filtered)
                return df_filtered
        except Exception as e:
            return f"Date is Not Find for Filter : {self.start_date} Error :{e}"
        
    ###function for iterate the Filterd well infomation of the given date
    def itterateWellInfomation(self):
        self.total_pdf_counts_per_api = []
        self.workover_pdf_counts_per_api = []
        self.drilling_pdf_counts_per_api = []
        self.completion_pdf_counts_per_api =[]
        self.directional_survey =[]
        self.LWDLog = []
        self.MUDLog = []
        self.total_well_name= []
        self.api_list =[]
        self.download_date = []
        self.log_data = []
        self.well_data_yes = []
        
        if os.path.exists(self.filterd_csv_path):
            loggingMessage.logger.info("############ Well Infomation Search ###############")
            df = pd.read_csv(self.filterd_csv_path)
            try:

                for i,(well_val,filtered_date,api) in enumerate(zip(df['Well Name'],df['Latest File (Count)'],df['API'])):
                    loggingMessage.logger.info(f"############# Searching the Well Name : {well_val} for the date : {filtered_date} ####################")
                    ## click on All well data form search the well Name 
                    self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="ContentPlaceHolder1_FullColumn_nav1_pnlNavigation"]/div/ul/li[3]/a'))).click()
                    time.sleep(10)
                    ##puting the well name inkeyword search box
                    search_well_name = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="tbKeyword"]')))
                    search_well_name.send_keys(well_val)
                    search_well_name.send_keys(Keys.RETURN)
                    time.sleep(5)

                    ### fetch the Well information after search the well Name 
                    all_well_table_info =self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="wellDataTable"]')))
                    well_information = all_well_table_info.find_elements(By.XPATH,'.//tbody/tr') 
                    self.itterration_remars_click_count = 0
                    for well_info in well_information:
                        source_portal = well_info.find_element(By.XPATH,'./td[13]').text
                        status = well_info.find_element(By.XPATH,'./td[8]').text
                        if source_portal=="XTO Energy" and status == "ACTIVE":
                            well_name = well_info.find_element(By.XPATH,'./td[3]').text
                            api = well_info.find_element(By.XPATH,'./td[4]').text
                            operator_name = well_info.find_element(By.XPATH,'./td[7]').text
                            if operator_name in self.operator_dict:
                                operator_name = self.operator_dict[operator_name]

                                
                            loggingMessage.logger.info(f"Status : {status} Matched for Operator: {operator_name} and Well {well_name}")
                            print(f"############# Searching the Well Name : {well_val} for the date : {filtered_date} ####################")
                            if self.region == 'bakken':
                                report_path = self.download_path+'\\'+operator_name+"\\"+well_name
                            if self.region == 'oklahoma':
                                report_path = self.download_path+"\\"+well_name
                            ### after getting the data of well click on well name for show the all infomation of Well
                            view_well_info = well_info.find_element(By.XPATH,'./td[3]/a')
                            view_well_info.click()
                            time.sleep(6)
                        else:
                            print("Error : Source Protal XTO Energey & Status Active is Not There.")
                            
                        ### now navigate to the main tab selectionfor this well's report
                        main_tabs_header = self.wait.until(
                            EC.visibility_of_element_located((By.ID,'ContentPlaceHolder1_FullColumn_RightColumn_RightColumn_tcReportCategories_header'))
                        )
                        time.sleep(2)
                        ##locate all main tabs 
                        main_tabs = main_tabs_header.find_elements(By.CSS_SELECTOR,'a.ajax__tab_tab')
                        count_pattern = re.compile(r'\((\d+)\)')
                        for main_tab in main_tabs:
                            try:
                                tab_text = main_tab.text.strip()
                                match = count_pattern.search(tab_text)
                                if match:
                                    main_count = int(match.group(1))
                                    if main_count > 0:
                                        print(f"Main Tab : {tab_text} , count : {main_count}")
                                        main_tab.click()
                                        time.sleep(2)
                                        body_selection = self.wait.until(
                                            EC.visibility_of_element_located((By.ID,'ContentPlaceHolder1_FullColumn_RightColumn_RightColumn_tcReportCategories_body'))
                                        )
                                        time.sleep(2)

                                        # find all sub-tab with the body tab
                                        sub_tabs = body_selection.find_elements(By.CSS_SELECTOR,'a.ajax__tab_tab')

                                        for sub_tab in sub_tabs:
                                            sub_tab_text = sub_tab.text.strip()
                                            
                                            #check for count in sub tab
                                            sub_match = count_pattern.search(sub_tab_text)
                                            if sub_match:
                                                sub_count = int(sub_match.group(1))
                                                if sub_count > 0:
                                                    print(f"Sub Active Tabs  : {sub_tab_text} , count : {sub_count}")
                                                    time.sleep(2)
                                                    sub_tab.click()
                                                    time.sleep(2)
                                                    #rest the counts for eatch iteration
                                                    total_pdf_count =0
                                                    workover_count = 0
                                                    drilling_count = 0
                                                    completion_count = 0
                                                    table_rows = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,".gv-alt, .gv-alt-row")))
                                                    self.api_remarks_click = 0
                                                    for row in table_rows:
                                                        # itterration_remars_click_count = 0
                                                        columns= row.find_elements(By.TAG_NAME,"td")
                                                        if len(columns) > 10:
                                                            effective_date_element = columns[3]
                                                            effective_date = effective_date_element.text.strip()
                                                            print(f"Effective Date strip : {effective_date}")
                                                            effective_date_only=effective_date.split(' ')[0]
                                                            date_obj= datetime.strptime(filtered_date,"%Y-%m-%d")
                                                            filter_formated_date =f"{date_obj.month}/{date_obj.day}/{date_obj.year}"
                                                            loggingMessage.logger.info(f"Date mached for Well Searched : {filter_formated_date} and effective date : {effective_date_only}")
                                                            print(f"Total Effective date only : {effective_date_only}")
                                                            #print(f"Effective Date is : {effective_date_only} and Filter Date is : {filter_formated_date}")
                                                                
                                                            # if self.start_date <= effective_date_only <= self.end_date:
                                                            #     print(f"Matched Date between Start {self.start_date} and End Date {self.end_date} with {effective_date_only}")
                                                            #     effective_date = effective_date_element.text.strip()
                                                            #     print(f"Matched Effective Date For : {effective_date}")
                    # #                                                 pdf_file_element = columns[1]
                    #                                                 pdf_file_name=pdf_file_element.text.strip()
                    #                                                 pdf_file_name = pdf_file_name.replace("#","-")
                    #                                                 log_type_element = columns[2]
                    #                                                 log_type = log_type_element.text.strip()
                    #                                                 final_status = columns[9]
                    #                                                 final_text = final_status.text.strip()
                    #                                                 #print(f"Log type is : {log_type}")
                    #                                                 if log_type == 'Partner Completion and Workover Report':
                    #                                                     log_type = 'Workover'
                    #                                                 elif log_type == 'Partner Daily Drilling Report':
                    #                                                     log_type = 'Drilling'
                    #                                                 elif log_type == 'Partner Completion Report':
                    #                                                     log_type = 'Completion'
                                                                    
                    #                                                 total_pdf_count =0
                    #                                                 ##handle the PDF download Remarks
                    #                                                 if len(columns) > 10:
                    #                                                     remarks_download_element = columns[1]
                    #                                                     remarks_link = remarks_download_element.find_element(By.TAG_NAME, "a")
                    #                                                     time.sleep(4)
                    #                                                     remarks_link.click()
                    #                                                     self.itterration_remars_click_count +=1
                    #                                                     time.sleep(4)
                    #                                                     print(f"Clicked on Remarks Link for PDF Download : {pdf_file_name}")
                    #                                                     final_path_of_pdf_update = report_path+"\\"+log_type
                                                                       
                    #                                                     pdf_file_path = os.path.join(self.export_path,pdf_file_name)
                    #                                                     pdf_path_after_move = os.path.join(final_path_of_pdf_update,pdf_file_name)
                    #                                                     final_pdf_path = pdf_file_path
                    #                                                     #construct the final PDF path
                    #                                                     final_pdf_path = f"{final_pdf_path}".format(final_pdf_path=final_pdf_path )
                    #                                                     os.makedirs(final_path_of_pdf_update,exist_ok=True)
                    #                                                     print(f"Final PDF Path  {pdf_path_after_move}")
                    #                                                     self.report_number = self.extract_report_number(final_pdf_path)
                    #                                                     if os.path.exists(pdf_path_after_move):
                    #                                                         # if not os.path.exists(final_path_of_pdf_update):
                    #                                                         print(f"Well {well_name} Already Updated with PDF {pdf_file_name} for {log_type} & {effective_date_only}. Skipping...")
                    #                                                         #self.log_data.append({"Update Report Date":self.today,"Well Name": well_name,"PDF Name ": pdf_file_name,"Log Type":log_type,"Effective Date":effective_date_only,"Status":"Already Updated"})
                    #                                                         self.log_data.append({"Update Report Date":self.today,"Well Name": well_name,"PDF Name ": pdf_file_name,"API 14":api,"Opearater Name":operator_name,"Log Type":log_type,"Effective Date":effective_date_only,"Report Number":self.report_number,"Status":"Already Updated"})
                    #                                                     else:
                                                                            
                    #                                                         shutil.move(final_pdf_path,final_path_of_pdf_update)
                    #                                                         total_pdf_count +=1
                    #                                                         print(f"PDF {pdf_file_name} Downloaded Successfully Move to Operatoer Folder . {final_path_of_pdf_update}")
                    #                                                         self.log_data.append({"Update Report Date":self.today,"Well Name": well_name,"PDF Name ": pdf_file_name,"API 14":api,"Opearater Name":operator_name,"Log Type":log_type,"Effective Date":effective_date_only,"Report Number":self.report_number,"Status":"Downloaded"})
                    #                                                         # self.log_data.append({"Update Report Date":self.today,"Well Name": well_name,"PDF Name ": pdf_file_name,"Log Type":log_type,"Effective Date":effective_date_only,"PDF Count's":self.api_remarks_click,"Status":"Downloaded"})
                                                                    
                    #                                                         if log_type == 'Workover':
                    #                                                             #workover_count+=1
                    #                                                             workover_count =self.report_number
                    #                                                         elif log_type == 'Drilling':
                    #                                                             #drilling_count += 1
                    #                                                             drilling_count = self.report_number
                    #                                                         elif log_type == 'Completion':
                    #                                                             #completion_count += 1
                    #                                                             completion_count = self.report_number

                    #                                                         well_data_column_name = tab_text.split('(')[0].strip()
                    #                                                         if well_data_column_name == "Well Data":

                    #                                                             if final_text == "Yes":
                    #                                                                 if log_type == "Directional Surveys":
                    #                                                                     self.directional_survey.append("YES(Final)")
                    #                                                                 elif log_type == "LWD Log":
                    #                                                                     self.LWDLog.append("YES(Final)")
                    #                                                                 elif log_type == "MUD Log":
                    #                                                                     self.MUDLog.append("YES(Final)")
                    #                                                             else:
                    #                                                                 if log_type == "Directional Surveys":
                    #                                                                     self.directional_survey.append("YES")
                    #                                                                 elif log_type == "LWD Log":
                    #                                                                     self.LWDLog.append("YES")
                    #                                                                 elif log_type == "MUD Log":
                    #                                                                     self.MUDLog.append("YES")
                    #                                                         else:
                    #                                                             self.directional_survey.append(0)
                    #                                                             self.MUDLog.append(0)
                    #                                                             self.LWDLog.append(0)
                    #                                                 else:
                    #                                                     print(f"Error: Unable to Download the PDF bcz of file name Not Found")        
                    #                                             else:
                    #                                                 print(f"Error : Given Start Date : {self.start_date} & end date : {self.end_date} Not Mateched with Effective date")
                            except Exception as e:
                                print(f"Error : {e}")                                                
                                                                            
                    # self.api_remarks_click +=self.itterration_remars_click_count
                    # print(f"PDF Download Counts : {self.api_remarks_click}")
                    # # self.log_data.append({"Update Report Date":self.today,"Well Name": well_name,"PDF Name ": pdf_file_name,"API 14":api,"Opearater Name":operator_name,"Log Type":log_type,"Effective Date":effective_date_only,"PDF Count's":self.api_remarks_click,"Report Number":self.report_number,"Status":"Downloaded"})                                                    
                    # #self.download_date.append(effective_date)
                    # self.api_list.append(api)
                    # self.total_pdf_counts_per_api.append(self.api_remarks_click)
                    # # print(f"For Current API {api} and {well_name} Total PDF Counts is : {self.api_remarks_click}")
                    # self.workover_pdf_counts_per_api.append(workover_count)
                    # self.drilling_pdf_counts_per_api.append(drilling_count)
                    # self.completion_pdf_counts_per_api.append(completion_count)   
                    # self.total_well_name.append(well_name)
                    # self.download_date.append(self.today)
                                    
                    #self.api_14.append(api)
                if len(self.api_list) > 0:
                    print(f"Tracking Sheet Updated Started ..")
                    loggingMessage.logger.info(f"Tracking Sheet Updated Started ..")
                

                    self.upateReport()
                    loggingMessage.logger.info(f"Tracker Sheet Updated Successfully ")
                    print(f"Tracker Sheet Updated Successfully")
                else:
                    print("=======================================================================================================================================")
                    print(f"Tracking Sheet Not Updated for the Current Date Because No Reports Available or already Updated for that Date : {self.start_date}")

                    print("------------------Please Update the Report for Different Date -----------------------------------------------------------")
                        #print(f"Total PDF Download Clount is : {self.pdf_download_count}") 
                                  
            except Exception as e:
                print(f"Error: During the Well Search geting Some issue of filterd Well or PDSWDX WebPage Slowness, Please Re-Ran you BOT.")
                sys.exit(1)
            # finally:
            #     print(f"Total OBO WELL Updated Successfully on Lan Path: {well_completed} and Updating Tracker Sheet For the API 14 is : {self.api_14}")
        else:
            print(f"Sorry, We are not geeting any Filterwd Well for the Given Date Range : {self.start_date} - {self.end_date}")
        self.driver.close()

    def upateReport(self):

        print(f"Total API 14 List is : {self.api_list}")
        print(f"Total PDF counts as Per API : {self.total_pdf_counts_per_api}")
        print(f"Total PDF WORKOVER counts : {self.workover_pdf_counts_per_api}")
        print(f"Total PDF Drilling Counts : {self.drilling_pdf_counts_per_api}")
        print(f"Total Completion PDF Counst Report Count : {self.completion_pdf_counts_per_api}")
        print(f"Total Well Searched : {self.total_well_name}")
        print(f"Downloaded Date : {self.download_date}")
        print(f"Directiona Survey Column Matched : {self.directional_survey}")
        print(f" MUD Log Column Matched : {self.MUDLog}")
        print(f"LWD LOG Survey Column Matched : {self.LWDLog}")
        ### Log result file export
        tracker_df = pd.DataFrame(self.log_data)
        completion_tracker_sheet = f"Completion_tracker_{self.today_file}_{self.region}.csv"
        tracker_path = os.path.join(self.export_path,completion_tracker_sheet)
        tracker_df.to_csv(tracker_path,index=False)
        #print(f"Total PDF Reprts Counts for Logs Type : {self.report_count_list}")
        #loggingMessage.logger.info(f"Total Well Searched : {self.total_well_name}")
        string_api_list = self.api_list
        int_api_list = [int(num) for num in string_api_list]      
        ##define the Values 
        condition_values=int_api_list  # list of APi 14  to match
        ### Dictionary of target columns with their specified values for eatch condition values
        target_columns_with_values = {
            #'NUMBER OF ITEMS DOWNLOADED':int_api_list,
            'DATE DOWNLOADED':self.download_date,
            'NUMBER OF ITEMS DOWNLOADED':self.total_pdf_counts_per_api,
            'DRILLING REPORTS':self.drilling_pdf_counts_per_api,
            'COMPLETION REPORTS':self.completion_pdf_counts_per_api,
            'WORKOVER REPORTS':self.workover_pdf_counts_per_api,
            'DIRECTIONAL SURVEY':self.directional_survey,
            'MUDLOGS':self.MUDLog,
            'LWDLOGS':self.LWDLog
        }
        df_tracker=pd.read_excel(self.tracker_sheet_path)
        for i, condition_value in enumerate(condition_values):
            #check if the condition_value exist in the tracker sheet and updat corrsponding row
            if condition_value in df_tracker['API 14'].values:
                for target_col,value in target_columns_with_values.items():
                    
                    try:
                        v = value[i]
                        
                        if v == 0:
                            print(f"Skipped Updating {target_col} for {condition_value} as value is zero.")
                        elif(isinstance(v,(int,float)) and v > 0) or (isinstance(v,str) and v.strip()):
                            df_tracker.loc[df_tracker['API 14'] == condition_value,target_col]=v
                            #df_tracker[target_col]= df_tracker[target_col].replace(0,'')
                            print(f"Updated row where {target_col} is {condition_value} for {target_col} : {v}")
                        else:
                            print(f"Skipped updating {target_col} for {condition_value} due to invalid value: {v}")
                    except IndexError:
                        print(f"No Matching Value for {target_col} at index {i}; skiping or filling as needed.")
            else:
                print(f"Condition Value {condition_value} not found in 'API';Skipping.")

        df_tracker.to_excel(self.tracker_sheet_path,index=False)
        

    def extract_report_number(self,pdf_path):
        if pdf_path.endswith(".PDF"):
            with fitz.open(pdf_path) as pdf:
                for page_num in range(pdf.page_count):
                    page_text = pdf[page_num].get_text()
                    if 'Report #:' in page_text:
                        start_idx = page_text.find('Report #:') + len('Report #:')
                        report_number = page_text[start_idx:].split()[0]
                        return f"Report {report_number}"

                    elif 'Report #' in page_text:
                        start_idx = page_text.find('Report #') + len('Report #')
                        report_number = page_text[start_idx:].split()[0]
                        return f"Report {report_number}"

                    elif 'Rpt #' in page_text:
                        start_idx = page_text.find('Rpt #') + len('Rpt #')
                        report_number = page_text[start_idx:].split()[13]
                        return f"Report {report_number}"  

                    elif 'Report No:' in page_text:
                        start_idx = page_text.find('Report No:') + len('Report No:')
                        report_number = page_text[start_idx:].split()[1]
                        return f"Report {report_number}"
                
                    elif 'Report No.:' in page_text:
                        start_idx = page_text.find('Report No.: ') + len('Report No.:')
                        report_number = page_text[start_idx:].split()[13]
                        return f"Report {report_number}"
        else:
                    
            return f"Report 1"           

           

   
