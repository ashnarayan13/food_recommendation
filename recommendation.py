import json


def main():
    with open('full_data_clean.json', 'r') as f:
        currentDict = json.load(f)
    ing_list = int(input('Enter number of ingredients'))

    ingredients = currentDict['ingredient']
    temp = set()
    temp.add(1)
    temp.add(1)
    temp.add(2)
    temp.add(3)
    temp.add(3)
    print(temp)
    available_ingredients = []
    for i in range(ing_list):
        available_ingredients.append(input('Enter a ingredient'))
    print(available_ingredients)



if __name__ == '__main__':
    main()