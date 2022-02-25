import requests
from bs4 import BeautifulSoup as BSoup
import math


recipe_links = []

def get_rcp_from_page(soup, links_ls):
    recipes = soup.find_all("a", {"class":"standard-card-new__article-title"})
    for recipe in recipes:
        links_ls.append(recipe.get("href"))

    return links_ls

orig_url ="https://www.bbcgoodfood.com/search/recipes/page/1?q=food&sort=-relevance"

bbc_goodfoods_content = requests.get(orig_url).text
soup = BSoup(bbc_goodfoods_content, "html.parser")
recipe_links = get_rcp_from_page(soup, recipe_links)

recipe_counter_class = "tab-horizontal-item__label-count"
recipe_count = soup.find("span", {"class": recipe_counter_class})
recipe_count = recipe_count.text.replace(",","")[1:-1]
recipe_count_int = int(recipe_count)
recipe_pages = math.ceil(recipe_count_int / 24) 

for pg_num in range(2,recipe_pages+1):
    page_url = f"https://www.bbcgoodfood.com/search/recipes/page/{pg_num}?q=food&sort=-relevance"
    page_content = requests.get(page_url).text
    curr_page_soup = BSoup(page_content, "html.parser")
    recipes = curr_page_soup.find_all("a")

    get_rcp_from_page(curr_page_soup, recipe_links)

