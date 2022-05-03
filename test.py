from shutil import register_archive_format
from numpy import size
import rohub
import json
import re
from haversine import inverse_haversine, Direction
'''
valid_area = rohub.list_valid_research_areas()

area_list2 = rohub.list_valid_research_areas()
f = open("Massive-ROs-Creator\ROs.json", "r")
entry_json = f.read()
f.close()
entry_dictionary = json.loads(entry_json)
area_list= []
valid_area.append(None)
area_list_mapped = []
for ro in entry_dictionary:
    for area in ro.get("research area"):
        
        if (not area in valid_area): 
            if (not area in area_list):

                area_list.append(area)
    
        elif area in valid_area:
            if (not area in area_list_mapped):
                area_list_mapped.append(area)



print (area_list_mapped)
print (area_list)
print (valid_area)
'''





#rohub.login(username="georgehadib@gmail.com", password="George123#")



#rohub.ros_set_authors(identifier="4a739398-ba93-43ac-bd3f-265c7634bf3d",agents=[{'display_name':"Geo Test4",'email':"geo.test4@rohub.com"}])

#rohub.ros_set_authors(identifier="6933c3b3-f754-4b22-ac9f-7f099039608d",agents=[{'display_name':"Geo Test4",'email':"geo.test4@rohub.com"}])
'''

geo_type = ""
raw_geolocation = "Box - Eastlimit: 1400000 Westlimit: -200000 Northlimit: 6900000 Southlimit: 5680000 Uplimit: * Downlimit: * Units: meters Zunits: * Projection: UTM Zone for East/Northlimit: 31W Zone for West/Southlimit: 1C Name: Central North Sea and surroundings"

coordinates = []

if ("Point" in raw_geolocation):
            geo_type = "Point"
            raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
            longitude = raw_geolocation[:raw_geolocation.find(" ")]
            raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
            latitude = raw_geolocation[:raw_geolocation.find(" ")]
            coordinates = [float(longitude),float(latitude)]

elif ("Box"):
            geo_type = "polygon"
            raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
            print (raw_geolocation)

            eastlimit = float(raw_geolocation[:raw_geolocation.find(" ")])
            raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
            print (raw_geolocation)
            westlimit = float(raw_geolocation[:raw_geolocation.find(" ")])
            raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
            print (raw_geolocation)
            northlimit = float(raw_geolocation[:raw_geolocation.find(" ")])
            raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
            print (raw_geolocation)
            southlimit = float(raw_geolocation[:raw_geolocation.find(" ")])
            raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
            print (raw_geolocation)
            uplimit = float(raw_geolocation[:raw_geolocation.find(" ")])
            raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
            downlimit = float(raw_geolocation[:raw_geolocation.find(" ")])
            point_1 = [eastlimit,northlimit,uplimit]
            point_2 = [eastlimit,northlimit,downlimit]
            point_3 = [eastlimit,southlimit,uplimit]
            point_4 = [eastlimit,southlimit,downlimit]
            point_5 = [westlimit,northlimit,uplimit]
            point_6 = [westlimit,northlimit,downlimit]
            point_7 = [westlimit,southlimit,uplimit]
            point_8 = [westlimit,southlimit,downlimit]
            coordinates = [point_1,point_2,point_3,point_4,point_5,point_6,point_7,point_8]

geolocation = {
                "@context": {
                    "geojson": "https://purl.org/geojson/vocab#"
                },
                "type": "Feature",
                "geometry": {
                    "type": geo_type,
                    "coordinates": coordinates
                }
            }
print (geolocation)
#rohub.ros_export_to_rocrate(identifier="ea189093-31d7-4663-82a6-b8cacdfea011",filename="Zhong.jsonld")

'''
'''
raw_geolocation = "Point - East: 473647.19 North: 8669050.64 Elevation: * Units: metres Zunits: * Projection: UTM Zone: 33N Name: *"
raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
longitude = float(raw_geolocation[:raw_geolocation.find(" ")])/1000
longitude = list(inverse_haversine((0,0),longitude,Direction.EAST))
raw_geolocation = raw_geolocation[raw_geolocation.find(":")+2:]
latitude = float(raw_geolocation[:raw_geolocation.find(" ")])/1000
latitude = list(inverse_haversine((0,0),latitude,Direction.NORTH))
coordinates = [longitude[1],latitude[0]]
print (coordinates)


raw_geolocation = "Box - Eastlimit: 180 Westlimit: -180 Northlimit: 90 Southlimit: -90 Uplimit: 20000 Downlimit: -9000 Units: signed decimal degrees Zunits: m Projection: GPS [WGS'84] Name: *"

raw_geolocation = raw_geolocation.replace("*","0")
raw_geolocation.replace ("ï", "i")

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
print (coordinates)




f = open("GIT\Massive-ROs-Creator\ROs.json", "r")

entry_json = f.read()
f.close()
entry_dictionary = json.loads(entry_json)

print (len(entry_dictionary))


'''









