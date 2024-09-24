from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Parofdsl', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Parolni takrorlang', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        data = self.cleaned_data
        if data['password1'] and data['password2']:
            if len(data['password1']) >= 4:
                if data['password1'] == data['password2']:
                    return data['password1']
                else:
                    raise ValidationError("ikkala parol bir biriga teng emas")
            else:
                raise ValidationError("parol uzunligi to'rtta belgidan ko'p bo'lishi kerak")
        else:
            raise ValidationError("iltimos ikkala maydonga ham parol kiriting")


class CustomUserRegistrationForm(UserCreationForm):
    date_of_birthday = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    user_profile_photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'date_of_birthday', 'user_profile_photo', 'password1', 'password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']


class ProfileEditForm(forms.ModelForm):
    class Meta:
         model = Profile
         fields = ['user_profile_photo', 'date_of_birthday']

