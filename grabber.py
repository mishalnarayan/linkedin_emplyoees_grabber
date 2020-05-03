 # -*- coding: utf-8 -*-
import xlsxwriter
import glob
import selenium
import sys
sys.setrecursionlimit(100000)
from datetime import datetime
from time import gmtime, strftime, localtime
start_time = datetime.now()
from selenium import webdriver
from bs4 import BeautifulSoup as soup
import pandas as pd
import os
import time
import csv
import urllib,urllib2,cookielib
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random
from selenium.webdriver.common.keys import Keys

failed_execution = ['Execution completed successfully']

def filter_chooser(title,region):
	button = browser.find_element_by_id('ember4074')
	button.click()
	time.sleep(1.5)
	title = browser.find_element_by_id('search-advanced-title')
	title.clear()
	title.send_keys(title) #enter email
	browser.find_element_by_id('ember2659').send_keys(region)
	time.sleep(0.5)
	ActionChains(browser).send_keys(Keys.DOWN).perform()
	ActionChains(browser).send_keys(Keys.RETURN).perform()
	browser.find_element_by_class_name('search-advanced-facets__button--apply ml4 mr2 artdeco-button artdeco-button--3 artdeco-button--primary ember-view').click()
	time.sleep(1.0)





#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

# Working with linkied in ********************************************************************************************************************************

#Reading company to be crawled from csv file***************************************************************************************************************************************
company_list = []
df = pd.read_csv("company_name.csv")
for x in df["company_name"] :
  company_list.append(x)

Resuming_needed = False
try :
  df = pd.read_csv("output.csv")
  Resuming_needed = True
except :
  pass
if Resuming_needed :
  to_remove = []
  for x in df["company_name"] :
	if x in company_list :
	  to_remove.append(x)
  for deleting in to_remove :
  	try :
		company_list.remove(deleting)
	except :
		pass
print company_list

#Initial start and account login***************************************************************************************************************************************

browser = webdriver.Chrome()
time.sleep(1)
browser.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")

email = browser.find_element_by_name('session_key')
email.clear()
password = browser.find_element_by_name('session_password')
password.clear()

email.send_keys('username') #enter email
password.send_keys('password') #enter password
password.send_keys(Keys.RETURN)

time.sleep(30)


with open('output.csv','a') as o1 :
	f1 = csv.writer(o1,quoting=csv.QUOTE_ALL)
	if Resuming_needed == False :
		f1.writerow(["company_name","people_name","position","location","company_page_link"])

