from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
import urllib.request
import os

# OS module
print(os.getcwd())
os.chdir('D:/NMIMS/Sem.3/DAP')


#  Any infinity scroll URL
var = input("Enter search query:")
url = "https://in.pinterest.com/search/pins/?q=" + var 
ScrollNumber = int(input("No. of time you want scroll:"))  # The depth we wish to load
sleepTimer = 1    # Waiting 1 second for page to load
alt = []
src = []


#  Bluetooth bug circumnavigate
options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])

'''driver = webdriver.Chrome(executable_path='D:/Softwares/chromedriver.exe')'''
driver = webdriver.Chrome()
driver.get(url)


# Data collection
for i in range(1,ScrollNumber):
    driver.execute_script("window.scrollTo(1,100000)")
    print("scrolling")
    time.sleep(sleepTimer)

soup = BeautifulSoup(driver.page_source,'html.parser')

l1 = []
l2 = []

for link in soup.find_all('img'):
    l1.append(link.get('src'))
    l2.append(link.get('alt'))

i = int(input("Enter a range:"))
urls = l1[:i]
names = l2[:i]
d1 = {"PIN_URL":urls, "PIN_NAME":names}

driver.quit()

# Converting DataFrame to csv file
df = pd.DataFrame(d1)
csv_name = var + ".csv"
csv_name = csv_name.replace(" ", "_")
df.to_csv(csv_name, index=False)


# To download images from .csv file
def url_to_jpg(i, url, file_path):
    """
    i : number of image
    urls : a URL address of a given image
    file_path : where to save the final image
    """
    filename = var+'-{}.jpg'.format(i)
    full_path = '{}{}'.format(file_path, filename)
    urllib.request.urlretrieve(url, full_path)
    print('{} saved.'.format(filename))


# Creating folder for search query
os.mkdir('D:/NMIMS/Sem.3/DAP/'+var)


# Set Constants
Filename = csv_name
File_path = 'D:/NMIMS/Sem.3/DAP/'+var+'/'


# Read list of URLs as Pandas DataFrame
url_s = pd.read_csv(Filename)


# Save Images to the Directory by iterating through the list
for i,url in enumerate(url_s.values):
    url_to_jpg(i, url[0], File_path)
