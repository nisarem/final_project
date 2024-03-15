#!/usr/bin/env python
# coding: utf-8

# In[14]:


#pip install letterboxdpy
#pip install -U rottentomatoes-python


# In[15]:


import pandas as pd
import pickle
import requests
from bs4 import BeautifulSoup
from scrapy import Selector
from pandas import json_normalize

import rottentomatoes as rt
from json import (
  JSONEncoder,
  dumps as json_dumps,
  loads as json_loads,
)


# ## First try: Webscraping Rotten Tomatoes for Movie Reviews

# Although my attempts for writing a function to extract reviews of a movie by taking the movie's page as an argument was successful, I realised that the links for movies in rotten tomatoes are not consistent. 
# 
# __For example:__
# 
#  - Dune: Part Two (2024) link : https://www.rottentomatoes.com/m/dune_part_two (seems reasonable)
#  - Dune (2021) link : https://www.rottentomatoes.com/m/dune_2021 (getting weird)
#  - https://www.rottentomatoes.com/m/dune --> link for the miniseries Dune (2000) directed by John Harrison

# In[16]:


#first try for webscraping for movie reviews: rotten tomatoes
#rt = 'https://www.rottentomatoes.com/m/dune_part_two/reviews?type=top_critics'
#req = requests.get(rt)
#res = req.content
#soup1 = BeautifulSoup(res, 'html.parser')


# In[17]:


#function for extracting reviews
def get_comments_rt(url,n=20):
    try:
        response = requests.get(url)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the review table
            review_table = soup.find("div", class_="review_table")
            
            # If review table exists, find all review text elements
            if review_table:
                review_texts = review_table.find_all("p", class_="review-text")
                
                # Extract the text of the first 20 reviews or all available comments if less than 20
                comments = []
                for i, review_text in enumerate(review_texts):
                    if i == n:
                        break
                    comments.append(review_text.get_text(strip=True))
                
                return comments
            else:
                print("Review table not found.")
                return None
        else:
            print("Failed to retrieve page. Status code:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None


# In[18]:


#function trial
#n = 10
#comments = get_comments_rt(rt,n)
#if comments:
#    print(f"First {n} comments:")
#    for i, comment in enumerate(comments, 1):
#        print(f"{i}. {comment}")
#else:
#    print("No comments found.")


# In[19]:


#len(comments)


# Unfortunately there were no way to standardize the link of the movies chosen from which I would extract the reviews. So I decided to look elsewhere. 

# ## Second try: Webscraping Letterboxd for Movie Reviews

# I chose to try webscraping Letterboxd for reviews, because:
# 
# 1. Letterboxd is a commonly used platform for movie reviews. It also has feature for its users to like other user's comments. I can use the most popular reviews to evaluate the movie by simply sorting the reviews by their likes. 
# 2. Letterboxd uses TMDb api which is free and public. I have access to that api as well, so I try to find a common way to identify movies and their page links for Letterboxd. 
# 
# I though I had the same link problem with Letterboxd until I ran into this link: 
# https://letterboxd.com/about/film-data/
# 
# The page explains that the format 'https://letterboxd.com/tmdb/{tmdb_film_id}' redirects to the movie's Letterboxd page. I then decided to create a class for review extraction for the movies by using the movies' TMDb ID. 
#  

# In[25]:


class Scraper:

    def __init__(self, domain: str):
        self.base_url = domain
        self.headers = {
            "referer": domain,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        self.builder = "lxml"

    def get_parsed_page(self, path: str) -> BeautifulSoup:
        #gets the soup of the page in a given path
        url = self.base_url + path
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raises an error for non-200 status codes
        except requests.RequestException as e:
            raise Exception(f"Error connecting to {url}: {e}")

        try:
            dom = BeautifulSoup(response.text, self.builder)
        except Exception as e:
            raise Exception(f"Error parsing response from {url}: {e}")

        if response.status_code != 200:
            message = dom.find("section", {"class": "message"})
            message = message.strong.text if message else None
            messages = json.dumps({
                'code': response.status_code,
                'reason': str(response.reason),
                'url': url,
                'message': message
            }, indent=2)
            raise Exception(messages)
        return dom
            
    def get_link(self) -> str:
        #gets the link from a letterboxd movie page
        url = self.base_url
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raises an error for non-200 status codes
        except requests.RequestException as e:
            raise Exception(f"Error connecting to {url}: {e}")
    
        try:
            dom = BeautifulSoup(response.text, self.builder)
            cont = dom.select_one("head > meta[property='og:url']")
            if cont:
                link = cont['content']
            else:
                raise Exception("Meta tag 'og:url' not found.")
        except Exception as e:
            raise Exception(f"Error parsing response from {url}: {e}")
        return link
    
    def extract_reviews(self, soup: BeautifulSoup, num_reviews: int = 12) -> list:
        reviews = []
        film_details = soup.find_all('li', class_='film-detail')
        for film_detail in film_details:
            spoilers_div = film_detail.find('div', class_='hidden-spoilers expanded-text')
            if spoilers_div:
                review_text = spoilers_div.text.strip()
            else:
                review_text = film_detail.find('div', class_='body-text -prose collapsible-text').text.strip()
            reviews.append(review_text)
            if len(reviews) == num_reviews:  # Break if the desired number of reviews is reached
                break
        return reviews


# In[26]:


#lttx = 'https://letterboxd.com/tmdb/27205'


# In[29]:


def get_reviews_from_link(domain: str, num_reviews: int = 12) -> list:
    scraper = Scraper(domain)
    link = scraper.get_link()
    scraper = Scraper(link)
    path = 'reviews/by/activity/'
    dom = scraper.get_parsed_page(path)
    return scraper.extract_reviews(dom, num_reviews)


# In[ ]:





# In[30]:


#reviews = get_reviews_from_link(lttx, num_reviews=10)
#display(reviews)


# ### EUREKA !!!

# Here is my attempts and drafts to write this code:

# In[11]:


# a = Scraper(lttx)
# rew_link = a.get_link()
# b = Scraper(rew_link)
# path = 'reviews/by/activity/'
# dom = b.get_parsed_page(path)
# revi = b.extract_reviews(dom)


# In[12]:


# def extract_reviews(soup):
#     reviews = []
    
#     film_details = soup.find_all('li', class_='film-detail')
#     for film_detail in film_details:
#         spoilers_div = film_detail.find('div', class_='hidden-spoilers expanded-text')
#         if spoilers_div:
#             review_text = spoilers_div.text.strip()
#         else:
#             review_text = film_detail.find('div', class_='body-text -prose collapsible-text').text.strip()
#         reviews.append(review_text)
#     return reviews



# extracted_reviews = extract_reviews(dom)
# print(extracted_reviews)


# In[ ]:


# texts = []

# film_details = dom.find_all('li', class_='film-detail')
# for film_detail in film_details:
#       spoilers_div = film_detail.find('div', class_='hidden-spoilers expanded-text')
#     if spoilers_div:
#         text = spoilers_div.text.strip()
#     else:
#         text = film_detail.find('div', class_='body-text -prose collapsible-text').text.strip()
#     texts.append(text)

# display(texts)


# In[ ]:





# In[23]:


bechreq = requests.get("http://bechdeltest.com/api/v1/getAllMovies")
bechreq.text


# In[22]:





# In[ ]:




