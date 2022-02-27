# from ctypes import alignment
import tkinter as tk # import tkinter library
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from PIL import ImageTk, Image
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

account_sid = "ACff8ab1fefd1fb3ce487325457522a330"
auth_token = "173d51f33714563d28a12e1554308331"
client = Client(account_sid, auth_token)

barcode_number = -1
url = "https://au.openfoodfacts.org/cgi/search.pl?search_terms="
foodName = "Error"

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
         to='+61435072202'
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

    # for link in recipe_links:
    #     recipe = read_recipe(link)
    #     if recipe == None:
    #         continue
    #     else:
    #         all_recipes.append(recipe)

        print(len(all_recipes), f"{round(i / 34.58, 2)}%")
        save_to_json(all_recipes, "recipes.json")




def stringToDate(dateString):
    date_object = datetime.strptime(dateString, '%d/%m/%Y').date()
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

def readValues():
    with open("food.json", "r") as read_file:
        data = json.load(read_file)
    food = data
    print("Food")
    for i in food:
        print("Name: {0}, Expiry: {1}, Category: {2}, Location: {3}".format(i['name'],stringToDate(i['expiry']),i['category'],i['location']))

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
    global foodName

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
        foodName = BSoup(webpageContent, "html.parser").title.text
        print(foodName)
        if foodName == "Search results - Australia" or foodName == "Error":
           foodName = "Error"
        
        NFname.insert(-1, foodName)

    return image

def main():
    # Main function to start app

    # create a window to ADD INGREDIENTS and view FOOD AT HOME
    global window1
    window1 = tk.Tk()
    window1.title("Best Before") # name title of window
    window1.geometry("1500x1500") # window size
    # insert app logo
    logo = Image.open("logo.png")
    logo = logo.resize((150, 100))
    logo = ImageTk.PhotoImage(image = logo)
    lb1 = tk.Label(window1, image = logo) # label
    lb1.place(x = 620, y = 20) # position label


    #----------------------------------------ADD INGREDIENTS-------------------------------------------------------
    # 'add ingredient' title
    lb1 = tk.Label(window1, text = "Add food", font = ("Arial Bold", 16), fg = "white", bg = "#ABBD5C") # label
    lb1.place(x = 200, y = 170) # position label
    
    # select ingredient type prompt
    lb1 = tk.Label(window1, text = "Select food type: ", font = ("Proxima Nova", 12, "bold italic"), fg = "black") # label
    lb1.place(x = 60, y = 215) # position label


    # set up widgets for adding ingredient
    # variable to store value of radiobutton selection (e.g. v1.get() == "Fresh")
    global v1
    v1 = tk.StringVar() 
    
    # create produce selection radio buttons
    rbtn1 = tk.Radiobutton(window1, text = "Fresh", font = ("Proxima Nova", 12), var = v1, value = "Fresh", command = chooseFresh)
    rbtn1.place(x = 240, y = 215)

    rbtn2 = tk.Radiobutton(window1, text = "Packaged", font = ("Proxima Nova", 12), var = v1, value = "Packaged", command = chooseNonFresh) ###
    rbtn2.place(x = 320, y = 215)

    rbtn3 = tk.Radiobutton(window1, text = "Leftovers", font = ("Proxima Nova", 12), var = v1, value = "Leftovers", command = chooseLeftover) ###
    rbtn3.place(x = 420, y = 215)

    rbtn4 = tk.Radiobutton(window1, text = "Frozen", font = ("Proxima Nova", 12), var = v1, value = "Frozen", command = chooseFrozen) ###
    rbtn4.place(x = 510, y = 215)


    #----------------------------------------TREE INVENTORY-------------------------------------------------------
    # 'View existing food' prompt
    lb1 = tk.Label(window1, text = "Food at home", font = ("Arial Bold", 16), fg = "white", bg = "#ABBD5C") # label
    lb1.place(x = 800, y = 170) # position label


    # define tree inventory
    # defining tree view 
    global tree
    tree = ttk.Treeview(window1, columns = ("Food", "Best before", "Days remaining"), show = "headings", height = 20)
    tree.heading("Food", text = "Food", command = sortBy) # set heading names
    tree.heading("Best before", text = "Best before")
    tree.heading("Days remaining", text = "Days remaining")
    tree.place(x = 750, y = 215) # place tree
    # send_sms('milk', 'fridge', '02/03/2022')
    #----------------------------------------RECIPE PAGE-------------------------------------------------------


    #------
    # run the window
    window1.mainloop() 
    

    return


##-------------------------WHEN FOOD TYPE IS SELECTED (e.g. Fresh, Non-fresh)---------------------------------------

