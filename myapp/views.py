from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .models import Data
from .serializers import DataSerializer
from bs4 import BeautifulSoup
import requests
from collections import defaultdict
import json
import re
from pymongo import MongoClient
import pymongo

url_data = {
    'Display Type': "display_tech",
    'Features': 'with',
    'Brands': 'brand',
    'Screen Size': 'display',
    'Screen Resolution': 'display_res',
    'ROM': 'memory',
    'Battery Size': 'battery_size',
    'RAM': 'ram',
    'CPU': 'cpu',
    'Front Camera': 'front_cam',
    'Rear Camera': 'camera',
}

url_sort_data = {
    '' : '',
    'Price Low to High': "sort=price&asc=1",
    'Price High to Low': 'sort=price&asc=0',
    'Popularity': 'sort=pop&asc=0',
    'CPU Speed': 'sort=cpu&asc=0',
    'Battery Capacity': 'sort=battery&asc=0',
    'Camera Resolution': 'sort=camera&asc=0',
    'Ram': 'sort=pop&asc=0',
    'Inbuilt Memory': 'sort=mem&asc=0'
}

def process_url(data_dict: dict, selectedOption, min_option, max_option) -> str:
    base_url = "https://www.smartprix.com/mobiles/"
    url_parts = []
    for key, values in data_dict.items():
        url_parts.append("-".join(values) + "-" + url_data[key])
    url = base_url + "/".join(url_parts)

    if min_option != '' and max_option != '':
        url = url + '/price-' + min_option + "_to_" + max_option

    elif min_option != '' and max_option == '':
        url = url + '/price-above_' + min_option

    elif min_option == '' and max_option != '':
        url = url + '/price-below_' + max_option

    url = url + '?' + url_sort_data[selectedOption]
    # print(f'Inside Process_Url : {url}')
    return url

# def fetch_data(url):
#     r = requests.get(url)
#     soup = BeautifulSoup(r.text, 'html.parser')

#     name_arr = []
#     specs_arr = []
#     price_arr = []
#     img_arr = []

#     img_src = soup.select('div.has-features div.sm-img-wrap img')
#     for img in img_src:
#         src = img.get('src')
#         img_arr.append(src)

#     phone_name = soup.select('div.has-features a.name h2')
#     for name in phone_name:
#         if "(" in name.text:
#             split_parts = name.text.split('(')
#             only_name = split_parts[0].strip()
#             name_arr.append(only_name)
#         else:
#             name_arr.append(name.text)

#     specs = soup.select('div.has-features ul.sm-feat.specs li')
#     for spec in specs:
#         specs_arr.append(spec.text)

#     prices = soup.select('div.has-features span.price')
#     for price in prices:
#         price_arr.append(price.text)

#     specs_8_list = [specs_arr[i:i + 8] for i in range(0, len(specs_arr), 8)]

#     myData = []
#     for name, price, img, specs in zip(name_arr, price_arr, img_arr, specs_8_list):
#         data_dict = {
#             'Name': name,
#             'Price': price,
#             'Image': img,
#             'Specs': specs
#         }
#         myData.append(data_dict)

#     return myData

