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
    
    # check if the nearest area prompt comes up    
    if browser.find_element_by_xpath("//*[contains(text(), 'choose nearest area')] | //*[@value='choose nearest area']"):
        print('subregions found')
        print('looking for number of subregions')
        i = 0
        # choose nearest area
        # select first choice
        # assume no more than seven subregions
        # determine how many subregions there are
        for subregion in range(1, 15, 2): # subregion identifiers come in odd numbers only
            try:
                browser.find_element_by_css_selector('.picker > blockquote:nth-child(1) > label:nth-child(' + \
                                                    str(subregion) + ') > input:nth-child(1)')
                i += 1
                print('subregion %i found') % (i)

                print('looking for another') % (i)
            except:
                pass
        print('no more subregions to log, proceeding to select subregion')
        print('number of subregions is: ' + str(i))
#        webnav_to_subregion(region, i) # use this function to select subregions
        # I've rerouted this because I don't need to post to all subregions in a given area
        # Posts still show up in the larger area if they are in any of the subregions
        
    else:
        print('no subregions, proceeding to post information')
        
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
    todays_date = datetime.date.fromordinal(730920).strftime('%m/%d/%y')
    
    # log date of posting
    f_out.write(str(todays_date))
    print('date written to file: %s') % (todays_date)

    # hit final submit button    
    browser.find_element_by_css_selector('.bigbutton') # add .click() to this to finish posting
    
    # feedback prints
    print('%s posted') % (region)



##########################
# store region posted to #
##########################


##############################################
# store confirmation information in csv file #
##############################################
'''
dtg of posting
url for confirmation
if it needs a phone number
'''


############################################################
# forward all confirmation emails to central email address #
############################################################





import csv
from selenium import webdriver
import time

browser = webdriver.Firefox() # define browser object


f_in = open("C:\Users\Zachary\python_scripts\craigslist_test.csv", 'r')
data = csv.DictReader(f_in)

f_out = open("C:\Users\Zachary\python_scripts\craigslist_test_output.csv", 'w')
f_out.write('email,region,zip,date,confirmation_link\n')


for row in data:
    email_address = row['email'].lower()
    region = row['region'].lower()
    zip_code = row['zip']
    link = row['link']
    title = row['title']
    body_text = row['body']
    
    print('writing: %s, %s, %s to file') % (email_address, region, zip_code)
    f_out.write(str(email_address) + ',' + str(region) + ',' + str(zip_code)) # still to post: date, confirmation link provided by craigslist
    print('%s, %s, %s, written to file') % (email_address, region, zip_code)

    print('navigating to %s dialogue') % (region)
    webnav_to_region(region)
    
    print('webnav_to_region function complete, passing arguments to data_entry function')    
    data_entry(region, email_address, title, body_text, zip_code)
    print('data entry function for %s complete') % (region)
    print('**************')
    time.sleep(3)

browser.quit()
f_in.close()
f_out.close()
print('program complete. congrats!')
