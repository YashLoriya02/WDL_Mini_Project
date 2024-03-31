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

def fetch_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    name_arr = []
    specs_arr = []
    price_arr = []
    img_arr = []

    img_src = soup.select('div.has-features div.sm-img-wrap img')
    for img in img_src:
        src = img.get('src')
        img_arr.append(src)

    phone_name = soup.select('div.has-features a.name h2')
    for name in phone_name:
        if "(" in name.text:
            split_parts = name.text.split('(')
            only_name = split_parts[0].strip()
            name_arr.append(only_name)
        else:
            name_arr.append(name.text)

    specs = soup.select('div.has-features ul.sm-feat.specs li')
    for spec in specs:
        specs_arr.append(spec.text)

    prices = soup.select('div.has-features span.price')
    for price in prices:
        price_arr.append(price.text)

    specs_8_list = [specs_arr[i:i + 8] for i in range(0, len(specs_arr), 8)]

    myData = []
    for name, price, img, specs in zip(name_arr, price_arr, img_arr, specs_8_list):
        data_dict = {
            'Name': name,
            'Price': price,
            'Image': img,
            'Specs': specs
        }
        myData.append(data_dict)

    return myData

myData = fetch_data('https://www.smartprix.com/mobiles/')

class DataListCreate(generics.ListCreateAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

def about(request):
    return render(request, 'about.html')

def homepage(request):
    return render(request, 'homepage.html')

def home(request):
    context = {
        "myData": myData
    }
    return render(request, 'home.html', context)

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
        final_url = process_url(data_dict=result_dict, selectedOption=selectedOption, min_option=min_option, max_option=max_option)   
        myData = fetch_data(final_url)
        return JsonResponse({'data': myData}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
