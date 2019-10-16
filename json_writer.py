import json
import pandas

#df = pandas.read_json('rewrite.json')

#print(df.dtypes)
#print(df.head())

def cleanInput(currentDict):
    #print(currentDict)
    new_dict = dict()
    new_dict['name'] = currentDict['name']
    new_dict['date'] = currentDict['date']
    new_dict['time'] = currentDict['time']
    new_dict['category'] = currentDict['category']
    ing = currentDict['ingredient']
    diff = currentDict['difficulty']
    serves = currentDict['serves']
    qty = currentDict['quantity']
    for v in new_dict['name']:
        index = 0
        for i in range(len(ing)):
            if v in ing[i][0]:
                index = i
                break
        ing[index].pop(0)
        qty[index].pop(0)
        if len(ing[index])==0:
            ing[index].append('unknown')
            qty[index].append('0')
        new_dict.setdefault('ingredient', []).append(ing[index])
        new_dict.setdefault('quantity', []).append(qty[index])
        new_dict.setdefault('serves', []).append(serves[index])
        new_dict.setdefault('difficulty', []).append(diff[index])
    return new_dict

def fixEmpty(input):
    repeat = dict()
    name = input['name']
    time = input['time']
    date = input['date']
    cat = input['category']
    ing = input['ingredient']
    qty = input['quantity']
    serves = input['serves']
    diff = input['difficulty']
    print(len(name))
    count = 0
    for i in range(len(ing)):
        if ing[i][0] == 'unknown':
            count += 1
    print(count)

def main():
    with open('rewrite.json', 'r') as f:
        currentDict = json.load(f)
    new_dict = cleanInput(currentDict)
    with open('data.json', 'w') as fp:
        json.dump(new_dict, fp, indent=4)

    final = fixEmpty(new_dict)

if __name__ == '__main__':
    main()