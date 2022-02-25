def storeValues(Name, Expiry, Category, Location):
    print("store: {0}, {1}, {2}, {3}".format(Name,Expiry,Category,Location))


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
   elif usrInput == "Q":
       loopvar = False