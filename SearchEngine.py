import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time

domain = "Natural sciences"
field = "Earth science"
subfield = ""
description = "climate"

PATH = r'A static path to your local webdriver'
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

#scrape list
try:
	content = driver.find_element_by_id("searchresult-section")
	list_of_content = content.find_elements_by_class_name("rf-edt-c-cnt")
	list_of_ids = []
except:
	NoSuchElementException: print ("There is no results for your search. Please modify your enteries and try again")
	exit()

for i in range (0, len(list_of_content),5):
	list_of_content[i] = list_of_content[i].get_attribute("innerHTML")

	list_of_content[i] = list_of_content[i][list_of_content[i].find(""";">""")+3:list_of_content[i].find(""";">""")+22]
	list_of_content[i]
	#print (list_of_content[i])
	list_of_ids.append(list_of_content[i])

page_counter = 2

while (1):
	time.sleep(1)

	try:

		next_page = driver.find_element_by_id ("searchResultForm:j_idt61_ds_"+str(page_counter)).click()
		time.sleep(1)

		print("breakpoint 1")
		content = driver.find_element_by_id("searchresult-section")
		list_of_content = content.find_elements_by_class_name("rf-edt-c-cnt")
		for i in range (0, len(list_of_content),5):
			list_of_content[i] = list_of_content[i].get_attribute("innerHTML")

			list_of_content[i] = list_of_content[i][list_of_content[i].find(""";">""")+3:list_of_content[i].find(""";">""")+22]
			list_of_content[i]
			#print (list_of_content[i])
			list_of_ids.append(list_of_content[i])
		page_counter+=1
	except:
		NoSuchElementException:	print (list_of_ids)
		print("Your querey was excuted correctly and information was saved")
		exit()



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
