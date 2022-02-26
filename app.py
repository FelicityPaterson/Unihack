import json 

freshFoodList = ["apple", "kiwi fruit", "mango", "plum", "bok choy", "broccoli", "carrot", "cucumber", "potato", "nut"]
freshFoodLengthDay = ["7", "7", "10", "4","3","4", "21", "7", "14","112"] 

frozenFoodList = ["fish", "leftovers", "cold meats", "Ham", " baked goods", "Lamb", "Chicken", "mushrooms", "Beef", "fruit","veggies"]
frozenFoodLengthMonth = ["3", "3", "3", "6", "6", "9", "9", "9", "12","12","12"]


with open("food.json", "r") as read_file:
    data = json.load(read_file)
food = data

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
        print("Name: {0}, Expiry: {1}, Category: {2}, Location: {3}".format(i['name'],i['expiry'],i['category'],i['location']))

def nonFreshFoodInput():
    name = input("Name of Item ")
    expiry = input("Enter expiry in format dd-mm-yyyy ")
    category = input("Category ")
    location = input("Storage location ")
    storeValues(name,expiry,category,location)



loopvar = True
while loopvar == True:
   usrInput = input("Enter command: F for Fresh food, N for Non-Fresh food, Fr for frozen, L for leftovers, Q for Exit ").upper()
   if usrInput == "F":
       print("Fresh food")
   elif usrInput == "N":
       nonFreshFoodInput()
   elif usrInput == "FR":
       print("frozen food")
   elif usrInput == "L":
       print("leftovers")
   elif usrInput == "P":
       readValues()
   elif usrInput == "Q":
       loopvar = False
read_file.close()
