# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 14:47:20 2016

@author: Zachary
"""

################
# Load to city #
################

def open_body_text(city):
    '''
    opens browser
    navigates through craigslist posting fields
    '''
    # open incognito browser
    
    browser.implicitly_wait(3) # wait 3 seconds when doing find_element before carrying on    
    
    browser.get('http://www.craigslist.org/about/sites') #opens webpage with get() method on browser object

    # find and click input city
    browser.find_element_by_link_text(city).click()
    
    # select 'post to classifieds'
    browser.find_element_by_link_text('post to classifieds').click()
    
    # click community
    browser.find_element_by_css_selector('.picker > blockquote:nth-child(1) > label:nth-child(29)').click()    
    # click volunteers
    browser.find_element_by_css_selector('.picker > blockquote:nth-child(1) > label:nth-child(26)').click()
    
    # sometimes further location choices are offered
    # defaults to biggest area -- first choice
    try:
        browser.find_element_by_css_selector('.picker > blockquote:nth-child(1) > label:nth-child(1) > input:nth-child(1)').click()
    except:
        pass

##############
# data entry #
##############

def data_entry(city, email_address, title, body_text, zip_code):
    '''
    calls open_body_text() function to get to data entry fields
    selects and inputs arguments to fill in fields
    submits arguments and posts on local craigslist
    outputs the zip and date of when it was posted
    '''
    import datetime
    
    open_body_text(city)    
    
    # select first email entry field
    email_field = browser.find_element_by_css_selector('#FromEMail')
    email_field.click()

    # enter email
    email_field.send_keys(email_address) # pass string to send keys method

    # select second
    email_field_2 = browser.find_element_by_css_selector('#ConfirmEMail')
    email_field_2.click()
    
    # enter email
    email_field_2.send_keys(email_address) # pass string to send keys method

    # select title field
    title_field = browser.find_element_by_css_selector('#PostingTitle')
    title_field.click()
    
    # post title
    title_field.send_keys(title)

    # select body field
    body_field = browser.find_element_by_css_selector('#PostingBody')
    body_field.click()
    
    # post body and link
    body_field.send_keys(body_text + '\n\n' + link) 
    
    #select postal code field
    zip_field = browser.find_element_by_css_selector('#postal_code')
    zip_field.click()

    # post zip code
    zip_field.send_keys(zip_code)    

    # hit 'do not show on maps' button    
    try:
        browser.find_element_by_css_selector('#wantamap').click()
    except:
        pass
    
    # hit submit button to post data
    browser.find_element_by_css_selector('.bigbutton').click()
    
    # hit submit button to not post images
    browser.find_element_by_css_selector('.done').click()    
    
    todays_date = datetime.date.fromordinal(730920).strftime('%m/%d/%y')
    f_out.write(str(zip_code) + ',' + str(todays_date) + '\n')
    print('%s written to file on %s') % (zip_code, todays_date)
    
    # hit final submit button    
    browser.find_element_by_css_selector('.bigbutton').click()
    
    # feedback prints
    print('%s, %s, %s posted') % (email_address, city, zip_code)



import csv
from selenium import webdriver
import time

browser = webdriver.Firefox() # define browser object

f_in = open("C:\\Users\\Zachary\\OneDrive\\Documents\\4. Technical\\Programming\\Python\\Arianna's CEO postings\\ceo_posting_day2.csv", 'r')
data = csv.DictReader(f_in)

f_out = open("C:\\Users\\Zachary\\OneDrive\\Documents\\4. Technical\\Programming\Python\\Arianna's CEO postings\\zips_used.csv", 'w')
f_out.write('zip,date\n')


for row in data:
    email_address = row['email'].lower()
    city = row['city'].lower()
    zip_code = row['zip']
    link = row['link']
    title = row['title']
    body_text = row['body']
    print('writing: %s, %s, %s') % (email_address, city, zip_code)


    data_entry(city, email_address, title, body_text, zip_code)
    print('**************')
    time.sleep(5)

browser.quit()
f_in.close()
f_out.close()
print('program complete. congrats!')