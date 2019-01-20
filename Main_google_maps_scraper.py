from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

import csv
import threading
import time
try:
    import tkinter as tk
    from tkinter import messagebox as msg, filedialog
    from tkinter import *
except:
    import Tkinter as tk
    import tkMessageBox as msg
    from Tkinter import *

from GUI import *

def open_url(url, num_retries=5):
    try:
        driver = webdriver.Chrome()
        driver.get(url)
    except:
        if num_retries > 0:
            driver.quit()
            open_url(url, num_retries-1)
    return driver

class google_maps_scraper():

    def __init__(self, master):

        # self.keyword = keyword
        self.start_url = 'https://www.google.com/maps/search/'

        self.master = master
        self.total_data = []
        self.gui = main_GUI(master, self.total_data, self.endApplication)

        self.running = 1
        self.periodicCall()

        self.i = 0

        self.url_dict = []
        self.company_names = []

        #self.go_to_search()


    def periodicCall(self):
        if self.running == 0:
            print('Exit')
            import sys
            #self.master.quit()
            self.master.destroy()

            sys.exit(1)
        elif self.running == 1:
            if self.gui.start == True:
                self.keyword = self.gui.keyword
                self.running = 2
                self.thread1 = threading.Thread(target=self.go_to_search)
                self.thread1.start()
        elif self.running == 2:
            self.gui.insert_data()


        self.master.after(2000, self.periodicCall)

    def endApplication(self):
        self.running = 0

    def go_to_search(self):

        filename = self.keyword + '.csv'
        self.output_file = open(filename, 'w', encoding='utf-8', newline='')
        self.writer = csv.writer(self.output_file)
        headers = ['Company Name', 'Address', 'Category', 'Star Rating', 'Number of Reviews',
                   'Phone Number', 'Website']
        self.writer.writerow(headers)

        self.driver = open_url(self.start_url)

        input = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search Google Maps']")))
        search_btn = WebDriverWait(self.driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Search']")))

        input.send_keys(self.keyword)
        time.sleep(2)
        search_btn.click()
        self.scraping_onepage()
        self.running = 0

    def scraping_onepage(self):

        self.item_index = 0
        self.skip_index = 0
        while 1:
            if len(self.company_names) >= 50 or self.skip_index >= 80:
                break

            print(self.item_index)
            companies = WebDriverWait(self.driver, 50).until(
                EC.presence_of_all_elements_located((By.XPATH, "//h3[@class='section-result-title']")))
            self.item_cnt = len(companies)

            if companies[self.item_index].text not in self.company_names:
                self.skip_index = 0
                self.company_names.append(companies[self.item_index].text)

                self.org_url = self.driver.current_url

                companies[self.item_index].click()
                print(self.org_url)

                self.scraping_onecompany()

                self.driver.get(self.org_url)
                time.sleep(5)
            else:
                self.skip_index += 1

            self.item_index += 1

            if self.item_index == self.item_cnt:
                self.item_index = 0
                #self.driver.delete_all_cookies()
                next_btn = WebDriverWait(self.driver, 50).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@id='section-pagination-button-next']")))
                next_btn.click()
                print('Next Button: Clicked Successfully')
                time.sleep(5)
                companies = WebDriverWait(self.driver, 50).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//h3[@class='section-result-title']")))
                self.item_cnt = len(companies)

                if self.item_cnt == 0:
                    break
        self.driver.quit()
        self.output_file.close()


    def scraping_onecompany(self):
        i = 0
        while 1:
            if i > 200:
                company_name = ''
                break
            else:
                i += 1

                company_name = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//h1[@class='section-hero-header-title']"))
                )
            if company_name.text is not '':
                company_name = company_name.text
                break


        try:
            rating = self.driver.find_element_by_css_selector('span.section-star-display').text
        except:
            rating = ''
        try:
            reviews = self.driver.find_element_by_css_selector('ul.section-rating-term-list').find_element_by_css_selector(
                'button.widget-pane-link').text
        except:
            reviews = ''

        section_infos = self.driver.find_elements_by_css_selector('div.section-info')

        try:
            address = self.driver.find_elements_by_css_selector('div.section-info')[0].text
        except:
            address = ''

        website = ''
        phone = ''


        for section_info in section_infos:
            try:
                #website_lbl = section_info.find_element_by_xpath("//span[@aria-label='Website']")
                website_lbl = section_info.find_element_by_css_selector("span.section-info-icon.maps-sprite-pane-info-website")
                website = website_lbl.find_element_by_xpath('..').find_element_by_css_selector('span.section-info-text').text
            except:
                pass

            try:
                #phone_lbl = section_info.find_element_by_xpath("//span[@aria-label='Phone']")
                phone_lbl = section_info.find_element_by_css_selector("span.section-info-icon.maps-sprite-pane-info-phone")
                phone = phone_lbl.find_element_by_xpath('..').find_element_by_css_selector('span.section-info-text').text
            except:
                pass

        try:
            category = self.driver.find_element_by_css_selector('span.section-rating-term').text
        except:
            category = ''

        element = {
            'company_name': company_name,
            'address': address,
            'category': category,
            'star_rating': rating,
            'review_numbers': reviews,
            'phone': phone,
            'websites': website
        }
        #if element not in self.total_data:
        print(element)
        self.total_data.append(element)
        # driver.execute_script("window.history.go(-1)")
        row = [
            element['company_name'],
            element['address'],
            element['category'],
            element['star_rating'],
            element['review_numbers'],
            element['phone'],
            element['websites'],
        ]
        self.writer.writerow(row)

    def save_to_csv(self):
        filename = self.keyword + '.csv'
        self.output_file = open(filename, 'w', encoding='utf-8', newline='')
        self.writer = csv.writer(self.output_file)
        headers = ['Company Name', 'Address', 'Category', 'Star Rating', 'Number of Reviews',
                   'Phone Number', 'Website']
        self.writer.writerow(headers)
        for i, element in enumerate(self.total_data):
            row = [
                element['company_name'],
                element['address'],
                element['category'],
                element['star_rating'],
                element['review_numbers'],
                element['phone'],
                element['websites'],
            ]
            self.writer.writerow(row)
        self.output_file.close()


if __name__ == '__main__':

    start_time = time.time()

    keywords = [
        'solar sacramento ca',
        'Solar San Diego Ca'
    ]

    root = tk.Tk()

    app = google_maps_scraper(root)
    root.mainloop()
    elapsed_time = time.time() - start_time
    print(elapsed_time)


