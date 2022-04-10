from time import sleep
from bs4 import BeautifulSoup
from numpy import product
from pip import main
import requests
import json 
from os import path 


def alita_products_list():
    soup = BeautifulSoup(requests.get("https://www.alitacomics.com/es/844-comic").text, "html.parser")

    all_pags = []

    for i in soup.find_all("a", {"class": "js-search-link"}):
        all_pags.append(i.get("href"))

    max_pags_posible = []
    for i in all_pags:
        split = i.split("=")
        for j in split:
            if j.isdigit():
                max_pags_posible.append(int(j))

    all_comics = []
    for i in range(1,max(max_pags_posible)+1):
        soup = BeautifulSoup(requests.get("https://www.alitacomics.com/es/844-comic?page=" + str(i)).text, "html.parser")
        for k in soup.find_all("section", {"id": "products"}):
            hijos = k.find_all("span", {"class": "h3 product-title"})
            for j in hijos:
                referencias = j.find_all("a")
                for m in referencias:
                    all_comics.append(m.get("href"))
        print("Page " + str(i) + " done")

    return all_comics



def alita_products_info(url):
    details = {}
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    for i in soup.find_all("div", {"class": "tab-pane fade"}):
        details = json.loads(i.get("data-product"))
    return details



def main():
    filename = "./Details.json"
    listObject = []

    all_products = alita_products_list()
    sleep(5)

    for i in all_products:
        listObject.append(alita_products_info(i))
        print("product " + str(all_products.index(i)) + " of " + str(len(all_products)) + " done")
    
    with open(filename, "w") as file:
        json.dump(listObject, file, indent=4)


if __name__ == "__main__":
    main()