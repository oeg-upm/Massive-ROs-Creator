from turtle import pu
import requests
import json

f = open("GIT\Massive-ROs-Creator\ROs.json", "r")
entry_json = f.read()
f.close()
entry_dictionary = json.loads(entry_json)

def openAire_datasets(doi:str):
        openAireURL = "https://api.openaire.eu/search/datasets"

        payload = {
                'doi': doi,
                'format': "json",
                'size':100
        }
        response = requests.get(openAireURL, params=payload).json()
        #f = open("Massive-ROs-Creator\Enrichment.json", "w")
        #f.write(json.dumps(response, indent=4, sort_keys=True))
        #f.close()
        #print (response)
        if '"results": null' in str(response):
                return None
        else:
                #print(type(response))
                return response
        
        

def openAire_pub(doi:str):
        openAireURL = "https://api.openaire.eu/search/publications"

        payload = {
                'doi': doi,
                'format': "json",
                'size':100
        }
        response = requests.get(openAireURL, params=payload).json()
        
        #print (response)
        if "'results': None" in str(response):
                return None
        else:
                #print(type(response))
                return response
        
        
enriched_ROs = []
for ro in entry_dictionary:
        enrichment_RO_raw = openAire_datasets(ro.get("id")) 
        if enrichment_RO_raw != None and not "'results': None" in str(enrichment_RO_raw):
                #print(enrichment_RO_raw)
                enrichment_RO_raw = enrichment_RO_raw.get("response").get("results").get("result")[0]
                ro["date_of_collection"] = enrichment_RO_raw.get("header").get("dri:dateOfCollection").get("$")
                ro["date_of_transformation"] = enrichment_RO_raw.get("header").get("dri:dateOfTransformation").get("$")
                enrichment_RO_raw = enrichment_RO_raw.get("metadata").get("oaf:entity").get("oaf:result")

                if "classname" in enrichment_RO_raw.get("bestaccessright").keys() : 
                        ro["bestaccessright"] = enrichment_RO_raw.get("bestaccessright").get("classname")

                if "children" in enrichment_RO_raw.keys():
                        if "result" in enrichment_RO_raw.get("children").keys():
                                results = []
                                for result in enrichment_RO_raw.get("children").get("result"):
                                        dateofacceptance = ""
                                        publisher = ""
                                        if "dateofacceptance" in result.keys():
                                                dateofacceptance = result.get("dateofacceptance").get("$")
                                        if "publisher" in result.keys():
                                                publisher = result.get("publisher").get("$")
                                        result_aux = {"date_of_acceptance":dateofacceptance, "publisher":publisher}
                                        results.append(result_aux)
                                ro["Children Results"] = results
                #print (enrichment_RO_raw.get("collectedfrom"))
                collectedfrom = []

                if type(enrichment_RO_raw.get("collectedfrom"))==list and "collectedfrom" in enrichment_RO_raw.keys():
                        collectedfrom = []
                        for source in enrichment_RO_raw.get("collectedfrom"):
                                name = ""
                                #print (source)
                                if type(source)==dict and "@name" in source.keys():
                                        #print (source)
                                        name = source.get("@name")
                                        #print (name)
                                        collectedfrom.append(name)
                              
                        ro["Collected From"] = collectedfrom
                elif (enrichment_RO_raw.get("collectedfrom"))==dir:
                        name = enrichment_RO_raw.get("collectedfrom").get("@name")
                        collectedfrom.append(name)


                if "creator" in enrichment_RO_raw.keys():
                        if not ro.get("Creator") == None:
                                creator_list = ro.get("Creator")
                                #print (creator_list)
                        else:
                                creator_list = []
                        
                        for creator in enrichment_RO_raw.get("creator"):
                        
                                #print (creator)
                                if type(creator) == dict:
                                        creator_list.append(creator)
                        #print (creator_list)
                        ro["Creator"] = creator_list
                ####################All creator ????????????


                if "language" in  enrichment_RO_raw.keys():
                        language = ""
                        if "@classname" in enrichment_RO_raw.get("language").keys():
                                language = enrichment_RO_raw.get("language").get("@classname")
                        ro["language"] = language

                if "publisher" in enrichment_RO_raw.keys():
                        publisher = enrichment_RO_raw.get("publisher").get("$")
                        ro["publisher"] = publisher

                if "resourcetype" in enrichment_RO_raw.keys():
                        resourcetype = enrichment_RO_raw.get("resourcetype").get("@classname")
                        ro["resourcetype"] = publisher

                if "subject" in enrichment_RO_raw.keys():
                        subject_list = ro["research area"]
                        for subject in enrichment_RO_raw.get("subject"):
                                name = subject.get("$")
                                #print (name)
                                if name not in subject_list:
                                        subject_list.append(name)
                        ro["research area"] = subject_list


        for publication in ro.get("science publication"):
                if "doi.org" in publication:
                        publication_doi = publication[publication.find(".org")+5:]
                        enrichment_SP_raw = openAire_pub(publication_doi)
                        
                       
                        if enrichment_SP_raw != None:
                                enrichment_SP_raw = enrichment_SP_raw.get("response").get("results").get("result")[0].get("metadata").get("oaf:entity").get("oaf:result")
                            
                                #f = open("Massive-ROs-Creator\Enrichment.json", "w")
                                #f.write(json.dumps(enrichment_SP_raw, indent=4, sort_keys=True))
                                #f.close()
                                #print(enrichment_SP_raw)
                                creator_list = []
                                if type(enrichment_SP_raw.get("creator"))==list:
                                        for creator in enrichment_SP_raw.get("creator"):
                                                if type(creator)==dict:
                                                        #print (creator)
                                                        creator_list.append({"$" : creator.get("$"),"@rank" : creator.get("@rank")})
                                else:
                                        if type(creator)==dict:
                                                
                                                creator_list.append({"$" : creator.get("$"),"@rank" : creator.get("@rank")})
                                relevant_date_list = []
                                for date in enrichment_SP_raw.get("relevantdate"):
                                        #print (date)
                                        if type(date)==dict:
                                                relevant_date_list.append({"$" : date.get("$"),"@classid" : date.get("@classid")})
                                subject_list = []
                                if type(enrichment_SP_raw.get("subject"))==list:
                                        for subject in enrichment_SP_raw.get("subject"):
                                                subject_list.append(subject.get("$"))
                               
                                country_list = []
                                if (type(enrichment_SP_raw.get("country"))==list):
                                        for country in enrichment_SP_raw.get("country"):
                                                #print(country)
                                                country_list.append(country.get("@classname"))
                                elif (not enrichment_SP_raw.get("country")==None):
                                        #print(enrichment_SP_raw.get("country"))
                                        country_list.append(enrichment_SP_raw.get("country").get("@classname"))
                                format_list = []
                                if type(enrichment_SP_raw.get("format"))==list:
                                        for format in enrichment_SP_raw.get("format"):
                                                format_list.append(format.get("$"))
                                elif (not enrichment_SP_raw.get("format") == None):
                                        format_list.append(enrichment_SP_raw.get("format").get("$"))
                                enrichment_SP = {}
                                try:
                                        enrichment_SP["publication"] = publication,
                                except:
                                        continue
                                try:
                                        enrichment_SP["@bestaccessright_classname"] = enrichment_SP_raw.get("bestaccessright").get("@classname")
                                except:
                                        continue
                                try:

                                        enrichment_SP["@country_classname"] = country_list
                                except:
                                        continue
                                try:
                                        enrichment_SP["creator"] = creator_list
                                except:
                                        continue
                                try:
                                        enrichment_SP["date_of_acceptance"] = enrichment_SP_raw.get("dateofacceptance").get("$")
                                except:
                                        continue
                                try:
                                        enrichment_SP["format"] = format_list
                                except:
                                        continue
                                try:
                                        enrichment_SP["@language_classname"] = enrichment_SP_raw.get("language").get("@classname")
                                except:
                                        continue
                                try:
                                        enrichment_SP["relevant_date"] = enrichment_SP_raw.get("resulttype").get("@classid")
                                except:
                                        continue
                                try:
                                        enrichment_SP["@resulttype_publication"] = relevant_date_list
                                except:
                                        continue
                                try:
                                        enrichment_SP["subject"] = subject_list
                                except:
                                        continue
                                
                                         
                                
                                if ("context" in enrichment_SP_raw.keys()):
                                        #print(enrichment_SP_raw.get("context"))
                                        if (type(enrichment_SP_raw.get("context"))==dict):
                                                enrichment_SP["context"] =  {
                                                        "@label" : enrichment_SP_raw.get("context").get("@label"),
                                                        "@type" : enrichment_SP_raw.get("context").get("@type"),
                                                }
                                                if "category" in enrichment_SP_raw.get("context"):
                                                        enrichment_SP["context"]["@category_label"] = enrichment_SP_raw.get("context").get("category").get("@label")
                                        elif (type(enrichment_SP_raw.get("context"))==list):
                                                enrichment_SP["context"] = []
                                                for context in enrichment_SP_raw.get("context"):
                                                        aux = {
                                                        "@label" : context.get("@label"),
                                                        "@type" : context.get("@type"),
                                                         }
                                                        if "category" in context.keys():
                                                                #print (context)
                                                                if type(context.get("category"))==dict:
                                                                        aux["@category_label"] = context.get("category").get("@label")
                                                                elif type (context.get("category"))==list:
                                                                        aux["@category_label"] = []
                                                                        for cat in context.get("category"):
                                                                                aux["@category_label"].append(cat.get("@label"))
                                                        enrichment_SP["context"].append(aux)
                                ro["science publication"].append (enrichment_SP)
                                try:
                                        ro["science publication"].remove (enrichment_SP.get("publication")[0])
                                except:
                                        continue
        
        enriched_ROs.append(ro)

f = open("GIT\Massive-ROs-Creator\enrichedROs.json", "w")
f.write(json.dumps(enriched_ROs, indent=4, sort_keys=True))
f.close()


        #print(response.json())
