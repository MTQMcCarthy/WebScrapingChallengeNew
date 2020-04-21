#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies sopied in from other notebook and repo
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import os
import time
import requests


# In[2]:


# Set the directory where chromedriver exists
executable_path = {'executable_path':'C:/bin/chromedriver.exe'} 
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit Nasa news url 
url = "https://mars.nasa.gov/news/"
browser.visit(url)


# In[4]:


jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(jpl_url)
time.sleep(1)
browser.click_link_by_partial_text('FULL IMAGE')
time.sleep(1)
expand = browser.find_by_css('a.fancybox-expand')
expand.click()
time.sleep(1)

jpl_html = browser.html
jpl_soup = bs(jpl_html, 'html.parser')

img_relative = jpl_soup.find('img', class_='fancybox-image')['src']
image_path = f'https://www.jpl.nasa.gov{img_relative}'
print(image_path)


# In[5]:


# HTML Object
html = browser.html

# Parse HTML with Beautiful Soup
soup = bs(html, 'html.parser')

# Retrieve the latest element that contains news title and news_paragraph
news_title = soup.find('div', class_='content_title').find('a')
news_p = soup.find('div', class_='article_teaser_body').text

# Display scraped data 
print(news_title)
print(news_p)


# In[6]:


# JPL Mars Space Images - Featured Image
featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(featured_image_url)


# In[7]:


# HTML Object 
html_image = browser.html

# Parse HTML with Beautiful Soup
soup = bs(html_image, "html.parser")

# Retrieve background-image url from style tag 
image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

# Website Url 
main_url = "https://www.jpl.nasa.gov"

# Concatenate website url with scraped route
image_url = main_url + image_url

# Display full link to featured image
image_url


# In[8]:


# Mars Weather
# Visit Mars Weather Twitter through splinter module
weather_url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(weather_url)

time.sleep(1)


# In[9]:


# HTML Object 
html_weather = browser.html

# Parse HTML with Beautiful Soup
soup = bs(html_weather, 'html.parser')

# Find all elements that contain tweets
latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

# Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. 
# Save the tweet text for the weather report as a variable called mars_weather
 
for tweet in latest_tweets: 
    mars_weather = tweet.find('p').text
    if 'Sol' and 'pressure' in mars_weather:
        print(mars_weather)
        break
    else: 
        pass


# In[10]:


# Mars facts
url = "https://space-facts.com/mars/"
browser.visit(url)

# Use Pandas to "read_html" to parse the URL
tables = pd.read_html(url)

# Find Mars Facts DataFrame in the lists of DataFrames
df = tables[1]

# Assign the columns
df.columns = ['Description', 'Value']
html_table = df.to_html(table_id="html_tbl_css",justify='left',index=False)
data = df.to_dict(orient='records') 
df


# In[11]:


# Save html to folder and show as html table string
mars_df = df.to_html(classes = 'table table-striped')
print(mars_df)


# In[12]:


# Mars Hemispheres
# Visit hemispheres website through splinter module 
hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hemispheres_url)


# In[13]:


# HTML Object
html_hemispheres = browser.html

# Parse HTML with Beautiful Soup
soup = bs(html_hemispheres, 'html.parser')
# Retreive all items that contain mars hemispheres information
items = soup.find_all('div', class_='item')

# Create empty list for hemisphere urls 
hemisphere_image_urls = []

# Store the main_ul 
hemispheres_main_url = 'https://astrogeology.usgs.gov'

# Loop through the items previously stored -- for some reason this gave me trouble but 
for i in items: 
    # Store title
    title = i.find('h3').text
    
    # Store link that leads to full image website
    partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
    # Visit the link that contains the full image website 
    browser.visit(hemispheres_main_url + partial_img_url)
    
    # HTML Object of individual hemisphere information website 
    partial_img_html = browser.html
    
    # Parse HTML with Beautiful Soup for every individual hemisphere information website 
    soup = bs( partial_img_html, 'html.parser')
    
    # Retrieve full image source 
    img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
    # Append the retreived information into a list of dictionaries 
    hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    

# Display hemisphere_image_urls
hemisphere_image_urls


# In[ ]:




