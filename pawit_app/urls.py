
from django.urls import path
from . import views

urlpatterns = [
  #  path('pet-search/', views.pet_search, name='pet_search'),
    #path('export-pets/', views.export_pets_csv, name='export_pets_csv'),
   # path('import-pets/', views.import_pets_csv, name='import_pets_csv'),
    path('pet-dashboard/', views.pet_dashboard, name='pet_dashboard'),

]
