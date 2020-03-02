#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Install dependencies
import pandas as pd
import os
from bs4 import BeautifulSoup
import requests
from pprint import pprint
import json


# In[2]:


# URL's of pages to be scraped
# NASA news web page = "https://mars.nasa.gov/news/"
nasa_news_url = "https://mars.nasa.gov/api/v1/news_items/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&blank_scope=Latest"
jpl_images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
jpl_base = "https://www.jpl.nasa.gov"
mars_weather_url = "https://twitter.com/marswxreport?lang=en"
mars_facts_url = "http://space-facts.com/mars/"
usgs_images_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"


# In[3]:


# Response function to use requests
def response(url):
    response = requests.get(url)
    return response


# Function to write response infomration to file
def open_file(file_name, response):
    with open(file_name, "w+") as write_file:
        json.dump(response, write_file)


# In[4]:


# Mars news scrape -we will use the JSON response from the news page.  "https://mars.nasa.gov/api/v1/news_items/*
# This is an API and returns a nested JSON with all the information we need (title, short description, etc.)


# In[5]:


mars_news_json = response(nasa_news_url).json()


# In[6]:


# The code below was sourced from https://hackersandslackers.com/extract-data-from-complex-json-python/
# It extracts nested data from a complex JSON
def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results


# In[7]:


titles = extract_values(mars_news_json, "title")


# In[8]:


# Extract the most recent title.  They are in order from newest to oldest in the titles list
news_title = titles[0]


# In[9]:


# Bonus return the short paragrapgh text "description"
descriptions = extract_values(mars_news_json, "description")
print(descriptions[0])


# In[10]:


# Get URL for Featured JPL Mars IMage
mars_image_text = response(jpl_images_url).text


# In[11]:


soup = BeautifulSoup(mars_image_text, "lxml")
footer_tag = soup.footer.a.attrs


# In[12]:


# Get the url for the featured image on the JPL Mars page
img_url = footer_tag["data-fancybox-href"]
featured_image_url = jpl_base + img_url


# In[13]:


# get the latest Mars weather from twitter
mars_twitter_text = response(mars_weather_url).text


# In[14]:


soup = BeautifulSoup(mars_twitter_text, "lxml")
mars_weather = soup.find(class_="tweet-text").get_text()


# In[15]:


# get mars facts from space-facts.com using pandas


# In[16]:


dfs = pd.read_html(mars_facts_url, header=None)[0].rename(
    columns={0: "description", 1: "value"}
)


# In[17]:


# Convert string to dataframe
mars_facts_df = pd.DataFrame(dfs)


# In[18]:


# Get mars hemisphere images from usgs
mars_usgs_text = response(usgs_images_url).text
astro_usgs_base_url = "https://astrogeology.usgs.gov"


# In[19]:


soup = BeautifulSoup(mars_usgs_text, "lxml")
mars_usgs_tags = soup.find_all(class_="itemLink product-item")


# In[20]:


# Get names of thumbnail images
h3_tags = soup.find_all("h3")
titles = [t.text for t in h3_tags]


# In[21]:


# Get link to site for full size image page
hrefs_link_page = [(astro_usgs_base_url + t.attrs["href"]) for t in mars_usgs_tags]


# In[22]:


# assign the image urls to a list.  These will be used by Requests to get the high res image link
image_urls = [
    hrefs_link_page[0],
    hrefs_link_page[1],
    hrefs_link_page[2],
    hrefs_link_page[3],
]


# In[23]:


def get_high_res_link(url):
    high_res_images = response(url).text
    soup = BeautifulSoup(high_res_images, "lxml")
    link = soup.find_all(target="_blank")[0]["href"]
    return link


# In[24]:


# Use Requests to go to each image_url page and get the link to the high res image
img_url = []
for i in image_urls:
    img_url.append(get_high_res_link(i))


# In[25]:


# Convert lists to dicts with title and img_url as keys
# Append the dictionary with the image url string and the hemisphere title to a list.
hemisphere_images = [
    {"title": titles[i], "img_url": img_url[i]} for i in range(len(img_url))
]


# In[ ]:


# In[ ]:


# In[ ]: