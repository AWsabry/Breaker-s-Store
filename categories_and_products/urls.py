from django.urls import path
from . import views


app_name = 'categories_and_products'


urlpatterns = [
    path('',views.index,name='index',),
    path('games',views.games,name='games'),
    path('store',views.store,name='store'),
    path('details/<slug:categoryslug>/',views.code_details,name='code_details'),
    path('searchedPage',views.searchedPage,name='searchedPage'),
    path('GamesCodes/<slug:Gameslug>/',views.GamesCodes,name='GamesCodes'),
    path('filter',views.filtering_test,name='filter'),

]
