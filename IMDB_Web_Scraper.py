# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import numpy as np
import time


def get_movies(num_movies, path):
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions() 
    driver = webdriver.Chrome(executable_path=path, options=options) #Change the path to where chromedriver is in your home folder.
    driver.set_window_size(1120, 1000)

    #Open Specified URL with keyword you want to search for
    URL = "https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating"
    driver.get(URL)
    
    movies = []
    ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
    

    while len(movies) < num_movies:
        
        try:
            #Wait until the web page load
            element = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(
                    EC.presence_of_element_located((By.ID, "main"))
                    )
        
            movie_button = element.find_elements_by_xpath('.//div[@class="lister-item mode-advanced"]')

            for movie in movie_button:

                print("Progress: {}".format("" + str(len(movies)) + "/" + str(num_movies)))
                if len(movies) >= num_movies:
                    break

                try:
                    title = movie.find_element_by_xpath('.//h3[@class="lister-item-header"]').text
                except NoSuchElementException:
                    title = np.NaN
                
                try: 
                    certificate = movie.find_element_by_xpath('.//span[@class="certificate"]').text
                except NoSuchElementException:
                    certificate = np.NaN
                    
                try:    
                    duration = movie.find_element_by_xpath('.//span[@class="runtime"]').text
                except NoSuchElementException:
                    duration = np.NAN
                    
                try:
                    genre = movie.find_element_by_xpath('.//span[@class="genre"]').text
                except NoSuchElementException:
                    genre = np.NaN
                    
                try:
                    rate = movie.find_element_by_xpath('.//strong').text 
                except NoSuchElementException:
                    rate = np.NaN
                
                try: 
                    metascore = movie.find_element_by_xpath('.//span[@class="metascore  favorable"]').text
                except NoSuchElementException:
                    metascore = np.NaN
                    
                try:
                    descr = movie.find_element_by_xpath('.//p[@class="text-muted"]').text
                except NoSuchElementException:
                    descr = np.NaN
                
                try:
                    cast = movie.find_element_by_xpath('.//p[@class=""]').text
                except NoSuchElementException:
                    cast = np.NaN
                
                try:
                    info = movie.find_element_by_xpath('.//p[@class="sort-num_votes-visible"]').text
                except NoSuchElementException:
                    info = np.NaN
                
                movies.append({
                    "Title": title,
                    "Certificate": certificate,
                    "Duration": duration,
                    "Genre": genre,
                    "Rate": rate,
                    "Metascore": metascore,
                    "Description": descr,
                    "Cast": cast,
                    "Info": info
                    })
            try:
                if len(movies) < num_movies:
                    element.find_element_by_xpath('.//a[@class="lister-page-next next-page"]').click()
                    time.sleep(20)
                
            except NoSuchElementException:
                print("Scraping terminated before reaching target number of movies. Needed {}, got {}.".format(num_movies, len(movies)))
                driver.quit()
                break   
            
        finally:
            if len(movies) >= num_movies:
                driver.quit()

    return pd.DataFrame(data=movies)

PATH = "C:\Program Files (x86)\chromedriver.exe"
df = get_movies(1000, PATH)
df.to_csv("IMDB top 1000")
