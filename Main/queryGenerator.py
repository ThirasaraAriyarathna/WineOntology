import rdflib

g = rdflib.Graph()
g.parse("wine.rdf")

# ?x wine:locatedIn ?region .
# ?x rdf:type wine:Winery . / ?x wine:hasMaker ?winery

results = g.query(
        """
        PREFIX wine: <http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#> 
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?region
        WHERE { 
           ?x wine:hasMaker ?region .
        }
        ORDER BY (?region)
        """)
for row in results:
    print(row.region)
    print
#PREFIX vin: <http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#>
#PREFIX owl: <http://www.w3.org/2002/07/owl#>
#PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>





#     ?x wine:hasFlavor wine:Strong .
#     ?x wine:locatedIn wine:NewZealandRegion .
#     ?x wine:hasSugar wine:Dry .

# PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#     PREFIX foaf: <http://xmlns.com/foaf/0.1/>
#     SELECT *
#        WHERE {
#           ?person foaf:name ?name.
#           ?person foaf:knows ?someone.
#           ?someone foaf:name ?name1.
#           FILTER(?name1 = \"prabodha\").




# def intentQuerySupport():

    # ?x wine:hasFlavor wine:Strong .
    # ?x wine:hasSugar wine:Dry

