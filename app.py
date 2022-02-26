import json 
import datetime


freshFoodList = ["apple", "kiwi fruit", "mango", "plum", "bok choy", "broccoli", "carrot", "cucumber", "potato", "nut"]
freshFoodLengthDay = ["7", "7", "10", "4","3","4", "21", "7", "14","112"] 

frozenFoodList = ["fish", "leftovers", "cold meats", "Ham", " baked goods", "Lamb", "Chicken", "mushrooms", "Beef", "fruit","veggies"]
frozenFoodLengthMonth = ["3", "3", "3", "6", "6", "9", "9", "9", "12","12","12"]


with open("food.json", "r") as read_file:
    data = json.load(read_file)
food = data

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


loopvar = True
while loopvar == True:
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
read_file.close()
