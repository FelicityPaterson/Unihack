recipecount = 0

def recipepage(): #####
    # Called when findARecipeBtn is clicked, creates new window for recipe page
    global recipecount
    global window2

    window2 = tk.Toplevel()
    window2.title("Recipe Results")
    window2.geometry("1500x1500")

    # insert app logo
    logo = Image.open("logo.png")
    logo = logo.resize((150, 100))
    logo = ImageTk.PhotoImage(image = logo)
    RPlb1 = tk.Label(window2, image = logo) # label
    RPlb1.place(x = 620, y = 20) # position label

    # insert recipe
    formatRecipe(recipecount, "Stew", "5", "40 mins", "3", ("100g pudding rice",
      "butter, for the dish",
      "50g sugar",
      "700ml semi-skimmed milk",
      "pinch of grated nutmeg or strip lemon zest",
      "1 bay leaf, or strip lemon zest"), "Cook slowly.", ("Heat the oven to 150C/130C fan/gas 2. Wash and drain the rice. Butter a 850ml\u00a0baking dish, then tip in the rice and sugar and stir through the milk. Sprinkle in the nutmeg\u00a0and top with the bay leaf or lemon zest.",
      "Cook for 2 hrs or until the pudding wobbles ever so slightly when shaken.")) 
    recipecount += 1

    # next recipe
    nextBtn = tk.Button(window2, text = "Next", command = recipepage)
    nextBtn.place(x = 1300, y = 160)

    window2.mainloop()

    return

def formatRecipe(count, title, rating, duration, servings, ingredients, tips, instr):
    # Function to format recipe

    # title
    titlelbl = tk.Label(window2, text = f"{title}", font = ("Prixima Nova", 30, "bold")) # label
    titlelbl.pack(side = "top", pady = 150) # position label

    # recipe count
    recipeCountlbl = tk.Label(window2, text = f"Recipe {count+1}", font = ("Arial Bold", 16), fg = "white", bg = "orange")
    recipeCountlbl.place(x = 120, y = 160)

    # ratings
    ratinglbl = tk.Label(window2, text = f"Rating: {rating} / 5", font = ("Proxima Nova", 16, "bold")) # label
    ratinglbl.place(x = 120, y = 240) # position label

    # duration
    durationlbl = tk.Label(window2, text = f"Duration: {duration}", font = ("Proxima Nova", 16, "bold")) # label
    durationlbl.place(x = 120, y = 280) # position label

    # servings
    servinglbl = tk.Label(window2, text = f"Serving: {servings}", font = ("Proxima Nova", 16, "bold")) # label
    servinglbl.place(x = 120, y = 320) # position label

    # ingredients
    ingrtlbl = tk.Label(window2, text = f"Ingredient", font = ("Arial Bold", 16), fg = "white", bg = "#ABBD5C") # label
    ingrtlbl.place(x = 120, y = 400) # position label

    ingrtList = tk.Label(window2, text = f"{ingredients}", font = ("Proxima Nova", 12))
    ingrtList.place(x = 120, y = 435, width = 400) # position label

    # instructions
    stepslbl = tk.Label(window2, text = f"Steps / Instructions", font = ("Arial Bold", 16), fg = "white", bg = "#ABBD5C") # label
    stepslbl.place(x = 650, y = 240) # position label

    stepsList = tk.Text(window2, font = ("Proxima Nova", 12))
    stepsList.insert(1.0, f"{instr}")
    stepsList.config(state = DISABLED)
    stepsList.place(x = 650, y = 300, width = 600)
    
    # tips
    tipslbl = tk.Label(window2, text = f"{tips}", font = ("Proxima Nova", 12, "italic")) # label
    tipslbl.place(x = 650, y = 280) # position label