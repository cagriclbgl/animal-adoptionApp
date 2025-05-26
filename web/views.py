from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import City, Shelter, Donation 
from .models import Pet
from .forms import PetForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pet, Profile, Application
from .forms import PetForm, ApplicationForm
from django.shortcuts import render, get_object_or_404
from .models import Pet
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import City, Shelter, Donation
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Vet
from .models import City, District, Vet
from .models import Vet, Rating
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm

def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'web/pet_detail.html', {'pet': pet})

def edit_profile(request):
    # Profil düzenleme mantığı burada
    return render(request, 'web/edit_profile.html')

def start(request):
    return render(request, 'web/start.html')

def home(request):
    return render(request, 'web/home.html')

def cat_breeds(request):
    return render(request, 'web/cat_breeds.html')

def dog_breeds(request):
    return render(request, 'web/dog_breeds.html')



@login_required
def food_donation(request):
    cities = City.objects.all()
    shelters = Shelter.objects.all()

    if request.method == 'POST':
        try:
            # Formdan gelen amount değerini al
            amount = request.POST.get('amount')
            
            Donation.objects.create(
                user=request.user,
                city_id=request.POST['city'],
                shelter_id=request.POST['shelter'],
                amount=amount,  # Formdan gelen değeri kullan
                donor_name=f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
            )
            return redirect('donation_success')
        except Exception as e:
            messages.error(request, f'Hata: {str(e)}')

    return render(request, 'web/food_donation.html', {
        'cities': cities,
        'shelters': shelters
    })

def donation_success(request):
    return render(request, 'web/donation_success.html')

@login_required
def give_for_adoption(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            messages.success(request, 'İlan başarıyla yayınlandı!', extra_tags='pet_adoption')
            form = PetForm()
    else:
        form = PetForm()
    return render(request, 'web/give_for_adoption.html', {'form': form})

def adopt(request):
    pets = Pet.objects.all()
    
    # Filtreleme işlemleri
    pet_type = request.GET.get('pet_type')
    gender = request.GET.get('gender')
    city = request.GET.get('city')
    age = request.GET.get('age')
    
    if pet_type:
        pets = pets.filter(pet_type=pet_type)
    if gender:
        pets = pets.filter(gender=gender)
    if city:
        pets = pets.filter(city=city)
    if age:
        if age == '0-1':
            pets = pets.filter(age__lte=1)
        elif age == '1-3':
            pets = pets.filter(age__gte=1, age__lte=3)
        elif age == '3-5':
            pets = pets.filter(age__gte=3, age__lte=5)
        elif age == '5+':
            pets = pets.filter(age__gte=5)
    
    context = {
        'pets': pets,
    }
    return render(request, 'web/adopt.html', context)


def find_vet(request):
    selected_city_id = request.GET.get('city')
    selected_district_id = request.GET.get('district')
    search_query = request.GET.get('search', '')

    cities = City.objects.all()
    districts = District.objects.filter(city_id=selected_city_id) if selected_city_id else District.objects.none()
    vets = Vet.objects.all()

    if selected_city_id:
        vets = vets.filter(city_id=selected_city_id)
    if selected_district_id:
        vets = vets.filter(district_id=selected_district_id)
    if search_query:
        vets = vets.filter(name__icontains=search_query)
    for vet in vets:
        avg = vet.average_rating()
        vet.filled_stars = int(round(avg))
        
    return render(request, 'web/find_vet.html', {
        'cities': cities,
        'districts': districts,
        'vets': vets,
        'selected_city': selected_city_id,
        'selected_district': selected_district_id,
        'search_query': search_query,
    })

def rate_vet(request, vet_id):
    if request.method == 'POST':
        score = int(request.POST.get('score'))
        vet = Vet.objects.get(id=vet_id)
        rating, created = Rating.objects.update_or_create(
            user=request.user,
            vet=vet,
            defaults={'score': score}
        )
        return redirect('find-vet')  # Geri listeye döner
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Giriş başarılıysa ana sayfaya yönlendir
    else:
        form = AuthenticationForm()
    return render(request, 'web/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Kayıt olurken otomatik giriş yap
            return redirect('home')  # Kayıt başarılıysa ana sayfaya yönlendir
    else:
        form = UserCreationForm()
    return render(request, 'web/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    my_pets = Pet.objects.filter(owner=request.user)
    my_applications = Application.objects.filter(applicant=request.user)
    my_donations = Donation.objects.filter(user=request.user)  # mama bağışları
    received_applications = Application.objects.filter(pet__owner=request.user, status='pending')
    
    context = {
        'my_pets': my_pets,
        'my_applications': my_applications,
        'received_applications': received_applications,
        'my_donations': my_donations,

    }
    return render(request, 'web/profile.html', context)

def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'web/pet_detail.html', {'pet': pet})

@login_required
def apply_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.pet = pet
            application.applicant = request.user
            application.save()
            return redirect('profile')
    else:
        form = ApplicationForm()
    
    return render(request, 'web/apply_pet.html', {'form': form, 'pet': pet})



@require_POST
@login_required
def approve_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, pet__owner=request.user)
    application.status = 'approved'
    application.save()
    messages.success(request, 'Başvuru onaylandı!')
    return redirect('profile')

@require_POST
@login_required
def reject_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, pet__owner=request.user)
    application.status = 'rejected'
    application.save()
    messages.success(request, 'Başvuru reddedildi!')
    return redirect('profile')

@login_required
def pet_delete(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    pet.delete()
    return redirect('profile')  # profil sayfasına geri yönlendirme


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profiliniz başarıyla güncellendi!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, 'web/edit_profile.html', context)