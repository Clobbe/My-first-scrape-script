#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import unicodecsv as csv

url_base ="http://wwww.cafekartan.se"
city = "/Göteborg/Inom_Vallgraven/?sida="
page_num = 1

store = ['StoreTitle,StoreAdress,StoreTele,']

#loop start
while (page_num < 35):

	url = url_base + city + str(page_num)

	print url

	r = requests.get(url)

	soup1 = BeautifulSoup(r.content, "lxml")
	stores = soup1.find_all("h3") #hämta alla h3-taggar

	num_entities = int(len(stores) - 1)  #antal objekt i array:n

	del stores[num_entities]

	i = 0

	while i < num_entities:
		j = str(stores[i])
		j = j[j.find("/"):] #hitta vilken plats i  "/" finns
		j = j[:j.find("\"")] #hitta vilken plats i  " " "  finns
		stores[i] = j #ersätt tidigare värdet i listan med det nya
		i = i + 1
		# print stores[i]

	num_entities = int(len(stores))


	time.sleep(5) #paus i 5 sekunder

	i = 0
	
	while i < num_entities:
		store_url = url_base + stores[i] #skapa ny url
		get_html = requests.get(store_url) #hämta url
		soup_store = BeautifulSoup(get_html.content, "lxml") #spara ned html

		store_title = soup_store.find_all("h1") #hitta alla H1-taggar
		store_title = str(store_title) #gör om till str
		store_title =  store_title[store_title.find(">")+1:] #tvätta till vänster om
		store_title =  store_title[:store_title.find("<")] #tvätta till höger om

		store_adress_div = soup_store.find_all("div",{"class":"adr"}) #hitta adressen
		store_adress_div = str(store_adress_div) #gör om till str
		store_adress = store_adress_div[store_adress_div.find("street-address\">")+16:] #tvätta till vänster om
		store_adress = store_adress[:store_adress.find("<")] #tvätta till höger om

		store_tele_div = soup_store.find_all("div",{"class":"tel"}) #hitta telenummer
		store_tele_div = str(store_tele_div) #gör om till str
		store_tele = store_tele_div[store_tele_div.find("0"):] #tvätta till vänster om
		store_tele = store_tele[:store_tele.find("<")] #tvätta till höger om

		store = store + [store_title + "," + store_adress + "," + store_tele + ","]

		print "entitet: " + str(i) + " check!"

		time.sleep(5) #paus i 5 sekunder
		i = i + 1

	myfile = open('results.csv','wb')
	wrtr = csv.writer(myfile, delimiter=',')
	for row in store:
	    wrtr.writerow([row])
	    myfile.flush() # whenever you want, and/or
	myfile.close() # when you're done.


	page_num = page_num + 1

	print "klar med sida: " + str(page_num)

	time.sleep(5) #paus i 5 sekunder