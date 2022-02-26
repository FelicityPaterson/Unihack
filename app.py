import requests
from bs4 import BeautifulSoup as BSoup
import math
import json
import os
import re


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
    json_urls = json.dumps(object_to_save, indent=2)

    json_file = open(filename, 'w')
    json_file.write(json_urls)
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
            print("EXIT")
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
        instructions.append(item.p.text)

    return instructions


def get_tips(rcp_soup):
    tips_section = rcp_soup.find("h6", text="RECIPE TIPS")
    tips = []
    if not tips_section:
        return tips

    for sib in tips_section.next_siblings:
        tips.append(sib.p.text)


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
    print(datetime_str)
    print(re.search("[0-9]*H", datetime_str))


def get_cook_time(rcp_soup):
    time_section = rcp_soup.find_all("time")
    # total_time = time_section.get("datetime")
    time1 = time_section[0].get("datetime")
    parse_duration(time1)


def read_recipe(url):
    recipe_content = requests.get(url).text
    recipe_soup = BSoup(recipe_content, "html.parser")
    ingredients = get_ingrds(recipe_soup)
    instructions = get_instrs(recipe_soup)
    tips = get_tips(recipe_soup)
    name = get_rcp_name(recipe_soup)
    rating = get_rating(recipe_soup)
    time = get_cook_time(recipe_soup)
    return ingredients, instructions


def run():
    recipe_links = get_all_rcp_urls()
    save_to_json(recipe_links, "recipe_urls.json")
    ingrds, instrcs = read_recipe(recipe_links[17])




if __name__ == "__main__":
    run()
