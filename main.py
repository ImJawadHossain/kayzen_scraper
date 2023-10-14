import time


from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




###########################################
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Initialize the Google Sheets API client
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('api_data_vaiya.json', scope)
gc = gspread.authorize(credentials)

# Open a specific Google Sheet by its title
worksheet = gc.open('Kayzen').sheet1
#################################################




options = Options()

options.set_preference("network.http.pipelining", True)
options.set_preference("browser.cache.memory.capacity", 65536)
options.set_preference("browser.display.show_image_placeholders", False)
options.set_preference("network.http.pipelining.maxrequests", 8)
options.set_preference("permissions.default.image", 2)
options.set_preference("geo.prompt.testing", True)
options.set_preference("geo.prompt.testing.allow", False)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://momomedia.kayzen.io/login")

input("Enter: ")

count_page = 8

count_page_data = 25

sheet_row_count = 2

while count_page <= 319:

    driver.get('https://momomedia.kayzen.io/creatives?page='+str(count_page)+'&limit=25&perfAdvId=13176')


    data_count = 1

    while data_count <= 200:

        def get_id_data():
            try:
                # Code for getting ID data
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, str('/html[1]/body[1]/div[1]/div[1]/div[1]/md-content[1]/dl-creative-page[1]/div[2]/div[1]/div[1]/md-tab-body[1]/dl-creative-list[1]/div[2]/div[1]/div[1]/md-data-table-container[1]/div[1]/table[1]/tbody[1]/tr["+str(data_count)+"]/td[2]/div[1]'))))
                id_text = driver.find_element("xpath", str("/html[1]/body[1]/div[1]/div[1]/div[1]/md-content[1]/dl-creative-page[1]/div[2]/div[1]/div[1]/md-tab-body[1]/dl-creative-list[1]/div[2]/div[1]/div[1]/md-data-table-container[1]/div[1]/table[1]/tbody[1]/tr["+str(data_count)+"]/td[2]/div[1]")).text
                print(id_text)
                return id_text
            except:
                pass

        def get_name_data():
            try:
                # Code for getting Name data
                name_text = driver.find_element("xpath", str("/html[1]/body[1]/div[1]/div[1]/div[1]/md-content[1]/dl-creative-page[1]/div[2]/div[1]/div[1]/md-tab-body[1]/dl-creative-list[1]/div[2]/div[1]/div[1]/md-data-table-container[1]/div[1]/table[1]/tbody[1]/tr["+str(data_count)+"]/td[3]/div[1]")).text
                print(name_text)
                return name_text
            except:
                pass


        def get_video_url():
            try:
                # Code for getting Video url
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/md-content/dl-creative-page/div[2]/div/div/md-tab-body/dl-creative-list/div[2]/div/div/md-data-table-container/div/table/tbody/tr["+str(data_count)+"]/td[4]/dl-creative-preview/span')))
                driver.find_element("xpath", str("/html/body/div[1]/div/div/md-content/dl-creative-page/div[2]/div/div/md-tab-body/dl-creative-list/div[2]/div/div/md-data-table-container/div/table/tbody/tr["+str(data_count)+"]/td[4]/dl-creative-preview/span")).click()


                iframe = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/iframe')))

                driver.switch_to.frame(iframe)

                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div/mat-dialog-container/kz-creative-view-dialog/div[2]/kz-creative-phones/div/kz-asset-file-phone-preview[1]/div[2]/div[1]/kz-asset-file-preview/kz-videojs-player/div/video')))



                video_element = driver.find_element("xpath", "/html/body/div/div[2]/div/mat-dialog-container/kz-creative-view-dialog/div[2]/kz-creative-phones/div/kz-asset-file-phone-preview[1]/div[2]/div[1]/kz-asset-file-preview/kz-videojs-player/div/video")
                video_url = video_element.get_attribute('src')
                print(video_url)

                driver.find_element("xpath", "/html/body/div/div[2]/div/mat-dialog-container/kz-creative-view-dialog/div[1]/button").click()
                driver.switch_to.default_content()

                return video_url
            except:
                driver.find_element("xpath", "/html/body/div/div[2]/div/mat-dialog-container/kz-creative-view-dialog/div[1]/button").click()
                driver.switch_to.default_content()



        update_data = [get_id_data(), get_name_data(), get_video_url()]
        worksheet.append_row(update_data)

        data_count += 1




    print("####################################################################")
    count_page += 1
