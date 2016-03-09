# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 14:47:20 2016

@author: Zachary
"""
'''

Given an input file with:
Location: region, state
Contact: email, phone number
Message: title, body, survey link

Opens a new browser window
Selects posting region based off location information
Stores posting region and state

Checks if there are multiple subregions
Logs what those subregions are

Pulls message information from input file
Posts message information
Pulls contact information from input file
Posts contact information

If there were subregions, Iterates over subregions to post into each

checks posting confirmation
forwards confirmation to central email address < don’t know if I can actually do this

Delivers output file with:
Location: region, state
Contact: email, phone number
Confirmation: dtg of posting, url for confirmation

Forwards all confirmation emails to central email address < don’t know if I can actually do this

'''



################
# Load to region #
################

def webnav_to_region(region):
    '''
    opens browser
    navigates through craigslist posting fields
    '''
    # open incognito browser
    
    browser.implicitly_wait(1) # wait 1 seconds when doing find_element before carrying on    
    
    browser.get('http://www.craigslist.org/about/sites') #opens webpage with get() method on browser object

    # find and click input region
    browser.find_element_by_link_text(region).click()
    
    # select 'post to classifieds'
    browser.find_element_by_link_text('post to classifieds').click()
    
    # click community
    browser.find_element_by_css_selector('.picker > blockquote:nth-child(1) > label:nth-child(29)').click()    
    # click volunteers
    browser.find_element_by_css_selector('.picker > blockquote:nth-child(1) > label:nth-child(26)').click()
    # defaults to biggest area -- first choice

    try:
        print('skipping subregion dialogue, choosing first choice for subregion')
        browser.find_element_by_css_selector('.picker > blockquote:nth-child(1) > label:nth-child(1) > input:nth-child(1)').click()
        try:
            # sometimes there is a neighborhood prompt
            # ignore neighborhood prompt by clicking 'bypass this step'
            browser.find_element_by_css_selector('.picker > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(3) > input:nth-child(1)').click()                                    
        except:
            print('time to create posting for region: %s') % (region)
            pass
    except:
        print('no subregion dialogue found')
        pass

#####################    
# select subregions #
#####################        
def webnav_to_subregion(region, i):
    '''
    for every subregion that was found
    pulls open a new browser window to navigate to data entry prompts
    '''
    subregion_count = 0
    for subregion in range(1, int(i), 2):
        subregion_count += 1        
        # open incognito browser    
        browser.implicitly_wait(1) # wait 1 seconds when doing find_element before carrying on    
        
        browser.get('http://www.craigslist.org/about/sites') #opens webpage with get() method on browser object
    
        # find and click input region
        browser.find_element_by_link_text(region).click()
        
        # select 'post to classifieds'
        browser.find_element_by_link_text('post to classifieds').click()
        
        # click community
        browser.find_element_by_css_selector('.picker > blockquote:nth-child(1) > label:nth-child(29)').click()    

        # click volunteers
        browser.find_element_by_css_selector('.picker > blockquote:nth-child(1) > label:nth-child(26)').click()

        # click nearest area
        # each selection box goes from 1 to 3 to 5 to 7, etc
        browser.find_element_by_css_selector('.picker > blockquote:nth-child(1) > label:nth-child(' + \
                                            str(2*int(subregion_count)-1) + ') > input:nth-child(1)').click()

        # log the subregions for that region into csv output file         
        print('logging subregion %i') % (subregion_count)

        # insert logging here

        print('subregion %i logged') % (subregion_count)
        
        # sometimes there is a neighborhood prompt
        # ignore neighborhood prompt by clicking 'bypass this step'
        browser.find_element_by_css_selector('.picker > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > label:nth-child(3) > input:nth-child(1)').click()                                    
        print('time to create posting for subregion %i') % (subregion_count)
    
##############
# data entry #
##############

def data_entry(region, email_address, title, body_text, zip_code):
    '''
    calls open_body_text() function to get to data entry fields
    selects and inputs arguments to fill in fields
    submits arguments and posts on local craigslist
    outputs the zip and date of when it was posted
    '''
    import datetime
    print('data_entry function begun')

    
    # select first email entry field
    email_field = browser.find_element_by_css_selector('#FromEMail')
    email_field.click()

    # enter email
    email_field.send_keys(email_address) # pass string to send keys method
    print('email entered')

    # select second
    email_field_2 = browser.find_element_by_css_selector('#ConfirmEMail')
    email_field_2.click()
    
    # enter email
    email_field_2.send_keys(email_address) # pass string to send keys method
    print('email address entered')
    
    # select title field
    title_field = browser.find_element_by_css_selector('#PostingTitle')
    title_field.click()
    
    # post title
    title_field.send_keys(title)
    print('title entered')
    # select body field
    body_field = browser.find_element_by_css_selector('#PostingBody')
    body_field.click()
    
    # post body and link
    body_field.send_keys(body_text + '\n\n' + link) 
    print('message body and link entered')
    
    #select postal code field
    zip_field = browser.find_element_by_css_selector('#postal_code')
    zip_field.click()

    # post zip code
    zip_field.send_keys(zip_code)    
    print('zip code posted')
    
    # hit 'do not show on maps' button    
    try:
        browser.find_element_by_css_selector('#wantamap').click()
    except:
        pass
    
    # hit submit button to post data
    browser.find_element_by_css_selector('.bigbutton').click()
    
    # hit submit button to not post images
    browser.find_element_by_css_selector('.done').click()    

    # log information to output    
    todays_date = datetime.date.fromordinal(730918).strftime('%m/%d/%y')
    
    # log date of posting
    f_out.write(str(todays_date))
    print('date written to file: %s') % (todays_date)
    f_out.write(str(posting_day) + ',' + str(renewal_group) + ',' + str(region) + ',' + str(state) + ',' + \
                str(zip_code) + ',' + str(name) + ',' + str(email_address) + ','  + str(title) + ',' + \
                str(body_text) + ',' + str(link) + '\n')
    print('all input information posted to output file')
    print('need to add confirmation link to file')

    # hit final submit button
    try:    
        browser.find_element_by_css_selector('.bigbutton').click() # add .click() to this to finish posting
        print('bigbutton css element found')
    except:
        browser.find_element_by_css_selector('.button').click()
        print('button css element found')
    else:
        pass
    print('%s posted') % (region)






import csv
from selenium import webdriver
import time

browser = webdriver.Firefox() # define browser object

f_in = open("C:\\Users\\Zachary\\OneDrive\\Documents\\4. Technical\\Programming\\Python\\Arianna's CEO postings\\input\\day_1.csv", 'r')
data = csv.DictReader(f_in)

f_out = open("C:\\Users\\Zachary\\OneDrive\\Documents\\4. Technical\\Programming\\Python\\Arianna's CEO postings\\output\\day_1.csv", 'w')
f_out.write('posting_date,posting_day,renewal_group,region,state,zip,name,email,title,body,posting_link,confirmation_link\n')

for row in data:
    region = row['Region'] # originally had this with a .lower() method but link text is case specific in selenium apparently
    state = row['State'].lower()
    zip_code = row['Zip']
    email_address = row['Emails'].lower()
    body_text = row['Body']
    link = row['Posting Link']
    title = row['Title']
    posting_day = row['Posting Day']
    renewal_group = row['Renewal Group'] 
    name = row['Name'].lower()
    
    
    print('navigating to %s dialogue') % (region)
    webnav_to_region(region)
    
    print('webnav_to_region function complete, passing arguments to data_entry function')    
    data_entry(region, email_address, title, body_text, zip_code)
    print('data entry function for %s complete') % (region)
    print('**************')
    time.sleep(1)

browser.quit()
f_in.close()
f_out.close()
print('posting complete. congrats!')





##############################################
# store confirmation information in csv file #
##############################################

# confirmation renewals
'''
open link in new window
click renew posting link
checks to see if there is no post to renew to see if the post been flagged or deleted
if flagged or deleted, fills a cell in output
'''
#f_in = open("C:\Users\Zachary\python_scripts\craigslist_test_output.csv", 'r')
#data = csv.DictReader(f_in)
#f_out = open("C:\Users\Zachary\python_scripts\renewal_tracker.csv", 'w')
#
#for row in data:
#    email_address = row['email'].lower()
#    region = row['region'].lower()
#    state = row['state'].lower()
#    postcode = row['zip']
#    confirmation_link = row['confirmation_link'].lower()
#    posting_day = row['posting_day']
#    renewal_day = row['renewal_day']
#    renewal_flag = row['renewal_flag']
#    
#    # open link in new window
#    browser.get(confirmation_link) #opens webpage with get() method on browser object
#    print('loading %s confirmation link') % (region)
#    f_out.write(str(email_address) + ',' + str(region) + ',' + str(state) + ',' + str(postcode) + ',' + str(confirmation_link) + \
#                str(posting_day))
#    print('written to file: %s, %s, %s, %s, %s, %s') % (email_address, region, state, postcode, confirmation_link, posting_day)    
#
#    # is there a post to renew?
#    try:
#        browser.find_element_by_css_selector('RENEWAL POSTING CSS THING').click() # click renew posting link
#        f_out.write('posting confirmed')
#    except:
#        # if no, fills a cell in output
#        f_in.write('no renewal posting found')
#        
#f_in.close()
#print('renewals complete')
