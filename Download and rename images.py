import requests
from bs4 import BeautifulSoup
import pandas as pd
import xlsxwriter
import re
from openpyxl import load_workbook
from datetime import datetime
import os
from os.path  import basename
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

image_list = []
df = pd.read_excel('/Users/janiceteo/Documents/YoRipe/Commune Kitchen/CommuneKitchen.xlsx', 'Sheet1')
for r in range(len(df)):
    pageResponse = requests.get(df['RecipeURL'][r], headers = headers)
    html_page = BeautifulSoup(pageResponse.text, 'html.parser')
    imageURL = 'https://www.communekitchen.com' + html_page.find('div', class_="wsite-image wsite-image-border-none ").find('a').img['src']
    if imageURL is not None:
        JPEGstart = imageURL.rfind('/') + 1
        currentImageID = imageURL[JPEGstart:]
        os.chdir('/Users/janiceteo/Documents/YoRipe/Commune Kitchen/')
        with open(basename(imageURL), "wb") as f:
            f.write(requests.get(imageURL).content)
        newImageID = 'CommuneKitchen' + df['recipename'][r].replace(" ","") + ".jpg"
        os.rename(currentImageID, newImageID)
    else:
        newImageID = ""
    image_list.append(newImageID)
os.chdir('/Users/janiceteo/Documents/YoRipe/Commune Kitchen/')
df = pd.DataFrame({'imageID': image_list})
writer = pd.ExcelWriter('communeKitchenImages.xlsx',engine='xlsxwriter',options={'strings_to_urls': False})
df.to_excel(writer, 'Sheet1', index = False)