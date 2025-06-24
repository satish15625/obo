import fitz
import os
li = [1,2,3]
def extract_report_number(pdf_path):
    pdf_count = len([f for f in os.listdir(r"C:\\Users\sakum49\Desktop\EXXON\PDSWDX_Bakken_oklahoma\input\oklahoma_lan\MOSELEY EAST 0203-25-36 1WHX\Drilling") if f.upper().endswith(".PDF")])
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
            
            elif 'Report Number:' in page_text:
                start_idx = page_text.find('Report Number:')
                report_number = page_text[start_idx:].split()[2]
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
            
        return f"Report {pdf_count}" 

report_path =r'C:\\Users\sakum49\Desktop\EXXON\PDSWDX_Bakken_oklahoma\input\oklahoma_lan\MOSELEY EAST 0203-25-36 1WHX\Drilling\MOSELEY EAST 0203-25-36 1WHX DDR (02-21-2025).PDF'
print(extract_report_number(report_path))