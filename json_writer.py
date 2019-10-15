import json

data = {'people':[{'name': 'Scott', 'website': 'stackabuse.com', 'from': 'Nebraska'}]}

temp = {'x': 'y'}
#print(data['people'].append(temp))

flattened_list = []
print(data.values())
for x in data.values():
    for y in x:
        flattened_list.append(y)

flattened_list_ = []
for x in flattened_list:
    for y in x:
        flattened_list_.append(y)
print(flattened_list_)
exit(1)
data['website'] = ['a', 'b', 'c']
print(json.dumps(data, indent=4))