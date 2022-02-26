import tkinter as tk # import tkinter library
from tkinter import ttk
from tkcalendar import Calendar

freshls = ["Apple", "Orange", "Cucumber"]
#create a window
window = tk.Tk()
window.title("The App") # name title of window
window.geometry("1200x800") # window size


class App:
    def __init__(self):
        self.produceType = tk.StringVar()
        self.combo = ttk.Combobox(window, values = freshls, state = "readonly") # values for objects, state = "readonly" to disable typing
        self.cal = Calendar(window)

    def main(self):

        # create app tite
        lb1 = tk.Label(window, text= "BEST BEFORE", font=("Arial Bold", 30), fg = "green") # label
        lb1.pack(side = "top") # position label

        # create produce selection radio buttons
        rbtn1 = tk.Radiobutton(window, text = "Fresh", var = self.produceType, value = "Fresh")
        rbtn1.pack(side = "top")

        rbtn2 = tk.Radiobutton(window, text = "Non-fresh", var = self.produceType, value = "Non-fresh") ###
        rbtn2.pack(side = "top")

        btn1 = tk.Button(window, text = "Select", command = self.produceSelected)
        btn1.pack(side = "top")

        window.mainloop() # run the window
    
    def showWidget(self, widget):
        widget.pack(side = "top")
    
    def hideWidget(self, widget):
        widget.pack_forget()

    def produceSelected(self):
        if self.produceType.get() == "Fresh":
            self.showWidget(self.combo)
            self.showWidget(self.cal)

        if self.produceType.get() == "Non-fresh":
            self.hideWidget(self.combo)
            self.hideWidget(self.cal)



BetterBefore = App()
BetterBefore.main()


