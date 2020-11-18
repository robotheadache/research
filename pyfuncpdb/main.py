from pypdb import *
import json 
import requests
import threading
import csv
import time 


start = time.perf_counter()
rcsb="https://data.rcsb.org/graphql"
found_pdbs = Query('6EQE', query_type="structure").search()

hits = []
funcGroup = "C(=O)O"
def parseData(jsondata, funcGroup, protName):
    if jsondata["data"]["entry"]["nonpolymer_entities"] != None:
        for ent in jsondata["data"]["entry"]["nonpolymer_entities"]:
            if funcGroup in ent['nonpolymer_comp']['rcsb_chem_comp_descriptor']['SMILES']:
                print(funcGroup + " found!")
                hits.append(protName)
                break
    print("Finished parsing protein", protName)
    
print("There are " + str(len(found_pdbs)) + " proteins!")
for protein in found_pdbs:
    query = """{
      entry(entry_id: "%s") {
        nonpolymer_entities {
          nonpolymer_comp {
            rcsb_chem_comp_descriptor {
              SMILES
            }
          }
        }
      }
    }""" % protein
    ligands = requests.post(rcsb, json={'query' : query})
    
    if ligands.status_code == 200:
       try:
            threading.Thread(target=parseData, args=(json.loads(ligands.text), funcGroup, protein)).start()
       except:
            print ("Error: unable to start thread")
    else:
        print("Request threw an oopsie: " + ligands.status_code)

elapsed_time = time.perf_counter() - start

print("Finished parsing in " + str(elapsed_time) + " seconds.")
print("Approximately " + str(elapsed_time/len(found_pdbs)) + " per protein.")


with open("output.csv", 'w') as out:
        outFile = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for protein in hits:
            outFile.writerow(protein)

