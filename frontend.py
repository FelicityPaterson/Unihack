from ctypes import alignment
import tkinter as tk # import tkinter library
from tkinter import ttk
from tkcalendar import Calendar

def main():
    # create a window for ingredient add
    global window1
    window1 = tk.Tk()
    window1.title("Best Before") # name title of window
    window1.geometry("800x1500") # window size

    # title
    lb1 = tk.Label(window1, text = "BEST BEFORE", font = ("Proxima Nova Bold", 25), fg = "orange") # label
    lb1.place(x = 290, y = 10) # position label

    # 'add ingredient' title
    lb1 = tk.Label(window1, text = "Add food", font = ("Arial Bold", 16), fg = "white", bg = "green") # label
    lb1.place(x = 200, y = 70) # position label

    typeChoose()


    window1.mainloop() # run the window

    return

    

def typeChoose():
    v1 = tk.StringVar() # variable linking radiobuttons
    
    # select ingredient type prompt
    lb1 = tk.Label(window1, text = "Select food type: ", font = ("Proxima Nova", 12, "bold italic"), fg = "black") # label
    lb1.place(x = 60, y = 115) # position label

    # create produce selection radio buttons
    rbtn1 = tk.Radiobutton(window1, text = "Fresh", font = ("Proxima Nova", 12), var = v1, value = "Fresh", command = chooseFresh)
    rbtn1.place(x = 240, y = 115)

    rbtn2 = tk.Radiobutton(window1, text = "Non-fresh", font = ("Proxima Nova", 12), var = v1, value = "Non-fresh", command = chooseNonFresh) ###
    rbtn2.place(x = 320, y = 115)

    rbtn3 = tk.Radiobutton(window1, text = "Leftover", font = ("Proxima Nova", 12), var = v1, value = "Leftover", command = chooseLeftover) ###
    rbtn3.place(x = 420, y = 115)

    rbtn4 = tk.Radiobutton(window1, text = "Frozen", font = ("Proxima Nova", 12), var = v1, value = "Frozen", command = chooseFrozen) ###
    rbtn4.place(x = 510, y = 115)

    return


def chooseFresh():
    print("FRESH") # TEST
    freshFoodList = ["Apple", "Kiwi fruit", "Mango", "Plum", "Bok choy", "Broccoli", "Carrot", "Cucumber", "Potato", "Nut"]
    
    # done button
    FSdonebtn = tk.Button(window1, text = "Done") #####
    FSdonebtn.place(x = 330, y = 410)


    # drop-down menu
    FSlb1 = tk.Label(window1, text = "Select Fresh food:", font = ("Proxima Nova", 12)) # prompt
    FSlb1.place(x = 60, y = 160)

    FSfood = ttk.Combobox(window1, values = freshFoodList, state = "readonly") # menu widget
    FSfood.place(x = 240, y = 160)


    # date bought
    FSlb2 = tk.Label(window1, text = "Enter date bought: ", font = ("Proxima Nova", 12)) # prompt
    FSlb2.place(x = 60, y = 215)

    FSdatebought = Calendar(window1)
    FSdatebought.place(x = 240, y = 215)

    # list of Fresh widgets
    global FSwidgets
    FSwidgets = [FSlb1, FSfood, FSdatebought, FSlb2, FSdonebtn]

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
    print("NONFRESH") # TEST
    nonFreshFoodList = ["A", "B", "C"] #########
    nonFreshFoodLocList = ["Fridge", "Pantry", "Freezer"]

    # done button
    NFdonebtn = tk.Button(window1, text = "Done") #####
    NFdonebtn.place(x = 330, y = 550)

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

    # list of non-fresh widgets
    global NFwidgets
    NFwidgets = [NFlb1, NFname, NFfood, NFloc, NFexpirydate, NFlb2, NFlb3, NFlb4, NFdonebtn]

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
    print("LEFTOVER") # TEST

    # done button
    LOdonebtn = tk.Button(window1, text = "Done") #####
    LOdonebtn.place(x = 330, y = 410)

    # name
    LOlb1 = tk.Label(window1, text = "Enter leftover name:", font = ("Proxima Nova", 12)) # prompt
    LOlb1.place(x = 60, y = 160)

    LOname = tk.Entry(window1, bd = 3) # entry box
    LOname.place(x = 240, y = 155)


    # date cooked
    LOlb2 = tk.Label(window1, text = "Select date cooked: ", font = ("Proxima Nova", 12)) # prompt
    LOlb2.place(x = 60, y = 215)

    LOdatecooked = Calendar(window1)
    LOdatecooked.place(x = 240, y = 215)

    # list of widgets
    global LOwidgets
    LOwidgets = [LOlb1, LOname, LOdatecooked, LOlb2, LOdonebtn]

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
    print("FROZEN") # TEST
    frozenFoodList = ["Fish", "Leftovers", "Cold meats", "Ham", "Baked goods", "Lamb", "Chicken", "Mushrooms", "Beef", "Fruit", "Veggies"]

    # done button
    FZdonebtn = tk.Button(window1, text = "Done") #####
    FZdonebtn.place(x = 330, y = 410)

    # type
    FZlb1 = tk.Label(window1, text = "Select frozen food type:", font = ("Proxima Nova", 12)) # prompt
    FZlb1.place(x = 60, y = 160)

    FZfood = ttk.Combobox(window1, values = frozenFoodList, state = "readonly") # menu widget
    FZfood.place(x = 240, y = 160)


    # date frozen
    FZlb2 = tk.Label(window1, text = "Enter date frozen: ", font = ("Proxima Nova", 12)) # prompt
    FZlb2.place(x = 60, y = 215)

    FZdatefrozen = Calendar(window1)
    FZdatefrozen.place(x = 240, y = 215)

    # list of Frozen widgets
    global FZwidgets
    FZwidgets = [FZlb1, FZfood, FZdatefrozen, FZlb2, FZdonebtn]

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
    for widget in widgetList:
        widget.place_forget()
    return



main()
