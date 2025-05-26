import csv
import io
from django.http import HttpResponse
from django.shortcuts import render, redirect
from web.models import Pet  # Pet modeli web app içindeyse bu şekilde kalmalı

def pet_dashboard(request):
    # 🔍 Arama işlemi
    query_breed = request.GET.get('breed')
    query_pet_type = request.GET.get('pet_type')
    query_gender = request.GET.get('gender')

    pets = Pet.objects.all()

    if query_breed:
        pets = pets.filter(breed__icontains=query_breed)
    if query_pet_type:
        pets = pets.filter(pet_type__icontains=query_pet_type)
    if query_gender:
        pets = pets.filter(gender__iexact=query_gender)

    # 📤 Export işlemi
    if 'export' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="pets.csv"'
        writer = csv.writer(response)
        writer.writerow(['Breed', 'Type', 'Gender', 'Age'])
        for pet in pets:
            writer.writerow([pet.breed, pet.pet_type, pet.gender, pet.age])
        return response

    # 📥 Import işlemi
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        next(io_string)  # başlığı atla

        for row in csv.reader(io_string):
            if len(row) >= 4:
                Pet.objects.create(
                    breed=row[0],
                    pet_type=row[1],
                    gender=row[2],
                    age=int(row[3]) if row[3].isdigit() else 0
                )
        return redirect('pet_dashboard')

    return render(request, 'pet_dashboard.html', {'pets': pets})
