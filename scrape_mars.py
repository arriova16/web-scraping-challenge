from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager

def mars_scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    news_soup = soup(html, 'html.parser')
    time.sleep(1)
    mars_news_result = news_soup.find_all('div', class_='list_text')[0]
    news_title = mars_news_result.find('div', class_='content_title').text
    news_p = mars_news_result.find('div', class_='article_teaser_body').text
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    spaceimage_soup = soup(html, 'html.parser')
    spaceimage_soup_result = spaceimage_soup.find_all('div', class_='floating_text_area')[0]
    featured_image_url = spaceimage_soup_result.find('a', class_='showimg fancybox-thumbs').get('href')
    featured_image_url = url + featured_image_url
    mars_table = pd.read_html('https://galaxyfacts-mars.com/')[1]
    mars_table.columns = ['Description', 'Metrics']
    mars_table_html = mars_table.to_html()
    # browser.find_by_css('a.product-item img')[0].click()
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')
    hemisphere_img_list = hemisphere_soup.find_all('a', class_='itemLink product-item')
    hrefs = []
    for img_url in hemisphere_img_list:
        hrefs.append(img_url.get('href'))
    hrefs = hrefs[:-1]
    hrefs = list(set(hrefs))
    hemisphere_image_urls = []
    for img_url in hrefs:
        secondary_link = url + img_url
        browser.visit(secondary_link)
        time.sleep(2)
        html = browser.html
        secondary_link_soup = soup(html, 'html.parser')
        final_url = secondary_link_soup.find('a', text = 'Sample').get('href')
        final_url = url + final_url
        img_title = secondary_link_soup.find('h2', class_='title').text
        img_title = img_title.replace(' Enhanced', '')
        d = {"title": img_title, "img_url": final_url}
        hemisphere_image_urls.append(d)
    browser.quit()
    mars_dictionary = {"news_title": news_title, 
                        "news_p": news_p,
                        "featured_image_url": featured_image_url,
                        "mars_table": mars_table_html,
                        "hemispheres": hemisphere_image_urls}
    return mars_dictionary