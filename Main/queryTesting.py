import rdflib

g = rdflib.Graph()
g.parse("wine.rdf")

# prefixes for ontology querying
RDF_PREFIX = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
RDFS_PREFIX = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>"
WINE_PREFIX = "PREFIX wine: <http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#>"

queryString = '''   SELECT ?x
                                WHERE {
                                ?x rdf:type  wine:Winery}'''
raw_results = g.query(RDF_PREFIX + WINE_PREFIX + queryString)
for row in raw_results:
    print row.x
