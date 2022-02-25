import requests
from bs4 import BeautifulSoup as BSoup
import math
import json


recipe_links = []
recipe_pages = 0

def get_rcp_from_page(soup, links_ls):
    recipes = soup.find_all("a", {"class":"standard-card-new__article-title"})
    for recipe in recipes:
        links_ls.append(recipe.get("href"))

    return links_ls


def get_rcp_number(soup):
    recipe_counter_class = "tab-horizontal-item__label-count"
    recipe_count = soup.find("span", {"class": recipe_counter_class})
    recipe_count = recipe_count.text.replace(",","")[1:-1]
    recipe_count_int = int(recipe_count)
    return math.ceil(recipe_count_int / 24)


def boil_soup(pg_number):
    url = f"https://www.bbcgoodfood.com/search/recipes/page/{pg_number}?q=food&sort=-relevance"
    bbc_goodfoods_content = requests.get(url).text
    return BSoup(bbc_goodfoods_content, "html.parser")


def full_url(link_text):
    return "https://www.bbcgoodfood.com" + link_text


def run():
    # begin scraping
    first_soup = boil_soup(1)
    recipe_links = get_rcp_from_page(first_soup, recipe_links)
    recipe_pages = get_rcp_number(first_soup)


    for pg_num in range(2,recipe_pages+1):
        curr_page_soup = boil_soup(pg_num)
        recipe_links = get_rcp_from_page(curr_page_soup, recipe_links)


if __name__ == "__main__":
    run()
