from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
import re
import pandas as pd
import time

def scrape():
    #Initialize PyMongo to work with MongoDBs
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    #Define database and collection
    db = client.mars_db

    #Setup for splinter
    executable_path = {'executable_path': '../For Submission/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    #Website to scrape with BeautifulSoup
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    html = browser.html
    soup = bs(html, 'html.parser')

    #Pull info needed from page as list
    results_text = soup.find_all('div',class_="content_title")
    news_title = results_text[1].text
    print(news_title)

    #Pull info needed from page as list
    para_text = soup.find('div',class_="article_teaser_body")
    news_p = para_text.text
    print(news_p)

    #Website to scrape with BeautifulSoup
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')

    #Pull image url
    image_result = jpl_soup.find('article')['style'].replace("background-image: url('",'').replace("');",'')
    image_url= "https://www.jpl.nasa.gov" + image_result
    print(image_url)

    #Website to scrape with BeautifulSoup
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    time.sleep(5)
    twitter_html = browser.html
    twitter_soup = bs(twitter_html, 'html.parser')
    twitter_results = twitter_soup.find_all(text=re.compile("InSight"))
    mars_weather = twitter_results[0]
    print(mars_weather)

    #Website to scrape with BeautifulSoup
    facts_url = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(facts_url)
    facts_df = pd.DataFrame(facts_table[0])
    facts_df.columns = ["Description","Value"]
    facts_df.set_index("Description", inplace=True)
    html_table = facts_df.to_html(header=False)
    print(html_table)

    #Website to scrape with BeautifulSoup
    astrog_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astrog_url)
    astrog_html = browser.html
    astrog_soup = bs(astrog_html, 'html.parser')

    #Parse results and scrape titles and img links
    astrog_results = astrog_soup.find_all('div',class_="description")
    hemisphere_image_urls = []
    for result in astrog_results:
        
        #Add title to dictionary
        title = result.h3.text.replace(" Enhanced","")
        
        #Add url for full size image to dictionary
        browser.visit("https://astrogeology.usgs.gov/" + result.a['href'])
        nested_html = browser.html
        nested_soup = bs(nested_html, 'html.parser')
        nested_results = nested_soup.find('img',class_="wide-image")
        link = "https://astrogeology.usgs.gov" + nested_results['src']
        
        #Add dictionary to list
        hemisphere_image_urls.append({"title":title,"img_url":link})

    print(hemisphere_image_urls)

    # Create dictionary with scraped data
    final_dict={"news_title": news_title,
            "news_p": news_p,
            "featured_img_url": image_url,
            "mars_weather": mars_weather,
            "hemisphere_img_urls": hemisphere_image_urls,
            "html_table":html_table}
    print(final_dict)

    browser.quit()

    return final_dict

