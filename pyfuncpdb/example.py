import json
import requests

query= """
 {
       entry(entry_id: "4HHB") {
         struct {
            pdbx_descriptor
        }
          }
    }
 """
example = requests.post("https://data.rcsb.org/graphql", json={"query": query})


print(example.text)
