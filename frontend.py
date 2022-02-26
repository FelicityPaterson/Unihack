from ctypes import alignment
import tkinter as tk # import tkinter library
from tkinter import ttk
from tkcalendar import Calendar

def main():
    # create a window to ADD INGREDIENTS and view FOOD AT HOME
    global window1
    window1 = tk.Tk()
    window1.title("Best Before") # name title of window
    window1.geometry("1500x1500") # window size

    # insert app logo
    lb1 = tk.Label(window1, text = "BEST BEFORE", font = ("Proxima Nova Bold", 25), fg = "orange") # label
    lb1.place(x = 620, y = 20) # position label


    #----------------------------------------ADD INGREDIENTS-------------------------------------------------------
    # 'add ingredient' title
    lb1 = tk.Label(window1, text = "Add food", font = ("Arial Bold", 16), fg = "white", bg = "green") # label
    lb1.place(x = 200, y = 70) # position label
    
    # select ingredient type prompt
    lb1 = tk.Label(window1, text = "Select food type: ", font = ("Proxima Nova", 12, "bold italic"), fg = "black") # label
    lb1.place(x = 60, y = 115) # position label


    # set up widgets for adding ingredient
    # variable to store value of radiobutton selection (e.g. v1.get() == "Fresh")
    global v1
    v1 = tk.StringVar() 
    
    # create produce selection radio buttons
    rbtn1 = tk.Radiobutton(window1, text = "Fresh", font = ("Proxima Nova", 12), var = v1, value = "Fresh", command = chooseFresh)
    rbtn1.place(x = 240, y = 115)

    rbtn2 = tk.Radiobutton(window1, text = "Non-fresh", font = ("Proxima Nova", 12), var = v1, value = "Non-fresh", command = chooseNonFresh) ###
    rbtn2.place(x = 320, y = 115)

    rbtn3 = tk.Radiobutton(window1, text = "Leftovers", font = ("Proxima Nova", 12), var = v1, value = "Leftovers", command = chooseLeftover) ###
    rbtn3.place(x = 420, y = 115)

    rbtn4 = tk.Radiobutton(window1, text = "Frozen", font = ("Proxima Nova", 12), var = v1, value = "Frozen", command = chooseFrozen) ###
    rbtn4.place(x = 510, y = 115)


    #----------------------------------------TREE INVENTORY-------------------------------------------------------
    # 'View existing food' prompt
    lb1 = tk.Label(window1, text = "Food at home", font = ("Arial Bold", 16), fg = "white", bg = "green") # label
    lb1.place(x = 800, y = 70) # position label


    # define tree inventory
    # defining tree view 
    global tree
    tree = ttk.Treeview(window1, columns = ("Food", "Best before", "Days remaining"), show = "headings", height = 20)
    tree.heading("Food", text = "Food", command = sortBy) # set heading names
    tree.heading("Best before", text = "Best before")
    tree.heading("Days remaining", text = "Days remaining")
    tree.place(x = 750, y = 115) # place tree

    #----------------------------------------RECIPE PAGE-------------------------------------------------------


    #------
    # run the window
    window1.mainloop() 

    return


##-------------------------WHEN FOOD TYPE IS SELECTED (e.g. Fresh, Non-fresh)---------------------------------------

