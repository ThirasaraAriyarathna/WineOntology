import rdflib
import re


class QueryGenerator:

    g = rdflib.Graph()

    # prefixes for ontology querying
    RDF_PREFIX = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"
    RDFS_PREFIX = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>"
    WINE_PREFIX = "PREFIX wine: <http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#>"
    OWL_PREFIX = "PREFIX owl: <http://www.w3.org/2002/07/owl#>"
    FOOD_PREFIX = "PREFIX food: <http://www.w3.org/TR/2003/PR-owl-guide-20031209/food#> "

    outputAttribute = {"aboutWine": "wine", "aboutColor": "color", "aboutSugar": "sugar", "aboutFlavor": "flavor", "aboutBody": "body", "aboutGrape": "grape", "aboutMaker": "maker", "aboutRegion": "region", "info": "property"}
    queryAssets = {"sugar": '''{@wine@ wine:hasSugar @o@.} 
                                union {?baseWine rdfs:subClassOf ?restriction. ?restriction owl:onProperty wine:hasSugar. ?restriction owl:hasValue @0@. @wine@ a ?baseWine}. ''',
                   "flavor": '''{@wine@ wine:hasFlavor @o@.} 
                                union {?baseWine rdfs:subClassOf ?restriction. ?restriction owl:onProperty wine:hasFlavor. ?restriction owl:hasValue @o@. @wine@ a ?baseWine.}. ''',
                   "color": '''{@wine@ wine:hasColor @o@.}
                                union {?baseWine rdfs:subClassOf ?restriction. ?restriction owl:onProperty wine:hasColor. ?restriction owl:hasValue @o@. @wine@ a ?baseWine.}
                                union {?baseWine owl:intersectionOf ?list. ?list rdf:rest* [ rdf:first ?item ]. ?item owl:onProperty wine:hasColor. ?item owl:hasValue @o@. @wine@ a ?baseWine.}. ''',
                   "body": '''{@wine@ wine:hasBody @o@.}
                               union {?baseWine rdfs:subClassOf ?restriction. ?restriction owl:onProperty wine:hasBody. ?restriction owl:hasValue @o@. @wine@ a ?baseWine.}. ''',
                   "maker": '''{@wine@ wine:hasMaker @o@.}. ''',
                   "region": '''{@wine@ wine:locatedIn @o@.} 
                                 union {?baseWine rdfs:subClassOf ?restriction. ?restriction owl:onProperty wine:locatedIn. ?restriction owl:hasValue @o@. @wine@ a ?baseWine.} 
                                 union {?baseWine owl:intersectionOf ?list. ?list rdf:rest* [ rdf:first ?item ]. ?item owl:onProperty wine:locatedIn. ?item owl:hasValue @o@. @wine@ a ?baseWine.}. 
                                  ''',
                   "grape": '''{?wine wine:madeFromGrape @o@.}
                                union {?baseWine rdfs:subClassOf ?restriction. ?restriction owl:onProperty wine:madeFromGrape. ?restriction owl:hasValue @o@. ?wine a ?baseWine.} 
                                union {?baseWine owl:intersectionOf ?list. ?list rdf:rest* [ rdf:first ?item ]. ?item owl:onProperty wine:madeFromGrape. ?item owl:hasValue @o@. ?wine a ?baseWine.} 
                                union {?baseWine owl:intersectionOf ?list. ?list rdf:rest* [ rdf:first ?item ]. ?item owl:onProperty wine:madeFromGrape.?item owl:allValuesFrom ?class. ?class owl:oneOf ?list1. ?list1 rdf:rest* [rdf:first @o@]. ?wine a ?baseWine.}. '''
                   }

    def __init__(self):
        self.g.parse("wine.rdf")

    def assembler(self, intent, entities):
        queryCore = ''
        queryString = '''SELECT DISTINCT ?x WHERE { queryCore }'''
        queryString = queryString.replace("x", self.outputAttribute[intent])
        if intent == "info":
            if entities[0] == "wine":
                queryCore = "?property wine:hasMaker ?maker"
            else:
                queryCore = "?property rdf:type wine:" + entities[1]
        else:
            if intent == "aboutWine":
                pass
            else:
                queryCore += self.queryAssets[re.sub('about', '', intent).lower()]
                queryCore = re.sub('@o@', '?' + self.outputAttribute[intent], queryCore)
            # elif intent == "aboutColor":
            #     pass
            # elif intent == "aboutSugar":
            #     pass
            # elif intent == "aboutFlavor":
            #     pass
            # elif intent == "aboutBody":
            #     pass
            # elif intent == "aboutGrape":
            #     pass
            # elif intent == "aboutMaker":
            #     pass
            # elif intent == "aboutRegion":
            #     pass
            if entities["wine"] == 1:
                queryCore = re.sub('@wine@', "wine:" + entities["wine"][1], queryCore)
            else:
                for key in entities:
                    if entities[key][0] == 1:
                        entity = "wine:" + entities[key][1]
                        queryCore += re.sub('@o@', entity, self.queryAssets[key])
                    queryCore = re.sub('@wine@', '?wine', queryCore)

        # print queryCore
        queryString = queryString.replace("queryCore", queryCore)
        print queryString
        return queryString, self.outputAttribute[intent]

    def queryExecuter(self, queryString, output):
        results = []
        raw_results = self.g.query(
            self.RDF_PREFIX + self.WINE_PREFIX + self.OWL_PREFIX + self.FOOD_PREFIX + queryString)
        for row in raw_results:
            results.append(re.sub('http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#', '', str(row[output])))
        return results

    def queryAssembler(self, intent, entities):

        if intent == "aboutWine":
            queryString = '''   SELECT ?x
                                WHERE {
                                ?x wine:hasSugar  wine:''' + entities[0] + '''}'''
            output_variables = ["x"]
        elif intent == "flavor":
            queryString = '''   SELECT ?x
                                WHERE {
                                ?x wine:hasFlavor wine:''' + entities[0] + '''}'''
            output_variables = ["x"]
        elif intent == "winery":
            queryString = '''   SELECT ?x
                                WHERE {
                                ?x wine:hasMaker wine:''' + entities[0] + '''}'''
            output_variables = ["x"]
        elif intent == "region":
            queryString = '''   SELECT ?x
                                WHERE {
                                ?x wine:locatedIn wine:''' + entities[0] + '''}'''
            output_variables = ["x"]
        elif intent == "info":
            queryString = '''   SELECT DISTINCT ?x
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

# queryGenerator = QueryGenerator()
# queryGenerator.assembler('aboutWine', {"sugar": (1, "Sweet"), "flavor": (1, "Strong")})

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
    #                                 {?baseWine owl:intersectionOf ?list. ?list rdf:rest* [ rdf:first ?item ]. ?item owl:onProperty wine:madeFromGrape.?item owl:hasValue wine:''' + entity + '''. ?wine a ?baseWine.} union
    #                                 {?baseWine owl:intersectionOf ?list. ?list rdf:rest* [ rdf:first ?item ]. ?item owl:onProperty wine:madeFromGrape.?item owl:allValuesFrom ?class. ?class owl:oneOf ?list1. ?list1 rdf:rest* [rdf:first wine:''' + entity + ''']. ?wine a ?baseWine.}.'''


