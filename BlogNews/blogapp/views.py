from typing import ContextManager
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import requests


def index(request):
    # return HttpResponse("Hello, world. You're at the blogapp index.")
    return render(request, 'index.html')


def news(request):
    # key ='dfdf852152b9441e8f197844bc6f9226'
    # newsapi = NewsApiClient(api_key='dfdf852152b9441e8f197844bc6f9226')
    api_link = 'https://newsapi.org/v2/top-headlines?country=in&apiKey=dfdf852152b9441e8f197844bc6f9226'
    api_get = requests.get(api_link)
    api_get_json = api_get.json()
    news_dict = {}
    for i, article in enumerate(api_get_json['articles']):
        temp_dict = {'img_url': article['urlToImage'], 'author': article['source']['name'], 'title': article['title'], 'description': article['description'],
                     'url': article['url'], }
        # temp_dict = [article['author'], article['title'], article['description'],
        #              article['url'], article['urlToImage']]
        news_dict[i] = temp_dict

    return render(request, 'news.html', {'context': news_dict})
