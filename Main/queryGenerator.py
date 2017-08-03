import rdflib
import re


class QueryGenerator():

    g = rdflib.Graph()
    g.parse("wine.rdf")

    # prefixes for ontology querying
    RDF_PREFIX = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
    RDFS_PREFIX = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>"
    WINE_PREFIX = "PREFIX wine: <http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#>"

    def queryAssembler(self, intent, entities):

        if intent == "sugar":
            queryString = '''   SELECT ?x
                                WHERE {
                                ?x wine:hasSugar  wine:''' + entities[0] + '''}'''
            output_variables = ["x"]
        elif intent == "flavor":
            queryString = queryString = '''   SELECT ?x
                                WHERE {
                                ?x wine:hasFlavor wine:''' + entities[0] + '''}'''
            output_variables = ["x"]
        elif intent == "winery":
            queryString = queryString = '''   SELECT ?x
                                WHERE {
                                ?x wine:hasMaker wine:''' + entities[0] + '''}'''
            output_variables = ["x"]
        elif intent == "region":
            queryString = queryString = '''   SELECT ?x
                                WHERE {
                                ?x wine:locatedIn wine:''' + entities[0] + '''}'''
            output_variables = ["x"]
        elif intent == "info":
            queryString = queryString = '''   SELECT DISTINCT ?y
                                             WHERE {
                                             ?x wine:''' + entities[0] + ''' ?y
                                             }'''
            output_variables = ["y"]
        return {"queryString": queryString, "output": output_variables}

    def processor(self, intent, isInfo, entities):

        queryInputs = self.queryAssembler(intent, entities)
        raw_results = self.g.query(self.RDF_PREFIX + self.WINE_PREFIX + queryInputs["queryString"])
        results = {}
        if isInfo:
            arr = []
            for row in raw_results:
                arr.append(re.sub('http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#', '', str(row.y)))
            results["keywords"] = arr
        else:
            for output in queryInputs["output"]:
                arr = []
                for row in raw_results:
                    arr.append(row[output])
                results[output] = arr
        return results



# ?x wine:locatedIn ?region .
# ?x rdf:type wine:Winery . / ?x wine:hasMaker ?winery
# queryString = queryString = '''   SELECT DISTINCT ?y
#                                   WHERE {
#                                   ?x wine:hasSugar ?y
#                                   }'''
# results = g.query(RDF_PREFIX + WINE_PREFIX + queryString)
# sugarTypes = []
# for row in results:
#         sugarTypes.append(re.sub('http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#', '', str(row.y)))
#         print sugarTypes

# def supportQuery(type):
#     keywords = []
#     if type == 1:
#         queryString = queryString = '''   SELECT DISTINCT ?y
#                                   WHERE {
#                                   ?x wine:hasSugar ?y
#                                   }'''
#         results = g.query(RDF_PREFIX + WINE_PREFIX + queryString)
#
#         for row in results:
#             keywords.append(re.sub('http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#', '', str(row.y)))
#
#
#     elif type == 2:
#         queryString = queryString = '''   SELECT DISTINCT ?y
#                                           WHERE {
#                                           ?x wine:hasFlavor ?y
#                                           }'''
#         results = g.query(RDF_PREFIX + WINE_PREFIX + queryString)
#
#     print keywords
#     return keywords


# results = g.query(
#         RDF_PREFIX + WINE_PREFIX +
#         """
#         SELECT ?winery
#         WHERE {
#            ?x
#         }
#         ORDER BY (?region)
#         """)
# for row in results:
#     print(row.winery)
#     print
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

