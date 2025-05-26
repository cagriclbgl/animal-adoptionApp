from django.contrib import admin
from .models import City, Shelter, Donation
from .models import Pet
from .models import Vet
from .models import Rating

class PetAdmin(admin.ModelAdmin):
    list_display = ('id', 'breed', 'pet_type', 'owner', 'city', 'created_at', 'is_active')
    list_filter = ('pet_type', 'is_active', 'city', 'created_at')
    search_fields = ('breed', 'owner__username', 'description')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'owner')
    fieldsets = (
        (None, {
            'fields': ('owner', 'pet_type', 'breed', 'age', 'gender')
        }),
        ('Detaylar', {
            'fields': ('city', 'description', 'photo', 'is_active')
        }),
    )

admin.site.register(Pet, PetAdmin)

class ShelterInline(admin.TabularInline):
    model = Shelter
    extra = 1

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'shelter_count')
    inlines = [ShelterInline]
    
    def shelter_count(self, obj):
        return obj.shelters.count()
    shelter_count.short_description = 'Barınak Sayısı'

class ShelterAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'donation_count')
    list_filter = ('city',)
    search_fields = ('name', 'city__name')
    
    def donation_count(self, obj):
        return obj.donations.count()
    donation_count.short_description = 'Toplam Bağış Sayısı'

class DonationAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'get_amount', 'get_city', 'get_shelter', 'donation_date')
    
    def get_amount(self, obj):
        return f"{obj.amount} TL"
    get_amount.short_description = 'Miktar'
    
    def get_user(self, obj):
        return obj.user.username if obj.user else "Anonim"
    get_user.short_description = 'Kullanıcı'
    
    def get_city(self, obj):
        return obj.city.name
    get_city.short_description = 'Şehir'
    
    def get_shelter(self, obj):
        return obj.shelter.name
    get_shelter.short_description = 'Barınak'

# Tek seferde kayıt
admin.site.register(City, CityAdmin)
admin.site.register(Shelter, ShelterAdmin)
admin.site.register(Donation, DonationAdmin)


@admin.register(Vet)
class VetAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'phone')
    search_fields = ('name', 'city__name')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('vet', 'user', 'score', 'rated_at')
    list_filter = ('score', 'rated_at')
    search_fields = ('vet__name', 'user__username')    