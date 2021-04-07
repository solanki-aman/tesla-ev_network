#!/usr/bin/env python
# coding: utf-8

# # Tesla Supercharger Stations

# ### Aman Solanki

import pandas as pd
import numpy as np
import googlemaps #collect longitude and latitude data
from uszipcode import SearchEngine #collect county data

#data collection
from bs4 import BeautifulSoup
import requests
import re


#tesla website with all supercharger addresses
url = 'https://www.tesla.com/findus/list/superchargers/United+States'

req_headers = {
    'casca'
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 axazs'
}

s = requests.Session()

r = s.get(url, headers=req_headers)
soup = BeautifulSoup(r.content, 'html.parser')


#find address and url of the supercharger
address = soup.find_all('span', attrs={'class': 'street-address'})
locality = soup.find_all('span', attrs={'class': 'locality'})
urlSoup = soup.find_all('a', attrs={'class': 'fn org url'})


#if the address is null, consider it as an upcoming supercharger station
ev_address = []
for i in address:
    if len(i)==0:
        ev_address.append('Coming-Soon')
    if len(i)==1:
        ev_address.append(str(i).split('>')[1].split('<')[0])


#city, state and zipcode of the supercharger
ev_locality = []
for j in locality:
    ev_locality.append(str(j).split('>')[1].split('<')[0])


#url of the specific supercharger
superChargerURL = []
for i in urlSoup:
    text = str(i)
    superChargerURL.append(text.split()[4].split('>')[0].split('=')[1].strip(' " " '))


#transform the collected data into a data frame
tesla_ev = pd.DataFrame()
tesla_ev['Address'] = ev_address
tesla_ev['Locality'] = ev_locality
tesla_ev['URL'] = superChargerURL
tesla_ev['Supercharger_Link'] = 'http://www.tesla.com' + tesla_ev['URL']


#drop incomplete url data
tesla_ev = tesla_ev.drop(['URL'],axis=1)

#considering only California Supercharging Stations
telsaEV_ca = tesla_ev[tesla_ev['Locality'].str.contains('CA')] 


#drop upcoming Supercharing Stations
comingSoonStations = telsaEV_ca[tesla_ev['Address'].str.contains('Coming-Soon')].index

telsaEV_ca = telsaEV_ca.drop(comingSoonStations)

#split city and zipcode data from Locality column
cityList = []
zipCodeList = []
for i in telsaEV_ca['Locality']:
    cityList.append(i.split(',')[0]) 
    
    if i.split()[-1].isnumeric() == True:
        zipCodeList.append(i.split()[-1])
    else:
        zipCodeList.append('0')

    
telsaEV_ca['City'] = cityList
telsaEV_ca['ZipCode'] = zipCodeList

#drop Locality column
telsaEV_ca = telsaEV_ca.drop(columns='Locality')

#append county name based on zipcode
search = SearchEngine(simple_zipcode=True)
countyList = []

for i in telsaEV_ca['ZipCode']:
    date = search.by_zipcode(i)
    dataDict = date.to_dict()
    countyList.append(dataDict['county'])
    
telsaEV_ca['County'] = countyList

#drop any record with missing value
telsaEV_ca = telsaEV_ca.dropna() 

telsaEV_ca.info()

telsaEV_ca.head()

#collect number of stations and charging rate threshold for each supercharger
chargingRateList = []
stationList = []
iteration = 0 
for link in telsaEV_ca['Supercharger_Link']:
    infoList = []
    
    url = link
    print(iteration, ':', link)
    
    req_headers = {
        'casca'
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 axazs'
    }

    s = requests.Session()

    r = s.get(url, headers=req_headers)
    soup2 = BeautifulSoup(r.content, 'html.parser')
    
    superchargerInfo = soup2.find_all('address', attrs={'class': 'vcard'})
    
    temp = superchargerInfo[0].find_all('p')
    
    for i in temp:
        info = i.text
        infoList.append(info)
        
    for i in infoList:
        if 'available 24/7' in i:
            index = infoList.index(i)
    
    stationTemp = infoList[index].split()[0]
    stationNum = re.findall(r'\d+', stationTemp)
    stationList.append(stationNum)
    
    chargingRateTemp = infoList[index].split()[-1]
    chargingRateNum = re.findall(r'\d+', chargingRateTemp)
    chargingRateList.append(chargingRateNum)
    
    iteration+=1
    
telsaEV_ca['ChargingStations'] = stationList
telsaEV_ca['ChargingRate'] = chargingRateList


telsaEV_ca.head()

#clean collected data
telsaEV_ca['ChargingStations'] = telsaEV_ca['ChargingStations'].str[0]
telsaEV_ca['ChargingRate'] = telsaEV_ca['ChargingRate'].str[0]

telsaEV_ca.isnull().sum() #4 missing values

#replace missing values
telsaEV_ca['ChargingStations'] = telsaEV_ca['ChargingStations'].replace(np.nan, '8', regex=True)
telsaEV_ca['ChargingRate'] = telsaEV_ca['ChargingRate'].replace(np.nan, '72', regex=True)

telsaEV_ca.head()


# ## Geocode Data (Google Maps API)


#reset index and create a new column for accurate location data
telsaEV_ca = telsaEV_ca.reset_index(drop=True)
telsaEV_ca['Full_Address'] = telsaEV_ca['Address'] + ', ' + telsaEV_ca['City']


telsaEV_ca['Full_Address'] = telsaEV_ca['Full_Address'].replace('North', 'N', regex=True)
telsaEV_ca['Full_Address'] = telsaEV_ca['Full_Address'].replace('Third', '3rd', regex=True)


#collect longtitude and latitudes based on the full address
gmaps = googlemaps.Client(key='AIzaSyDEtplNYD9h74Qu8F8Sq7DhudfsgA6KHlI') 

latList = []
lngList = []
iteration = 0

for i in telsaEV_ca['Full_Address']:
    print(iteration)
    geocode_result = gmaps.geocode(i)
    latList.append(geocode_result[0]['geometry']['location']['lat'])
    lngList.append(geocode_result[0]['geometry']['location']['lng'])
    iteration+=1
    
telsaEV_ca['Longitude'] = latList
telsaEV_ca['Latitude'] = lngList

telsaEV_ca.head()

telsaEV_ca = telsaEV_ca.drop(columns='Full_Address')

telsaEV_ca.to_csv("telsaEV_ca.csv")

telsaEV_ca = telsaEV_ca.drop(columns='Supercharger_Link')

telsaEV_ca.to_csv("telsaEV_ca.csv")

telsaEV_ca.head()




