import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
#These variables need to be changed to match the wanted search case
domain = "Natural sciences"
field = "Earth science"
subfield = ""
description = "climate"
#######################################
#Please don't remove the "r" before tha path variable
PATH = r'Here goes an absolute location of your Chromedriver'
driver = webdriver.Chrome(PATH)
link = "https://archive.sigma2.no/pages/public/search.jsf"

driver.get(link)

advanced_search = driver.find_element_by_id("searchForm:j_idt59:header:inactive")
advanced_search.click()
time.sleep(1)
#driver.get(link)

#Add domain
if (not domain==""):
	domain_menu = Select(driver.find_element_by_id("searchForm:domainMenu"))
	domain_menu.select_by_visible_text(domain)
	time.sleep(0.5)

#Add field
if (not field==""):
	field_menu = Select(driver.find_element_by_id("searchForm:fieldMenu"))
	field_menu.select_by_visible_text(field)
	time.sleep(0.5)

#Add subfield
if (not subfield==""):
	subfield_menu = Select(driver.find_element_by_id("searchForm:subfieldMenu"))
	subfield_menu.select_by_visible_text(subfield)

#Add description
if (not description==""):
	description_input = driver.find_element_by_name("searchForm:j_idt86")
	description_input.send_keys(description)

#excute query
search_button = driver.find_element_by_name("searchForm:j_idt318").click()
list_of_ids = []

#scrape list
try:
	content = driver.find_element_by_id("searchresult-section")
	list_of_content = content.find_elements_by_class_name("rf-edt-c-cnt")
except:
	NoSuchElementException: print ("There is no results for your search. Please modify your enteries and try again")
	driver.quit()
	exit()

for i in range (0, len(list_of_content),5):
	list_of_content[i] = list_of_content[i].get_attribute("innerHTML")
	list_of_content[i+2] = list_of_content[i+2].get_attribute("innerHTML")

	
	list_of_content[i] = list_of_content[i][list_of_content[i].find(""";">""")+3:list_of_content[i].find(""";">""")+22]
	list_of_content[i+2] = list_of_content[i+2][list_of_content[i+2].find(""";">""")+3:list_of_content[i+2].find("""</a>""")]
	new_ro = {"id":list_of_content[i],"title":list_of_content[i+2]}
	#print (list_of_content[i])
	list_of_ids.append(new_ro)

page_counter = 2

while (1):
	time.sleep(1)

	try:

		next_page = driver.find_element_by_id ("searchResultForm:j_idt61_ds_"+str(page_counter)).click()
		time.sleep(1)

		#print("breakpoint 1")
		content = driver.find_element_by_id("searchresult-section")
		list_of_content = content.find_elements_by_class_name("rf-edt-c-cnt")
		#print ("este es "+list_of_content[2].get_attribute("innerHTML"))
		for i in range (0, len(list_of_content),5):
			list_of_content[i] = list_of_content[i].get_attribute("innerHTML")
			list_of_content[i+2] = list_of_content[i+2].get_attribute("innerHTML")
			

			list_of_content[i] = list_of_content[i][list_of_content[i].find(""";">""")+3:list_of_content[i].find(""";">""")+22]
			list_of_content[i+2] = list_of_content[i+2][list_of_content[i+2].find(""";">""")+3:list_of_content[i+2].find("""</a>""")]
			#print (list_of_content[i+2])
			#print (list_of_content[i])
			new_ro = {"id":list_of_content[i],"title":list_of_content[i+2]}
			#print (list_of_content[i])
			list_of_ids.append(new_ro)

		page_counter+=1
		#print ("este es "+list_of_content[2])

	except:
		NoSuchElementException:	print (list_of_ids)
		print("Your querey was excuted correctly and information was saved")
		f = open("Massive-ROs-Creator\ToScrape.json", "w")
		f.write(json.dumps(list_of_ids))
		f.close()
		driver.quit()
		exit()

############################################ This program creates a json file in your working directory #################################################

#list_of_content[i].find("</a")
#####################ESTA ES UNA PRUEBA PARA SACAR MÁS DATOS DE LA LISTA######################
#for i in range (0, len(list_of_content)):
#	list_of_content[i] = list_of_content[i].get_attribute("innerHTML")
###
###	list_of_content[i] = list_of_content[i][list_of_content[i].find(""";">""")+3:list_of_content[i].find("</a")]
###	
##for i in range (0, len(list_of_content),5)
#	list	


#print (list_of_content[0].get_attribute("innerHTML"))
#list_of_content = list_of_content.find_elements_by_tag_name("a")

#selection = domain_menu.find_element_by_link_text("Natural sciences")
#domain_menu = domain_menu.find_element_by_link_text("Not defined")

#domain_menu.send_keys(domain)
#domain_menu.send_keys(Keys.RETURN)
#driver.quit()
