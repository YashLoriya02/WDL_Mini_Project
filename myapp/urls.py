# backend/myapp/urls.py
from django.urls import path
from .views import DataListCreate, home, receive_checkbox_ids, about , homepage, searchQuery, getSearchData

urlpatterns = [
    path('api/data/', DataListCreate.as_view(), name='data-list-create'),
    path('home/', home, name='home'),
    path('homepage/', homepage, name='homepage'),
    path('about/', about, name='about'),
    path('receive-checkbox-ids/', receive_checkbox_ids, name='receive_checkbox_ids'),
    path('searchQuery/', searchQuery, name='searchQuery'),
    path('getSearchData/', getSearchData, name='getSearchData'),
]