def chooseFresh(): 
    # Function run when Fresh option of radiobuttons selected. Creates relevant widgets for user input; choose fresh
    # food type and date food is bought. 

    # create fresh food list
    global freshFoodList
    global FSdatebought
    #-------------USER INPUT WIDGETS---------------
    # drop-down menu to select fresh food type
    FSlb1 = tk.Label(window1, text = "Select Fresh food:", font = ("Proxima Nova", 12)) # instructions
    FSlb1.place(x = 60, y = 260)

    global FSfood
    FSfood = ttk.Combobox(window1, values = freshFoodList, state = "readonly") # create widget
    FSfood.place(x = 240, y = 260)
    
    
    # calendar to select date bought
    FSlb2 = tk.Label(window1, text = "Enter date bought: ", font = ("Proxima Nova", 12)) # prompt
    FSlb2.place(x = 60, y = 315)

    FSdatebought = Calendar(window1)
    
    FSdatebought.place(x = 240, y = 315)
   
    print("-------------------------------------")
    print(FSdatebought.get_date())
    print("-------------------------------------")
    # done/insert button to finalise selection
    FSdonebtn = tk.Button(window1, text = "Insert", command = freshFoodData(FSfood.get(), FSdatebought.get_date())) #####
    FSdonebtn.place(x = 330, y = 510)

    #-------------HIDE WIDGETS FROM OTHER FOOD TYPES---------------

    # create a list of the Fresh food widgets
    global FSwidgets
    FSwidgets = [FSfood, FSdatebought, FSlb1, FSlb2, FSdonebtn]

    # hide widgets from other food types
    try:
        hideWidget(LOwidgets)
    except:
        pass
    try:
        hideWidget(NFwidgets) # hide widgets from other food types
    except:
        pass
    try:
        hideWidget(FZwidgets)
    except:
        pass

    return

def freshFoodData(name, date):
    print("-------------------------------------")
    print(date)
    print("-------------------------------------")
    i = 0
    timedays = 3
    while i < len(freshFoodList):
        if name == freshFoodList[i]:
            timedays = freshFoodLengthDay[i]
        i += 1
    dateVar = stringToDate(date)
    expiry = dateToString((dateVar + datetime.timedelta(days=timedays)))
    storeValues(name,expiry,'Fresh','Fridge')

def chooseNonFresh():
    # TO BE CHANGED. Function run when Packaged option of radiobuttons selected. Creates relevant widgets; prompt for 
    # user to scan QR code, location food is stored, and expiry date (?)

    nonFreshFoodLocList = ["Fridge", "Pantry", "Freezer"]

    #-------------USER INPUT WIDGETS---------------
    # name
    NFlb1 = tk.Label(window1, text = "Enter or scan for name:", font = ("Proxima Nova", 12)) # prompt
    NFlb1.place(x = 60, y = 260)

    NFscanbtn = tk.Button(window1, text = "Scan", font = ("Proxima Nova", 12), command = readBarcode) # scan button. link to scanning function with command = ...
    NFscanbtn.place(x = 400, y = 265) 

    global NFname
    NFname = tk.Entry(window1, bd = 3, width = 15) # entry box
    NFname.place(x = 240, y = 260)
    
    # location #######
    NFlb2 = tk.Label(window1, text = "Select location stored: ", font = ("Proxima Nova", 12)) # prompt
    NFlb2.place(x = 60, y = 315)

    NFloc = ttk.Combobox(window1, values = nonFreshFoodLocList, state = "readonly") # menu widget
    NFloc.place(x = 240, y = 315)

    # expiry date
    NFlb3 = tk.Label(window1, text = "Enter expiry date:", font = ("Proxima Nova", 12)) # prompt
    NFlb3.place(x = 60, y = 385)

    NFexpirydate = Calendar(window1)
    NFexpirydate.place(x = 240, y = 385)

    # done button
    NFdonebtn = tk.Button(window1, text = "Insert", command = foodInventoryInsert) 
    NFdonebtn.place(x = 330, y = 580)

    #-------------HIDE WIDGETS FROM OTHER FOOD TYPES---------------
    # list of non-fresh widgets
    global NFwidgets
    NFwidgets = [NFname, NFloc, NFexpirydate, NFscanbtn, NFlb1, NFlb2, NFlb3, NFdonebtn] ##### 

    # hide widgets from other food types
    try:
        hideWidget(LOwidgets)
    except:
        pass
    try:
        hideWidget(FSwidgets) # hide widgets from other food types
    except:
        pass
    try:
        hideWidget(FZwidgets)
    except:
        pass

    return

