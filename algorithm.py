import json
import re
from datetime import *


def stringToDate(dateString):
    date_object = datetime.strptime(dateString, '%d/%m/%Y').date()
    return date_object


def get_days_to_expiry(date):
    date = stringToDate(date)
    return (date - date.today()).days

def get_expiring_foods():
    with open('food.json', 'r') as f:
        foods = json.load(f)

    expiring_foods = []
    expiring_days = []
    for food in foods:
        expiring_foods.append(food['name'])
        days = get_days_to_expiry(food['expiry'])
        expiring_days.append(days)

    expire_info = []
    for i in range(0, len(expiring_foods)):
        if expiring_days[i] > 3:
            # IF INGREDIENT NOT EXPIREING IN 3 days DONT CHECK
            continue
        
        re_food = re.compile(expiring_foods[i].lower())
        expire_info.append((re_food, expiring_days[i]))

    return expire_info


def sort_best(rcps):
    rcps.sort(key=lambda x: x[0])


def get_best_recipes(expire_info):
    best_recipes = [(0, None), (0, None), (0, None), (0, None), (0, None), 
                    (0, None), (0, None), (0, None), (0, None), (0, None)]
    with open('recipes.json', 'r') as f:
        recipes = json.load(f)

    for i in range(0,100):
        score = 0
        for item in expire_info:
            food = item[0]
            days = item[1]
            if re.search(food, "|".join(recipes[i]['ingredients'])):
                score += 2 ** (4 - days)
        if score > best_recipes[0][0]:
            best_recipes[0] = (score, recipes[i])
        sort_best(best_recipes)

    best_recipes.reverse()
    return [x[1] for x in best_recipes]

get_best_recipes(get_expiring_foods())