## Building crawl payload ********************************************************************************************************************************
counting_company = 1
checking_link = "https://www.linkedin.com/company/cians-analytics/"
for single_company in company_list :

  time.sleep(5.0)
  company_page_link = "Not found"
  people_name = "Not found"
  position = "Not found"
  location = "Not found"


  print "currently working on company no : " + str(counting_company) + " of total " + str(len(company_list)) + " companies " + str((float(counting_company)/float(len(company_list)))*100.0) + " % completed"
  print "Crawling data for company : " + str(single_company)	
  browser.get("https://www.linkedin.com/search/results/companies/?keywords=cians&origin=GLOBAL_SEARCH_HEADER")
  search_field = browser.find_element_by_tag_name('input')
  search_field.clear()
  search_field.send_keys(single_company)
  search_field.send_keys(Keys.RETURN)
  time.sleep(1.4)


  page_soup = soup(browser.page_source,"html.parser")
 

  try :
	company_page_link = "https://www.linkedin.com" + str(page_soup.findAll("a",{"class" : "search-result__result-link ember-view"})[0]["href"])
	while company_page_link == checking_link :
		search_field = browser.find_element_by_tag_name('input')
		search_field.clear()
		search_field.send_keys(single_company)
		search_field.send_keys(Keys.RETURN)
		time.sleep(1.4)
		page_soup = soup(browser.page_source,"html.parser")
		company_page_link = "https://www.linkedin.com" + str(page_soup.findAll("a",{"class" : "search-result__result-link ember-view"})[0]["href"])
	browser.get(company_page_link)
	
	


	#clicking on about
	# check = True
	# while check :
	# 	try :
	# 		button = browser.find_element_by_partial_link_text('People')
	# 		button.click()
	# 		time.sleep(1.5)
	# 		check = False
	# 	except :
	# 		print "people button can not be clicked"
	  
	

	# try :
	# 	ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
	# 	time.sleep(0.2)
	# except :
	# 	pass
	page_soup = soup(browser.page_source,"html.parser")



	all_people_link = "https://www.linkedin.com" + str(page_soup.findAll("a",{"data-control-name" : "topcard_see_all_employees"})[0]["href"])

	browser.get(all_people_link)




	try :
		ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
		ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
		ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
		ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
		time.sleep(0.5)
	except :
		pass
	time.sleep(0.5)

	
	




	page_soup = soup(browser.page_source,"html.parser")

	page_count = 1
	with open('output.csv','a') as o1 : # just to help in resuming
		f1 = csv.writer(o1,quoting=csv.QUOTE_ALL)
		f1.writerow([single_company,people_name,position,location,company_page_link])

	older_page_soup = ""
	
	while page_count < 5000 :
		time.sleep(0.5)
		page_soup = soup(browser.page_source,"html.parser")
		

		if older_page_soup == page_soup :
			break

		for individual_person in page_soup.findAll("div",{"class" : "search-result__wrapper"}) :
			try :
				people_name = individual_person.findAll("h3",{"class" : "actor-name-with-distance search-result__title single-line-truncate ember-view"})[0].text.strip().encode('ascii', 'replace').replace("?", " ")
			except :
				people_name = "Not found"


			try :
				person_page_link = "https://www.linkedin.com" + str(individual_person.findAll("a",{"class" : "search-result__result-link ember-view"})[0]["href"])
			except :
				person_page_link = "Not found"


			try :
				position = individual_person.findAll("p",{"class" : "subline-level-1 t-14 t-black t-normal search-result__truncate"})[0].text.strip().encode('ascii', 'replace').replace("?", " ")
			except :
				position = "Not found"


			try :
				location = individual_person.findAll("p",{"class" : "subline-level-2 t-12 t-black--light t-normal search-result__truncate"})[0].text.strip().encode('ascii', 'replace').replace("?", " ")
			except :
				location = "Not found"


			# if str("at " + single_company[:3]) in position :
			# 	#if "coo" in position.lower() or "president" in position.lower() or "ceo" in position.lower() or "chief" in position.lower() or "vp" in position.lower() or "md" in position.lower() or "managing" in position.lower() or "manager" in position.lower() or "founder" in position.lower() or "director" in position.lower() or "cao" in position.lower() or "cto" in position.lower() or "head" in position.lower() or "avp" in position.lower() or "vice" in position.lower() or "associate" in position.lower() :

			with open('output.csv','a') as o1 :
				f1 = csv.writer(o1,quoting=csv.QUOTE_ALL)
				f1.writerow([single_company,people_name,position,location,person_page_link])
				print single_company				
				print people_name
				print position
				print location

		people_name = "Not found"
		position = "Not found"
		location = "Not found"
		
		tryier = ["/html/body/div[6]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[2]/artdeco-pagination/button[2]",
		"/html/body/div[6]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[2]/artdeco-pagination/button[2]",
		"/html/body/div[6]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[2]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]",
		"/html/body/div[6]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[2]/artdeco-pagination/button[2]",
		"/html/body/div[6]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[2]/artdeco-pagination/button[2]",
		"/html/body/div[6]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[2]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]",
		"/html/body/div[6]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[2]/artdeco-pagination/button[2]",
		"/html/body/div[6]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[2]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]",
		"/html/body/div[6]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[2]/artdeco-pagination/button[2]",
		"/html/body/div[6]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[2]/artdeco-pagination/button[2]",
		"/html/body/div[6]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[2]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]",
		"/html/body/div[5]/div[3]/div[3]/div/div[2]/div/div[2]/div/div/div/div/div[1]/artdeco-pagination/button[2]"]

		time.sleep(0.5)
		try :
			work_done = "ncompleted"
			for x in tryier :
				try :
					browser.find_element_by_xpath(x).click()
					print "executed"
					work_done = "completednm"
					break
				except:
					print "error"
					work_done = "completed"

			if work_done == "completed" :
				print "sleeping"
				time.sleep(30)

					
			time.sleep(2.0)
		except Exception as e:
			print(e)
			print "Next button can not be clicked"
			break
		older_page_soup = soup(browser.page_source,"html.parser")
		try :
			ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
			ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
			ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
			ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
			time.sleep(0.5)
		except :
			pass
		time.sleep(1.9)
		page_soup = soup(browser.page_source,"html.parser")
		page_count = page_count + 1


  except Exception as e :
  	print(e)
	company_page_link = "Not found"
	people_name = "Not found"
	position = "Not found"
	location = "Not found"
	
  
	with open('output.csv','a') as o1 :
		f1 = csv.writer(o1,quoting=csv.QUOTE_ALL)
		f1.writerow([single_company,people_name,position,location,company_page_link])
  counting_company = counting_company + 1

df = pd.read_csv("output.csv") #some shitty bug viewing in excel
os.remove("output.csv")
df.to_csv("output.csv",index = False)
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))











