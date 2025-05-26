from django import forms
from .models import Pet,Application
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['pet_type', 'breed', 'age', 'gender', 'city', 'description', 'photo']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control-file'}),

        }


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['pet_type', 'breed', 'age', 'gender', 'city', 'description', 'photo']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


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