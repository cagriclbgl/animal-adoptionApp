from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    bio = models.TextField(max_length=500, blank=True)

    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Shelter(models.Model):
    city = models.ForeignKey(City, related_name='shelters', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.city.name}"

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Yeni eklenen
    city = models.ForeignKey(City, related_name='donations', on_delete=models.CASCADE)
    shelter = models.ForeignKey(Shelter, related_name='donations', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation_date = models.DateTimeField(auto_now_add=True)
    donor_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.donor_name} - {self.amount} TL - {self.shelter.name}"
class Pet(models.Model):
    
    CITY_CHOICES = [
    ('istanbul', 'İstanbul'),
    ('ankara', 'Ankara'),
    ('izmir', 'İzmir'),
]

    PET_TYPE_CHOICES = [
        ('cat', 'Kedi'),
        ('dog', 'Köpek'),
    ]
    GENDER_CHOICES = [
        ('male', 'Erkek'),
        ('female', 'Dişi'),
    
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')
    pet_type = models.CharField(max_length=10, choices=PET_TYPE_CHOICES)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    city = models.CharField(max_length=50, choices=CITY_CHOICES)
    description = models.TextField()
    photo = models.ImageField(upload_to='pet_photos/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_pet_type_display()} - {self.breed} ({self.city})"
    def get_pet_type_display(self):
        return dict(self.PET_TYPE_CHOICES).get(self.pet_type, self.pet_type)
    
    def get_gender_display(self):
        return dict(self.GENDER_CHOICES).get(self.gender, self.gender)


    class Meta:
        verbose_name = "Hayvan İlanı"
        verbose_name_plural = "Hayvan İlanları"
        ordering = ['-created_at']  # Yeniden eskiye sıralama    

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('approved', 'Onaylandı'),
        ('rejected', 'Reddedildi'),
    ]
    
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    message = models.TextField()
    contact_info = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    application_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.applicant.username} - {self.pet.breed}"
    
class District(models.Model):
    city = models.ForeignKey(City, related_name='districts', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.city.name})" 
    


           
class Vet(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def average_rating(self):
        avg = self.ratings.aggregate(Avg('score'))['score__avg']
        return float(avg) if avg else 0.0

    def __str__(self):
        return f"{self.name} ({self.district.name}, {self.city.name})"


class Rating(models.Model):
    vet = models.ForeignKey(Vet, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, f"{i} yıldız") for i in range(1, 6)])
    rated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('vet', 'user')  # Her kullanıcı her veterinere 1 kez oy verebilir

    def __str__(self):
        return f"{self.user.username} → {self.vet.name}: {self.score} yıldız"    