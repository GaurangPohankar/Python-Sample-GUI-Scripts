import tkinter
from tkinter import ttk
from bs4 import BeautifulSoup
import urllib
import csv
import requests
import time
from getpass import getpass
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common import utils
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import codecs
import traceback
import re
from progress.bar import Bar


class Begueradj(tkinter.Frame):
    '''
    classdocs
    '''  
    def __init__(self, parent):
        '''
        Constructor
        '''
        tkinter.Frame.__init__(self, parent)
        self.parent=parent
        self.initialize_user_interface()

    def initialize_user_interface(self):
        """Draw a user interface allowing the user to type
        items and insert them into the treeview
        """
        self.parent.title("Google Places Scrapper")       
        self.parent.grid_rowconfigure(0,weight=1)
        self.parent.grid_columnconfigure(0,weight=1)
        self.parent.config(background="lavender")


        # Define the different GUI widgets
        self.dose_label = tkinter.Label(self.parent, text = "Enter Your Query:")
        self.dose_entry = tkinter.Entry(self.parent)
        self.dose_label.grid(row = 0, column = 0, sticky = tkinter.W)
        self.dose_entry.grid(row = 0, column = 1)

        self.modified_label = tkinter.Label(self.parent, text = "Enter City:")
        self.modified_entry = tkinter.Entry(self.parent)
        self.modified_label.grid(row = 1, column = 0, sticky = tkinter.W)
        self.modified_entry.grid(row = 1, column = 1)

        self.submit_button = tkinter.Button(self.parent, text = "Fetch", command = self.update_status)
        self.submit_button.grid(row = 2, column = 1, sticky = tkinter.W)
        self.exit_button = tkinter.Button(self.parent, text = "Exit", command = self.parent.quit)
        self.exit_button.grid(row = 0, column = 3)

        # Set the treeview
        self.tree = ttk.Treeview( self.parent, columns=('Phone','Ratings','Googlemaps','website','Address'))
        self.tree.heading('#0', text='Name')
        self.tree.heading('#1', text='Phone')
        self.tree.heading('#2', text='Ratings')
        self.tree.heading('#3', text='Googlemaps')
        self.tree.heading('#4', text='website')
        self.tree.heading('#5', text='Address')
        self.tree.column('#1', stretch=tkinter.YES)
        self.tree.column('#2', stretch=tkinter.YES)
        self.tree.column('#3', stretch=tkinter.YES)
        self.tree.column('#4', stretch=tkinter.YES)
        self.tree.column('#5', stretch=tkinter.YES)
        self.tree.column('#0', stretch=tkinter.YES)
        self.tree.grid(row=4, columnspan=4, sticky='nsew')
        self.treeview = self.tree
        # Initialize the counter
        self.i = 0


    def insert_data(self):
        """
        Insertion method.
        """
        for l in range(10):
            print(l)
            self.treeview.insert('', 'end', text="Item_"+str(self.i), values=(self.dose_entry.get()+" mg", self.modified_entry.get()))
            self.update()
            time.sleep(2)
        # Increment counter
        self.i = self.i + 1
        
    def update_status(self):
        search = self.dose_entry.get()
        city = self.modified_entry.get()
        unique_id = time.time()
        fields = ['SrNo', 'Name','Phone', 'Rating', 'GoogleMaps', 'Website', 'Address']
        
        def extrapolate_pagination(driver,ity):
            button = driver.find_element_by_class_name("section-pagination-button-next")
            print("bhau bhai")
            button.click()
            time.sleep(2)
            elements = driver.find_elements_by_class_name("section-result")
            bar = Bar('Processing', max=len(elements))
            nElement = len(elements)
            for index in range(nElement+1):
                    bar.next()
                    extrapolate_date(elements,index,driver,city)
                    try:
                            back = driver.find_element_by_xpath("//*[@class='section-back-to-list-button blue-link noprint']")
                            back.click()
                            time.sleep(5)
                            elements = driver.find_elements_by_class_name("section-result")
                            
                    except:
                            print('Finish')
                            quit()
            bar.finish()
	
        #!/usr/bin/env python
        # -*- coding: utf-8 -*-
        def extrapolate_gmaps(search,city):
                city = city.upper()
                driver = webdriver.Firefox(executable_path='./geckodriver')
                driver.set_window_size(1120, 550)
                try:
                        driver.get("https://www.google.com/maps/")
                except:
                        driver.save_screenshot('err.png')
                driver.save_screenshot('screenshot.png')
                #assert "Google Maps" in driver.title

                elem = driver.find_element_by_xpath("//*[@id='searchboxinput']")
                #elem.send_keys(search)
                elem.send_keys(search)
                #ristorante torino
                #elem.send_keys("pycon")
                elem.send_keys(Keys.RETURN)
                time.sleep(5)
                #elem.clear()
                elements = driver.find_elements_by_class_name("section-result")

                bar = Bar('Processing', max=len(elements))
                nElement = len(elements)
                for index in range(nElement+1):
                        bar.next()
                        extrapolate_date(elements,index,driver,city)
                        back = driver.find_element_by_xpath("//*[@class='section-back-to-list-button blue-link noprint']")
                        back.click()
                        time.sleep(3)
                        elements = driver.find_elements_by_class_name("section-result")
                bar.finish()

                assert "No results found." not in driver.page_source

        def extrapolate_date(elements,index,driver,city):
                if index == len(elements):
                        extrapolate_pagination(driver,city)
                print("")
                print(index)
                element = elements[index]
                
                try:
                        name = element.find_element_by_class_name('section-result-title').text
                        print(name)
                        name = name.strip()
                        name = name.replace("\"","\'")
                except:
                        traceback.print_exc()
                        name = ""

                try:
                        ratings = element.find_element_by_class_name('cards-rating-score').text
                        print(ratings)
                        ratings = ratings.strip()
                        ratings = ratings.replace("\"","\'")
                except:
                        traceback.print_exc()
                        ratings = ""
                element.click()
                time.sleep(3)
                        
                try:
                        info = driver.find_elements_by_class_name("section-info-text")
                except:
                        traceback.print_exc()
                try:
                        address = info[0].text
                        print(address)
                        print(info[1].text)
                        print(info[2].text)
                        print(info[3].text)
                        address = address.strip()
                        address = address.replace("\"","\'")
                except:
                        traceback.print_exc()
                        address = ""
                
                try:
                        site = driver.find_element_by_css_selector("a[data-attribution-url]")
                        site = site.get_attribute('data-attribution-url')
                        print(site)
                        site = site.strip()
                        site = site.replace("\"","\'")
                except:
                        traceback.print_exc()
                        site = ""

                self.treeview.insert('', 'end', text=str(self.i)+" : "+str(name), values=(info[3].text,ratings,info[1].text,info[2].text,address))
                self.update()
                self.i = self.i + 1
                dict_service = {}
                dict_service['SrNo'] = str(self.i)
                dict_service['Name'] = name
                dict_service['Phone'] = info[3].text
                dict_service['Rating'] = ratings
                dict_service['GoogleMaps'] = info[1].text
                dict_service['Website'] = info[2].text
                dict_service['Address'] = address
                
                with open(str(unique_id)+'.csv', 'a') as csvfile:
                    filewriter = csv.DictWriter(csvfile, delimiter=',', fieldnames=fields)
                    filewriter.writerow(dict_service)
                csvfile.close()
                #driver.close()
        extrapolate_gmaps(search,city)

def main():
    root=tkinter.Tk()
    d=Begueradj(root)
    root.mainloop()

if __name__=="__main__":
    main()

