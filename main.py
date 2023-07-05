# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 23:17:05 2023

@author: Oreoluwa
"""

import streamlit as st
from bs4 import BeautifulSoup
import requests

st.title("Jumia web scraper")
st.subheader("Find the cheapest laptop available for the selected options")

laptop = st.selectbox("Select the brand of laptop you want to find.", ("","Dell","HP"))
ram = st.selectbox("Select the RAM you want.", ("","4gb","8gb","16gb"))

small_dict = {}
big_dict = {}
name =[]
price = []  
links = []
url = f"https://www.jumia.com.ng/catalog/?q={laptop}+{ram}+ram"
results = requests.get(url).text
doc = BeautifulSoup(results,"html.parser")


#Finding the number of pages to be searched
page_div = doc.find(class_ = "pg-w -ptm -pbxl")
last_page = str(page_div.find_all(class_ = "pg")[-1]).split("#")[0].split("=")[-1]
last_page = int(last_page)


#Searching all the pages
for page in range(1,last_page+1):
    url = f"https://www.jumia.com.ng/catalog/?q={laptop}+{ram}+ram&page={page}#catalog-listing"
    results = requests.get(url).text
    doc = BeautifulSoup(results,"html.parser")
    
    
    #Accessing the name of the products and the prices
    big_div = doc.find(class_ = "-paxs row _no-g _4cl-3cm-shs")
    small_divs = big_div.find_all(class_ = "prd _fb col c-prd")
    
    
    #Extracting the prices, type casting them and storing the prices in a list
    for i in small_divs:
        temp_price_string = i.find(class_ = "prc").string
        temp_price_string = temp_price_string.replace("₦","")
        temp_price_string = temp_price_string.replace(",","")
        temp_price_string = temp_price_string.split("-")[-1]
        temp_price_string = temp_price_string.replace(" ","")
        price_int = int(temp_price_string)
        price.append(price_int)
        
    
    
   
    
  
    
#Storing the names of the products in a list 
for i in range(1,len(small_divs)): 
    name.append(small_divs[i].a['data-name'])
    links.append(small_divs[i].a['href']) 
    



#Creating a dictionary with the links as keys and a list of prices and names as the values
for i in range(0,len(name)):
    big_dict[links[i]] = [price[i],name[i]]
    
    

#Sorting the dictionary
sorted_dict = dict(sorted(big_dict.items(),key = lambda x:x[1]) )



#Finding the attributes of the cheapest laptop
cheapest_link = (list(sorted_dict.keys())[0])
cheapest_price = list(sorted_dict.values())[0][0]
cheapest_name = list(sorted_dict.values())[0][1]


#Printing out the attributes
st.write(f"The lowest price available for a {ram} {laptop} laptop is:")
st.write(f" Name: {cheapest_name}")
st.write(f"Price: {cheapest_price}")
link = f"Link: [link](jumia.com.ng{cheapest_link})"
st.markdown(f'''<a href={link}><button style="background-color:GreenYellow;">Link</button></a>)


