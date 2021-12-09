import rohub
import json

rohub.login(username="georgehadib@gmail.com", password="George123#")
#roro = rohub.search_ros_by_id("c9d776f7-58a2-4576-b4c1-65913d1dd896")
#print (roro)
#licenses=show_available_licenses()
#print(licenses)
f = open("Massive-ROs-Creator\ROs.json", "r")
entry_json = f.read()
f.close()
entry_dictionary = json.loads(entry_json)

for ro in entry_dictionary:
    new_ro = rohub.ros_create(title=ro.get("name"), research_areas=["Biology"],description=ro.get("description"),ros_type='Executable Research Object')
    #new_ro.add_copyright(display_name=ro.get("Creator"))
    #new_ro.add_contributor(display_name=ro.get("Creator"))
    folder_1 = new_ro.add_folders("Resources")
    #print(folder_1)
    folder_2 = new_ro.add_folders("Science Publications")
    new_ro.add_author(predicate="Creator",display_name=ro.get("Creator"))
    rohub.ros_add_author(identifier=new_ro.identifier,display_name=ro.get("Creator"))
    print(ro.get("Creator"))
    print(new_ro.get_content())
    new_ro.add_external_resource(res_type="Dataset",url=ro.get("url"),title=ro.get("name"),folder=folder_1.get("identifier"),description=ro.get("description"))
    for publication in ro.get("science publication"):
        if "http" in publication:
            new_ro.add_external_resource(res_type="Bibliographic Resource",url=publication,folder=folder_2.get("identifier"))
    new_ro.add_license("CC-BY-4.0")
    #new_ro.add_author()



    #new_ro.add_annotations()

    #ro.add_author("Geo H.")
    #ro.add_license("www.license.com")
    #ro.add_annotations("New annotation")
    #ro.add_contributor("Geo H.")
    #print(ro)

