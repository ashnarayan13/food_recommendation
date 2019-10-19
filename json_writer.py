import json
import pandas
import re
import fractions


# df = pandas.read_json('rewrite.json')

# print(df.dtypes)
# print(df.head())

def cleanInput(currentDict):
    # print(currentDict)
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
        if len(ing[index]) == 0:
            ing[index].append('unknown')
            qty[index].append('0')
        new_dict.setdefault('ingredient', []).append(ing[index])
        new_dict.setdefault('quantity', []).append(qty[index])
        new_dict.setdefault('serves', []).append(serves[index])
        new_dict.setdefault('difficulty', []).append(diff[index])
    qty_list = new_dict['quantity']
    ing_list = new_dict['ingredient']
    for rec in qty_list:
        if type(rec[0]) is list:
            # stitch the
            for i in range(len(rec)):
                rec[i] = ''.join(rec[i]).lower()
                rec[i] = re.sub(r"[^a-zA-Z0-9-\--\\]", " ", rec[i])
    for ing in ing_list:
        for i in range(len(ing)):
            ing[i] = ing[i].strip('\n').lower()
    return new_dict


def fixEmpty(input):
    words = ['from', 'optional', 'sized', 'medium', '\\', 'to taste']
    #normalize = ['cup', 'cups', 'scoop', 'scoops']
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
    # remove unnecessary words
    for i in range(len(qty)):
        for val in range(len(qty[i])):
            for j in words:
                if j in qty[i][val]:
                    if j == 'to taste':
                        qty[i][val] = qty[i][val].replace(j, '1 tsp')
                    else:
                        qty[i][val] = qty[i][val].replace(j, '')
    # get fractions
    for i in range(len(qty)):
        for val in range(len(qty[i])):
            if 'stick' in qty[i][val]:
                qty[i][val] = qty[i][val][0]
                #print(float(qty[i][val].split('/')[0])/float(qty[i][val].split('/')[1]))
    repeat['name'] = name
    repeat['time'] = time
    repeat['date'] = date
    repeat['ingredient'] = ing
    repeat['serves'] = serves
    repeat['category'] = cat
    repeat['difficulty'] = diff
    repeat['quantity'] = qty
    return repeat


def main():
    with open('rewrite.json', 'r') as f:
        currentDict = json.load(f)
    new_dict = cleanInput(currentDict)
    with open('data.json', 'w') as fp:
        json.dump(new_dict, fp, indent=4)

    final = fixEmpty(new_dict)
    with open('clean.json', 'w') as fp:
        json.dump(final, fp, indent=4)



if __name__ == '__main__':
    main()
