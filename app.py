from cmath import rect
from datetime import datetime
import requests
from bs4 import BeautifulSoup as BSoup
import math
import json
import os
import re
from contextlib import nullcontext
from pyzbar import pyzbar
from cv2 import cv2
from twilio.rest import Client


account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

barcode_number = -1
url = "https://au.openfoodfacts.org/cgi/search.pl?search_terms="


freshFoodList = ["apple", "kiwi fruit", "mango", "plum", "bok choy", "broccoli", "carrot", "cucumber", "potato", "nut"]
freshFoodLengthDay = ["7", "7", "10", "4","3","4", "21", "7", "14","112"] 

frozenFoodList = ["fish", "leftovers", "cold meats", "Ham", " baked goods", "Lamb", "Chicken", "mushrooms", "Beef", "fruit","veggies"]
frozenFoodLengthMonth = ["3", "3", "3", "6", "6", "9", "9", "9", "12","12","12"]


with open("food.json", "r") as read_file:
    data = json.load(read_file)
food = data


def send_sms(food, storage, date):

    message = client.messages \
    .create(
         body=f'The {food} in your {storage} has a best before of {date}.' + \
               '\nCheck out the app to see what recipes you can cook with it.',
         from_='+19034803993',
         to='+61435735171'
     )

    print(message.sid)


def get_rcp_from_page(soup, links_ls):
    recipes = soup.find_all("a", {"class":"standard-card-new__article-title"})
    for recipe in recipes:
        links_ls.append(full_url(recipe.get("href")))

    return links_ls


def get_rcp_number(soup):
    recipe_counter_class = "tab-horizontal-item__label-count"
    recipe_count = soup.find("span", {"class": recipe_counter_class})
    recipe_count = recipe_count.text.replace(",","")[1:-1]
    recipe_count_int = int(recipe_count)
    return math.ceil(recipe_count_int / 24), recipe_count_int


def boil_soup(pg_number):
    url = f"https://www.bbcgoodfood.com/search/recipes/page/{pg_number}?q=food&sort=-relevance"
    bbc_goodfoods_content = requests.get(url).text
    return BSoup(bbc_goodfoods_content, "html.parser")


def full_url(link_text):
    return "https://www.bbcgoodfood.com" + link_text


def save_to_json(object_to_save, filename):
    json_data = json.dumps(object_to_save, indent=2)

    json_file = open(filename, 'w')
    json_file.write(json_data)
    json_file.close()

    return True


def get_all_rcp_urls():
    temp_recipe_ls = []
    recipe_pages = 0

    # begin scraping
    first_soup = boil_soup(1)
    recipe_pages, recipe_num = get_rcp_number(first_soup)
    if os.path.exists("recipe_urls.json"):
        with open("recipe_urls.json") as file:
            r = json.load(file)

        if len(r) + 1 >= recipe_num:
            # if recipes number in the file is less than the current,
            # then redo the entire list.
            return r

    temp_recipe_ls = get_rcp_from_page(first_soup, temp_recipe_ls)

    # read_recipe(temp_recipe_ls[0])

    for pg_num in range(2, recipe_pages+1):
        curr_page_soup = boil_soup(pg_num)
        temp_recipe_ls = get_rcp_from_page(curr_page_soup, temp_recipe_ls)
        print(round(pg_num/recipe_pages * 100, 2), "%")

    return temp_recipe_ls


def get_ingrds(rcp_soup):
    ingredient_section = rcp_soup.find("section", {"class":"recipe__ingredients"})
    ingredients = []

    main_ingrds = ingredient_section.section

    for item in main_ingrds.ul:
        ingredients.append(item.text)

    if (main_ingrds.next_sibling):
        sub_ingrds = main_ingrds.next_siblings
    else:
        return ingredients

    for section in sub_ingrds:
        for item in section.ul:
            ingredients.append(item.text)

    return ingredients


def get_instrs(rcp_soup):
    instruction_section = rcp_soup.find("section", {"class":"recipe__method-steps"})
    instructions = []

    for item in instruction_section.ul:
        if item.p:
            instructions.append(item.p.text)
        else:
            instructions.append(item.text)


    return instructions


