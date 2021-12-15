import rohub
import json


rohub.login(username="yourmailaddress", password="youroasswird#")
#roro = rohub.search_ros_by_id("c9d776f7-58a2-4576-b4c1-65913d1dd896")
#print (roro)
#licenses=show_available_licenses()
#print(licenses)
f = open("Massive-ROs-Creator\ROs.json", "r")
entry_json = f.read()
f.close()
entry_dictionary = json.loads(entry_json)

for ro in entry_dictionary:
    new_ro = rohub.ros_create(title=ro.get("name"), research_areas=["Biology"],description=ro.get("description"),ros_type='Data-centric Research Object',template="Data Centric Research Object folders structure")
    #new_ro.add_copyright(display_name=ro.get("Creator"))
    #new_ro.add_contributor(display_name=ro.get("Creator"))
    geolocation = ""
    if "geolocation" in ro:
        geo_type = ""
        raw_geolocation = ro.get("geolocation")
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

        new_ro.add_geolocation(body_specification_json=geolocation)

    folder_1 = new_ro.add_folders("Resources")
    #print(folder_1)
    folder_2 = new_ro.add_folders("Science Publications")
    #new_ro.add_author(predicate="Creator",display_name=ro.get("Creator"))
    #rohub.ros_add_author(identifier=new_ro.identifier,display_name=ro.get("Creator"))
    print(ro.get("Creator"))
    print(new_ro.get_content())
    new_ro.add_external_resource(res_type="Dataset",url=ro.get("url"),title=ro.get("name"),folder=folder_1.get("identifier"),description=ro.get("description"))
    for publication in ro.get("science publication"):
        if "http" in publication:
            new_ro.add_external_resource(res_type="Bibliographic Resource",url=publication,folder=folder_2.get("identifier"))
    if ("creativecommons.org/licenses/by/4.0/legalcode" in ro.get("license")): 
        new_ro.set_license("CC-BY-4.0")
    elif ("data.norge.no/nlod/en/1.0/" in ro.get("license")): 
        new_ro.set_license("NLOD-1.0")
    
    
    #new_ro.set_authors(agents=["George"])

    #new_ro.add_annotations()

    #ro.add_author("Geo H.")
    #ro.add_license("www.license.com")
    #ro.add_annotations("New annotation")
    #ro.add_contributor("Geo H.")
    #print(ro)
