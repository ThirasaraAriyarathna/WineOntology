import rdflib
import re


class QueryGenerator():

    g = rdflib.Graph()
    g.parse("wine.rdf")

    # prefixes for ontology querying
    RDF_PREFIX = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
    RDFS_PREFIX = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>"
    WINE_PREFIX = "PREFIX wine: <http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#>"
    OWL_PREFIX = "PREFIX owl: <http://www.w3.org/2002/07/owl#>"
    FOOD_PREFIX = "PREFIX food: <http://www.w3.org/TR/2003/PR-owl-guide-20031209/food#> "

    outputAttribute = {"aboutWine": "wine", "aboutColor": "color", "aboutSugar":"sugar", "aboutFlavor": "flavor", "aboutBody": "body", "aboutGrape": "grape", "aboutMaker": "maker", "aboutRegion": "region"}
    queryAssets = {"sugar": ['''{?wine wine:hasSugar wine:''',
                            '''.} union {?baseWine rdfs:subClassOf ?restriction. ?restriction owl:onProperty wine:hasSugar. ?restriction owl:hasValue wine:''',
                            '''. ?wine a ?baseWine.}. '''],
                   "flavor": ['''{?wine wine:hasFlavor wine:''',
                            '''.} union {?baseWine rdfs:subClassOf ?restriction. ?restriction owl:onProperty wine:hasFlavor. ?restriction owl:hasValue wine:''',
                            '''. ?wine a ?baseWine.}. '''],
                   "color": ['''{?wine wine:hasColor wine:''',
                              '''.} union {?baseWine rdfs:subClassOf ?restriction. ?restriction owl:onProperty wine:hasColor. ?restriction owl:hasValue wine:''',
                              '''. ?wine a ?baseWine.} union {?baseWine owl:intersectionOf ?list. ?list rdf:rest* [ rdf:first ?item ]. ?item owl:onProperty wine:hasColor. ?item owl:hasValue wine:''',
                              '''. ?wine a ?baseWine.}. '''],
                   "body": ['''{?wine wine:hasBody wine:''',
                              '''.} union {?baseWine rdfs:subClassOf ?restriction. ?restriction owl:onProperty wine:hasBody. ?restriction owl:hasValue wine:''',
                              '''. ?wine a ?baseWine.}. '''],
                   "maker": ['''{?wine wine:hasMaker wine:''',
                              '''.}. '''],
                   "region": ['''{?wine wine:locatedIn wine:''',
                              '''.} union {?baseWine rdfs:subClassOf ?restriction. ?restriction owl:onProperty wine:locatedIn. ?restriction owl:hasValue wine:''',
                              '''. ?wine a ?baseWine.} union {?baseWine owl:intersectionOf ?list. ?list rdf:rest* [ rdf:first ?item ]. ?item owl:onProperty wine:locatedIn. ?item owl:hasValue wine:''',
                              '''. ?wine a ?baseWine.}. NOT EXISTS{?wine a wine:Region}.'''],
                   "grape": ['''{?wine wine:madeFromGrape wine:''',
                             '''.} union {?baseWine rdfs:subClassOf ?restriction. ?restriction owl:onProperty wine:madeFromGrape. ?restriction owl:hasValue wine:''',
                             '''. ?wine a ?baseWine.} union {?baseWine owl:intersectionOf ?list. ?list rdf:rest* [ rdf:first ?item ]. ?item owl:onProperty wine:madeFromGrape. ?item owl:hasValue wine:''',
                             '''.} union {?baseWine owl:intersectionOf ?list. ?list rdf:rest* [ rdf:first ?item ]. ?item owl:onProperty wine:madeFromGrape.?item owl:allValuesFrom ?class. ?class owl:oneOf ?list1. ?list1 rdf:rest* [rdf:first wine:''',
                             ''']. ?wine a ?baseWine.}.''']
                   }
    # sugar = '''{?wine wine:hasSugar wine:''' + entity + '''.} union
    #                                 {?baseWine rdfs:subClassOf ?restriction. ?restriction owl:onProperty wine:hasSugar. ?restriction owl:hasValue wine:''' + entity + '''. ?wine a ?baseWine.} union
    #                                 {?baseWine owl:intersectionOf ?list. ?list rdf:rest* [ rdf:first ?item ]. ?item owl:onProperty wine:hasSugar.?item owl:hasValue wine:''' + entity + '''. ?wine a ?baseWine.}.'''
    # flavor = '''{?wine wine:hasFlavor wine:''' + entity + '''.} union
    #                                 {?baseWine rdfs:subClassOf ?restriction. ?restriction owl:onProperty wine:hasSugar. ?restriction owl:hasValue wine:''' + entity + '''. ?wine a ?baseWine.} union
    #                                 {?baseWine owl:intersectionOf ?list. ?list rdf:rest* [ rdf:first ?item ]. ?item owl:onProperty wine:hasFlavor.?item owl:hasValue wine:''' + entity + '''. ?wine a ?baseWine.}.'''
    # color = '''{?wine wine:hasColor wine:''' + entity + '''.} union
    #                                 {?baseWine rdfs:subClassOf ?restriction. ?restriction owl:onProperty wine:hasColor. ?restriction owl:hasValue wine:''' + entity + '''. ?wine a ?baseWine.} union
    #                                 {?baseWine owl:intersectionOf ?list. ?list rdf:rest* [ rdf:first ?item ]. ?item owl:onProperty wine:hasColor.?item owl:hasValue wine:''' + entity + '''. ?wine a ?baseWine.}.'''
    # body = '''{?wine wine:hasBody wine:''' + entity + '''.} union
    #                                 {?baseWine rdfs:subClassOf ?restriction. ?restriction owl:onProperty wine:hasBody. ?restriction owl:hasValue wine:''' + entity + '''. ?wine a ?baseWine.} union
    #                                 {?baseWine owl:intersectionOf ?list. ?list rdf:rest* [ rdf:first ?item ]. ?item owl:onProperty wine:hasBody.?item owl:hasValue wine:''' + entity + '''. ?wine a ?baseWine.}.'''
    # maker = '''{?wine wine:hasMaker wine:''' + entity + '''.} union
    #                                 {?baseWine rdfs:subClassOf ?restriction. ?restriction owl:onProperty wine:hasMaker. ?restriction owl:hasValue wine:''' + entity + '''. ?wine a ?baseWine.} union
    #                                 {?baseWine owl:intersectionOf ?list. ?list rdf:rest* [ rdf:first ?item ]. ?item owl:onProperty wine:hasMaker.?item owl:hasValue wine:''' + entity + '''. ?wine a ?baseWine.}.'''
    # region = '''{?wine wine:locatedIn wine:''' + entity + '''.} union
    #                                 {?baseWine rdfs:subClassOf ?restriction. ?restriction owl:onProperty wine:locatedIn. ?restriction owl:hasValue wine:''' + entity + '''. ?wine a ?baseWine.} union
    #                                 {?baseWine owl:intersectionOf ?list. ?list rdf:rest* [ rdf:first ?item ]. ?item owl:onProperty wine:locatedIn.?item owl:hasValue wine:''' + entity + '''. ?wine a ?baseWine.}.
    #                                 not exists{?wine a wine:Region}.'''
    # grape = '''{?wine wine:madeFromGrape wine:''' + entity + '''.} union
    #                                 {?baseWine rdfs:subClassOf ?restriction. ?restriction owl:onProperty wine:madeFromGrape. ?restriction owl:hasValue wine:''' + entity + '''. ?wine a ?baseWine.} union
    #                                 {?baseWine owl:intersectionOf ?list. ?list rdf:rest* [ rdf:first ?item ]. ?item owl:onProperty wine:madeFromGrape.?item owl:hasValue wine:''' + entity + '''.} union
    #                                 {?baseWine owl:intersectionOf ?list. ?list rdf:rest* [ rdf:first ?item ]. ?item owl:onProperty wine:madeFromGrape.?item owl:allValuesFrom ?class. ?class owl:oneOf ?list1. ?list1 rdf:rest* [rdf:first wine:''' + entity + ''']. ?wine a ?baseWine.}.'''

    def assembler(self, intent, entities):
        queryCore = ''
        queryString = '''SELECT ?x WHERE { queryCore }'''
        if intent == "aboutWine":
            queryString = queryString.replace("x", self.outputAttribute[intent])
            for key in entities:
                if entities[key][0] == 1:
                    entity = entities[key][1]
                    queryCore +=self.queryAssets[key][0]
                    for i in self.queryAssets[key][1:]:
                        queryCore += entity
                        queryCore += i
            print queryCore
            print queryString.replace("queryCore", queryCore)
            queryString = queryString.replace("queryCore", queryCore)
            raw_results = self.g.query(self.RDF_PREFIX + self.WINE_PREFIX + self.OWL_PREFIX + self.FOOD_PREFIX + queryString)
            for row in raw_results:
                print row[self.outputAttribute[intent]]

        elif intent == "aboutColor":
            pass
        elif intent == "aboutSugar":
            pass
        elif intent == "aboutFlavor":
            pass
        elif intent == "aboutBody":
            pass
        elif intent == "aboutGrape":
            pass
        elif intent == "aboutMaker":
            pass
        elif intent == "aboutRegion":
            pass

    def queryAssembler(self, intent, entities):



        if intent == "aboutWine":
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
            queryString = queryString = '''   SELECT DISTINCT ?x
                                             WHERE {
                                             ?x rdf:type wine:''' + entities[0] + '''}'''
            output_variables = ["x"]
        return {"queryString": queryString, "output": output_variables}

    def processor(self, intent, isInfo, entities):

        queryInputs = self.queryAssembler(intent, entities)
        raw_results = self.g.query(self.RDF_PREFIX + self.WINE_PREFIX + self.RDFS_PREFIX + self.OWL_PREFIX + self.FOOD_PREFIX + queryInputs["queryString"])
        results = {}
        if isInfo:
            arr = []
            for row in raw_results:
                arr.append(re.sub('http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#', '', str(row.x)))
            results["keywords"] = arr
        else:
            for output in queryInputs["output"]:
                arr = []
                for row in raw_results:
                    arr.append(row[output])
                results[output] = arr
        return results

queryGenerator = QueryGenerator()
queryGenerator.assembler('aboutWine', {"sugar": (1, "Sweet"), "flavor": (1, "Strong")})

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