def get_tips(rcp_soup):
    tips_section = rcp_soup.find("h6", text="RECIPE TIPS")
    tips = []
    if not tips_section:
        return tips

    if not tips_section.next_sibling:
        return tips
    for sib in tips_section.next_siblings:
        tips.append(sib.text)


def get_rcp_name(rcp_soup):
    name = rcp_soup.find("h1")
    return name.text


def get_rating(rcp_soup):
    stars = rcp_soup.find_all("i", {"class":"rating__icon"})
    star_count = 0
    for star in stars:
        if "fill" in star.svg.use.get("xlink:href"):
            star_count += 0.5
    return star_count


def parse_duration(datetime_str):
    hours = re.search("([0-9]*)H", datetime_str)
    if hours:
        hours = int(hours.group(1))
    else:
        hours = 0

    minutes = re.search("([0-9]*)M", datetime_str)
    if minutes:
        minutes = int(minutes.group(1))
    else:
        minutes = 0

    seconds = re.search("([0-9]*)S", datetime_str)
    if seconds:
        seconds = int(seconds.group(1))
    else:
        seconds = 0

    return hours, minutes, seconds


def get_cook_time(rcp_soup):
    time_section = rcp_soup.find_all("time")
    days, hours, minutes, seconds = 0, 0, 0, 0
    for time in time_section:
        time = time.get("datetime")
        h, m, s = parse_duration(time)
        hours += h
        minutes += m
        seconds += s
    
    minutes += seconds // 60
    seconds = seconds % 60
    hours += minutes // 60
    minutes = minutes % 60
    days = hours // 24
    hours = hours % 24

    time_dict = {"days": days,
                 "hours": hours,
                 "minutes": minutes,
                 "seconds": seconds
                 }

    return time_dict


def get_servings(rcp_soup):
    serving_section = rcp_soup.find("div", {"class":"post-header__servings"})
    if not serving_section:
        return -1

    serves = serving_section.find("div", {"class":"icon-with-text__children"}).text
    serves = re.search("[0-9]+", serves)
    if serves:
        serves = int(serves.group(0))
    else:
        serves = -1
    return serves


def check_pg_exists(rcp_soup):
    error = rcp_soup.find("div", {"class":"template-error__header"})
    if error:
        return 0
    else:
        return 1


def read_recipe(url):
    recipe_content = requests.get(url).text
    recipe_soup = BSoup(recipe_content, "html.parser")

    if not check_pg_exists(recipe_soup):
        return None

    ingredients = get_ingrds(recipe_soup)
    instructions = get_instrs(recipe_soup)
    tips = get_tips(recipe_soup)
    name = get_rcp_name(recipe_soup)
    rating = get_rating(recipe_soup)
    time = get_cook_time(recipe_soup)
    servings = get_servings(recipe_soup)

    recipe = {"title": name,
              "rating": rating,
              "duration": time,
              "servings": servings,
              "ingredients": ingredients,
              "instructions": instructions,
              "tips": tips
              }
    return recipe


def runRecipeScraper():
    recipe_links = get_all_rcp_urls()
    save_to_json(recipe_links, "recipe_urls.json")
    all_recipes = []

    with open("recipes.json") as file:
        all_recipes = json.load(file)

    for i in range(len(all_recipes), len(recipe_links)):
        recipe = read_recipe(recipe_links[i])
        if recipe == None:
            continue
        else:
            all_recipes.append(recipe)

        print(len(all_recipes), f"{round(i / 34.58, 2)}%")
        save_to_json(all_recipes, "recipes.json")




def stringToDate(dateString):
    date_object = datetime.datetime.strptime(dateString, '%d/%m/%Y').date()
    return date_object

def dateToString(dateObject):
    date_time = dateObject.strftime("%d/%m/%Y")
    return date_time

