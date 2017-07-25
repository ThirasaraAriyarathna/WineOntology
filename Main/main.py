from languageProcessor import intentIdentifier

'''
Possible questions

-what are the available <low> sugar wines?
-what are the matching wines for <food>?
-what are the wines produced from <winery>?
-what are the available <strong> flavor wines?
'''

req = raw_input("bot$ ")
req.strip()
while len(req) > 0:
    intentIdentifier(req)
    req = raw_input("bot$ ")
