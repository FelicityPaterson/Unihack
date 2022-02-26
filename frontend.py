from ctypes import alignment
import tkinter as tk # import tkinter library
from tkinter import ttk
from tkcalendar import Calendar
from PIL import ImageTk, Image


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
    freshFoodList = ["Apple", "Kiwi fruit", "Mango", "Plum", "Bok choy", "Broccoli", "Carrot", "Cucumber", "Potato", "Nut"]
    
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

    # done/insert button to finalise selection
    FSdonebtn = tk.Button(window1, text = "Insert", command = foodInventoryInsert) #####
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

def chooseNonFresh():
    # TO BE CHANGED. Function run when Packaged option of radiobuttons selected. Creates relevant widgets; prompt for 
    # user to scan QR code, location food is stored, and expiry date (?)

    nonFreshFoodLocList = ["Fridge", "Pantry", "Freezer"]

    #-------------USER INPUT WIDGETS---------------
    # name
    NFlb1 = tk.Label(window1, text = "Enter or scan for name:", font = ("Proxima Nova", 12)) # prompt
    NFlb1.place(x = 60, y = 260)

    NFname = tk.Entry(window1, bd = 3, width = 15) # entry box
    NFname.place(x = 240, y = 260)

    NFscanbtn = tk.Button(window1, text = "Scan", font = ("Proxima Nova", 12), command = scanCode) # scan button. link to scanning function with command = ...
    NFscanbtn.place(x = 400, y = 265) 

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

    frozenFoodList = ["Fish", "Leftovers", "Cold meats", "Ham", "Baked goods", "Lamb", "Chicken", "Mushrooms", "Beef", "Fruit", "Veggies"]

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
