import rdflib
from nltk.stem.lancaster import LancasterStemmer

g = rdflib.Graph()
g.parse("wine.rdf")

# prefixes for ontology querying
RDF_PREFIX = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
RDFS_PREFIX = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>"
WINE_PREFIX = "PREFIX wine: <http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#>"
OWL_PREFIX = "PREFIX owl: <http://www.w3.org/2002/07/owl#>"
FOOD_PREFIX = "PREFIX food: <http://www.w3.org/TR/2003/PR-owl-guide-20031209/food#> "

# queryString = '''SELECT (COUNT(?wine) AS ?wine) WHERE {
#                 SELECT DISTINCT ?wine  WHERE {
#                 {?wine wine:hasSugar wine:Dry.} union
#                 {?baseWine rdfs:subClassOf ?restriction. ?restriction owl:onProperty wine:hasSugar. ?restriction owl:hasValue wine:Dry. ?wine a ?baseWine.} union
#                 {?baseWine owl:intersectionOf ?list. ?list rdf:rest* [ rdf:first ?item ]. ?item owl:onProperty wine:hasSugar. ?item owl:hasValue wine:Dry. ?wine a ?baseWine.}.}}'''

queryString = '''SELECT ?wine WHERE {?wine rdf:type owl:Restriction. ?wine owl:onProperty wine:hasColor. ?wine owl:hasValue wine:Red}'''
raw_results = g.query(RDF_PREFIX + WINE_PREFIX + OWL_PREFIX + FOOD_PREFIX + queryString)
for row in raw_results:
    print row.wine
    # print row.y
    # print row.x
    # print row.a