def chooseLeftover():
    # Function run when Leftover option of radiobuttons selected. Creates relevant widgets; name to give leftovers
    # and date leftovers were made.

    #-------------USER INPUT WIDGETS---------------
    # entry box to input name for leftovers
    LOlb1 = tk.Label(window1, text = "Enter leftover name:", font = ("Proxima Nova", 12)) # instructions
    LOlb1.place(x = 60, y = 260)

    LOname = tk.Entry(window1, bd = 3) # entry box
    LOname.place(x = 240, y = 255)

    # calendar to input date cooked
    LOlb2 = tk.Label(window1, text = "Select date cooked: ", font = ("Proxima Nova", 12)) # instructions
    LOlb2.place(x = 60, y = 315)

    LOdatecooked = Calendar(window1) # calendar
    LOdatecooked.place(x = 240, y = 315)

    # done button
    LOdonebtn = tk.Button(window1, text = "Insert", command = foodInventoryInsert) #####
    LOdonebtn.place(x = 330, y = 510)

    #-------------HIDE WIDGETS FROM OTHER FOOD TYPES---------------
    # list of widgets
    global LOwidgets
    LOwidgets = [LOname, LOdatecooked, LOlb1, LOlb2, LOdonebtn]

    # hide widgets from other food types
    try:
        hideWidget(NFwidgets)
    except:
        pass
    try:
        hideWidget(FSwidgets) # hide widgets from other food types
    except:
        pass
    try:
        hideWidget(FZwidgets)
    except:
        pass

    return

def chooseFrozen():
    # Function run when Frozen option of radiobuttons selected. Creates relevant widgets; type of frozen food and
    # date food was first frozen.

    global frozenFoodList
    
    #-------------USER INPUT WIDGETS---------------
    # drop-down menu to select frozen food type
    FZlb1 = tk.Label(window1, text = "Select frozen food type:", font = ("Proxima Nova", 12)) # prompt
    FZlb1.place(x = 60, y = 260)

    FZfood = ttk.Combobox(window1, values = frozenFoodList, state = "readonly") # menu widget
    FZfood.place(x = 240, y = 260)

    # calendar to input date frozen
    FZlb2 = tk.Label(window1, text = "Enter date frozen: ", font = ("Proxima Nova", 12)) # prompt
    FZlb2.place(x = 60, y = 315)

    FZdatefrozen = Calendar(window1)
    FZdatefrozen.place(x = 240, y = 315)

    # done button
    FZdonebtn = tk.Button(window1, text = "Insert", command = foodInventoryInsert) #####
    FZdonebtn.place(x = 330, y = 510)

    #-------------HIDE WIDGETS FROM OTHER FOOD TYPES---------------
    # list of Frozen widgets
    global FZwidgets
    FZwidgets = [FZfood, FZdatefrozen, FZlb1, FZlb2, FZdonebtn]

    # hide widgets from other food types
    try:
        hideWidget(LOwidgets)
    except:
        pass
    try:
        hideWidget(FSwidgets) # hide widgets from other food types
    except:
        pass
    try:
        hideWidget(NFwidgets)
    except:
        pass

    return


def hideWidget(widgetList):
    # Function called to hide widgets from other food types. Accepts a list of tk widgets.
    for widget in widgetList:
        widget.place_forget()

    return

def scanCode(): #####
    # Function to scan code for Packaged food
    print('SCANNED!')

##-------------------------AFTER FOOD TYPE IS SELECTED (e.g. Fresh, Non-fresh)---------------------------------------
def foodInventoryInsert(): #########
    # Function that inserts entries into the food inventory. Called when insert button is clicked. Displays food,
    # best before date, how many dates until it expires
    
    # inventoryList = []
    # inventoryList.append()
    print(FSdatebought.get_date())

    if v1.get() == "Fresh":
        tree.insert("", index = "end", values = (FSwidgets[0].get(), "", "")) ######
    elif v1.get() == "Packaged":
        tree.insert("", index = "end", values = (NFwidgets[0].get(), "", "")) ######### CHANGE TO ACCOMODATE SCANNER TOO
    elif v1.get() == "Leftovers":
        tree.insert("", index = "end", values = (LOwidgets[0].get(), "", "")) ######
    elif v1.get() == "Frozen":
        tree.insert("", index = "end", values = (FZwidgets[0].get(), "", "")) ######

    # Insert delete button to delete inventory insert
    deleteBtn = tk.Button(window1, text = "Delete", command = delInventoryEntry)
    deleteBtn.place(x = 1310, y = 600)

    # Insert find-a-recipe button now that at least one ingredient is added
    findARecipeBtn = tk.Button(window1, text = "Find a recipe!", command = recipepage)
    findARecipeBtn.place(x = 1000, y = 650)
    
    # for child in tree.get_children(): ####### potential way of iterating through items in tree?
    #     print(tree.item(child)["Values"])
    return

def sortBy(): ######
    # Function to sort entries in tree by food name/best before date/days remaining 
    pass

def delInventoryEntry():
    # Function to delete entries in tree with 'Delete' button
    tree.delete(tree.selection())
    return

##-------------------------------------------------RECIPE PAGE------------------------------------------------------

def recipepage(): #####
    # Called when findARecipeBtn is clicked, creates new window for recipe page
    window2 = tk.Toplevel()
    window2.title("Recipe Results")
    window2.geometry("1500x1500")

    # insert app logo
    logo = Image.open("logo.png")
    logo = logo.resize((150, 100))
    logo = ImageTk.PhotoImage(image = logo)
    RPlb1 = tk.Label(window2, image = logo) # label
    RPlb1.place(x = 620, y = 20) # position label

    # ....
    window2.mainloop()


main()
