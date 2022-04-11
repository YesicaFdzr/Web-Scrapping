from fileinput import filename
import json
from os import path
import pandas as pd


def edit_json_alita():
    filename = "./Details.json"
    with open(filename, "r", encoding='utf-8') as file:
        data = json.load(file)
    
    print(len(data))

    for i in data:
        if "features" in i:
            for j in i["features"]:
                name = j["name"]
                j.pop("name")
                value = j["value"]
                j.pop("value")
                i[name] = value
        else:
            print("features not in " + str(data.index(i)))

    return data

def clean_alita_dataset(json_file):

    data = pd.json_normalize(json_file) 

    data = data[['reference', 'price', 'date_add', 'name', 'description', 'category_name'
    ,'link', 'quantity', 'rate', 'Autor(es)', 'Editorial', 'Colección', 'Idioma', 'Fecha de publicación', 'Edad recomendada', 'Formato', 'ISBN']]

    data = data.dropna(how='all')

    return data



if __name__ == "__main__":
    data = edit_json_alita()
    data_alita = clean_alita_dataset(data)
    filename = "./Alita_comics_dataset.csv"

    with open(filename, "w", encoding='utf-8', newline = '\n') as file:
        data_alita.to_csv(file, index=False, sep = ";")