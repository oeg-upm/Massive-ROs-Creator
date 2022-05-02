import  rohub, time, json, sys
import threading
from threading import Thread


session_lock = False
updater_lock = False

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

rohub.login(username="georgehadib@gmail.com", password="George123#")

lista = rohub.list_my_ros()


def session_controler():
    while t1.is_alive():
        
        time.sleep(840)
        while updater_lock:
            time.sleep(1)
        session_lock = True
        rohub.login(username="georgehadib@gmail.com", password="George123#")
        session_lock = False

def ros_updater ():
    failed=[]
    
    for ro in entry_dictionary:
        updater_lock = True
        while session_lock:
            time.sleep(1)
        if (ro.get("name")[-1]==" "):
            ro["name"] = ro.get("name")[:-1]
        try:
            annotation_list = []
            citation = {"property":"http://purl.org/dc/terms/bibliographicCitation", "value":ro.get("citation")}
            created_on = {"property":"http://purl.org/dc/terms/created", "value":ro.get("created on")}
            data_manager = {"property":"https://schema.org/maintainer", "value":ro.get("data manager")}
            depositor = {"property":"https://schema.org/publisher", "value":ro.get("depositor")}
            rights_holder = {"property":"http://purl.org/dc/terms/rightsHolder", "value":ro.get("rights holder")}
            type = {"property":"http://purl.org/dc/terms/type", "value":ro.get("type")}
            id = lista.loc[lista.title == ro.get("name"),"identifier"].values[0]
            res_list =rohub.ros_list_resources(id)
            res = res_list.loc[res_list.type == "Dataset","identifier"].values[0]
            annotation_list.append(citation)
            annotation_list.append(created_on)
            annotation_list.append(data_manager)
            annotation_list.append(depositor)
            annotation_list.append(rights_holder)
            annotation_list.append(type)
            rohub.ros_add_annotations(identifier=id,resources=[res],body_specification_json= annotation_list)
            print("Annotations were added to Research Object with ID: "+id)  
        except: 
            print("No annotations were added to Research Object with name: "+ro.get("name")+". Please make sure that the RO exists.")
            failed.append(ro.get("name"))

        updater_lock = False
t1= threading.Thread(target=ros_updater)
t2= threading.Thread(target=session_controler)
t2.setDaemon(True)
t1.start()
t2.start()