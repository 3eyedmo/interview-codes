import pandas as pd
import json
from pathlib import Path
from brands import brands
import re
import string

quentity: dict = {
    "2": [
        r'\b۲عددی\b',
        r'\bدوعددی\b',
        r'\b2عددی\b',
        r'\b۲ عددی\b',
        r'\b2 عددی\b',
        r'\bدو عددی\b',
        r'\bعدددی\b'
    ],
    "3": [
        r'\b۳عددی\b',
        r'\b3عددی\b',
        r'\bسهعددی\b',
        r'\b۳ عددی\b',
        r'\b3 عددی\b',
        r'\bسه عددی\b'
    ],
    "4": [
        r'\b۴عددی\b',
        r'\b4عددی\b',
        r'\bچهارعددی\b',
        r'\b۴ عددی\b',
        r'\b4 عددی\b',
        r'\bچهار عددی\b'
    ],
    "5":[
        r'\b5عددی\b',
        r'\b۵عددی\b',
        r'\bپنجعددی\b',
        r'\bپنج عددی\b',
        r'\b۵ عددی\b',
        r'\b5 عددی\b',
    ]
}

def get_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def get_number(text):
    for number, list_values in quentity.items():
        for value in list_values:
            if re.search(value, text):
                return int(number)
    return 1

def get_brand(title):
    brand = "----"
    for brand_fa, brand_en in brands.items():
        if brand_fa in title:
            return brand_en   
    return brand


def get_model(title):
    common_fa_words: list = [
        "برای",
        "مناسب"
    ]
    q: str = "بسته"
    search_text = title
    if q in search_text:
        k = search_text.find(q)
        search_text = search_text[: k]
    for word in common_fa_words:
        if word in title:
            search_text = title[title.find(word): ]
            break
    sub_string = re.sub("[^a-zA-Z0-9]+[\s]+", '&&&' , search_text)
    model = " ".join(sub_string.split("&&&"))
    letters = string.ascii_letters + string.digits + " "
    for char in model:
        if char not in letters:
            model = model.replace(char, "")

    if "لایت" in search_text:
        model = model + " Lite"
    return model

my_boxes = [
    "فول",
    "پرشیا",
    "قاب تک",
    "تراست",
    "گلس راک",
    "وایکینگ",
    "ایرگلوری",
    "شیلد گلس"
]

def create_analyze_excel(filename):

    data = get_json(filename)

    new_data = list()
    for item in data:
        dkp = item.get("dkp")
        title = item.get("title")
        variants = item.get("product")
        quent = get_number(title)
        model = get_model(title)
        brand = get_brand(title)
        brand_name = item.get("brand").get("title_fa")
        if brand_name == "متفرقه":
            for i in my_boxes:
                if i in title:
                    brand_name=i
                    break

        valid_colors = list()
        for var in variants:
            color = var.get("color").get("title")
            if color not in valid_colors:
                valid_colors.append(color.strip())
        color_list = ", ".join(valid_colors)
        new_data.append({
            "brand": brand,
            "model": model,
            "title": title,
            "quentity": quent,
            "dkp": dkp,
            "colors": color_list,
            "box": brand_name
        })

    new_data_df = pd.DataFrame(new_data)
    box_grp = new_data_df.groupby(["box"])
    box_json = list()
    for box, rows in box_grp:
        box_json.append({
            "box": box,
            "tedad": len(rows)
        })
    box_df = pd.DataFrame(box_json)

    handler = pd.ExcelWriter(Path(str(filename).replace(".json", ".xlsx")), engine="xlsxwriter")
    new_data_df.to_excel(handler, sheet_name="total_data", index=False)
    box_df.to_excel(handler, sheet_name="analyse", index=False)
    handler.save()