def storeValues(Name, Expiry, Category, Location):
    print("store: {0}, {1}, {2}, {3}".format(Name,Expiry,Category,Location))
    object = {'name': Name, 'expiry': Expiry, 'category': Category, 'location': Location }
    food.append(object)
    with open("food.json", "w") as write_file:
        json.dump(food, write_file)
    write_file.close()
    #UPDATE FOOD LIST ON SIDE
    #READVALUES
    #^ TO UPDATE FOOD[]
    # HAVE VARIABLE FOR SORT TYPE (i.e 1= ALPHABETICAL)
    # INSERT THINGS IN TREE

def readValues():
    with open("food.json", "r") as read_file:
        data = json.load(read_file)
    food = data
    print("Food")
    for i in food:
        print("Name: {0}, Expiry: {1}, Category: {2}, Location: {3}".format(i['name'],stringToDate(i['expiry']),i['category'],i['location']))

def nonFreshFoodInput():
    name = input("Name of Item ")
    expiry = input("Enter expiry in format dd/mm/yyyy ")
    category = "Non Fresh"
    location = input("Storage location (fridge, freezer or pantry")
    storeValues(name,expiry,category,location)

def leftOvers():
    name = input("Name of Item ")
    cooked = input("Enter day cooked in format dd/mm/yyyy ")
    expiry = dateToString((stringToDate(cooked) + datetime.timedelta(days=3)))
    category = "LeftOvers"
    location = "Fridge"
    storeValues(name,expiry,category,location)

def frozenFood():
    name = input("Name of Item ")
    i = 0
    timemonths = 3
    while i < len(frozenFoodList):
        if name == frozenFoodList[i]:
            timemonths = frozenFoodLengthMonth[i]
        i += 1
    expiry = dateToString((datetime.datetime.now() + datetime.timedelta(days=30*timemonths)))
    category = "Frozen"
    location = "Freezer"
    storeValues(name,expiry,category,location)

def freshFood():
    name = input("Name of Item ")
    i = 0
    timedays = 3
    while i < len(freshFoodList):
        if name == freshFoodList[i]:
            timedays = freshFoodLengthDay[i]
        i += 1
    expiry = dateToString((datetime.datetime.now() + datetime.timedelta(days=timedays)))
    category = "Fresh"
    location = "Fridge"
    storeValues(name,expiry,category,location)

def readBarcode():
    global barcode_number
    cap = cv2.VideoCapture(0)
    while barcode_number == -1:
        # read the frame from the camera
        _, frame = cap.read()
        # decode detected barcodes & get the image
        # that is drawn
        frame = decode(frame)
        # show the image in the window
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)



def draw_barcode(decoded, image):
    # n_points = len(decoded.polygon)
    # for i in range(n_points):
    #     image = cv2.line(image, decoded.polygon[i], decoded.polygon[(i+1) % n_points], color=(0, 255, 0), thickness=5)
    image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top), 
                            (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                            color=(0, 255, 0),
                            thickness=5)
    return image

def decode(image):
    global url
    global barcode_number
    # decodes all barcodes from an image
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
        # draw the barcode
        image = draw_barcode(obj, image)
        # print barcode type & data
        print("Type:", obj.type)
        print("Data:", obj.data.decode())
        barcode_number = obj.data.decode()
        tempurl = url + str(barcode_number)
        webpageContent = requests.get(tempurl).text
        title = BSoup(webpageContent, "html.parser").title.text
        if title == "Search results - Australia" or title == "Error":
            print("error")
        else:
            print(title)
    return image

send_sms('milk', 'fridge', '02/03/2022')
loopvar = True
while loopvar == True:
   runRecipeScraper()
   usrInput = input("Enter command: F for Fresh food, N for Non-Fresh food, Fr for frozen, L for leftovers, Q for Exit ").upper()
   if usrInput == "F":
       print("Fresh food")
   elif usrInput == "N":
       nonFreshFoodInput()
   elif usrInput == "FR":
       frozenFood()
   elif usrInput == "L":
       leftOvers()
   elif usrInput == "P":
       readValues()
   elif usrInput == "Q":
       loopvar = False
   elif usrInput == "B":
       barcode_number = -1
       readBarcode()
read_file.close()