#print(rohub.users_find("Geo Test"))


















#rohub.ros_set_authors(identifier="6933c3b3-f754-4b22-ac9f-7f099039608d",agents=[{'display_name':"Geo Test",'email':"geo.test@rohub.com"}])


'''
dicti = {'cat': [{ 'id':1231412,'2344234':12309},{ 'id':1231412,'2344234':12309}]}
if ({ 'id':1231412,'2344234':12309} in dicti.get('cat')):
    print (True)

from threading import Thread
import time
import sys
def time1():
    time.sleep(5)
    print ("time 1")
def time2():
    time.sleep(15)
    if t1.is_alive():

        print ("time 2")

t1= Thread(target=time1)
t2= Thread(target=time2)
t2.setDaemon(True)
t1.start()
t2.start()
'''












#rohub.ros_set_authors(identifier="6933c3b3-f754-4b22-ac9f-7f099039608d",agents=[{'display_name':"Esteban G.",'email':"esteban.g@rohub.com"}])

#creator = "Weijian Zong. pojwqoej"
#creator_aux = re.sub(r'\.','',creator)
#print (creator_aux)
#email=creator[:creator.find(" ")]+creator[creator.find(" ")+1:]
#email = re.sub(' ','.',creator_aux)
#print(email)
#rohub.external_user_delete("2d997159-743f-49e0-a193-4c9286b5e7d1")
#rohub.external_user_add(display_name="Horst A. Obenhaus",email="Horst.Obenhaus@rohub.com")
#print(rohub.users_find("Horst.Obenhaus@rohub.com"))

'''
desc = "This dataset contains data presented in the paper \"Large-scale two-photon calcium imaging in freely moving mice\" Weijian Zong,Horst A. Obenhaus, Emilie R. Skytøen, Hanna Eneqvist, Nienke L. de Jong, Marina R. Jorge, May-Britt Moser, Edvard I. Moser (2022). It is complementary to the analysis code stored at <a href=\"http://github.com/kavli-ntnu/MINI2P_toolbox\" class=\"linkified\" target=\"_blank\">LINK</a>"
link = desc[desc.find("<a"):desc.find("</a")+4]
link_name = link[link.rfind("\"")+2:link.find("</a")]
link = link[link.find("\"")+1:]
link = link[:link.find("\"")]

desc_aux = desc[:desc.find("<a")]+link_name+": "+link+desc[desc.find("</a")+4:]
print (desc_aux)


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


s = "jkjhfda.fadsfasd.adfadsf.asdfsdfa@rohub.com"
while (s.count(".")>2):
    s = s[:s.find(".")]+s[s.find(".")+1:]

print (s)
'''
#test_s = "jjdfafadskl (adsod)"
#print (test_s[test_s.find("(")+1:test_s.find(")")]) 


dict1= [{'creator':"lkfjslkjf",'id':"jhafdkjhak"},{'creator':"lkfjsl22kjf",'id':"jhaf213123dkjhak"}]

print ("lkfjsl22kjf"in dict1)