def fetch_data(cat, val, result_dict, min_option, max_option, selectedOption):
    value_mapping = {
        "3000_mah_above" : "3000",
        "4000_mah_above" : "4000",
        "5000_mah_above" : "5000",
        "4_inch_5_inch" : "4",
        "5_inch_6_inch" : "5",
        "6_inch_and_above" : "6",
        "20_mp_above" : "20MP",
        "13_mp_above" : "13MP",
        "48_mp_above" : "48MP",
        "20_mp_above" : "20MP",
        "64_mp_above" : "64MP",
        "108_mp_above" : '108MP',
        "200_mp_above" : "200MP",
        "5_mp_above" : "5 MP",
        "8_mp_above" : "8 MP",
        "16_mp_above" : "16 MP",
        "12_mp_above" : "12 MP",
        "32_mp_above" : "32 MP",
        "2" : "2",
        "2.3" : "2.3",
        "2.4" : "2.4",
        "2.5" : "2.5",
        "2.6" : "2.6",
        "2.8" : "2.8",
        "3" : "3",
        "3_gb_above" : "3",
        "4_gb_above" : "4", 
        "6_gb_above" : "6", 
        "8_gb_above" : "8", 
        "12_gb_above" : "12", 
        "32_gb_above" : "32", 
        "64_gb_above" : "64", 
        "128_gb_above" : "128", 
        "256_gb_above" : "256", 
        "512_gb_above" : "512",
        "3g" : '3G', 
        "4g" : '4G', 
        "5g" : '5G',
        "samsung" : "samsung", 
        "xiaomi" : "xiaomi", 
        "apple" : "apple", 
        "oppo" : "oppo", 
        "vivo" : "vivo", 
        "asus" : "asus", 
        "google" : "google", 
        "realme" : "realme", 
        "oneplus" : "oneplus", 
        "poco" : "poco", 
        "motorola" : "motorola", 
    }

    field_mapping = {
    'Brands': 'Name',
    'Battery Size': 'Spec4',
    'Rear Camera': 'Spec6',
    'RAM': 'Spec3',
    'Screen Size' : "Spec5",
    "Front Camera" : "Spec6",
    "CPU" : "Spec2",
    "ROM" : "Spec3",
    "Features" : "Spec1"
    }

    ID = []
    Category = cat
        
    for item in val:
        ID.append(value_mapping[item])

    print("ID", ID)
    print("Category", Category)

    print(result_dict)

    query = {}

    for key, values in result_dict.items():
        if key in field_mapping:
            field_name = field_mapping[key]
            new_values = []
            for value in values:
                new_values.append(value_mapping[value])
            
            if field_name == "Spec6":
                print("Inside Camera")
                print(new_values, "------", field_mapping[key])
                regex_pattern = re.compile("|".join(new_values), re.IGNORECASE)
                query[field_name] = {'$regex': regex_pattern}
            else:
                regex_pattern = re.compile("|".join(new_values), re.IGNORECASE)
                query[field_name] = {'$regex': regex_pattern}


    client = MongoClient('mongodb://localhost:27017/')
    db = client.productData
    collection = db.mobiles

    if min_option != "" and max_option != "":
        query['Price'] = {
            "$lt" : int(max_option) , "$gt" : int(min_option)
        }
    elif min_option == "" and max_option != "":
        query['Price'] = {
            "$lt" : int(max_option) , "$gt" : 0
        }
    elif min_option != "" and max_option == "":
        query['Price'] = {
           "$gt" : int(min_option)
        }
    
    if selectedOption == "Price High to Low":
        matching_documents = collection.find(query).sort('Price', pymongo.DESCENDING)
    elif selectedOption == "Price Low to High":
        matching_documents = collection.find(query).sort('Price', pymongo.ASCENDING)
    else:
        matching_documents = collection.find(query)
    
    print(f'Query : {query}')

    new_list = []
    for item in matching_documents:
        item.pop('_id', None)
        new_item = {
            "name": item["Name"],
            "price": item["Price"],
            "image": item["IMG_URL"],
            "specs": [item["Spec1"], item["Spec2"], item["Spec3"], item["Spec4"], item["Spec5"], item["Spec6"], item["Spec7"], item["Spec8"]]
        }
        new_list.append(new_item)
        
    for item in new_list:
        print(item)
        print('-------------------------------------')

    print(len(new_list))

    return new_list 


class DataListCreate(generics.ListCreateAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

def about(request):
    return render(request, 'about.html')

def homepage(request):
    return render(request, 'homepage.html')

def home(request):
    context = {
        "myData": "myData"
    }
    return render(request, 'home.html')

def searchQuery(request):
    return render(request, 'searchQuery.html')    

@csrf_exempt
def getSearchData(request):
    if request.method == 'POST': 
        data = json.loads(request.body)
        query = data.get('query')
        print(query)
        client = MongoClient('mongodb://localhost:27017/')
        db = client['productData'] 
        collection = db['mobiles']

        regex_pattern = re.compile(f'.*{re.escape(query)}.*', re.IGNORECASE)
        query = {"Name": {"$regex": regex_pattern}}  

        results = collection.find(query)
        products = [product for product in results]

        new_list = []
        for item in products:
            item.pop('_id', None)
            new_item = {
                "name": item["Name"],
                "price": item["Price"],
                "image": item["IMG_URL"],
                "specs": [item["Spec1"], item["Spec2"], item["Spec3"], item["Spec4"], item["Spec5"], item["Spec6"], item["Spec7"], item["Spec8"]]
            }
            new_list.append(new_item)
        
        client.close()
        return JsonResponse({'data': new_list}, status=200)

@csrf_exempt
def receive_checkbox_ids(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        selectedOption = data.get('selectedOption')
        category = data.get('category')
        min_option = data.get('min_option')
        max_option = data.get('max_option')

        l1 = category
        l2 = id
        result_dict = defaultdict(list)
        for key, value in zip(l1, l2):
            result_dict[key].append(value)

        result_dict = dict(result_dict)
        myData = fetch_data(l1, l2, result_dict, min_option, max_option, selectedOption)

        return JsonResponse({'data': myData}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
