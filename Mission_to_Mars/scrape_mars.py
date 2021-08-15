from bs4 import BeautifulSoup as soup 
from splinter import Browser
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def mars_news(browser):

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)

    html = browser.html
    news_soup = soup(html, "html.parser")

    try:
        slide_elem = news_soup.select_one("div.list_text")
        slide_elem.find("div", class_ = "content_title")

        news_title = slide_elem.find("div", class_ = "content_title").get_text()

        news_p = slide_elem.find("div", class_ = "article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_p

#JPL Mars Space Images - Featured Image

def featured_image(browser):
    featured_image_url = 'https://spaceimages-mars.com'
    browser.visit(featured_image_url)

    full_image_elem = browser.find_by_tag("button")[1]
    full_image_elem.click()

    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

# Mars Facts

# more_info_url = 'https://galaxyfacts-mars.com'
# browser.visit(more_info_url)
# table = pd.read_html(more_info_url)
# df = table[0]
# df.head()

def mars_facts():
    try:
        df= pd.read_html("https://galaxyfacts-mars.com")[0]
    except BaseException:
        return None 
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace= True)
    return df.to_html(classes= "table table-striped")

# Mars Hemispheres

def hemisphere(browser):
    # Visit the USGS Astrogeology Science Center Site
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    hemisphere_image_urls = []

    # Get a List of All the Hemisphere
    links = browser.find_by_css('a.product-item img')

    # Next, loop through those links, click the link, find the sample anchor, return the href
    for i in range(len(links)):
        hemisphere = {}
    
        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css('a.product-item img')[i].click()
    
        # Next, we find the Sample image anchor tag and extract the href
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
    
        # Get Hemisphere title
        hemisphere['title'] = browser.find_by_css('h2.title').text
    
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere)
    
        # Finally, we navigate backwards
        browser.back()
    return hemisphere_image_urls


# Helper Function
def scrape_hemisphere(html_text):
    hemisphere_soup = soup(html_text, "html.parser")
    try: 
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        sample_element = None 
    hemisphere = {
        "title": title_element,
        "img_url": sample_element
    }
    return hemisphere

# Main Web Scraping Bot
def scrape_all():
   # executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', executable_path = 'chromedriver', headless=True)
    news_title, news_p = mars_news(browser)
    img_url = featured_image(browser)
    facts = table
    hemisphere_image_urls = hemisphere(browser)

    data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": img_url,
        "facts": table,
        "hemispheres": hemisphere_image_urls,
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())
