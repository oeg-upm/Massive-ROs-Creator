from importlib import resources
import re, threading,time
import rohub
import json
import sys
from haversine import inverse_haversine , Direction

rohub.login(username="georgehadib@gmail.com", password="George123#")
#roro = rohub.search_ros_by_id("c9d776f7-58a2-4576-b4c1-65913d1dd896")
#print (roro)
#licenses=show_available_licenses()
#print(licenses)
filename = ""
if (len(sys.argv) == 1):
    f = open("GIT\Massive-ROs-Creator\ROs.json", "r")
elif (len(sys.argv) == 2):
    try:
        f = open("GIT\Massive-ROs-Creator\\"+sys.argv[1], "r")
    except:
        sys.exit("A file with the name: \"" + sys.argv[1] + "\" couldn't be found. Please make sure to enter the correct file name.")
else:
    sys.exit("Bad entry! Please make sure to enter the right number of arguments.")

entry_json = f.read()
f.close()
entry_dictionary = json.loads(entry_json)

data_folder=""
raw_data_folder=""
metadata_folder=""
biblio_folder=""
creator_lock = False
session_lock = False
research_area_dict = {
    'Natural sciences'	:	['Life sciences' ,'Physical sciences','Environmental research']	,
    'Planetary science'	:	      ['Physical sciences']	,
    'Climate science'	:	     ['Climatology']	,
    'Glaciology'	:	     ['Earth sciences'	],
    'Algebra'	:	     ['mathematics'	],
    'Physical chemistry'	:	     ['Physical sciences', 'Chemistry']	,
    'Marine Biology'	:	    ['Biology'] 	,
    'Systems Biology'	:	    ['Biology'] 	,
    'Computational chemistry'	:	    ['Chemistry']	,
    'Tectonics'	:	    ['Earth sciences','Seismology']	,
    'Environmental science'	:	    ['Environmental research']	,
    'Immunogenetics'	:	    ['Genetics']	,
    'Pure Mathematics'	:	    ['mathematics']	,
    'Healthcare science'	:	    ['medicine']	,
    'Economics'	:	    ['Social sciences']	,
    'Energy economics'	:	    ['Social sciences']	,
    'Engineering'	:	   ['Applied sciences']	,
    'Cell Biology'	:	   ['Biology']	,
    'Evolutionary Biology'	:	  [ 'Biology'	],
    'Medicinal chemistry'	:	  [ 'Chemistry'	],
    'Agricultural economics'	:	  [ 'Environmental research' , 'Social sciences']	,
    'Health informatics'	:	   ['medicine', 'Life Science'] 	,
    'Physics'	:	   ['Physical sciences']	,
    'Computer engineering'	:	  ['Applied sciences']	,
    'Biophysics'	:	 ['Physical sciences', 'Biology', 'Life Science']	,
    'Professional and Applied sciences'	:	 ['Applied sciences'	],
    'Immunology'	:	 ['Biology' ,  'Medical science']	,
    'Earth science'	:	 ['Earth sciences']	,
    'Evolutionary Genetics'	:	 ['Genetics']	,
    'Genomics'	:	 ['Genetics']	,
    'Computer science'	:	 ['Information science' ,  'mathematics' ] 	,
    'Bioinformatics'	:	 ['Life sciences']	,
    'Formal sciences'	:	 ['mathematics' ]	,
    'Medical Imaging'	:	 ['Medical science']	,
    'Neuroscience'	:	 ['Neurobiology']	,
    'Structural Biology'	:	['Biology']	,
    'Computer security and reliability'	:	['Information science']	,
    'Programming languages'	:	['Information science']	,
    'Fluid dynamics'	:	['Physical sciences']	
}


def session_controler():
    while t1.is_alive():
        
        time.sleep(840)
        while creator_lock:
            time.sleep(1)
        session_lock = True
        rohub.login(username="georgehadib@gmail.com", password="George123#")
        session_lock = False
