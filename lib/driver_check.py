from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
#setup chrome options 
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")

#use webdriver-manager to get the correct chrome driver version automatically 
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

#open the website 
driver.get("http://www.google.com")
driver.guit()