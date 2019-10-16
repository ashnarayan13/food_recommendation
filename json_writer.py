import json
import pandas

#df = pandas.read_json('rewrite.json')

#print(df.dtypes)
#print(df.head())

with open('rewrite.json', 'r') as f:
    currentDict = json.load(f)
#print(currentDict)

data = currentDict['ingredient']
diff = currentDict['difficulty']
serves = currentDict['serves']
print(data)