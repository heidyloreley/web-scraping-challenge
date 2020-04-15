# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd

#Create function to scrape with splinter whenever is necessary
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

#Create function to run that will execute all scraping code and return one Python dictionary containing all of the scraped data.
def scrape():
    
# 1. MARS NEWS SITE
    
    #Get information from NASA web page
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    
    # Create BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')

    # News Title and Parragraph
    news_title = soup.find("div",class_="content_title").text
    news_p = soup.find("div", class_="rollover_description_inner").text 

# 2. JPL MARS SPACE IMAGE
    browser = init_browser()

    #Scrape information from JPL web page and inside second page
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.find_by_id('full_image').first.click()
    browser.links.find_by_partial_text('more info').first.click()
    html = browser.html

    # Create BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve full size image partial link (JPG format) and then full link
    feature_image = soup.find("figure", class_="lede").a["href"]
    featured_image_url ="https://www.jpl.nasa.gov/" + feature_image

    #Close Browser
    browser.quit()

# 3. MARS WEATHER TWEET

    #Get information from TWITTER web page
    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)

    # Create BeautifulSoup object
    soup = BeautifulSoup(response.content, 'html.parser')

    #Get the first Tweet Parragraph
    body_content =soup.body.find("p", class_="tweet-text")

    tweets=[]
    for body in body_content:
        tweets.append(body)

    #Wheater information of latest tweet
    mars_weather=tweets[0]

# 4. MARS FACTS

    #Get table information from SPACE FACTS web page (using pandas)
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)

    #Use fist table found and name its columns
    df=tables[0]
    df.columns = ["Mars characteristics","value"]
    
    #Remove INDEX column
    df.set_index("Mars characteristics", inplace = True)
    
    # Convert Dataframe into HTML code / Replace "new line" brakes with spaces
    html_table = df.to_html()
    html_table.replace('\n', '')


# 5. MARS HEMISPHERES
    browser = init_browser()

    #Scrape information from USGS Astrogeology web page and inside second page
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html

    # Create BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve LIST of 4 links 
    links_path = soup.find_all("div", class_="description")

    Links_to_Click=[]
    for links in links_path:
        partial_link= links.a["href"]
        final_url = "https://astrogeology.usgs.gov/"+partial_link
        Links_to_Click.append(final_url)

    # Get information of each Hemisphere, TITLE and IMAGE URL. Create List of 4 Dictionaries.
    hemisphere_image_urls =[]

    for i in range(len(Links_to_Click)):
        #visit/click new urls
        browser.visit(Links_to_Click[i])
        html2 = browser.html
        soup2 = BeautifulSoup(html2, 'html.parser')

        img_url = soup2.find("div",class_="downloads").a["href"]
        title = soup2.find("h2",class_="title").text

        mars_dict={"title": title,"img_url": img_url}
        hemisphere_image_urls.append(mars_dict)

        # Go back to the original page
        browser.back()

    #Close Browser
    browser.quit()

        
    # Dictionary to save all scraped information
    mars_dict = {"NewsTitle": news_title,
                "NewsDescription":news_p,
                "ImageURL":featured_image_url,
                "Weather":mars_weather,
                "Facts":html_table,
                "Hemispheres":hemisphere_image_urls
                }  

    return mars_dict




