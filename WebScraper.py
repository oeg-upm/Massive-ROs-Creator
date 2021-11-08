import selenium
import json
from selenium import webdriver
from html.parser import HTMLParser

PATH = r'C:\Users\Geo\Downloads\chromedriver_win32\chromedriver.exe'
driver = webdriver.Chrome(PATH)
f = open("Massive-ROs-Creator\ToScrape.json", "r")
entry_json = f.read()
f.close()
entry_dictionary = json.loads(entry_json)
result_list = []
for category in entry_dictionary.keys():
	for ro in entry_dictionary.get(category):
		print(ro)

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
		id = link [link.find("=")+1:]
		td_list[1] = td_list[1][0:td_list[1].find("<button")]
		title = td_list[1]
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
		description = td_list[18]
		td_list[20] = td_list[20][td_list[20].find("""rf-dt-c">""")+9:td_list[20].find("</td")]
		science_publication = td_list[20]
		td_list[24] = td_list[24][td_list[24].find("""rf-dt-c">""")+9:td_list[24].find("</td")]
		rights_holder = td_list[24]
		td_list[28] = td_list[28][td_list[28].find("""rf-dt-c">""")+9:td_list[28].find("</td")]
		data_manager = td_list[28]
		td_list[32] = td_list[32][td_list[32].find("""rf-dt-c">""")+9:td_list[32].find("</td")]
		depositor = td_list[32]
		citationHTML = element_0.find_elements_by_id ("citationAPA")
		citation = citationHTML[0].find_elements_by_tag_name("div")[0].get_attribute("innerHTML")

		RO = {	"id": id, 
				"type": category, 
				"name":title, 
				"description":description, 
				"url":link, 
				"research area":td_list[5], 
				"created on": td_list[8],
				"Creator":td_list[10], 
				"license":td_list[16], 
				"science publication":science_publication, 
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