def chooseFresh(): 
    # Function run when Fresh option of radiobuttons selected. Creates relevant widgets for user input; choose fresh
    # food type and date food is bought. 
    print("FRESH") ##### TEST

    # create fresh food list
    freshFoodList = ["Apple", "Kiwi fruit", "Mango", "Plum", "Bok choy", "Broccoli", "Carrot", "Cucumber", "Potato", "Nut"]
    
    #-------------USER INPUT WIDGETS---------------
    # drop-down menu to select fresh food type
    FSlb1 = tk.Label(window1, text = "Select Fresh food:", font = ("Proxima Nova", 12)) # instructions
    FSlb1.place(x = 60, y = 160)

    global FSfood
    FSfood = ttk.Combobox(window1, values = freshFoodList, state = "readonly") # create widget
    FSfood.place(x = 240, y = 160)
    
    # calendar to select date bought
    FSlb2 = tk.Label(window1, text = "Enter date bought: ", font = ("Proxima Nova", 12)) # prompt
    FSlb2.place(x = 60, y = 215)

    FSdatebought = Calendar(window1)
    FSdatebought.place(x = 240, y = 215)

    # done/insert button to finalise selection
    FSdonebtn = tk.Button(window1, text = "Insert", command = foodInventoryInsert) #####
    FSdonebtn.place(x = 330, y = 410)

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
    # TO BE CHANGED. Function run when Non-Fresh option of radiobuttons selected. Creates relevant widgets; prompt for 
    # user to scan QR code, location food is stored, and expiry date (?)

    print("NONFRESH") # TEST
    nonFreshFoodList = ["A", "B", "C"] #########
    nonFreshFoodLocList = ["Fridge", "Pantry", "Freezer"]

    #-------------USER INPUT WIDGETS---------------
    # category
    NFlb1 = tk.Label(window1, text = "Select non-fresh category:", font = ("Proxima Nova", 12)) # prompt
    NFlb1.place(x = 60, y = 160)

    NFfood = ttk.Combobox(window1, values = nonFreshFoodList, state = "readonly") # menu widget
    NFfood.place(x = 240, y = 160)

    # name
    NFlb2 = tk.Label(window1, text = "Enter non-fresh food name:\n(leave blank if not applicable)", font = ("Proxima Nova", 12), justify = "left") # prompt
    NFlb2.place(x = 60, y = 215)

    NFname = tk.Entry(window1, bd = 3) # entry box
    NFname.place(x = 240, y = 215)

    # location #######
    NFlb3 = tk.Label(window1, text = "Select location stored: ", font = ("Proxima Nova", 12)) # prompt
    NFlb3.place(x = 60, y = 285)

    NFloc = ttk.Combobox(window1, values = nonFreshFoodLocList, state = "readonly") # menu widget
    NFloc.place(x = 240, y = 285)

    # expiry date
    NFlb4 = tk.Label(window1, text = "Enter expiry date:", font = ("Proxima Nova", 12)) # prompt
    NFlb4.place(x = 60, y = 350)

    NFexpirydate = Calendar(window1)
    NFexpirydate.place(x = 240, y = 350)

    # done button
    NFdonebtn = tk.Button(window1, text = "Insert", command = foodInventoryInsert) #####
    NFdonebtn.place(x = 330, y = 550)

    #-------------HIDE WIDGETS FROM OTHER FOOD TYPES---------------
    # list of non-fresh widgets
    global NFwidgets
    NFwidgets = [NFname, NFfood, NFloc, NFexpirydate, NFlb1, NFlb2, NFlb3, NFlb4, NFdonebtn]

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

    print("LEFTOVER") # TEST

    #-------------USER INPUT WIDGETS---------------
    # entry box to input name for leftovers
    LOlb1 = tk.Label(window1, text = "Enter leftover name:", font = ("Proxima Nova", 12)) # instructions
    LOlb1.place(x = 60, y = 160)

    LOname = tk.Entry(window1, bd = 3) # entry box
    LOname.place(x = 240, y = 155)

    # calendar to input date cooked
    LOlb2 = tk.Label(window1, text = "Select date cooked: ", font = ("Proxima Nova", 12)) # instructions
    LOlb2.place(x = 60, y = 215)

    LOdatecooked = Calendar(window1) # calendar
    LOdatecooked.place(x = 240, y = 215)

    # done button
    LOdonebtn = tk.Button(window1, text = "Insert", command = foodInventoryInsert) #####
    LOdonebtn.place(x = 330, y = 410)

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

    print("FROZEN") # TEST
    frozenFoodList = ["Fish", "Leftovers", "Cold meats", "Ham", "Baked goods", "Lamb", "Chicken", "Mushrooms", "Beef", "Fruit", "Veggies"]

    #-------------USER INPUT WIDGETS---------------
    # drop-down menu to select frozen food type
    FZlb1 = tk.Label(window1, text = "Select frozen food type:", font = ("Proxima Nova", 12)) # prompt
    FZlb1.place(x = 60, y = 160)

    FZfood = ttk.Combobox(window1, values = frozenFoodList, state = "readonly") # menu widget
    FZfood.place(x = 240, y = 160)

    # calendar to input date frozen
    FZlb2 = tk.Label(window1, text = "Enter date frozen: ", font = ("Proxima Nova", 12)) # prompt
    FZlb2.place(x = 60, y = 215)

    FZdatefrozen = Calendar(window1)
    FZdatefrozen.place(x = 240, y = 215)

    # done button
    FZdonebtn = tk.Button(window1, text = "Insert", command = foodInventoryInsert) #####
    FZdonebtn.place(x = 330, y = 410)

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



##-------------------------WHEN FOOD TYPE IS SELECTED (e.g. Fresh, Non-fresh)---------------------------------------
def foodInventoryInsert(): #########
    # Function that inserts entries into the food inventory. Called when insert button is clicked. Displays food,
    # best before date, how many dates until it expires
    
    # inventoryList = []
    # inventoryList.append() #######

    if v1.get() == "Fresh":
        tree.insert("", index = "end", values = (FSwidgets[0].get(), "", "")) ######
    elif v1.get() == "Non-fresh":
        tree.insert("", index = "end", values = (NFwidgets[0].get(), "", "")) ######### SCANNER INSTEAD
    elif v1.get() == "Leftovers":
        tree.insert("", index = "end", values = (LOwidgets[0].get(), "", "")) ######
    elif v1.get() == "Frozen":
        tree.insert("", index = "end", values = (FZwidgets[0].get(), "", "")) ######

    # Insert delete button to delete inventory insert
    deleteBtn = tk.Button(window1, text = "Delete", command = delInventoryEntry)
    deleteBtn.place(x = 1310, y = 500)

    # Insert find-a-recipe button now that at least one ingredient is added
    findARecipeBtn = tk.Button(window1, text = "Find a recipe!", command = recipepage)
    findARecipeBtn.place(x = 1000, y = 550)
    
    # for child in tree.get_children(): #######
    #     print(tree.item(child)["Values"])
    return

def sortBy():
    pass


def delInventoryEntry():
    tree.delete(tree.selection())
    return

def recipepage():
    window2 = tk.Tk()
    window2.title("Recipe Results")
    window2.geometry("1500x1500")
    window2.mainloop()

main()
