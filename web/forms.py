from django import forms
from .models import Pet, Application, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Kullanıcı bilgilerini güncelleme
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# Profil bilgilerini güncelleme
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']

# Yeni kullanıcı kaydı (email destekli)
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-posta")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# Evcil hayvan formu (tek tanım, Bootstrap ile uyumlu)
class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['pet_type', 'breed', 'age', 'gender', 'city', 'description', 'photo']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

# Başvuru formu
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['message', 'contact_info']
        widgets = {
            'message': forms.Textarea(attrs={
                'placeholder': 'Neden bu hayvanı sahiplenmek istiyorsunuz?'
            }),
            'contact_info': forms.TextInput(attrs={
                'placeholder': 'İletişim bilgileriniz'
            })
        }
        labels = {
            'message': 'Başvuru Mesajınız',
            'contact_info': 'İletişim Bilgileriniz'
        }
