from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('home', views.home, name='home'),
    path('cat-breeds/', views.cat_breeds, name='cat-breeds'),
    path('dog-breeds/', views.dog_breeds, name='dog-breeds'),
    path('food-donation/', views.food_donation, name='food-donation'),
    path('donation-success/', views.donation_success, name='donation_success'),
    path('adopt/', views.adopt, name='adopt'),
    path('give-for-adoption/', views.give_for_adoption, name='give-for-adoption'),
    path('find-vet/', views.find_vet, name='find-vet'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile, name='profile'),
    path('pet/<int:pet_id>/apply/', views.apply_pet, name='apply_pet'),
    path('pet/<int:pet_id>/', views.pet_detail, name='pet_detail'),    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('application/<int:application_id>/approve/', views.approve_application, name='approve_application'),
    path('application/<int:application_id>/reject/', views.reject_application, name='reject_application'),
    path('application/delete/<int:pk>/', views.pet_delete, name='pet_delete'),
    path('rate-vet/<int:vet_id>/', views.rate_vet, name='rate_vet'),

]