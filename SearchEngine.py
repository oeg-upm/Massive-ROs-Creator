import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from html.parser import HTMLParser
import time

domain = "Natural sciences"
field = "Earth science"
subfield = "Geology"

PATH = r'C:\Users\Geo\Downloads\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(PATH)
link = "https://archive.sigma2.no/pages/public/search.jsf"

driver.get(link)

advanced_search = driver.find_element_by_id("searchForm:j_idt59:header:inactive")
advanced_search.click()
driver.get(link)
domain_menu = Select(driver.find_element_by_id("searchForm:domainMenu"))
#domain_menu.click()
domain_menu.select_by_visible_text("Natural sciences")
time.sleep(0.5)
field_menu = Select(driver.find_element_by_id("searchForm:fieldMenu"))
field_menu.select_by_visible_text("Earth science")
time.sleep(0.5)
subfield_menu = Select(driver.find_element_by_id("searchForm:subfieldMenu"))
subfield_menu.select_by_visible_text("Geology")
time.sleep(0.5)

search_button = driver.find_element_by_name("searchForm:j_idt318").click()
content = driver.find_element_by_id("searchresult-section")
list_of_content = content.find_elements_by_class_name("rf-edt-c-cnt")
i = 0
list_of_ids = []

for i in range (0, len(list_of_content),5):
	list_of_content[i] = list_of_content[i].get_attribute("innerHTML")

	list_of_content[i] = list_of_content[i][list_of_content[i].find(""";">""")+3:list_of_content[i].find(""";">""")+22]
	list_of_content[i]
	#print (list_of_content[i])
	list_of_ids.append(list_of_content[i])
print (list_of_ids)

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
driver.quit()
