import selenium
import json
from selenium import webdriver
from html.parser import HTMLParser
import time

PATH = r'C:\Users\Geo\Downloads\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(PATH)
f = open("Massive-ROs-Creator\ToScrape.json", "r")
entry_json = f.read()
f.close()
entry_dictionary = json.loads(entry_json)
result_list = []
for category in entry_dictionary.keys():
	for ro in entry_dictionary.get(category):
		#print(ro)

		# The following link is an example
		link = "https://archive.sigma2.no/pages/public/datasetDetail.jsf?id="+ro.get("id")

		driver.get(link)
		#wait = WebDriverWait(driver, 10).until(
		#       EC.presence_of_element_located((By.ID, "lp_initial"))
		#    ) # this waits until the page is loaded
		element_0 = driver.find_element_by_id("lp_initial")
		# (str(element_0.get_attribute("innerHTML")))
		td_raw_list = element_0.find_elements_by_tag_name("td")
		td_list = []
		for element in td_raw_list:
			td_list.append(element.get_attribute("innerHTML"))
		id = ro.get("id")
		td_list[1] = td_list[1][0:td_list[1].find("<button")]
		title =  ro.get("title")


		
		td_list[5] = td_list[5].replace("Domain: ","")
		td_list[5] = td_list[5].replace("Field: ","")
		td_list[5] = td_list[5].replace("Subfield: ","")
		#td_list[5]:research area (clean) (missing synchronisation with ROHub)
		#td_list[8]:created_on (clean) (format yyyy-mm-dd)
		td_list[10] = td_list[10][td_list[10].find("""rf-dt-c">""")+9:td_list[10].find("</td>")]
		#td_list[10]:creator (clean)
		#td_list[16]:license (needs parsing) (Ask Esteban)
		td_list[16] = td_list[16][td_list[16].find(""""h""")+1:td_list[16].find("""" """)]
		td_list[18] = td_list[18][td_list[18].find(">")+28:td_list[18].find("\n")]
		#td_list[18]:description
		description = driver.find_element_by_xpath("""//*[@id="linkify-example"]""").get_attribute("innerHTML")[27:]
	
		td_list[20] = td_list[20][td_list[20].find("""rf-dt-c">""")+9:td_list[20].find("</td")]
		publication_list = []
		counter = 0
		while(1):
			try:
				publication_list.append(str(driver.find_element_by_xpath("""//*[@id="datasetDetailForm:j_idt106:"""+str(counter)+""":j_idt107"]""").get_attribute("innerHTML")))
				counter = counter+1                                    
			except:
				break
		
		for publication in publication_list:
			pub_index = publication_list.index(publication)
			if "Published :" in publication:
				if "DOI: " in publication:
					index = publication.find("DOI: ")
					pub_aux = publication[index+5:publication.find(",")]
					if pub_aux == "":
						#print ("breakpoint 1")
						#print (publication)
						publication = publication[index+5:]
						#print (publication)

					else:
						publication = pub_aux
					publication = publication.replace("DOI:","")
					publication = publication.replace("doi:","")
					if not "https:" in publication:
						publication = "https://doi.org/" + publication
				elif "DOI:" in publication:
					index = publication.find("DOI:")
					publication = publication[index+4:]
					if not ("https:" in publication or "http" in publication):
						publication = "https://doi.org/" + publication
				elif "https" in publication:
					publication = publication[publication.find("https:"):]
			if "URL:" in publication:
				index = publication.find("URL:")
				if "<a href" in publication:
					publication = publication[index+14:publication.find("""" """)]
			
			publication = publication.replace ("DOI: ","")
			if """target=""" in publication:
				publication = publication [:publication.find("target=")-2]
			publication = publication.replace(" (primary)","")
			publication = publication.replace(" (primary","")
			publication_list[pub_index] = publication
			
		td_list[24] = td_list[24][td_list[24].find("""rf-dt-c">""")+9:td_list[24].find("</td")]
		rights_holder = driver.find_element_by_xpath("""//*[@id="datasetDetailForm:j_idt111:0:j_idt112"]""").get_attribute("innerHTML")

		
		td_list[28] = td_list[28][td_list[28].find("""rf-dt-c">""")+9:td_list[28].find("</td")]
		data_manager = driver.find_element_by_xpath("""//*[@id="datasetDetailForm:j_idt116:0:j_idt117"]""").get_attribute("innerHTML")
		td_list[32] = td_list[32][td_list[32].find("""rf-dt-c">""")+9:td_list[32].find("</td")]
		depositor = driver.find_element_by_xpath("""//*[@id="datasetDetailForm:j_idt121:0:j_idt122"]""").get_attribute("innerHTML")
		citationHTML = element_0.find_elements_by_id ("citationAPA")
		citation = citationHTML[0].find_elements_by_tag_name("div")[0].get_attribute("innerHTML")
		try:
			driver.find_element_by_xpath("""//*[@id="lp_initial"]/table[1]/tbody/tr[15]/td[2]/a/img""").click()
			driver.switch_to.window(driver.window_handles[1])
			time.sleep(1)
			try:
				geolocation = driver.find_element_by_xpath("""//*[@id="j_idt56:0:j_idt57"]""").get_attribute("innerHTML")
				driver.close()
				driver.switch_to.window(driver.window_handles[0])
			except:
				driver.close()
				driver.switch_to.window(driver.window_handles[0])
			
			RO = {	"id": id, 
					"type": category, 
					"name":title, 
					"description":description, 
					"url":link, 
					"research area":td_list[5], 
					"created on": td_list[8],
					"Creator":td_list[10], 
					"license":td_list[16], 
					"science publication":publication_list, 
					"rights holder":rights_holder, 
					"data manager": data_manager, 
					"depositor":depositor, 
					"citation":citation,
					"geolocation": geolocation}

		except:
			RO = {	"id": id, 
					"type": category, 
					"name":title, 
					"description":description, 
					"url":link, 
					"research area":td_list[5], 
					"created on": td_list[8],
					"Creator":td_list[10], 
					"license":td_list[16], 
					"science publication":publication_list, 
					"rights holder":rights_holder, 
					"data manager": data_manager, 
					"depositor":depositor, 
					"citation":citation}
				
		result_list.append(RO)


#print (RO)
#app_json = json.dumps(RO, sort_keys=True)
f = open("Massive-ROs-Creator\ROs.json", "w")
f.write(json.dumps(result_list, indent=4, sort_keys=True))
f.close()


driver.quit()
exit()
