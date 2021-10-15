# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import csv, time

import sys
from SPARQLWrapper import SPARQLWrapper, JSON


inputTsvFile = "../output/data.csv"

language = "fr"

properties = "P625,P17,P18,P281,P856,P268,P1566"

endpoint_url = "https://query.wikidata.org/sparql"

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

print("Reading input file to extract locations")
rows = []
with open(inputTsvFile, newline='\n', encoding="utf-8") as csvfile:
   spamreader = csv.reader(csvfile, delimiter='\t', quotechar='¤')
   readingLocation = False
   locations = {}
   lemmaLocations = {}
   location = ""
   lemmaLocation = ""
   locationLines = []
   lineNb = 0
   locationNb = 0
   for row in spamreader:
      rows.append(row + [""])
      if readingLocation:
         if len(row) > 12 and row[12] == "I-loc":
            # We are still reading a location
            if (len(locationLines) > 0) and (location[len(location)-1:len(location)] != "'") and (location[len(location)-1:len(location)] != "ʼ") and (location[len(location)-1:len(location)] != "’"):
               location += " "
            location += row[0]
            if (len(locationLines) > 0) and (lemmaLocation[len(lemmaLocation)-1:len(lemmaLocation)] != "'") and (lemmaLocation[len(lemmaLocation)-1:len(lemmaLocation)] != "ʼ") and (lemmaLocation[len(lemmaLocation)-1:len(lemmaLocation)] != "’"):
               lemmaLocation += " "
            lemmaLocation += row[1]
            locationLines.append(lineNb)
         else:
            # We have finished reading the location name: store the line numbers corresponding to this location
            readingLocation = False
            locationNb += 1
            if location in locations:
               locations[location] += locationLines
            else:
               locations[location] = locationLines
            if lemmaLocation in lemmaLocations:
               lemmaLocations[lemmaLocation] += locationLines
            else:
               lemmaLocations[lemmaLocation] = locationLines
            locationLines = []
            location = ""
            lemmaLocation = ""
      if len(row) > 12 and row[12] == "B-loc":
         # We are starting to read a new location name
         if (len(locationLines) > 0) and (location[len(location)-1:len(location)] != "'") and (location[len(location)-1:len(location)] != "ʼ") and (location[len(location)-1:len(location)] != "’"):
            location += " "
         if (len(locationLines) > 0) and (lemmaLocation[len(lemmaLocation)-1:len(lemmaLocation)] != "'") and (lemmaLocation[len(lemmaLocation)-1:len(lemmaLocation)] != "ʼ") and (lemmaLocation[len(lemmaLocation)-1:len(lemmaLocation)] != "’"):
            lemmaLocation += " "
         
         location += row[0]
         lemmaLocation += row[1]
         locationLines.append(lineNb)
         readingLocation = True
      lineNb += 1
      #print(lineNb)
      #print(', '.join(row))   
   if readingLocation:
      # We have finished reading the location name: store the line numbers corresponding to this location
      locationNb += 1
      if location in locations:
         locations[location] += locationLines
      else:
         locations[location] = locationLines
      if lemmaLocation in lemmaLocations:
         lemmaLocations[lemmaLocation] += locationLines
      else:
         lemmaLocations[lemmaLocation] = locationLines

locationList = sorted(lemmaLocations.keys())
print(str(len(locationList)) + " distinct locations found in a total of " + str(locationNb) + " locations.")

def findBestWikidata(query, wikidataResults):
      wikidataId = ""
      bestScore = 0
      for result in wikidataResults:
         #print(result)
         score = len(result.keys())
         # Bonus if the name matches exactly
         if query.lower() == result["itemLabel"]["value"].lower():
            score += 1
         if score > bestScore:
            bestScore = score
            wikidataId = result["item"]["value"]
            print("Found " + result["item"]["value"] + " (score: " + str(score) + ")")
            print(" => " + result["itemLabel"]["value"])
      return wikidataId

wikidataLoc = {}
for loc in locationList:
   # Build Wikidata query
   variables = "?item ?itemLabel";
   subject = "?item";
   focus = '  {?item rdfs:label "' + loc + '"@' + language + '} UNION {?item skos:altLabel "' + loc + '"@' + language + '}'
   constraints = ' WHERE {\n' + focus
   for prop in properties.split(","):
      variables += " ?" + prop + " ?" + prop + "Label";
      constraints += ".\n OPTIONAL{ " + subject + " wdt:" + prop + " ?" + prop + "}";
   sparqlQuery = "SELECT " + variables + constraints + ".\n SERVICE wikibase:label { bd:serviceParam wikibase:language \"[AUTO_LANGUAGE]," + language + "\". }\n }\n GROUP BY " + variables;
   print(" ")
   print("Looking for " + loc)
   
   wikidataResults = get_results(endpoint_url, sparqlQuery)["results"]["bindings"] 
   print(str(len(wikidataResults)) + " wikidata results found.")
   if len(wikidataResults) > 0:
      wikidataLoc[loc] = findBestWikidata(loc, wikidataResults)
      print("test =" + wikidataLoc[loc])
      print(lemmaLocations[loc])
      for line in lemmaLocations[loc]:
         rows[line][len(rows[line])-1] = wikidataLoc[loc]
      print("Inserted this wikidata Id into " + str(len(lemmaLocations[loc])) + " lines")
   else:
      print("No result found on Wikidata")
   
   
   time.sleep(2)
   
with open(inputTsvFile + ".wikidata.tsv", 'w', newline='', encoding="utf-8") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='\t',
                            quotechar='¤', quoting=csv.QUOTE_MINIMAL)
    for row in rows:
       spamwriter.writerow(row)