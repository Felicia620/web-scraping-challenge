from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless = False)

def scrape():
    browser = init_browser()
    mars_dict = {}

    url = "https://redplanetscience.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    latest_news_title = soup.find("div", class_ = "content_title").text
    
    latest_news_paragraph = soup.find("div", class_ = "article_teaser_body").text

    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    featured_image_url = "https://spaceimages-mars.com/image/featured/mars1.jpg"
    browser.visit(featured_image_url)

    url = "https://galaxyfacts-mars.com/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    mars_facts_table = pd.read_html(url)[1]
    df = mars_facts_table
    html_table = df.to_html()

    url = "https://marshemispheres.com/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    hemisphere_image_urls = []

    links = browser.find_by_css("a.product-item img")

    for i in range(len(links)):
    
        hemisphere = {}
    
        browser.find_by_css("a.product-item img")[i].click()

        sample = browser.links.find_by_text("Sample").first
        hemisphere["img_url"] = sample["href"]
    
        hemisphere["title"] = browser.find_by_css("h2.title").text
    
        hemisphere_image_urls.append(hemisphere)
    
        browser.back()

    mars_data = {
        "latest_news_title": latest_news_title,
        "latest_news_paragraph": latest_news_paragraph,
        "featured_image_url": featured_image_url,
        "html_table": html_table,
        "hemisphere_image_urls": hemisphere_image_urls}
    
    browser.quit()

    return mars_data