def ros_creator():     
    for ro in entry_dictionary:
        creator_lock = True
        while session_lock:
            time.sleep(1)
        areas = []
        for area in ro.get("research area"):
            if area in research_area_dict.keys():
                for valid_area in research_area_dict.get(area):
                    if (valid_area not in areas):
                        areas.append(valid_area)
        #print(areas)

                

        description=ro.get("description")
        while ("href" in description):
            link = description[description.find("href"):description.find("</a")+4]
            link_name = link[link.rfind("\"")+2:link.find("</a")]
            link = link[link.find("\"")+1:]
            link = link[:link.find("\"")]
            description = description[:description.find("<a")]+link_name+": "+link+description[description.find("</a")+4:]
        new_ro = rohub.ros_create(title=ro.get("name"), research_areas=areas,description=description,ros_type='Data-centric Research Object',use_template=True)
        #new_ro.add_copyright(display_name=ro.get("Creator"))
        owners = ro.get("Creator")
        owners_identificators = []
        for user in owners:
            if user[len(user)-1] == " ":
                user = user[:len(user)-2]
            clean_user = user.replace("ï","i").replace("ø","o").replace("é","e").replace("Ø","O").replace("ç","c").replace("ö","o").replace("ü","u").replace("Å", "A").replace("'",".").replace("Ø","O").replace("ć","c").replace("å","a")
            
    
            if rohub.users_find(user).empty or user not in list(rohub.users_find(user).loc[:,"display_name"]):
                if "(" in user:
                    email = clean_user[clean_user.find("(")+1:clean_user.find(")")].replace(" ",".")+"@rohub.com"
                    email = re.sub('[^a-zA-Z0-9@ \n\.]', '.', email)

                else:    
                    user_aux = re.sub('\.','',clean_user)
                    email = re.sub(' ', '.',user_aux)+"@rohub.com"
                    email = email.lower()
                while (1):
                    if ".." in email:
                        email = email.replace("..",".")
                    else:
                        break

            else:
                email = rohub.users_find(user).at[0,"username"]
            if {"display_name" : user, "email":email} not in owners_identificators:
                owners_identificators.append({"display_name" : user, "email":email})    
        new_ro.set_authors(agents=owners_identificators)


        #rohub.ros_set_authors(new_ro,agents=owners_identificators)

        # print(owner)
        



        folders_list = new_ro.list_folders().to_dict()
        #print (folders_list)
        for i in range(len(folders_list.get("identifier"))):
            if folders_list.get("name").get(i) =="data":
                data_folder = folders_list.get("identifier").get(i)
            elif folders_list.get("name").get(i) =="raw data":
                raw_data_folder = folders_list.get("identifier").get(i)
            elif folders_list.get("name").get(i) =="metadata":
                metadata_folder = folders_list.get("identifier").get(i)
            elif folders_list.get("name").get(i) =="biblio":
                biblio_folder = folders_list.get("identifier").get(i)
        #print(data_folder,biblio_folder,metadata_folder,raw_data_folder,sep="***")
    
            

        #new_ro.add_contributor(display_name=ro.get("Creator"))
        geolocation = ""
        if "geolocation" in ro:
            geo_type = ""
            raw_geolocation = ro.get("geolocation")
            coordinates = []
            
            #re.sub(r'*',r'0',raw_geolocation)
            raw_geolocation = raw_geolocation.replace("*",'0')
            if ("Units: meters" in raw_geolocation):
                if ("Point" in raw_geolocation):
                    geo_type = "Point"
                    raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
                    longitude = float(raw_geolocation[:raw_geolocation.find(" ")])/1000
                    longitude = list(inverse_haversine((0,0),longitude,Direction.EAST))
                    raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
                    latitude = float(raw_geolocation[:raw_geolocation.find(" ")])/1000
                    latitude = list(inverse_haversine((0,0),latitude,Direction.NORTH))
                    coordinates = [longitude[1],latitude[0]]

                elif ("Box") in raw_geolocation:
                    geo_type = "Polygon"
                    raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
                    eastlimit = float(raw_geolocation[:raw_geolocation.find(" ")])/1000
                    eastlimit = list(inverse_haversine((0,0),eastlimit,Direction.EAST))
                    raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
                    westlimit = float(raw_geolocation[:raw_geolocation.find(" ")])/1000
                    westlimit = list(inverse_haversine((0,0),westlimit,Direction.WEST))
                    raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
                    northlimit = float(raw_geolocation[:raw_geolocation.find(" ")])/1000
                    northlimit = list(inverse_haversine((0,0),northlimit,Direction.NORTH))
                    raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
                    southlimit = float(raw_geolocation[:raw_geolocation.find(" ")])/1000
                    southlimit = list(inverse_haversine((0,0),southlimit,Direction.NORTH))

                    raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
                    uplimit = float(raw_geolocation[:raw_geolocation.find(" ")])
                    raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
                    downlimit = float(raw_geolocation[:raw_geolocation.find(" ")])
                    point_1 = [westlimit[1],northlimit[0]]
                    point_2 = [eastlimit[1],northlimit[0]]
                    point_3 = [eastlimit[1],southlimit[0]]
                    point_4 = [westlimit[1],southlimit[0]]
                    #point_5 = [westlimit,northlimit,uplimit]
                    #point_6 = [westlimit,northlimit,downlimit]
                    #point_7 = [westlimit,southlimit,uplimit]
                    #point_8 = [westlimit,southlimit,downlimit]
                    coordinates = [point_1,point_2,point_3,point_4]
                    print (coordinates)
            elif "Units: deg" in raw_geolocation:
                if ("Point" in raw_geolocation):
                    geo_type = "Point"
                    raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
                    longitude = float(raw_geolocation[:raw_geolocation.find(" ")])
                    raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
                    latitude = float(raw_geolocation[:raw_geolocation.find(" ")])
                    coordinates = [longitude,latitude]

                elif ("Box") in raw_geolocation:
                    geo_type = "Polygon"
                    raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
                    eastlimit = float(raw_geolocation[:raw_geolocation.find(" ")])
                    raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
                    westlimit = float(raw_geolocation[:raw_geolocation.find(" ")])
                    raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
                    northlimit = float(raw_geolocation[:raw_geolocation.find(" ")])
                    raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
                    southlimit = float(raw_geolocation[:raw_geolocation.find(" ")])

                    raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
                    uplimit = float(raw_geolocation[:raw_geolocation.find(" ")])
                    raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
                    downlimit = float(raw_geolocation[:raw_geolocation.find(" ")])
                    point_1 = [westlimit,northlimit]
                    point_2 = [eastlimit,northlimit]
                    point_3 = [eastlimit,southlimit]
                    point_4 = [westlimit,southlimit]
                    #point_5 = [westlimit,northlimit,uplimit]
                    #point_6 = [westlimit,northlimit,downlimit]
                    #point_7 = [westlimit,southlimit,uplimit]
                    #point_8 = [westlimit,southlimit,downlimit]
                    coordinates = [point_1,point_2,point_3,point_4]
            geolocation = {
                    "@context": {
                        "geojson": "https://purl.org/geojson/vocab#"
                    },
                    
                    "type": "Feature",
                    #"bbox": [westlimit,northlimit,eastlimit,southlimit],
                    "geometry": {
                            "type": geo_type,
                            "coordinates": coordinates
                        }
            }
                    
            #   rohub.external_user_add()
            new_ro.add_geolocation(body_specification_json=geolocation)


        #new_ro.add_author(predicate="Creator",display_name=ro.get("Creator"))
        #rohub.ros_add_author(identifier=new_ro.identifier,display_name=ro.get("Creator"))
        #print(ro.get("Creator"))
        #print(new_ro.get_content())
        dataset = new_ro.add_external_resource(res_type="Dataset",input_url=ro.get("url"),title=ro.get("name"),folder="data",description=ro.get("description"))
        for publication in ro.get("science publication"):
            if type(publication)==str and "http" in publication and not " " in publication:
                pub = new_ro.add_external_resource(res_type="Bibliographic Resource",input_url=publication,folder="biblio")
            elif type(publication)==dict:
                pub = new_ro.add_external_resource(res_type="Bibliographic Resource",input_url=publication.get("publication"),folder="biblio")

        #dataset.assign_doi(ro.get("id"))
        if ("creativecommons.org/licenses/by/4.0/legalcode" in ro.get("license")): 
            new_ro.set_license("CC-BY-4.0")

            dataset.set_license("CC-BY-4.0")
        elif ("data.norge.no/nlod/en/1.0/" in ro.get("license")): 
            new_ro.set_license("NLOD-1.0")

            dataset.set_license("NLOD-1.0")
        #new_ro.set_authors(agents=["George"])
        #rohub.ros_add_annotations(identifier = new_ro, resources=dataset, body_specification_json=)
        #new_ro.add_annotations()
        
        #ro.add_author("Geo H.")
        #ro.add_license("www.license.com")
        #ro.add_annotations("New annotation")
        #ro.add_contributor("Geo H.")
        #print(ro)
        creator_lock = False

t1= threading.Thread(target=ros_creator)
t2= threading.Thread(target=session_controler)
t2.setDaemon(True)
t1.start()
t2.start()
